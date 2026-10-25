"""
The Dossier — Urban Rental Trust Protocol & Redline Copilot.

Entry point. Sets up persistent, user-friendly left-sidebar navigation,
instant 1-click interactive demo access, and dispatches to views.

Run:  streamlit run app.py
"""

import streamlit as st

from core.db import init_db, create_or_get_user, save_scan
from core.nav import register, go_to
from core.premium_theme import apply_premium_theme
from core.i18n import setup_language, t
from core.extractor import analyze
from core.sample import SAMPLE_CONTRACT
from views import (
    dashboard,
    property_guide,
    society_reviews,
    scan,
    tenant_workspace,
    roommates,
    rulebook_view,
    about_pitch,
)

st.set_page_config(
    page_title="The Dossier — Rental Agreement Scanner & Redline Copilot",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_premium_theme()

init_db()


def render_login() -> bool:
    st.markdown(
        """
        <div class='login-shell'>
            <div class='eyebrow' style='color:#93c5fd;'>The Dossier · Urban Rental Trust Protocol</div>
            <h1>Your rental record, protected in one place.</h1>
            <p>Smart contract risk audits, instant balanced redlines, verified building resilience metrics (DTI™), and algorithmic security deposit recovery.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------ #
    # ⚡ 1-CLICK INSTANT DEMO ACCESS (SEAMLESS EXPLORATION)
    # ------------------------------------------------------------------ #
    with st.container(border=True):
        st.markdown("### ⚡ Instant Interactive Demo")
        st.caption("Explore the complete platform with preloaded Mumbai rental data, verified listings, and contract risk audits in 1 click:")
        if st.button("🚀 Explore Instant Demo (1-Click)", type="primary", use_container_width=True, key="instant_demo_login"):
            user_id, _ = create_or_get_user("Demo User", "1234")
            st.session_state.user_id = user_id or 1
            st.session_state.username = "Explorer"
            # Preload active scan so results are immediately ready
            res = analyze(SAMPLE_CONTRACT)
            st.session_state.result = res
            st.session_state.findings = res.get("findings", [])
            st.session_state.contract_text = SAMPLE_CONTRACT
            st.session_state.filename = "Mumbai Bachelor Rental Agreement (Sample Walkthrough)"
            st.session_state.analysis_done = True
            save_scan("Mumbai Bachelor Rental Agreement (Sample Walkthrough)", res, user_id=st.session_state.user_id)
            st.rerun()

    st.write("")
    with st.expander("👤 Standard Sign-in / Create Account", expanded=False):
        with st.form("login_form"):
            username = st.text_input("Name", placeholder="e.g. Nikita")
            password = st.text_input("4-digit password", type="password", max_chars=4, placeholder="Example: 1234")
            submitted = st.form_submit_button("Continue", use_container_width=True)
        if submitted:
            user_id, error = create_or_get_user(username, password)
            if error:
                st.error(error)
            else:
                st.session_state.user_id = user_id
                st.session_state.username = username.strip()
                st.rerun()

    st.caption("Designed for Mumbai Metropolitan Region (MMR). All data is saved persistently in the local database.")
    return False


def main() -> None:
    if not st.session_state.get("user_id"):
        render_login()
        return

    setup_language()

    # Enhanced, User-Friendly Navigation Pages
    pages = {
        "dashboard": st.Page(dashboard.render, title="Dashboard", icon="📊", url_path="dashboard", default=True),
        "scan": st.Page(scan.render, title="Scanner & Redline Copilot", icon="📑", url_path="scanner"),
        "workspace": st.Page(tenant_workspace.render, title="Deposit Shield & Escrow", icon="🛡️", url_path="deposit-shield"),
        "society": st.Page(society_reviews.render, title="Society Ratings & Photos", icon="🏢", url_path="society-ratings"),
        "property": st.Page(property_guide.render, title="Find & List Homes", icon="🏡", url_path="homes"),
        "roommates": st.Page(roommates.render, title="Roommate Match & Co-Living", icon="👥", url_path="roommates"),
        "pitch": st.Page(about_pitch.render, title="Executive Pitch & 2026 Vision", icon="🚀", url_path="pitch"),
    }
    register(pages)

    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 0.2rem 0 0.8rem 0; border-bottom: 1px solid rgba(255,255,255,0.18); margin-bottom: 0.75rem;">
                <div style="font-size: 0.7rem; letter-spacing: 0.12em; text-transform: uppercase; color: #93c5fd; font-weight: 700;">Urban Rental Trust Protocol</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin: 0.15rem 0;">THE DOSSIER</div>
                <div style="font-size: 0.75rem; color: #cbd5e1;">Redline Copilot · DTI™ · 2026 Vision</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(f"👤 Signed in: **{st.session_state.get('username', 'User')}**")
        if st.button("Sign out", key="sign_out", use_container_width=True):
            for key in ("user_id", "username", "result", "filename", "uploaded_file", "analysis_done"):
                st.session_state.pop(key, None)
            st.rerun()

    nav = st.navigation(list(pages.values()), position="sidebar")
    nav.run()


main()
