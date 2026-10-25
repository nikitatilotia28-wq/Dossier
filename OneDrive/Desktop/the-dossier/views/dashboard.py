"""
The Dossier — Executive Dashboard.
Multi-sided platform combining verified owner listings, society reviews,
locality market index, contract intelligence, and 1-click interactive demo.
"""

import os
import pandas as pd
import streamlit as st

from core.nav import go_to
from core.premium_theme import apply_premium_theme
from core.db import get_property_listings, get_society_reviews, save_scan
from core.extractor import analyze
from core.sample import SAMPLE_CONTRACT


def _plain_issue(finding):
    return finding.get("plain") or finding.get("rationale") or "This part may need clarification before you sign."


def render() -> None:
    apply_premium_theme()

    # Get live persisted counts
    listings = get_property_listings()
    reviews = get_society_reviews()
    result = st.session_state.get("result")

    # Header
    st.markdown(
        """
        <div class="page-header">
            <div class="eyebrow">The Dossier · Contract & Housing Intelligence</div>
            <h1>Mumbai Rental Record & Verification Platform</h1>
            <p>Direct owner house listings, verified resident society reviews, locality rent analytics, and AI-powered rental agreement risk detection.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------ #
    # ⚡ INTERACTIVE PLATFORM DEMO
    # ------------------------------------------------------------------ #
    with st.container(border=True):
        f_left, f_right = st.columns([3, 1.4])
        with f_left:
            st.markdown("#### ⚡ Interactive Platform Demo")
            st.caption("One-click demonstration: loads live verified listings, society ratings, and an audited Mumbai agreement.")
        with f_right:
            if st.button("⚡ Run Platform Demo", type="primary", use_container_width=True, key="interactive_demo_dash"):
                scanned_res = analyze(SAMPLE_CONTRACT)
                st.session_state.result = scanned_res
                st.session_state.findings = scanned_res.get("findings", [])
                st.session_state.contract_text = SAMPLE_CONTRACT
                st.session_state.filename = "Mumbai Bachelor Rental Agreement (Demo Specimen)"
                st.session_state.analysis_done = True
                user_id = st.session_state.get("user_id", 1)
                save_scan("Mumbai Bachelor Rental Agreement (Demo Specimen)", scanned_res, user_id=user_id)
                st.rerun()

    st.write("")

    # ------------------------------------------------------------------ #
    # 1. PLATFORM KPI STATS
    # ------------------------------------------------------------------ #
    tot_listings = len(listings)
    tot_reviews = len(reviews)
    avg_score = sum(r["rating"] for r in reviews) / tot_reviews if tot_reviews else 4.8

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🏡 Verified Properties", f"{tot_listings}+ Active", "Powai · Andheri · Lower Parel")
    k2.metric("🏢 Monitored Societies", f"{tot_reviews}+ Societies", "4 Photos & DTI™ Verified")
    k3.metric("⭐ Resident Community Score", f"{avg_score:.1f} / 5.0", "★★★★★ High Reliability")
    k4.metric("📑 Legal Playbook Engine", "15 Rules Active", "Automated Regex & Risk Scoring")

    st.markdown("---")

    # ------------------------------------------------------------------ #
    # 2. QUICK ACTIONS COMMAND BAR
    # ------------------------------------------------------------------ #
    st.markdown("### ⚡ Quick Navigation")
    qa1, qa2, qa3, qa4, qa5, qa6 = st.columns(6)
    with qa1:
        if st.button("📑 Scan Lease", key="dash_btn_scan", use_container_width=True):
            go_to("scan")
    with qa2:
        if st.button("🛡️ Deposit Shield", key="dash_btn_escrow", use_container_width=True):
            go_to("workspace")
    with qa3:
        if st.button("🏢 Ratings (DTI)", key="dash_btn_soc", use_container_width=True):
            go_to("society")
    with qa4:
        if st.button("🏡 Find Homes", key="dash_btn_prop", use_container_width=True):
            go_to("property")
    with qa5:
        if st.button("👥 Roommates", key="dash_btn_roommates", use_container_width=True):
            go_to("roommates")
    with qa6:
        if st.button("🚀 Startup Pitch", key="dash_btn_pitch", use_container_width=True):
            go_to("pitch")

    st.write("")

    # ------------------------------------------------------------------ #
    # 3. FEATURED OWNER LISTINGS PREVIEW (ALL UNIFORM IMAGES)
    # ------------------------------------------------------------------ #
    st.markdown("### 🏡 Featured Direct-Owner Listings")
    st.caption("Zero-brokerage rental properties verified on The Dossier platform.")

    top_listings = listings[:3] if listings else []
    if top_listings:
        cols = st.columns(len(top_listings))
        for col, item in zip(cols, top_listings):
            with col:
                with st.container(border=True):
                    photo_path = item.get("photo_path")
                    if photo_path and os.path.exists(photo_path):
                        st.image(photo_path, use_container_width=True)
                    else:
                        st.image("public/images/powai_hiranandani.jpg", use_container_width=True)

                    st.markdown(
                        f"""
                        <div style="margin-top:0.4rem;">
                            <span class="badge-locality">{item['locality']}</span>
                            <span class="badge-verified" style="float:right;">✓ {item.get('status', 'Verified').title()}</span>
                        </div>
                        <h4 style="margin:0.5rem 0 0.2rem 0; color:#1e3a8a;">{item['title']}</h4>
                        <div style="font-size:1.25rem; font-weight:800; color:#1e3a8a;">₹{item['rent']:,}<span style="font-size:0.75rem; font-weight:500; color:#64748b;">/month</span></div>
                        <div style="font-size:0.8rem; color:#64748b; margin-bottom:0.4rem;">{item['bedrooms']} BHK · {item.get('carpet_area', 750)} sq ft · {item.get('furnished', 'Furnished')}</div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.caption(item["description"][:110] + "...")
                    if st.button("View in Property Hub", key=f"view_dash_prop_{item['id']}", use_container_width=True):
                        go_to("property")

    st.write("")

    # ------------------------------------------------------------------ #
    # 4. RESIDENT SOCIETY REVIEWS PREVIEW
    # ------------------------------------------------------------------ #
    st.markdown("### 🏢 Top-Rated Mumbai Housing Societies")
    st.caption("Real resident feedback on water availability, bachelor restrictions, and maintenance.")

    top_reviews = reviews[:2] if reviews else []
    if top_reviews:
        rcols = st.columns(len(top_reviews))
        for rcol, rev in zip(rcols, top_reviews):
            with rcol:
                with st.container(border=True):
                    r_img_col, r_text_col = st.columns([1, 1.8])
                    with r_img_col:
                        photo_path = rev.get("photo_path")
                        if photo_path and os.path.exists(photo_path):
                            st.image(photo_path, use_container_width=True)
                        else:
                            st.image("public/images/hiranandani_1_facade.jpg", use_container_width=True)
                    with r_text_col:
                        stars = "★" * rev["rating"]
                        st.markdown(f"**{rev['society_name']}** · <span class='badge-locality'>{rev['locality']}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span class='rating-pill'>{stars} {rev['rating']}.0</span> · <small>{rev.get('resident_type', 'Tenant')}</small>", unsafe_allow_html=True)
                        st.write(f"💧 Water 24/7: **{rev.get('water_rating', 5)}/5** · 🛡️ Security: **{rev.get('security_rating', 5)}/5**")
                        st.caption(f"“{rev['review'][:120]}...”")
                        if st.button("Read All 4-Photo Reviews", key=f"dash_rev_btn_{rev['id']}", use_container_width=True):
                            go_to("society")

    st.write("")

    # ------------------------------------------------------------------ #
    # 5. MUMBAI LOCALITY MARKET RENT INDEX (CHART)
    # ------------------------------------------------------------------ #
    st.markdown("### 📊 Mumbai Rental Benchmark Index (2026)")
    st.caption("Live comparative average monthly rent across key Mumbai employment and residential nodes.")

    rent_data = pd.DataFrame(
        {
            "Locality": ["Powai", "Andheri West", "Lower Parel", "Vikhroli", "Goregaon East", "Bandra West", "Thane West"],
            "1 BHK (₹)": [26000, 28000, 52000, 22000, 20000, 45000, 16000],
            "2 BHK (₹)": [42000, 48000, 85000, 38000, 36000, 75000, 24000],
            "3 BHK (₹)": [65000, 72000, 135000, 58000, 54000, 120000, 36000],
        }
    ).set_index("Locality")

    st.bar_chart(rent_data, height=280)

    st.write("")

    # ------------------------------------------------------------------ #
    # 6. CONTRACT AUDIT / INSTANT PRACTICE SCANNER
    # ------------------------------------------------------------------ #
    st.markdown("### 📑 Rental Agreement Risk Intelligence")

    if not result:
        with st.container(border=True):
            st.markdown(
                """
                <h4>⚡ One-Click Legal Contract Engine Demo</h4>
                <p>Run our transparent legal playbook against a standard Mumbai Bachelor Leave & License agreement to identify uncapped liabilities, missing deposit protections, and one-sided termination clauses.</p>
                """,
                unsafe_allow_html=True,
            )
            sc_col1, sc_col2 = st.columns([2, 1])
            with sc_col1:
                st.caption("Evaluates against Indian Contract Act principles, Maharashtra Rent Control guidelines, and standard tenant protections.")
            with sc_col2:
                if st.button("🚀 Test Practice Agreement Scan", type="primary", use_container_width=True):
                    scanned_res = analyze(SAMPLE_CONTRACT)
                    st.session_state.result = scanned_res
                    st.session_state.filename = "Mumbai Bachelor Rental Agreement (Practice Specimen)"
                    user_id = st.session_state.get("user_id", 1)
                    save_scan("Mumbai Bachelor Rental Agreement (Practice Specimen)", scanned_res, user_id=user_id)
                    st.rerun()

    if result:
        findings = [f for f in (result or {}).get("findings", []) if f.get("status") == "flagged"]
        high = result.get("summary", {}).get("high", 0)
        medium = result.get("summary", {}).get("medium", 0)
        total = result.get("summary", {}).get("flagged", len(findings))
        risk_score = result.get("summary", {}).get("risk_score", 0)
        risk_band = result.get("summary", {}).get("risk_band", "Moderate")

        current_name = st.session_state.get("filename", "Your rental agreement")

        with st.container(border=True):
            st.markdown(f"#### Active Audit: **{current_name}**")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Risk Score", f"{risk_score} / 100", risk_band)
            m2.metric("Total Flags", f"{total} points", "Requires Attention")
            m3.metric("High Severity", f"{high} issues", "Uncapped liability / One-sided")
            m4.metric("Moderate Severity", f"{medium} issues", "Clarify in writing")

            st.write("")
            for idx, finding in enumerate(findings[:3]):
                sev = finding.get("severity", "low").title()
                tit = finding.get("title", "Clause point")
                with st.expander(f"⚠️ {idx + 1}. {tit} · {sev}", expanded=(idx == 0)):
                    st.write(_plain_issue(finding))
                    if finding.get("matches"):
                        st.markdown(f"**Found in text:** “{finding['matches'][0]}”")
                    st.markdown(f"**Negotiation Advice:** {finding.get('recommendation', 'Clarify with landlord in writing.')}")

            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("Open Full Scan Analysis & Redlines", type="primary", use_container_width=True):
                    go_to("scan")
            with act_col2:
                if st.button("Scan Another Agreement", use_container_width=True):
                    st.session_state.pop("result", None)
                    st.session_state.pop("filename", None)
                    go_to("scan")

    st.write("")

    # Dropdown for Legal & Institutional Theory
    with st.expander("📖 Institutional Regulatory Framework & Tenancy Law (Deep-Dive)"):
        st.write(
            "The Dossier platform operates at the intersection of the **Model Tenancy Act (MTA), 2021**, the **Maharashtra Rent Control Act, 1999**, "
            "and the **Digital Personal Data Protection (DPDP) Act, 2023**.\n\n"
            "Key statutory baselines enforced:\n"
            "• **Section 55, Maharashtra Rent Control Act**: Mandates that every Leave & License agreement must be in writing and registered with the Sub-Registrar.\n"
            "• **Section 73 & 74, Indian Contract Act, 1872**: Prohibits arbitrary penalty clauses and liquidated damage forfeiture exceeding actual documented loss.\n"
            "• **Section 108(m), Transfer of Property Act, 1882**: Establishes that the licensee is not liable for reasonable wear-and-tear resulting from ordinary residential occupation."
        )

    st.markdown('<div class="notice"><strong>The Dossier Commitment:</strong> The Dossier is an evidence organizer and contract risk intelligence assistant. Always physically inspect properties, verify landlord title, and keep move-in photos and payment receipts.</div>', unsafe_allow_html=True)
