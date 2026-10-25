"""
SQLite persistence.

Tables:
  scans          — one row per contract scanned (headline stats + full result JSON)
  findings       — one row per flagged clause, linked to a scan (for aggregates)
  rule_settings  — per-rule enabled flag + optional severity override

Kept small and dependency-free (stdlib sqlite3 only).
"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "dossier.db")


def _connect() -> sqlite3.Connection:
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r["name"] == column for r in rows)


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                filename     TEXT NOT NULL,
                scanned_at   TEXT NOT NULL,
                word_count   INTEGER NOT NULL,
                checks       INTEGER NOT NULL,
                flagged      INTEGER NOT NULL,
                high         INTEGER NOT NULL,
                medium       INTEGER NOT NULL,
                low          INTEGER NOT NULL,
                risk_score   INTEGER NOT NULL,
                risk_band    TEXT NOT NULL,
                raw_json     TEXT
            )
            """
        )
        if not _column_exists(conn, "scans", "user_id"):
            conn.execute("ALTER TABLE scans ADD COLUMN user_id INTEGER")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS findings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id     INTEGER NOT NULL,
                clause_type TEXT NOT NULL,
                title       TEXT NOT NULL,
                severity    TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans (id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rule_settings (
                rule_id  TEXT PRIMARY KEY,
                enabled  INTEGER NOT NULL DEFAULT 1,
                severity TEXT
            )
            """
        )
        # Migrate older DBs that predate the raw_json column.
        if not _column_exists(conn, "scans", "raw_json"):
            conn.execute("ALTER TABLE scans ADD COLUMN raw_json TEXT")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rental_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                record_type TEXT NOT NULL,
                title TEXT NOT NULL,
                details TEXT NOT NULL,
                status TEXT NOT NULL,
                record_date TEXT NOT NULL,
                attachment_path TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        if not _column_exists(conn, "rental_records", "user_id"):
            conn.execute("ALTER TABLE rental_records ADD COLUMN user_id INTEGER")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS property_listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL, locality TEXT NOT NULL, rent INTEGER NOT NULL,
                bedrooms INTEGER NOT NULL, furnished TEXT NOT NULL, description TEXT NOT NULL,
                photo_path TEXT, status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL
            )
        """)
        for col, col_type in [
            ("society_name", "TEXT"),
            ("deposit", "INTEGER"),
            ("carpet_area", "INTEGER"),
            ("bachelor_policy", "TEXT"),
            ("amenities", "TEXT"),
            ("owner_name", "TEXT"),
            ("owner_phone", "TEXT"),
        ]:
            if not _column_exists(conn, "property_listings", col):
                conn.execute(f"ALTER TABLE property_listings ADD COLUMN {col} {col_type}")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS society_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL, society_name TEXT NOT NULL, locality TEXT NOT NULL,
                rating INTEGER NOT NULL, review TEXT NOT NULL, photo_path TEXT,
                created_at TEXT NOT NULL
            )
        """)
        for col, col_type in [
            ("resident_type", "TEXT"),
            ("water_rating", "INTEGER"),
            ("security_rating", "INTEGER"),
            ("maintenance_rating", "INTEGER"),
            ("bachelor_rating", "INTEGER"),
            ("pros", "TEXT"),
            ("cons", "TEXT"),
        ]:
            if not _column_exists(conn, "society_reviews", col):
                conn.execute(f"ALTER TABLE society_reviews ADD COLUMN {col} {col_type}")

        seed_default_data(conn)


# --------------------------------------------------------------------------- #
def _password_hash(password: str) -> str:
    import hashlib
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_or_get_user(username: str, password: str) -> tuple[int | None, str | None]:
    username = username.strip().lower()
    if len(username) < 2:
        return None, "Please enter a name with at least 2 characters."
    if not (len(password) == 4 and password.isdigit()):
        return None, "Password must be exactly 4 digits, for example 1234."
    with _connect() as conn:
        row = conn.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            if row["password_hash"] != _password_hash(password):
                return None, "That password does not match this account."
            return int(row["id"]), None
        cur = conn.execute("INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)", (username, _password_hash(password), datetime.now().isoformat(timespec="seconds")))
        return int(cur.lastrowid), None


def get_user(user_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


# Scans
# --------------------------------------------------------------------------- #
def save_scan(filename: str, result: dict, user_id: int | None = None) -> int:
    s = result["summary"]
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO scans
                (user_id, filename, scanned_at, word_count, checks, flagged,
                 high, medium, low, risk_score, risk_band, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            ,
            (
                user_id,
                filename,
                datetime.now().isoformat(timespec="seconds"),
                result["word_count"],
                s["checks"],
                s["flagged"],
                s["high"],
                s["medium"],
                s["low"],
                s["risk_score"],
                s["risk_band"],
                json.dumps(result),
            ),
        )
        scan_id = cur.lastrowid
        for f in result["findings"]:
            if f["status"] == "flagged":
                conn.execute(
                    "INSERT INTO findings (scan_id, clause_type, title, severity) VALUES (?, ?, ?, ?)",
                    (scan_id, f["clause_type"], f["title"], f["severity"]),
                )
        return scan_id


def get_overview() -> dict:
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM scans").fetchone()["c"]
        flagged = conn.execute("SELECT COALESCE(SUM(flagged),0) AS s FROM scans").fetchone()["s"]
        high = conn.execute("SELECT COALESCE(SUM(high),0) AS s FROM scans").fetchone()["s"]
        top_types = conn.execute(
            """
            SELECT clause_type, COUNT(*) AS n
            FROM findings GROUP BY clause_type ORDER BY n DESC LIMIT 5
            """
        ).fetchall()
        bands = conn.execute(
            "SELECT risk_band, COUNT(*) AS n FROM scans GROUP BY risk_band"
        ).fetchall()
        return {
            "total_scans": total,
            "total_flagged": flagged,
            "total_high": high,
            "top_clauses": [(r["clause_type"], r["n"]) for r in top_types],
            "bands": {r["risk_band"]: r["n"] for r in bands},
        }


def get_recent(limit: int = 5) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM scans ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_all_scans(user_id: int | None = None) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM scans WHERE user_id = ? OR user_id IS NULL ORDER BY id DESC", (user_id,)).fetchall()
        return [dict(r) for r in rows]


def get_scan(scan_id: int) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM scans WHERE id = ?", (scan_id,)).fetchone()
        if not row:
            return None
        data = dict(row)
        if data.get("raw_json"):
            try:
                data["result"] = json.loads(data["raw_json"])
            except (ValueError, TypeError):
                data["result"] = None
        return data


def delete_scan(scan_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM findings WHERE scan_id = ?", (scan_id,))
        conn.execute("DELETE FROM scans WHERE id = ?", (scan_id,))


def clear_scans() -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM findings")
        conn.execute("DELETE FROM scans")


def save_rental_record(record_type: str, title: str, details: str, status: str, record_date: str, attachment_path: str | None = None, user_id: int | None = None) -> int:
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO rental_records (user_id, record_type, title, details, status, record_date, attachment_path, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, record_type, title, details, status, record_date, attachment_path, datetime.now().isoformat(timespec="seconds")),
        )
        return int(cur.lastrowid)


def get_rental_records(limit: int = 100, user_id: int | None = None) -> list[dict]:
    with _connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM rental_records WHERE user_id = ? OR user_id IS NULL ORDER BY id DESC LIMIT ?", (user_id, limit)).fetchall()]


def delete_rental_record(record_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM rental_records WHERE id = ?", (record_id,))


def save_property_listing(
    user_id: int,
    title: str,
    locality: str,
    rent: int,
    bedrooms: int,
    furnished: str,
    description: str,
    photo_path: str | None = None,
    society_name: str = "",
    deposit: int = 0,
    carpet_area: int = 0,
    bachelor_policy: str = "Bachelors Welcome",
    amenities: str = "",
    owner_name: str = "Property Owner",
    owner_phone: str = "",
    status: str = "pending",
) -> int:
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO property_listings 
                (user_id, title, locality, rent, bedrooms, furnished, description, photo_path, 
                 society_name, deposit, carpet_area, bachelor_policy, amenities, owner_name, owner_phone, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, title, locality, rent, bedrooms, furnished, description, photo_path,
                society_name, deposit, carpet_area, bachelor_policy, amenities, owner_name, owner_phone, status,
                datetime.now().isoformat(timespec="seconds")
            )
        )
        return int(cur.lastrowid)


def update_property_listing_status(listing_id: int, status: str) -> None:
    with _connect() as conn:
        conn.execute("UPDATE property_listings SET status = ? WHERE id = ?", (status, listing_id))


def get_property_listings(limit: int = 100) -> list[dict]:
    with _connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM property_listings ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]


def delete_property_listing(listing_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM property_listings WHERE id = ?", (listing_id,))


def save_society_review(
    user_id: int,
    society_name: str,
    locality: str,
    rating: int,
    review: str,
    photo_path: str | None = None,
    resident_type: str = "Tenant",
    water_rating: int = 5,
    security_rating: int = 5,
    maintenance_rating: int = 5,
    bachelor_rating: int = 5,
    pros: str = "",
    cons: str = "",
) -> int:
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO society_reviews 
                (user_id, society_name, locality, rating, review, photo_path,
                 resident_type, water_rating, security_rating, maintenance_rating, bachelor_rating, pros, cons, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, society_name, locality, rating, review, photo_path,
                resident_type, water_rating, security_rating, maintenance_rating, bachelor_rating, pros, cons,
                datetime.now().isoformat(timespec="seconds")
            )
        )
        return int(cur.lastrowid)


def get_society_reviews(limit: int = 100) -> list[dict]:
    with _connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM society_reviews ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]


def delete_society_review(review_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM society_reviews WHERE id = ?", (review_id,))


def seed_default_data(conn: sqlite3.Connection) -> None:
    """Pre-seed database with realistic Mumbai listings and society reviews if empty."""
    # Seed property listings
    count = conn.execute("SELECT COUNT(*) AS c FROM property_listings").fetchone()["c"]
    if count == 0:
        sample_listings = [
            (
                1,
                "Lakefront 2BHK with Private Balcony",
                "Hiranandani Gardens (Somerset)",
                "Powai",
                42000,
                120000,
                2,
                850,
                "Fully furnished",
                "Bachelors & Working Professionals Welcome",
                "24/7 Water,Power Backup,Lift,Gym,Clubhouse,Gas Pipeline,Reserved Parking,Security / CCTV",
                "High-floor apartment with unhindered Powai lake view. Italian modular kitchen with piped gas, AC in all rooms, and dedicated covered car parking. European architecture campus with supermarkets and cafes within 2 mins walk.",
                "public/images/powai_hiranandani.jpg",
                "Rajesh Sharma",
                "+91 98201 44520",
                "verified",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Designer 1BHK near Metro Line 2A",
                "Windermere Lokhandwala",
                "Andheri West",
                28500,
                85000,
                1,
                560,
                "Semi-furnished",
                "Working Professionals Preferred",
                "Lift,24/7 Water,Security / CCTV,Power Backup,Visitor Parking",
                "Well-ventilated flat situated in the heart of Lokhandwala Complex. Walking distance to Infinity Mall, metro station, and commercial hubs. Society is peaceful with 24/7 security guards.",
                "public/images/andheri_lokhandwala.jpg",
                "Priya Kulkarni",
                "+91 98192 33100",
                "verified",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Luxury 3BHK Urban Forest View",
                "Godrej The Trees",
                "Vikhroli",
                58000,
                175000,
                3,
                1220,
                "Fully furnished",
                "Bachelors & Families Welcome",
                "24/7 Water,Power Backup,Gym,Swimming Pool,Clubhouse,Gas Pipeline,EV Charging,Security / CCTV",
                "Award-winning sustainable township right off the Eastern Express Highway. Modern wooden flooring, high-end white goods, wide green balcony, and world-class retail promenade. 15 mins to BKC via flyover.",
                "public/images/vikhroli_godrej.jpg",
                "Ananya Deshmukh",
                "+91 97690 12845",
                "verified",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Modern 1RK Compact Bachelor Studio",
                "Oberoi Woods & Esquire",
                "Goregaon",
                19000,
                50000,
                1,
                390,
                "Fully furnished",
                "Bachelors Only",
                "Lift,Power Backup,Security / CCTV,Wi-Fi Ready,Piped Gas",
                "Compact and smart studio setup perfect for IT/media professionals. Direct pedestrian entry to Oberoi Mall and 5 mins to Western Express Highway metro. Fully equipped with bed, wardrobe, and fridge.",
                "public/images/goregaon_oberoi.jpg",
                "Vikram Malhotra",
                "+91 98210 77412",
                "pending",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Spacious 2BHK in Gated Township",
                "Rustomjee Urbania (Azziano)",
                "Thane",
                24000,
                70000,
                2,
                790,
                "Semi-furnished",
                "All Welcome",
                "24/7 Water,Power Backup,Lift,Gym,Garden / Park,Kids Play Area,Security / CCTV",
                "Well-lit corner 2BHK with open mountain view. Self-contained 127-acre township with Poddar International School, rooftop stargazing zone, and daily AC shuttle to Thane station.",
                "public/images/thane_rustomjee.jpg",
                "Sunita Iyer",
                "+91 99304 88210",
                "verified",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Boutique 2BHK Sea-Breeze Apartment",
                "Sea Pearl Apartments",
                "Andheri West",
                48000,
                150000,
                2,
                920,
                "Fully furnished",
                "Bachelors & Working Professionals Welcome",
                "24/7 Water,Power Backup,Lift,Sea View,Gas Pipeline,Reserved Parking",
                "Tastefully curated home with sea breeze, false ceiling lighting, modular kitchen, and double-glazed soundproof windows. Quiet residential street with easy access to Versova metro.",
                "public/images/bandra_penthouse.jpg",
                "Farhan Merchant",
                "+91 98200 66190",
                "verified",
                datetime.now().isoformat(timespec="seconds")
            ),
        ]
        conn.executemany(
            """
            INSERT INTO property_listings 
                (user_id, title, society_name, locality, rent, deposit, bedrooms, carpet_area,
                 furnished, bachelor_policy, amenities, description, photo_path, owner_name, owner_phone, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_listings
        )

    # Seed society reviews
    count_reviews = conn.execute("SELECT COUNT(*) AS c FROM society_reviews").fetchone()["c"]
    if count_reviews == 0:
        sample_reviews = [
            (
                1,
                "Hiranandani Gardens (Somerset & Verona)",
                "Powai",
                5,
                "Tenant (Living here 2 years)",
                5, 5, 5, 4,
                "Continuous 24/7 high-pressure municipal water supply without tanker reliance. European street design, tree-lined walking tracks, super responsive estate management, and MyGate visitor clearance.",
                "Visitor parking inside the complex is strictly limited. Society charges a one-time tenant movement fee of ₹1,000 and requires standard police verification form.",
                "One of the best managed residential townships in Mumbai. Great lifestyle for working professionals in Powai and Vikhroli tech parks. Bachelors are accepted if paperwork is in order.",
                "public/images/society_hiranandani.jpg",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Godrej The Trees",
                "Vikhroli",
                5,
                "Tenant (Living here 1 year)",
                5, 5, 5, 5,
                "Zero moral policing! Bachelors are treated with total dignity and equal amenity access. Beautiful sustainable campus with Taj hotel, cafes, brewery, and retail promenade on campus.",
                "Rents and maintenance deposits are on the higher side. Highway traffic can get noisy during evening rush if flat faces Eastern Express Highway.",
                "Exceptional community. 24/7 piped gas, RO water systems, top-notch gym and Olympic pool. If your office is in BKC, Kanjurmarg, or Powai, this is unbeatable.",
                "public/images/society_godrej.jpg",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Oberoi Woods & Esquire",
                "Goregaon",
                4,
                "Owner (Living here 3 years)",
                5, 5, 4, 3,
                "Unbeatable Western suburb connectivity with direct flyover to Western Express Highway and private access corridor to Oberoi Mall. Magnificent landscaped podium.",
                "Society committee has strict guest guidelines for bachelor tenants: overnight guests must be logged on the app in advance. Move-in shifting timings strictly 10 AM to 6 PM.",
                "Top-tier construction quality and acoustic insulation. Water and power backup are 100% reliable. Tenants must ensure the owner signs the society NOC before move-in date.",
                "public/images/society_oberoi.jpg",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Lokhandwala Complex (Windermere & Green Acres)",
                "Andheri West",
                4,
                "Tenant (Living here 3 years)",
                4, 4, 4, 5,
                "Most bachelor-friendly locality in Western Mumbai. Vibrant 24/7 food culture, gyms, and quick auto/metro connectivity. Friendly neighborhood.",
                "Monsoon waterlogging near main market road junction. BMC water supply comes twice a day into underground tanks, so water pumps run on fixed schedules.",
                "Great for creative and tech professionals. Landlords here are accustomed to bachelor tenants and lease agreements are straightforward.",
                "public/images/andheri_lokhandwala.jpg",
                datetime.now().isoformat(timespec="seconds")
            ),
            (
                1,
                "Rustomjee Urbania (Azziano)",
                "Thane",
                4,
                "Tenant (Living here 2 years)",
                4, 5, 4, 4,
                "Amazing value for money. Flat size is almost 40% bigger than what you get in Western suburbs for the same rent. 40+ amenities including sports club and grocery supermarket.",
                "Peak hour Thane toll naka bottleneck if driving towards Mumbai between 8:30 AM and 10:30 AM.",
                "Very clean, organized township with strict security guards and good maintenance staff. Dedicated app for raising plumbing and electrical tickets.",
                "public/images/society_rustomjee.jpg",
                datetime.now().isoformat(timespec="seconds")
            ),
        ]
        conn.executemany(
            """
            INSERT INTO society_reviews 
                (user_id, society_name, locality, rating, resident_type, water_rating, security_rating,
                 maintenance_rating, bachelor_rating, pros, cons, review, photo_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            sample_reviews
        )

    # Ensure Lodha Park is present in property_listings
    has_lodha = conn.execute("SELECT COUNT(*) AS c FROM property_listings WHERE society_name LIKE '%Lodha%'").fetchone()["c"]
    if has_lodha == 0:
        conn.execute(
            """
            INSERT INTO property_listings 
                (user_id, title, society_name, locality, rent, deposit, bedrooms, carpet_area,
                 furnished, bachelor_policy, amenities, description, photo_path, owner_name, owner_phone, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "Sky Villa 3BHK in 7-Acre Private Park",
                "Lodha Park (The Park)",
                "Lower Parel",
                115000,
                350000,
                3,
                1450,
                "Fully furnished",
                "All Welcome",
                "24/7 Water,Power Backup,Lift,Gym,Swimming Pool,Clubhouse,Gas Pipeline,EV Charging,Security / CCTV,Concierge",
                "Ultra-luxury residence in South Mumbai's prestigious 7-acre private park development. Marble finishes, modular Poggenpohl kitchen, panoramic sea and racecourse views. Full access to Evander Holyfield gym, heated indoor pool, and private cinema.",
                "public/images/lowerparel_lodha.jpg",
                "Karan Singhania",
                "+91 98200 88910",
                "verified",
                datetime.now().isoformat(timespec="seconds")
            )
        )

    # Ensure Lodha Park is present in society_reviews
    has_lodha_rev = conn.execute("SELECT COUNT(*) AS c FROM society_reviews WHERE society_name LIKE '%Lodha%'").fetchone()["c"]
    if has_lodha_rev == 0:
        conn.execute(
            """
            INSERT INTO society_reviews 
                (user_id, society_name, locality, rating, resident_type, water_rating, security_rating,
                 maintenance_rating, bachelor_rating, pros, cons, review, photo_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "Lodha Park (Allura & Parkside)",
                "Lower Parel",
                5,
                "Tenant (Living here 2 years)",
                5, 5, 5, 5,
                "World-class private 7-acre park in the center of Lower Parel. 100% municipal RO water, biometric security, zero bachelor discrimination, and immediate access to commercial hubs (One World Center, High Street Phoenix).",
                "High maintenance fees and stringent move-in delivery protocols with elevator booking required 48 hours in advance.",
                "Peak corporate luxury living in Mumbai. Perfect for senior software engineers, founders, and finance professionals working in Lower Parel or BKC.",
                "public/images/society_lodha.jpg",
                datetime.now().isoformat(timespec="seconds")
            )
        )


# --------------------------------------------------------------------------- #
# Rule settings (editable playbook)
# --------------------------------------------------------------------------- #
def get_rule_settings() -> dict[str, dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT rule_id, enabled, severity FROM rule_settings").fetchall()
        return {
            r["rule_id"]: {"enabled": bool(r["enabled"]), "severity": r["severity"]}
            for r in rows
        }


def set_rule_setting(rule_id: str, enabled: bool, severity: str | None) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO rule_settings (rule_id, enabled, severity)
            VALUES (?, ?, ?)
            ON CONFLICT(rule_id) DO UPDATE SET enabled = excluded.enabled,
                                               severity = excluded.severity
            """,
            (rule_id, 1 if enabled else 0, severity),
        )


def reset_rule_settings() -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM rule_settings")
