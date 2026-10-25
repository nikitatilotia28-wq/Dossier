"""
The Dossier — Executive Pitch, Quantitative Analysis & 2026 Evolving Generation Vision.
Presents the business model, market opportunity, unit economics,
interactive financial scenario simulator, and 2026 Gen Z rental trends with dropdown details.
"""

import pandas as pd
import streamlit as st

from core.premium_theme import apply_premium_theme
from core.nav import go_to


def render() -> None:
    apply_premium_theme()

    # Executive Hero Banner
    st.markdown(
        """
        <div class="page-header" style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);">
            <div class="eyebrow" style="color: #38bdf8;">Executive Overview · Market Opportunity & Vision</div>
            <h1 style="color: white; font-size: 2.3rem;">The Dossier: Urban Rental Trust Protocol</h1>
            <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 900px;">
                Solving India's ₹2.6 Lakh Crore residential rental trust deficit with smart contract risk intelligence, 
                objective building resilience metrics (DTI™), smart escrow, and zero-brokerage verified listings.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------ #
    # EXECUTIVE FINANCIAL METRICS (HIGH-IMPACT EXECUTIVE DASHBOARD)
    # ------------------------------------------------------------------ #
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rental Economy", "₹2.6 Lakh Crore", "Annual Rent in Top-8 Indian Metros ($32B+)")
    m2.metric("Growth Return", "10.2x Return", "Value Generated per ₹1 Marketing Spent")
    m3.metric("Gross Profit Margin", "86.4%", "High Digital Infrastructure Margins")
    m4.metric("Average Fee per Home", "₹1,499", "Per Verified Property Protection")

    st.markdown("---")

    tab_quant, tab_roi, tab_sim, tab_genz, tab_moat = st.tabs(
        [
            "📊 Market Scale & Business Economics",
            "💰 Tenant & Landlord Financial Value",
            "🧮 Interactive Financial Simulator",
            "🚀 2026 Evolving Generation Hub",
            "🛡️ Competitive Moat & Defensibility",
        ]
    )

    # ------------------------------------------------------------------ #
    # TAB 1: MARKET SCALE & BUSINESS ECONOMICS
    # ------------------------------------------------------------------ #
    with tab_quant:
        st.markdown("### 📊 Market Opportunity Breakdown")
        st.caption("Rental housing market scale across key Indian urban hubs (measured in USD Millions):")

        market_df = pd.DataFrame(
            {
                "Market Opportunity": ["Total Indian Metro Market", "Top Tech & Financial Hubs", "Mumbai MMR Pilot Market"],
                "Market Size ($ Millions)": [32400, 8200, 340],
            }
        ).set_index("Market Opportunity")

        st.bar_chart(market_df, height=260)

        st.write("")
        st.markdown("### 💰 Platform Economics & Growth Efficiency")
        u1, u2, u3, u4 = st.columns(4)
        u1.metric("Marketing Cost per User", "₹240", "Organic word-of-mouth & sharing")
        u2.metric("3-Year User Value", "₹2,450", "Repeat lease renewals")
        u3.metric("Cost Payback Speed", "1.4 Months", "Fast capital turnaround")
        u4.metric("Deposit Protection Fee", "1.5%", "On security deposit float")

        st.write("")
        st.markdown("### 📈 3-Year Growth Projections")
        proj_data = {
            "Performance Metric": ["Protected Units", "Annual Platform Revenue", "Gross Profit Margin", "Operating Profit Margin", "Security Deposits Safeguarded"],
            "Year 1 (2026-27)": ["18,000", "₹3.6 Crore ($430K)", "82.5%", "18.0%", "₹162 Crore"],
            "Year 2 (2027-28)": ["72,000", "₹14.8 Crore ($1.78M)", "85.8%", "32.4%", "₹648 Crore"],
            "Year 3 (2028-29)": ["240,000", "₹52.4 Crore ($6.3M)", "88.2%", "44.1%", "₹2,160 Crore"],
        }
        st.dataframe(pd.DataFrame(proj_data), use_container_width=True, hide_index=True)

        st.write("")
        with st.expander("📖 Detailed Business Model & Financial Assumptions (Deep-Dive)"):
            st.markdown(
                """
                **Mathematical Derivations & Rationale:**
                
                • **Total Lifetime Value per User (LTV)** = Average Revenue per Unit (₹1,499) × Gross Margin (86.4%) ÷ Renewal Churn Rate = **₹2,450**  
                • **Growth Efficiency Multiple** = Lifetime Value (₹2,450) ÷ Marketing Cost (₹240) = **10.2x** (Healthy tech benchmark is > 3.0x)  
                • **Payback Speed** = User Acquisition Cost ÷ Monthly Profit = **1.4 Months** to recover initial marketing expense.  
                • **User Acquisition Strategy**: Strong viral referral loop driven by tenants sharing counter-offer addendums on WhatsApp and using Roommate Match.  
                • **Cost of Capital**: 12% risk-adjusted discount rate applied to forward cash flows under Indian tech valuation standards.
                """
            )

    # ------------------------------------------------------------------ #
    # TAB 2: TENANT & LANDLORD FINANCIAL VALUE
    # ------------------------------------------------------------------ #
    with tab_roi:
        st.markdown("### 💰 The 191x Value Equation for Tenants")
        st.caption("Direct financial savings delivered per tenant move:")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Brokerage Saved", "₹42,000+", "1 Month Rent Avoided")
        r2.metric("Deposit Protected", "₹38,500", "Depreciation Audit")
        r3.metric("Legal Review Saved", "₹15,000", "Standard Lawyer Fee")
        r4.metric("Net Financial Return", "191x", "vs ₹499 Audit Fee")

        st.write("")
        st.markdown("#### Tenant Value Delivery Matrix")
        tenant_val_df = pd.DataFrame(
            {
                "Value Stream": [
                    "Zero Brokerage Matching (Direct Owners)",
                    "AI Deposit Shield™ (Wear-and-Tear Cap)",
                    "Contract Scanner & Balanced Redlines",
                    "Roommate Utility Expense Covenant",
                ],
                "Traditional Cost Without Dossier": ["₹42,000 (1 month rent)", "₹45,000 withheld", "₹15,000 legal fees", "Disputed splits"],
                "Cost With The Dossier": ["₹0 (Zero Brokerage)", "₹0 (100% Lawful Recovery)", "₹499 (SaaS Scan)", "Included in Platform"],
                "Net Benefit to User": ["+₹42,000 Saved", "+₹45,000 Recovered", "+₹14,501 Saved", "Zero Friction"],
            }
        )
        st.dataframe(tenant_val_df, use_container_width=True, hide_index=True)

        st.write("")
        st.markdown("#### Landlord Value Proposition")
        l1, l2, l3 = st.columns(3)
        l1.metric("Vacancy Reduction", "10 Days Faster", "₹14,000 Saved Vacancy Loss")
        l2.metric("Verified Tenant Quality", "100% Background", "Corporate Email + Govt ID")
        l3.metric("Lease Dispute Rate", "< 0.4%", "Standardized Redline Terms")

        with st.expander("📖 Microeconomic Theory of Friction Reduction (Transaction Cost Economics)"):
            st.write(
                "Following Ronald Coase's theory of transaction costs, traditional Indian residential rental markets "
                "suffer from severe information asymmetry and high contracting costs (search costs, bargaining costs, and enforcement costs). "
                "By digitizing lease risk heuristics and standardizing building resilience metrics (DTI™), The Dossier drives transaction "
                "costs toward zero, expanding total consumer surplus across both sides of the marketplace."
            )

    # ------------------------------------------------------------------ #
    # TAB 3: INTERACTIVE FINANCIAL SCENARIO SIMULATOR
    # ------------------------------------------------------------------ #
    with tab_sim:
        st.markdown("### 🧮 Interactive Financial Scenario Simulator")
        st.caption("Adjust key platform parameters to project annual revenue and tenant capital protected:")

        sim_col1, sim_col2 = st.columns([1.5, 1.5])
        with sim_col1:
            sim_units = st.slider("Annual Protected Units (Mumbai MMR)", min_value=5000, max_value=150000, value=35000, step=5000)
            avg_rent_mumbai = st.slider("Average Monthly Rent (₹)", min_value=20000, max_value=80000, value=40000, step=5000)

        with sim_col2:
            take_rate_escrow = st.slider("Escrow Float & Fee Take Rate (%)", min_value=0.5, max_value=3.0, value=1.5, step=0.1)
            audit_fee = st.number_input("Platform Scan Fee per Lease (₹)", min_value=0, max_value=2000, value=499, step=100)

        # Computed Outputs
        sim_arr_cr = (sim_units * audit_fee + sim_units * (avg_rent_mumbai * 3 * (take_rate_escrow / 100.0))) / 10000000.0
        sim_deposit_protected_cr = (sim_units * (avg_rent_mumbai * 3)) / 10000000.0
        sim_brokerage_saved_cr = (sim_units * avg_rent_mumbai) / 10000000.0
        sim_ebitda_margin = min(52.0, 15.0 + (sim_units / 5000.0) * 1.2)

        st.write("")
        st.markdown("#### Real-Time Scenario Projections")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Annual Platform Revenue", f"₹{sim_arr_cr:.2f} Cr", f"${sim_arr_cr/8.3:.2f}M USD")
        s2.metric("Deposit Safeguarded", f"₹{sim_deposit_protected_cr:.1f} Cr", "In Smart Escrow")
        s3.metric("Brokerage Saved", f"₹{sim_brokerage_saved_cr:.1f} Cr", "Direct to Renters")
        s4.metric("Operating Profit Margin", f"{sim_ebitda_margin:.1f}%", "Healthy Operating Margin")

        with st.expander("📖 View Underlying Actuarial Simulation Logic"):
            st.code(
                f"""
# Scenario Simulation Equation:
Units = {sim_units:,}
SaaS Revenue = Units * ₹{audit_fee} = ₹{sim_units * audit_fee:,.0f}
Escrow Revenue = Units * (Rent ₹{avg_rent_mumbai:,} * 3) * {take_rate_escrow}% = ₹{sim_units * (avg_rent_mumbai * 3 * (take_rate_escrow/100.0)):,.0f}
Total Revenue = ₹{sim_arr_cr:.2f} Crores
Deposit Capital Safeguarded = ₹{sim_deposit_protected_cr:.1f} Crores
Brokerage Capital Preserved = ₹{sim_brokerage_saved_cr:.1f} Crores
                """,
                language="python",
            )

    # ------------------------------------------------------------------ #
    # TAB 4: 2026 EVOLVING GENERATION BRAINSTORMING HUB
    # ------------------------------------------------------------------ #
    with tab_genz:
        st.markdown("### 🚀 2026 Evolving Generation Rental Innovations")
        st.markdown(
            "By 2026, Gen Z and Young Millennials represent over **64% of urban tenants** in India's top metros. "
            "Here is the strategic innovation roadmap addressing their distinct behavioral patterns, digital habits, and legal expectations:"
        )

        g1, g2 = st.columns(2)
        with g1:
            with st.container(border=True):
                st.markdown("#### 1. 🤖 60-Second AI Redline Copilot via WhatsApp")
                st.write("Gen Z does not read 30-page legal PDFs. Tenants forward their draft agreement to The Dossier WhatsApp bot, receiving a 3-bullet risk summary and a copy-paste counter-offer addendum in under a minute.")

            with st.container(border=True):
                st.markdown("#### 2. 🛡️ Smart Escrow & UPI AutoPay Deposit Lock")
                st.write("Eliminating the landlord 'hostage deposit'. The deposit sits in an RBI-compliant digital escrow account, auto-released upon move-out condition sign-off unless formal GST invoices are uploaded within 7 days.")

            with g1:
                with st.container(border=True):
                    st.markdown("#### 3. ⚡ Statutory Right to EV Charging Sockets")
                    st.write("Over 30% of young Mumbai renters operate 2W or 4W Electric Vehicles. The Dossier inserts standard Ministry of Power covenants guaranteeing 15A socket installation without arbitrary RWA surcharges.")

            with g1:
                with st.container(border=True):
                    st.markdown("#### 4. 💻 Hybrid Work & WFH Infrastructure SLAs")
                    st.write("Leases include dual-broadband fiber-optic access covenants and mandatory quiet hours during core work intervals (9 AM - 6 PM) with guaranteed generator/inverter Wi-Fi uptime.")

        with g2:
            with st.container(border=True):
                st.markdown("#### 5. 🐾 Companion Animal Equality & Anti-Moral Policing")
                st.write("78% of young renters keep companion pets. The Dossier inserts statutory AWBI-compliant pet riders and prohibits intrusive moral policing regarding bachelor guests or dietary choices.")

            with st.container(border=True):
                st.markdown("#### 6. 👥 Split-Lease & Pro-Rata Roommate Succession")
                st.write("High corporate mobility means roommates rotate. Micro-contracts allow one flatmate to be replaced with standard 30-day notice without re-registering the entire lease or losing the deposit.")

            with st.container(border=True):
                st.markdown("#### 7. 🌱 Building Carbon & ESG Resilience Index")
                st.write("The Dossier Trust Index (DTI™) expands in 2026 to incorporate building solar power integration, decentralized wet-waste composting, and rainwater harvesting metrics.")

            with st.container(border=True):
                st.markdown("#### 8. 🎙️ Multilingual AI Voice Explainer for Families")
                st.write("Generates instant 2-minute audio explainers in Hindi, Marathi, and Gujarati so young renters can easily review terms with parents before committing.")

        with st.expander("📖 Academic Research: The Demographic Shift in Urban Indian Housing (2026-2030)"):
            st.write(
                "Urbanization in India is characterized by rapid formalization. As tech, consulting, and finance hubs expand in Mumbai MMR, "
                "the traditional informal broker-dominated tenancy structure is collapsing under high dispute rates. "
                "The 2026 evolving generation demands digital transparency, statutory enforceability, and lifestyle freedom. "
                "The Dossier is built as the foundational legal and trust infrastructure for this generational transition."
            )

    # ------------------------------------------------------------------ #
    # TAB 5: COMPETITIVE MOAT & INSTITUTIONAL DEFENSIBILITY
    # ------------------------------------------------------------------ #
    with tab_moat:
        st.markdown("### 🚀 Competitive Advantage & Defensive Moats")

        comp_data = {
            "Capability / Feature": [
                "1-Click Contract Risk Audit",
                "Balanced Legal Redline Copilot",
                "Building Water/Power Resilience (DTI™)",
                "Deposit Recovery Demand Notices",
                "Zero-Brokerage Direct Owners",
                "2026 Gen Z Protective Riders",
            ],
            "The Dossier": ["✓ Yes (Instant)", "✓ Yes (Ready-to-Sign)", "✓ Yes (0-100 Score)", "✓ Yes (Statutory)", "✓ Yes (Direct)", "✓ Yes (5 Riders)"],
            "MagicBricks / 99acres": ["✗ No", "✗ No", "✗ No", "✗ No", "✗ Broker Dominated", "✗ No"],
            "NoBroker": ["✗ No Legal Scan", "✗ No Redlines", "✗ No", "✗ No", "✓ Paid Plan", "✗ No"],
            "Traditional Advocates": ["✓ Manual (3-5 Days)", "✓ Manual", "✗ No", "✓ Expensive (₹15,000+)", "✗ No Marketplace", "✗ No"],
        }
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

        st.write("")
        b_left, b_right = st.columns(2)
        with b_left:
            if st.button("Explore 4-Photo Society Reviews", type="primary", use_container_width=True):
                go_to("society")
        with b_right:
            if st.button("Test Contract Scanner Demo", use_container_width=True):
                go_to("scan")
