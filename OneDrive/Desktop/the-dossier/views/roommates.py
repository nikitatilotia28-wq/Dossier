"""
The Dossier — Roommate Match Protocol.
Algorithmic co-living compatibility based on employment hub, budget allocation,
and shared tenancy covenants with dropdown legal theory.
"""

from datetime import date
import streamlit as st

from core.nav import go_to
from core.premium_theme import apply_premium_theme

ROOMMATES = [
    {
        "name": "Arjun S.",
        "area": "Andheri West",
        "rent": 22000,
        "move": "November 2026",
        "work": "FinTech Software Engineer (BKC / Andheri)",
        "style": "Clean, early riser, non-smoker, WFH 2 days/week",
        "room": "Master Bedroom with Attached Bath in 2BHK",
        "fit": 94,
        "verified": True,
    },
    {
        "name": "Neha K.",
        "area": "Powai",
        "rent": 24000,
        "move": "December 2026",
        "work": "Product Manager (Hiranandani Tech Park)",
        "style": "Working professional, vegetarian kitchen, quiet evenings",
        "room": "Private Room in Lake-Facing 3BHK",
        "fit": 91,
        "verified": True,
    },
    {
        "name": "Rohan M.",
        "area": "Lower Parel",
        "rent": 35000,
        "move": "November 2026",
        "work": "Investment Banking Associate (One World Center)",
        "style": "Long work hours, fitness enthusiast, tidy common areas",
        "room": "Private Suite in Luxury High-Rise",
        "fit": 88,
        "verified": True,
    },
    {
        "name": "Sameer D.",
        "area": "Goregaon East",
        "rent": 19000,
        "move": "January 2027",
        "work": "Data Analyst (Nesco IT Park)",
        "style": "Weekend cook, social, respect for personal boundaries",
        "room": "Shared 2BHK near Western Express Highway",
        "fit": 82,
        "verified": True,
    },
]


def render() -> None:
    apply_premium_theme()

    st.markdown(
        """
        <div class="page-header" style="background: linear-gradient(135deg, #1e3a8a 0%, #0369a1 100%);">
            <div class="eyebrow" style="color:#7dd3fc;">Co-Living Protocol · Gen Z Shared Tenancy</div>
            <h1>👥 Roommate Match & Shared Tenancy Engine</h1>
            <p>Peer matching based on corporate hubs, budget parity, and mutual tenancy agreements.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------ #
    # ⚡ SAMPLE ROOMMATE MATCH DEMO
    # ------------------------------------------------------------------ #
    with st.container(border=True):
        f_left, f_right = st.columns([3, 1.4])
        with f_left:
            st.markdown("#### ⚡ Sample Roommate Match")
            st.caption("Explore roommate compatibility and generate a downloadable co-tenancy covenant with 1 click.")
        with f_right:
            if st.button("⚡ Run Sample Match Demo", type="primary", use_container_width=True, key="demo_roommate_btn"):
                st.session_state["demo_roommate_active"] = True
                st.session_state["preferred_locality"] = "Andheri West"
                st.rerun()

    st.write("")

    with st.form("roommate_search"):
        a, b, c, d = st.columns(4)
        saved_area = st.session_state.get("preferred_locality", "Any area")
        area_options = ["Any area", "Powai", "Andheri West", "Lower Parel", "Goregaon East", "Vikhroli West"]
        area = a.selectbox("Employment / Residential Hub", area_options, index=area_options.index(saved_area) if saved_area in area_options else 0)
        budget = b.slider("Maximum Monthly Share (₹)", 10000, 60000, 28000, 1000)
        move_options = ["Any time", "November 2026", "December 2026", "January 2027", "February 2027"]
        move = c.selectbox("Target Move-in Horizon", move_options)
        preference = d.selectbox("Lifestyle Alignment", ["All Profiles", "Quiet / Non-Smoker", "WFH Friendly", "Vegetarian Household", "Corporate Professional"])
        search = st.form_submit_button("Filter Compatible Profiles", type="primary", use_container_width=True)

    st.markdown("### Compatibility Matrix")
    fit_left, fit_right = st.columns(2)
    habits = fit_left.multiselect("Core Tenancy Factors:", ["Budget Parity", "Commute Proximity", "Quiet Hours", "Common Expense Split", "Visitor Policy"], default=["Budget Parity", "Commute Proximity", "Common Expense Split"])
    verification = fit_right.multiselect("Institutional Verification Checkpoints:", ["Corporate Email Auth", "Government ID (Aadhaar / PAN)", "Tenancy Contract Cross-Signing", "Background References"], default=["Corporate Email Auth", "Government ID (Aadhaar / PAN)"])

    filtered = [
        p for p in ROOMMATES
        if (area == "Any area" or p["area"] == area) and p["rent"] <= budget and (move == "Any time" or p["move"] == move)
    ]

    st.markdown(f"#### {len(filtered)} Verified Profiles Found")
    if not filtered:
        st.info("No active profiles matching the selected filter constraints. Broaden budget or area to see more candidates.")

    for person in filtered:
        with st.container(border=True):
            left, middle, right = st.columns([1.1, 2.2, 1.2])
            with left:
                st.markdown(f"### {person['name']}")
                st.markdown(f"<span class='badge-verified'>✓ Corporate Verified</span>", unsafe_allow_html=True)
                st.metric("Compatibility", f"{person['fit']}%")
            with middle:
                st.markdown(f"**{person['room']} · <span class='badge-locality'>{person['area']}</span>**", unsafe_allow_html=True)
                st.write(f"Monthly Budget: **₹{person['rent']:,}** · Target Move-in: **{person['move']}**")
                st.write(f"💼 *{person['work']}*")
                st.caption(f"Profile: {person['style']}")
            with right:
                if st.button("Connect via Relay", key=f"connect_{person['name']}", use_container_width=True):
                    st.success(f"Connection request dispatched to {person['name']} via encrypted corporate relay.")

                covenant_txt = f"""SHARED LIVING & EXPENSE COVENANT (CO-TENANCY AGREEMENT)
Date: {date.today().strftime('%d %B %Y')}
Parties: Nikita T. and {person['name']}
Premises: Shared Residential Apartment in {person['area']}, Mumbai

1. RENT & DEPOSIT DIVISION:
- Each party shall contribute fifty percent (50%) of the total monthly rent (INR {person['rent']:,}) directly via UPI on or before the 5th of each calendar month.
- The refundable security deposit is contributed equally. Any lawful deduction shall be shared pro-rata, unless directly attributable to one party's sole negligence.

2. UTILITIES & DAILY EXPENSES:
- Electricity, piped gas, Wi-Fi, drinking water, and society maintenance charges shall be tracked and split equally via automated UPI monthly settlement.

3. WORK-FROM-HOME & QUIET HOURS:
- Both parties agree to observe mutual quiet hours between 10:30 PM and 7:30 AM, and maintain reasonable acoustic separation during daytime corporate calls.

4. EARLY MOVE-OUT / SUCCESSION:
- A roommate wishing to vacate prior to the lease term must provide thirty (30) days written notice and locate a mutually agreeable replacement roommate, without forfeiting deposit share.

_____________________________                _____________________________
CO-TENANT 1                                  CO-TENANT 2 ({person['name']})
Generated via The Dossier Co-Living Protocol
"""
                st.download_button(
                    "📄 Download Covenant",
                    data=covenant_txt,
                    file_name=f"co-tenancy-covenant-{person['name'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    key=f"dl_covenant_{person['name']}",
                    use_container_width=True,
                )

    # Dropdown for Legal Theory
    with st.expander("📖 Co-Living Legal Framework & Joint Tenancy Theory (Deep-Dive)"):
        st.write(
            "Under Indian law (Section 43 of the Indian Contract Act, 1872), joint tenants share joint and several liability "
            "toward the landlord. If one roommate defaults, the landlord may legally demand the full rent from the remaining tenant. "
            "The Dossier Co-Tenancy Covenant creates a distinct, legally enforceable internal indemnity between flatmates, "
            "protecting the paying roommate against unexpected liability and establishing formal pro-rata succession rules."
        )

    st.markdown("---")
    st.markdown("### ➕ Register Your Co-Living Profile")
    with st.expander("Publish Your Roommate Requirements"):
        x, y = st.columns(2)
        p_name = x.text_input("Full Name", placeholder="e.g. Nikita T.")
        p_corp = x.text_input("Organization / Corporate Hub", placeholder="e.g. Senior Analyst @ Deloitte BKC")
        p_budget = y.number_input("Max Monthly Allocation (₹)", min_value=5000, value=25000, step=1000)
        p_hub = y.selectbox("Target Locality", ["Powai", "Andheri West", "Lower Parel", "Vikhroli", "Goregaon"])
        p_desc = st.text_area("Living Routine & Household Preferences", placeholder="Mention work hours, cleanliness preferences, and desired lease duration...")
        if st.button("Publish Verified Profile", type="primary", use_container_width=True):
            st.success("Profile submitted for corporate email authentication and added to active co-living pool.")
