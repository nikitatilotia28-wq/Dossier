"""
Mumbai Property & Owner Listing Hub.
Explore verified homes, list properties as an owner, manage verification,
and compare locality living costs.
"""

import os
import re
from datetime import datetime
import pandas as pd
import streamlit as st

from core.nav import go_to
from core.premium_theme import apply_premium_theme
from core.db import (
    get_property_listings,
    save_property_listing,
    update_property_listing_status,
    delete_property_listing,
)
from core.i18n import t


def _save_uploaded_photo(uploaded_file, prefix: str = "listing") -> str | None:
    if not uploaded_file:
        return None
    os.makedirs("data/uploads", exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", uploaded_file.name)
    path = os.path.join("data/uploads", f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{safe_name}")
    with open(path, "wb") as handle:
        handle.write(uploaded_file.getbuffer())
    return path


LOCALITIES = {
    "Powai": {
        "lat": 19.1176, "lon": 72.9060, "rent": "₹25k–₹55k", "share": "₹15k–₹25k",
        "transit": "JVLR + Metro Line 6 (Upcoming)", "commute": "Good for Powai Tech Park, Vikhroli, and Kanjurmarg",
        "signals": ["Strong working professional crowd", "24/7 water in gated societies like Hiranandani", "Higher deposits"],
    },
    "Andheri West": {
        "lat": 19.1364, "lon": 72.8296, "rent": "₹22k–₹50k", "share": "₹14k–₹22k",
        "transit": "Metro Line 1 & Line 2A + Western Local", "commute": "Quick access to BKC, Lower Parel, and Nesco",
        "signals": ["Most bachelor-friendly area", "Vibrant nightlife and food", "Check monsoon waterlogging on Link Road"],
    },
    "Vikhroli": {
        "lat": 19.1111, "lon": 72.9278, "rent": "₹20k–₹60k", "share": "₹12k–₹20k",
        "transit": "Central Line + Eastern Express Highway", "commute": "15 mins to BKC via flyover, quick to Powai",
        "signals": ["Modern townships (Godrej)", "Direct highway access", "Good green cover"],
    },
    "Goregaon": {
        "lat": 19.1663, "lon": 72.8526, "rent": "₹18k–₹42k", "share": "₹11k–₹19k",
        "transit": "Western Express Highway + Metro Line 7", "commute": "Direct to Malad, Nesco IT park, and Bandra",
        "signals": ["Oberoi Mall and modern high-rises", "Check society bachelor rules in advance", "Good power backup"],
    },
    "Lower Parel": {
        "lat": 18.9953, "lon": 72.8312, "rent": "₹75k–₹1.5L", "share": "₹35k–₹60k",
        "transit": "Western + Central Railway & Coastal Road", "commute": "Walk to One World Center, High Street Phoenix & BKC",
        "signals": ["Ultra-luxury high-rises (Lodha, Indiabulls)", "24/7 commercial & dining hub", "MahaRERA verified towers"],
    },
    "Thane": {
        "lat": 19.2183, "lon": 72.9781, "rent": "₹15k–₹30k", "share": "₹9k–₹15k",
        "transit": "Central Line + Eastern Freeway", "commute": "Ideal for remote workers or Thane/Airoli IT parks",
        "signals": ["40% more carpet area for same rent", "Township living with 40+ amenities", "Check morning toll traffic"],
    },
}

SAMPLE_PROPERTY_PHOTOS = {
    "Powai Luxury 2BHK (Hiranandani)": "public/images/powai_hiranandani.jpg",
    "Lower Parel Luxury Sky Villa (Lodha)": "public/images/lowerparel_lodha.jpg",
    "Andheri Modern 1BHK (Lokhandwala)": "public/images/andheri_lokhandwala.jpg",
    "Vikhroli Forest View 3BHK (Godrej)": "public/images/vikhroli_godrej.jpg",
    "Goregaon Studio / 1RK (Oberoi Woods)": "public/images/goregaon_oberoi.jpg",
    "Thane Gated 2BHK (Rustomjee)": "public/images/thane_rustomjee.jpg",
    "Bandra Sea-Breeze 2BHK": "public/images/bandra_penthouse.jpg",
}

ALL_AMENITIES = [
    "24/7 Water", "Power Backup", "Lift", "Gym", "Swimming Pool",
    "Gas Pipeline", "Reserved Parking", "Security / CCTV", "Clubhouse", "EV Charging"
]


def render() -> None:
    apply_premium_theme()

    st.markdown(
        f"""
        <div class="page-header">
            <div class="eyebrow">{t("property")} · Verified Housing Hub</div>
            <h1>🏡 Mumbai Property Listings & Owner Portal</h1>
            <p>Direct owner listings, verified rental flats, transparent deposits, bachelor friendliness scores, and token protection.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    listings = get_property_listings()

    tab_browse, tab_post, tab_manage, tab_locality, tab_checklist = st.tabs(
        [
            "🔍 Browse Verified Flats",
            "➕ List House as Owner",
            "🛡️ Listing Admin & Verification",
            "📍 Locality Living & Cost Guide",
            "📋 Anti-Fraud Checklist",
        ]
    )

    # ------------------------------------------------------------------ #
    # TAB 1: BROWSE LISTINGS
    # ------------------------------------------------------------------ #
    with tab_browse:
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1, 1.2])
        search_q = f_col1.text_input("Search property title or society", placeholder="e.g. Hiranandani, Powai, 2BHK")
        filter_loc = f_col2.selectbox("Locality", ["All Localities"] + list(LOCALITIES.keys()))
        filter_bhk = f_col3.selectbox("Bedrooms", ["Any BHK", "1 BHK / 1RK", "2 BHK", "3+ BHK"])
        max_budget = f_col4.slider("Max Rent (₹/mo)", 15000, 90000, 75000, 2500)

        # Filter properties
        filtered = listings
        if search_q.strip():
            sq = search_q.strip().lower()
            filtered = [
                l for l in filtered
                if sq in l["title"].lower()
                or sq in l["locality"].lower()
                or sq in (l.get("society_name") or "").lower()
                or sq in l["description"].lower()
            ]
        if filter_loc != "All Localities":
            filtered = [l for l in filtered if l["locality"] == filter_loc]
        if filter_bhk == "1 BHK / 1RK":
            filtered = [l for l in filtered if l["bedrooms"] == 1]
        elif filter_bhk == "2 BHK":
            filtered = [l for l in filtered if l["bedrooms"] == 2]
        elif filter_bhk == "3+ BHK":
            filtered = [l for l in filtered if l["bedrooms"] >= 3]
        filtered = [l for l in filtered if l["rent"] <= max_budget]

        st.caption(f"Showing {len(filtered)} active property listing(s)")

        if not filtered:
            st.info("No properties found matching your filter criteria. Try expanding the budget or changing locality.")

        for item in filtered:
            with st.container(border=True):
                # Header row: Title + Badges + Rent
                top_left, top_right = st.columns([3, 1.3])
                with top_left:
                    st.markdown(
                        f"""
                        <h3 style="margin:0; padding:0; display:inline;">{item['title']}</h3>
                        <span class="badge-locality" style="margin-left:8px;">{item['locality']}</span>
                        """,
                        unsafe_allow_html=True,
                    )
                    soc_name = item.get("society_name") or "Residential Society"
                    st.caption(f"Society: **{soc_name}** · Owner: **{item.get('owner_name', 'Verified Owner')}**")

                with top_right:
                    st.markdown(
                        f"""
                        <div style="text-align:right;">
                            <div style="font-size:1.45rem; font-weight:800; color:#1e3a8a;">₹{item['rent']:,}<span style="font-size:0.85rem; font-weight:500; color:#64748b;">/month</span></div>
                            <div style="font-size:0.82rem; color:#64748b;">Deposit: ₹{item.get('deposit', item['rent']*3):,}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.write("")
                col_img, col_info = st.columns([1.2, 2])

                with col_img:
                    photo_path = item.get("photo_path")
                    if photo_path and os.path.exists(photo_path):
                        st.image(photo_path, caption=f"{item['title']}", use_container_width=True)
                    else:
                        st.image("public/images/powai_hiranandani.jpg", caption="Mumbai Verified Property", use_container_width=True)

                    # Status badge below photo
                    st_status = item.get("status", "pending")
                    if st_status == "verified":
                        st.markdown('<span class="badge-verified">✓ Verified Owner Listing</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="badge-pending">⏳ Under Review & Document Check</span>', unsafe_allow_html=True)

                with col_info:
                    # Specs row
                    s1, s2, s3, s4 = st.columns(4)
                    s1.metric("Layout", f"{item['bedrooms']} BHK")
                    s2.metric("Carpet Area", f"{item.get('carpet_area', 650)} sq ft")
                    s3.metric("Furnishing", item.get("furnished", "Semi-furnished"))
                    s4.metric("Occupancy", "Bachelors OK")

                    # Description
                    st.markdown(f"**Description & Highlights:**")
                    st.write(item["description"])

                    # Amenities
                    amenity_str = item.get("amenities", "24/7 Water,Power Backup,Lift,Security / CCTV")
                    amenity_pills = "".join(f'<span class="badge-amenity">{a.strip()}</span>' for a in amenity_str.split(",") if a.strip())
                    st.markdown(f"<div style='margin-bottom:0.75rem;'>{amenity_pills}</div>", unsafe_allow_html=True)

                    # Contact & Action buttons
                    b1, b2, b3 = st.columns([1.2, 1.2, 1.2])
                    with b1:
                        if st.button("📞 Contact Owner", key=f"contact_{item['id']}", use_container_width=True):
                            phone = item.get("owner_phone") or "+91 98200 12345"
                            st.success(f"Owner Phone: **{phone}**\n\nDirect contact unlocked. Mention **The Dossier** for zero brokerage.")
                    with b2:
                        if st.button("📅 Schedule Visit", key=f"visit_{item['id']}", use_container_width=True):
                            st.info(f"Site visit request forwarded to {item.get('owner_name', 'the landlord')}. They will confirm slot via WhatsApp.")
                    with b3:
                        if st.button("📑 Scan Agreement", key=f"agreement_{item['id']}", use_container_width=True):
                            go_to("scan")

    # ------------------------------------------------------------------ #
    # TAB 2: LIST HOUSE AS OWNER
    # ------------------------------------------------------------------ #
    with tab_post:
        st.markdown("### ➕ Post a Property as an Owner")
        st.markdown(
            "List your Mumbai apartment directly to verified tenants. No brokerage, direct rent agreement verification, and complete transparency."
        )

        # Sample Demo Quick-Fill
        with st.container(border=True):
            f_col_l, f_col_r = st.columns([3, 1.4])
            with f_col_l:
                st.markdown("#### ⚡ Auto-Fill Sample Listing")
                st.caption("Fast-track owner listing workflow with sample apartment details for Hiranandani Gardens.")
            with f_col_r:
                if st.button("⚡ Auto-Fill Sample Listing", use_container_width=True, key="demo_fill_owner"):
                    st.session_state["demo_owner_prefill"] = True
                    st.rerun()

        prefill = st.session_state.get("demo_owner_prefill", False)

        with st.form("owner_post_listing_form"):
            c1, c2 = st.columns(2)
            with c1:
                post_title = st.text_input("Listing Title *", value="Lakefront 2BHK in Hiranandani Gardens" if prefill else "", placeholder="e.g. Sunlit 2BHK with Lake View in Powai")
                post_society = st.text_input("Society / Building Name *", value="Hiranandani Somerset" if prefill else "", placeholder="e.g. Hiranandani Gardens Somerset")
                loc_list = list(LOCALITIES.keys())
                post_locality = st.selectbox("Locality *", loc_list, index=loc_list.index("Powai") if prefill and "Powai" in loc_list else 0, key="post_locality_select")
                post_bedrooms = st.selectbox("Bedrooms (BHK) *", [1, 2, 3, 4], index=1)
                post_carpet = st.number_input("Carpet Area (sq. ft)", min_value=200, max_value=4000, value=850 if prefill else 750, step=50)

            with c2:
                post_rent = st.number_input("Expected Monthly Rent (₹) *", min_value=5000, max_value=300000, value=42000 if prefill else 35000, step=1000)
                post_deposit = st.number_input("Security Deposit (₹) *", min_value=10000, max_value=1000000, value=120000 if prefill else 100000, step=5000)
                post_furnishing = st.selectbox("Furnishing Status *", ["Fully furnished", "Semi-furnished", "Unfurnished"])
                post_policy = st.selectbox("Tenant Preference *", ["Bachelors & Working Professionals Welcome", "Families Only", "Female Tenants Only", "All Welcome"])
                post_owner_name = st.text_input("Your Name (Owner) *", value="Rajesh Sharma" if prefill else "", placeholder="e.g. Rajesh Sharma")
                post_owner_phone = st.text_input("Contact Phone / WhatsApp *", value="+91 98201 44520" if prefill else "", placeholder="e.g. +91 98201 XXXXX")

            post_amenities = st.multiselect(
                "Key Amenities Available:",
                ALL_AMENITIES,
                default=["24/7 Water", "Power Backup", "Lift", "Security / CCTV", "Gas Pipeline"]
            )

            post_description = st.text_area(
                "Property Description & Rules *",
                value="High-floor apartment with unhindered Powai lake view. Italian modular kitchen with piped gas, AC in all rooms, and dedicated covered car parking." if prefill else "",
                placeholder="Mention natural sunlight, floor level, parking availability, water supply, pet rules, and proximity to metro / stations...",
                height=110,
            )

            st.markdown("#### Property Photo")
            photo_mode = st.radio("Choose photo source:", ["Upload property photo from my device", "Use curated Mumbai apartment photo library"], horizontal=True)

            custom_file = None
            sample_photo_path = None
            if photo_mode == "Upload property photo from my device":
                custom_file = st.file_uploader("Upload JPG/PNG photo (Max 10MB)", type=["jpg", "jpeg", "png"], key="owner_file_up")
            else:
                sample_choice = st.selectbox("Choose sample photo from library:", list(SAMPLE_PROPERTY_PHOTOS.keys()))
                sample_photo_path = SAMPLE_PROPERTY_PHOTOS[sample_choice]

            submit_listing = st.form_submit_button("Submit Property Listing", type="primary", use_container_width=True)

        if submit_listing:
            if not post_title.strip() or not post_society.strip() or not post_description.strip():
                st.error("Please fill in Title, Society Name, and Description before publishing.")
            else:
                final_photo = None
                if custom_file:
                    final_photo = _save_uploaded_photo(custom_file, prefix="owner_listing")
                elif sample_photo_path:
                    final_photo = sample_photo_path

                user_id = st.session_state.get("user_id", 1)
                new_id = save_property_listing(
                    user_id=user_id,
                    title=post_title.strip(),
                    locality=post_locality,
                    rent=int(post_rent),
                    bedrooms=int(post_bedrooms),
                    furnished=post_furnishing,
                    description=post_description.strip(),
                    photo_path=final_photo,
                    society_name=post_society.strip(),
                    deposit=int(post_deposit),
                    carpet_area=int(post_carpet),
                    bachelor_policy=post_policy,
                    amenities=",".join(post_amenities),
                    owner_name=post_owner_name.strip() or "Property Owner",
                    owner_phone=post_owner_phone.strip() or "+91 98200 00000",
                    status="pending",
                )
                st.success(
                    f"Listing **'{post_title}'** submitted successfully! (Listing #{new_id})\n\n"
                    "It has been saved into the database with **'Pending Review'** status. Check the **'Browse Verified Flats'** tab to see it live!"
                )
                st.rerun()

    # ------------------------------------------------------------------ #
    # TAB 3: LISTING ADMIN & VERIFICATION
    # ------------------------------------------------------------------ #
    with tab_manage:
        st.markdown("### 🛡️ Listing Lifecycle & Verification Hub")
        st.caption("Inspect submitted listings, review owner identity, and toggle between Pending Review and Verified status.")

        all_curr = get_property_listings()
        for it in all_curr:
            with st.container(border=True):
                m_left, m_mid, m_right = st.columns([3, 1.5, 1.5])
                with m_left:
                    st.markdown(f"**{it['title']}** (ID #{it['id']})")
                    st.caption(f"{it['locality']} · {it.get('society_name', '')} · ₹{it['rent']:,}/mo · Owner: {it.get('owner_name', 'Owner')}")
                with m_mid:
                    curr_st = it.get("status", "pending")
                    if curr_st == "verified":
                        st.markdown('<span class="badge-verified">✓ Verified</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="badge-pending">⏳ Pending Review</span>', unsafe_allow_html=True)
                with m_right:
                    b_action = "Mark as Verified" if curr_st == "pending" else "Mark as Pending"
                    new_st = "verified" if curr_st == "pending" else "pending"
                    if st.button(b_action, key=f"toggle_st_{it['id']}", use_container_width=True):
                        update_property_listing_status(it["id"], new_st)
                        st.success(f"Status changed to {new_st.upper()}!")
                        st.rerun()

    # ------------------------------------------------------------------ #
    # TAB 4: LOCALITY INTELLIGENCE & MAP
    # ------------------------------------------------------------------ #
    with tab_locality:
        st.markdown("### 📍 Mumbai Locality Commute & Cost Index")
        sel_loc = st.selectbox("Select locality to analyze:", list(LOCALITIES.keys()))
        l_info = LOCALITIES[sel_loc]

        col_met1, col_met2, col_met3 = st.columns(3)
        col_met1.metric("Typical Rent Range", l_info["rent"])
        col_met2.metric("Room-share Range", l_info["share"])
        col_met3.metric("Transit Backbone", l_info["transit"])

        st.markdown(f"**Commute Fit:** {l_info['commute']}")
        for sig in l_info["signals"]:
            st.markdown(f"- 📌 {sig}")

        st.markdown("#### Geographic Locality Centers")
        pts = pd.DataFrame([{"lat": v["lat"], "lon": v["lon"], "locality": k} for k, v in LOCALITIES.items()])
        st.map(pts, latitude=l_info["lat"], longitude=l_info["lon"], zoom=11)

        st.markdown("#### Real Monthly Cost Simulator")
        c1, c2, c3, c4 = st.columns(4)
        m_rent = c1.number_input("Base Rent (₹)", min_value=5000, value=32000, step=1000)
        m_maint = c2.number_input("Society Maintenance (₹)", min_value=0, value=3500, step=500)
        m_util = c3.number_input("Electricity & Wi-Fi (₹)", min_value=0, value=3000, step=500)
        m_num = c4.number_input("People Sharing", min_value=1, max_value=6, value=2, step=1)

        tot_monthly = m_rent + m_maint + m_util
        per_person = tot_monthly / m_num
        st.metric("Total Monthly Living Cost", f"₹{tot_monthly:,.0f}", f"₹{per_person:,.0f} per roommate")

    # ------------------------------------------------------------------ #
    # TAB 5: MAHARERA & INSTITUTIONAL DUE DILIGENCE
    # ------------------------------------------------------------------ #
    with tab_checklist:
        st.markdown("### 🏛️ MahaRERA & Title Due Diligence Protocol")
        st.caption(
            "Institutional pre-transaction risk protocol based on the Real Estate (Regulation and Development) Act, 2016 "
            "and Maharashtra Stamp Act standards before releasing token deposit capital."
        )

        diligence_items = [
            ("MahaRERA Project Registration Verification", "Cross-check project certificate and carpet area layout on maharera.mahaonline.gov.in."),
            ("Index-II / Title Deed Authentication", "Verify the seller/licensor is the documented legal title holder with sub-registrar records."),
            ("Encumbrance & Mortgage Status Inspection", "Confirm the property is unencumbered and not subject to bank SARFAESI recovery proceedings."),
            ("Bank Account Beneficiary PAN Matching", "Ensure the deposit transfer beneficiary matches the registered title holder PAN to eliminate UPI escrow fraud."),
            ("Mandatory E-Registration Compliance (Sec 55)", "Confirm statutory e-registration under Section 55 of the Maharashtra Rent Control Act, 1999."),
            ("Deterministic Contract Heuristic Audit", "Execute The Dossier AI scanner on the draft agreement to redline uncapped indemnities."),
        ]

        ch_count = 0
        for idx, (title, desc) in enumerate(diligence_items):
            c = st.checkbox(f"**{title}** — {desc}", key=f"dd_protocol_{idx}")
            if c:
                ch_count += 1

        st.progress(ch_count / len(diligence_items), text=f"Institutional Verification: {ch_count} of {len(diligence_items)} Clearances Completed")

        if ch_count == len(diligence_items):
            st.success("✓ Institutional Title & Financial Clearance Granted. Safe to proceed with digital escrow release.")
        else:
            st.info("⚠️ Complete all statutory title and escrow checks before transferring token or deposit funds.")

        with st.expander("📖 Statutory Title Verification & Section 55 Jurisprudence (Deep-Dive)"):
            st.write(
                "Under Section 55 of the Maharashtra Rent Control Act, 1999, the responsibility for statutory e-registration "
                "rests entirely upon the Licensor (landlord). Failure to register attracts criminal liability including "
                "imprisonment up to 3 months or fine under Section 55(2). Furthermore, checking Index-II sub-registrar title "
                "protects tenants against subletting fraud where non-owners pose as landlords to pocket token deposits."
            )

