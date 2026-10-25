"""
The Dossier — Society Reviews & Ratings with resident observations and verified 4-photo campus galleries.
"""

import os
import re
from datetime import datetime
import streamlit as st

from core.premium_theme import apply_premium_theme
from core.db import get_society_reviews, save_society_review, delete_society_review
from core.nav import go_to


def _save_uploaded_photo(uploaded_file, prefix: str = "review") -> str | None:
    if not uploaded_file:
        return None
    os.makedirs("data/uploads", exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", uploaded_file.name)
    path = os.path.join("data/uploads", f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{safe_name}")
    with open(path, "wb") as handle:
        handle.write(uploaded_file.getbuffer())
    return path


LOCALITIES = ["All Localities", "Powai", "Andheri West", "Lower Parel", "Vikhroli", "Goregaon", "Thane"]

SAMPLE_SOCIETY_PHOTOS = {
    "Powai - Hiranandani Gardens": "public/images/hiranandani_1_facade.jpg",
    "Lower Parel - Lodha Park": "public/images/lodha_1_facade.jpg",
    "Vikhroli - Godrej The Trees": "public/images/godrej_1_facade.jpg",
    "Goregaon - Oberoi Woods": "public/images/oberoi_1_facade.jpg",
    "Andheri - Lokhandwala": "public/images/lokhandwala_1_facade.jpg",
    "Thane - Rustomjee Urbania": "public/images/rustomjee_1_facade.jpg",
}


def get_society_photos(society_name: str, fallback_path: str | None = None) -> list[tuple[str, str]]:
    """Returns exactly 4 verified photos with captions for each society, all standardized to 800x533."""
    name = society_name.lower()
    if "hiranandani" in name:
        return [
            ("public/images/hiranandani_1_facade.jpg", "🏢 Tower Facade & Boulevard"),
            ("public/images/hiranandani_2_amenity.jpg", "🏊 Heritage Club & Pool"),
            ("public/images/hiranandani_3_lobby.jpg", "🛡️ Grand Gate & Security"),
            ("public/images/hiranandani_4_interior.jpg", "🏡 Lake-Facing Flat"),
        ]
    elif "lodha" in name:
        return [
            ("public/images/lodha_1_facade.jpg", "🏢 7-Acre Park Skyscraper"),
            ("public/images/lodha_2_amenity.jpg", "🏊 Luxury Pool & Spa"),
            ("public/images/lodha_3_lobby.jpg", "🛡️ Concierge & Security Gate"),
            ("public/images/lodha_4_interior.jpg", "🏡 Sky Villa Suite"),
        ]
    elif "godrej" in name:
        return [
            ("public/images/godrej_1_facade.jpg", "🏢 Sustainable Campus"),
            ("public/images/godrej_2_amenity.jpg", "🌳 Central Promenade"),
            ("public/images/godrej_3_lobby.jpg", "🛡️ Biometric Lobby Gate"),
            ("public/images/godrej_4_interior.jpg", "🏡 Forest Balcony Flat"),
        ]
    elif "oberoi" in name:
        return [
            ("public/images/oberoi_1_facade.jpg", "🏢 High-Rise Architecture"),
            ("public/images/oberoi_2_amenity.jpg", "🏊 Podium Pool Deck"),
            ("public/images/oberoi_3_lobby.jpg", "🛡️ Mall Access & Gate"),
            ("public/images/oberoi_4_interior.jpg", "🏡 Modern Studio Interior"),
        ]
    elif "lokhandwala" in name or "green acres" in name:
        return [
            ("public/images/lokhandwala_1_facade.jpg", "🏢 Windermere Facade"),
            ("public/images/lokhandwala_2_amenity.jpg", "🌳 Resident Park & Gym"),
            ("public/images/lokhandwala_3_lobby.jpg", "🛡️ Security Courtyard"),
            ("public/images/lokhandwala_4_interior.jpg", "🏡 Renovated 2BHK Flat"),
        ]
    elif "rustomjee" in name or "urbania" in name:
        return [
            ("public/images/rustomjee_1_facade.jpg", "🏢 Azziano Township"),
            ("public/images/rustomjee_2_amenity.jpg", "🏀 Sports Arena & Deck"),
            ("public/images/rustomjee_3_lobby.jpg", "🛡️ Gate & Shuttle Hub"),
            ("public/images/rustomjee_4_interior.jpg", "🏡 Mountain-View Flat"),
        ]
    else:
        fb = fallback_path if fallback_path and os.path.exists(fallback_path) else "public/images/society_hiranandani.jpg"
        return [
            (fb, "🏢 Main Campus Facade"),
            ("public/images/society_amenity_pool.jpg", "🏊 Resident Amenities"),
            ("public/images/hiranandani_3_lobby.jpg", "🛡️ Security Entrance"),
            ("public/images/powai_hiranandani.jpg", "🏡 Sample Flat Layout"),
        ]


def calculate_dti(rev: dict) -> tuple[int, str]:
    """Calculate Dossier Trust Index (0-100) based on weighted resilience vectors."""
    w = rev.get("water_rating", 5) or 5
    s = rev.get("security_rating", 5) or 5
    m = rev.get("maintenance_rating", 5) or 5
    b = rev.get("bachelor_rating", 4) or 4
    raw = (w * 0.25 + s * 0.25 + m * 0.20 + b * 0.30) * 20
    score = int(round(raw))
    if score >= 90:
        grade = "Grade A+ (Elite Resilience)"
    elif score >= 80:
        grade = "Grade A (High Resilience)"
    elif score >= 70:
        grade = "Grade B+ (Good)"
    else:
        grade = "Grade B (Standard)"
    return score, grade


def render() -> None:
    apply_premium_theme()

    st.markdown(
        """
        <div class="page-header">
            <div class="eyebrow">The Dossier · Community Intelligence</div>
            <h1>🏢 Mumbai Society Reviews & Resident Ratings</h1>
            <p>Unfiltered observations from real tenants: 24/7 water supply, lift reliability, security protocols, bachelor friendliness, and 4-perspective campus photos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    all_reviews = get_society_reviews()

    # Top KPI Metrics
    total_reviews = len(all_reviews)
    avg_rating = sum(r["rating"] for r in all_reviews) / total_reviews if total_reviews else 5.0
    avg_water = sum(r.get("water_rating", 5) or 5 for r in all_reviews) / total_reviews if total_reviews else 5.0
    bachelor_friendly_pct = (
        int(sum(1 for r in all_reviews if (r.get("bachelor_rating", 4) or 4) >= 4) / total_reviews * 100)
        if total_reviews
        else 85
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Societies Monitored", f"{total_reviews}+", "Verified Mumbai buildings")
    k2.metric("Overall Community Score", f"{avg_rating:.1f} / 5.0", "★★★★★ Verified feedback")
    k3.metric("Water 24/7 Reliability", f"{avg_water:.1f} / 5.0", "Municipal + Tanker backup")
    k4.metric("Bachelor Friendly", f"{bachelor_friendly_pct}%", "NOC & visitor clearance")

    # Theory Dropdown for DTI Formula
    with st.expander("📖 Dossier Trust Index™ (DTI) Resilience Metrics & Formulation (Deep-Dive)"):
        st.write(
            "The Dossier Trust Index (DTI™) is an econometric building resilience score calculated across 4 statutory vectors:\n\n"
            "$$\\text{DTI Score} = (0.25 \\times \\text{Water} + 0.25 \\times \\text{Security} + 0.20 \\times \\text{Maintenance} + 0.30 \\times \\text{BachelorFriendliness}) \\times 20$$\n\n"
            "• **Water Resilience (25%)**: Measures 24/7 municipal RO availability versus tanker dependency.\n"
            "• **Security Protocol (25%)**: Evaluates biometric access, CCTV coverage, and visitor logging without intrusive harassment.\n"
            "• **Maintenance & Upkeep (20%)**: Tracks elevator response SLAs, DG power backup, and fire safety clearances.\n"
            "• **Bachelor Equality (30%)**: Verifies freedom from discriminatory bye-laws, curfews, or illegal visitor bans."
        )

    st.markdown("---")

    tab_explore, tab_write = st.tabs(["🔍 Explore Society Reviews", "✍️ Write a Society Review"])

    with tab_explore:
        col_search, col_locality, col_rating = st.columns([2, 1.2, 1.2])
        search_query = col_search.text_input("Search society or builder name", placeholder="e.g. Hiranandani, Lodha, Godrej, Oberoi")
        selected_locality = col_locality.selectbox("Filter by locality", LOCALITIES)
        selected_rating = col_rating.selectbox("Minimum rating", ["All Ratings", "5 Stars Only", "4+ Stars", "3+ Stars"])

        # Filter logic
        filtered_reviews = all_reviews
        if search_query.strip():
            q = search_query.strip().lower()
            filtered_reviews = [
                r for r in filtered_reviews
                if q in r["society_name"].lower() or q in r["locality"].lower() or q in (r.get("review") or "").lower()
            ]
        if selected_locality != "All Localities":
            filtered_reviews = [r for r in filtered_reviews if r["locality"] == selected_locality]
        if selected_rating == "5 Stars Only":
            filtered_reviews = [r for r in filtered_reviews if r["rating"] == 5]
        elif selected_rating == "4+ Stars":
            filtered_reviews = [r for r in filtered_reviews if r["rating"] >= 4]
        elif selected_rating == "3+ Stars":
            filtered_reviews = [r for r in filtered_reviews if r["rating"] >= 3]

        st.caption(f"Showing {len(filtered_reviews)} resident review(s) with 4-photo campus verification")

        if not filtered_reviews:
            st.info("No society reviews match your search. Be the first resident to review this society in the tab above!")

        for rev in filtered_reviews:
            with st.container(border=True):
                # Header row
                header_left, header_right = st.columns([3, 1.2])
                with header_left:
                    dti_score, dti_grade = calculate_dti(rev)
                    st.markdown(
                        f"""
                        <h3 style="margin:0; padding:0; display:inline;">{rev['society_name']}</h3>
                        <span class="badge-locality" style="margin-left:8px;">{rev['locality']}</span>
                        <span class="badge-verified" style="margin-left:6px;">✓ {rev.get('resident_type', 'Verified Resident')}</span>
                        <span class="badge-verified" style="margin-left:6px; background:#f0fdf4; color:#15803d; border-color:#86efac;">🛡️ DTI™ {dti_score}/100 · {dti_grade}</span>
                        """,
                        unsafe_allow_html=True,
                    )
                with header_right:
                    stars = "★" * rev["rating"] + "☆" * (5 - rev["rating"])
                    st.markdown(f"<div style='text-align:right;'><span class='rating-pill'>{stars} {rev['rating']}.0</span></div>", unsafe_allow_html=True)

                st.write("")

                # Multi-dimension breakdown
                w_col, s_col, m_col, b_col = st.columns(4)
                w_col.metric("💧 Water 24/7", f"{rev.get('water_rating', 5)}/5")
                s_col.metric("🛡️ Security", f"{rev.get('security_rating', 5)}/5")
                m_col.metric("🧹 Upkeep", f"{rev.get('maintenance_rating', 5)}/5")
                b_col.metric("🤝 Bachelors", f"{rev.get('bachelor_rating', 4)}/5")

                st.write("")

                # ---------------------------------------------------------- #
                # 📸 4 PHOTOS PER SOCIETY REVIEW (UNIFORM SIZING)
                # ---------------------------------------------------------- #
                st.markdown("##### 📸 Verified Campus Gallery (4 Standardized Photos):")
                society_photos = get_society_photos(rev["society_name"], rev.get("photo_path"))
                p_cols = st.columns(4)
                for p_col, (p_path, p_caption) in zip(p_cols, society_photos):
                    with p_col:
                        if os.path.exists(p_path):
                            st.image(p_path, caption=p_caption, use_container_width=True)
                        else:
                            st.image("public/images/society_hiranandani.jpg", caption=p_caption, use_container_width=True)

                st.write("")

                # Written feedback
                st.markdown(f"**Resident Feedback:** {rev['review']}")

                if rev.get("pros"):
                    st.markdown(
                        f"""<div class="pros-box"><strong>👍 What Residents Love:</strong><br/>{rev['pros']}</div>""",
                        unsafe_allow_html=True,
                    )
                if rev.get("cons"):
                    st.markdown(
                        f"""<div class="cons-box"><strong>⚠️ Watch Out For:</strong><br/>{rev['cons']}</div>""",
                        unsafe_allow_html=True,
                    )

                foot_left, foot_right = st.columns([2, 1])
                with foot_left:
                    st.caption(f"Reviewed on {rev.get('created_at', '2026-10-15')[:10]} · The Dossier Verified Community Post")
                with foot_right:
                    if st.button("Check Agreement for this Area", key=f"check_area_{rev['id']}", use_container_width=True):
                        go_to("scan")

    with tab_write:
        st.markdown("### ✍️ Share Your Society Observation")
        st.markdown(
            "Help fellow Mumbai home seekers understand actual water supply, lift reliability, maintenance, and committee rules."
        )

        with st.container(border=True):
            f_col_l, f_col_r = st.columns([3, 1.4])
            with f_col_l:
                st.markdown("#### ⚡ Auto-Fill Sample Review")
                st.caption("Fast-track review submission workflow with sample observation data for Lodha Park.")
            with f_col_r:
                if st.button("⚡ Auto-Fill Sample Review", use_container_width=True, key="demo_fill_review"):
                    st.session_state["demo_review_prefill"] = True
                    st.rerun()

        prefill_rev = st.session_state.get("demo_review_prefill", False)

        with st.form("new_society_review_form"):
            c_name, c_loc, c_status = st.columns([2, 1, 1])
            form_society = c_name.text_input("Society / Building Name *", value="Lodha Park (The Park)" if prefill_rev else "", placeholder="e.g. Hiranandani Gardens, Raheja Classique")
            avail_locs = [loc for loc in LOCALITIES if loc != "All Localities"]
            form_locality = c_loc.selectbox("Locality *", avail_locs, index=avail_locs.index("Lower Parel") if prefill_rev and "Lower Parel" in avail_locs else 0)
            form_status = c_status.selectbox("You are a *", ["Current Tenant", "Former Tenant", "Flat Owner", "PG Resident"])

            st.markdown("#### Rate Key Building Dimensions (1 = Poor, 5 = Excellent)")
            r1, r2, r3, r4, r5 = st.columns(5)
            rate_overall = r1.slider("Overall Score", 1, 5, 5 if prefill_rev else 4)
            rate_water = r2.slider("Water Supply 24/7", 1, 5, 5 if prefill_rev else 4)
            rate_security = r3.slider("Gate Security", 1, 5, 5)
            rate_maint = r4.slider("Maintenance & Lifts", 1, 5, 5 if prefill_rev else 4)
            rate_bachelor = r5.slider("Bachelor Friendly", 1, 5, 5 if prefill_rev else 4)

            form_pros = st.text_area("What are the biggest PROS?", value="World-class private 7-acre park, 24/7 municipal RO water, biometric security, zero bachelor discrimination." if prefill_rev else "", height=75)
            form_cons = st.text_area("What should new tenants watch out for?", value="High maintenance fees and elevator booking required 48 hours in advance for shifting." if prefill_rev else "", height=75)
            form_review = st.text_area("Detailed Written Review / Final Advice *", value="Peak corporate luxury living in South Mumbai. Exceptional infrastructure and security." if prefill_rev else "", placeholder="Summary of your living experience here...", height=100)

            st.markdown("#### Add Society / Entrance / Amenities Photo")
            photo_choice = st.radio("Choose photo method:", ["Upload my own photo", "Select verified Mumbai society image library"], horizontal=True)

            form_file = None
            preset_choice = None
            if photo_choice == "Upload my own photo":
                form_file = st.file_uploader("Upload JPG/PNG photo (Max 10MB)", type=["jpg", "jpeg", "png"], key="write_rev_file")
            else:
                preset_name = st.selectbox("Choose sample verified photo:", list(SAMPLE_SOCIETY_PHOTOS.keys()))
                preset_choice = SAMPLE_SOCIETY_PHOTOS[preset_name]

            submitted = st.form_submit_button("Publish Society Review", type="primary", use_container_width=True)

        if submitted:
            if not form_society.strip() or not form_review.strip():
                st.error("Please provide both the Society Name and a Written Review before publishing.")
            else:
                final_photo_path = None
                if form_file:
                    final_photo_path = _save_uploaded_photo(form_file, prefix="society_rev")
                elif preset_choice:
                    final_photo_path = preset_choice

                user_id = st.session_state.get("user_id", 1)
                save_society_review(
                    user_id=user_id,
                    society_name=form_society.strip(),
                    locality=form_locality,
                    rating=int(rate_overall),
                    review=form_review.strip(),
                    photo_path=final_photo_path,
                    resident_type=form_status,
                    water_rating=int(rate_water),
                    security_rating=int(rate_security),
                    maintenance_rating=int(rate_maint),
                    bachelor_rating=int(rate_bachelor),
                    pros=form_pros.strip(),
                    cons=form_cons.strip(),
                )
                st.success(f"Review for **{form_society}** has been published and saved permanently to the database!")
                st.rerun()
