"""
The Dossier — Rental Agreement Scanner & Redline Copilot.
Simple, user-friendly contract risk auditing with 1-click specimen walkthrough,
instant balanced redline generation, 2026 Gen Z lease riders, and dropdown legal theory.
"""

from datetime import date
import streamlit as st

from core.premium_theme import apply_premium_theme
from core.extractor import extract_text, analyze
from core.db import save_scan
from core.sample import SAMPLE_CONTRACT, SAMPLE_CONTRACT_LONG
from core.rulebook import get_rules


BALANCED_REDLINES = {
    "uncapped_liability": (
        "The total cumulative liability of the Licensee arising out of or in connection with this Agreement "
        "shall in all circumstances be strictly limited to an amount equivalent to two (2) months' license fee "
        "actually paid, except in cases of proven gross negligence or wilful misconduct."
    ),
    "missing_liability_cap": (
        "Neither party shall be liable to the other for indirect, special, incidental, or consequential damages. "
        "The maximum aggregate liability of either party shall be capped at the total amount of the refundable security deposit."
    ),
    "indemnity": (
        "The Licensee shall indemnify and defend the Licensor solely against direct, third-party claims resulting directly "
        "from a material breach of this Agreement by the Licensee, provided prompt written notice is served with reasonable opportunity to defend."
    ),
    "termination": (
        "Either party may terminate this Agreement without cause by giving thirty (30) days prior written notice. "
        "In the event of an alleged breach, the non-breaching party shall provide a mandatory cure period of fifteen (15) "
        "business days prior to termination."
    ),
    "deposit": (
        "The Licensor shall return the entire interest-free refundable security deposit simultaneously with vacant physical "
        "handover of keys. Any deduction shall require prior itemized written notice accompanied by original GST tax invoices. "
        "Delayed refund beyond 7 business days shall accrue interest at 12% per annum under Section 73 of the Indian Contract Act."
    ),
    "auto_renewal": (
        "This Agreement shall not automatically renew. Any renewal or extension shall require mutual written consent "
        "and a newly registered Leave and License agreement executed prior to expiry."
    ),
    "governing_law": (
        "This Agreement shall be governed by and construed in accordance with the laws of Maharashtra, India. "
        "Any dispute shall be resolved through amicable mediation, or referred to sole arbitration in Mumbai under the Arbitration and Conciliation Act, 1996."
    ),
    "confidentiality": (
        "Both parties agree to treat personal identity documents, financial records, and communication exchanged under this "
        "tenancy as confidential, strictly protected under the Digital Personal Data Protection Act, 2023."
    ),
    "house_rules": (
        "Society bylaws and rules shall apply equally to all residents without discriminatory restrictions regarding guests, "
        "food habits, or curfew, subject to standard municipal quiet hours."
    ),
    "repairs": (
        "Structural, concealed plumbing, electrical, and pre-existing fixture maintenance shall be the sole responsibility "
        "of the Licensor. The Licensee shall not be liable for normal wear-and-tear resulting from ordinary residential occupation."
    ),
}

DEFAULT_REDLINE = (
    "Both parties agree to perform their respective obligations in good faith. Any modification, penalty, or deduction under "
    "this clause shall require mutual written consent and a minimum of fifteen (15) days written cure notice."
)

# 2026 Evolving Generation (Gen Z) Protective Lease Riders
GENZ_2026_RIDERS = [
    {
        "id": "ev_charging",
        "title": "⚡ Right to EV Charging Socket (2026 Mobility Rider)",
        "category": "Mobility & Sustainability",
        "clause": (
            "The Licensor hereby grants permission for the Licensee to connect a standard 15A / Level-2 Electric Vehicle "
            "charging socket to the flat's electricity meter at the designated parking slot. The Licensor agrees to sign standard "
            "society NOC forms without imposing arbitrary surcharge fees."
        ),
        "rationale": "By 2026, EV adoption in Mumbai metros exceeds 30%. Landlords frequently delay signing society NOCs without this explicit lease right.",
    },
    {
        "id": "wfh_broadband",
        "title": "💻 Hybrid Work / WFH SLA & High-Speed Fiber Guarantee",
        "category": "Remote Work Infrastructure",
        "clause": (
            "The Licensor guarantees unrestricted access for fiber-optic broadband installation through multiple Tier-1 ISPs. "
            "Quiet working hours shall be maintained on premises during business hours (9:00 AM to 6:00 PM), and building inverter/generator "
            "backup shall support continuous Wi-Fi connectivity."
        ),
        "rationale": "Remote and hybrid work is standard for young tech and finance professionals. ISP access hurdles cause immediate productivity loss.",
    },
    {
        "id": "digital_escrow",
        "title": "🛡️ Smart Digital Escrow & Auto-Release Deposit Clause",
        "category": "Financial Protection",
        "clause": (
            "The refundable security deposit of INR [AMOUNT] shall be lodged in a designated RBI-compliant third-party escrow account. "
            "Upon mutual digital key handover sign-off, the escrow shall automatically disburse 100% of the deposit to the Licensee's "
            "bank account within seven (7) business days, unless a formal dispute with original GST contractor invoices is lodged."
        ),
        "rationale": "Eliminates the 'hostage deposit' dynamic where landlords arbitrarily withhold moving capital.",
    },
    {
        "id": "pet_equality",
        "title": "🐾 Companion Animal & Anti-Moral Policing Rider",
        "category": "Lifestyle & Equality",
        "clause": (
            "Domestic companion pets (dogs/cats) are expressly permitted in accordance with Animal Welfare Board of India guidelines. "
            "No housing society or landlord committee shall impose arbitrary size restrictions, extra elevator cess, or visitor curfew "
            "penalties on bachelor or pet-owning tenants."
        ),
        "rationale": "78% of Gen Z urban renters keep companion pets. Unregulated RWAs frequently attempt unlawful eviction.",
    },
    {
        "id": "roommate_succession",
        "title": "👥 Co-Living Succession & Pro-Rata Roommate Assignment",
        "category": "Shared Tenancy",
        "clause": (
            "In the event one named Licensee relocates due to professional transfer, the remaining Licensees shall have the right "
            "to substitute a replacement roommate upon thirty (30) days written notice and standard identity verification, without "
            "forfeiting the existing security deposit or terminating the underlying tenancy."
        ),
        "rationale": "High corporate mobility requires flexible co-living succession without costly lease cancelation penalties.",
    },
]


def render() -> None:
    apply_premium_theme()

    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "sample_loaded" not in st.session_state:
        st.session_state.sample_loaded = False

    st.markdown(
        """
        <div class="page-header" style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);">
            <div class="eyebrow" style="color:#93c5fd;">Smart LegalTech Engine · Deterministic 15-Rule Rulebook</div>
            <h1>📑 Rental Agreement Scanner & Redline Copilot</h1>
            <p>Scan your rental agreement, detect unfair clauses in seconds, and generate ready-to-sign balanced replacement clauses.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------ #
    # ⚡ 1-CLICK QUICK SPECIMEN WALKTHROUGH
    # ------------------------------------------------------------------ #
    with st.container(border=True):
        f_left, f_right = st.columns([3, 1.4])
        with f_left:
            st.markdown("#### ⚡ Quick Specimen Walkthrough")
            st.caption("Instantly run the analysis engine on a standard Mumbai Bachelor Leave & License agreement without uploading files.")
        with f_right:
            if st.button("⚡ Run Instant Specimen Scan", type="primary", use_container_width=True, key="instant_specimen_scanner"):
                text = SAMPLE_CONTRACT
                res = analyze(text)
                st.session_state.analysis_done = True
                st.session_state.findings = res.get("findings", [])
                st.session_state.contract_text = text
                st.session_state.filename = "Mumbai Bachelor Rental Agreement (Specimen Walkthrough)"
                st.session_state.result = res
                st.session_state.sample_loaded = True
                save_scan(st.session_state.filename, res, st.session_state.get("user_id"))
                st.rerun()

    st.write("")

    tab_upload, tab_results, tab_genz = st.tabs(
        [
            "📤 Upload Custom Contract",
            "📊 Scan Results & Redlines",
            "🚀 2026 Evolving Generation Riders",
        ]
    )

    with tab_upload:
        render_upload_tab()

    with tab_results:
        render_results_tab()

    with tab_genz:
        render_genz_riders_tab()


def render_upload_tab() -> None:
    col1, col2 = st.columns([1.6, 1.2])

    with col1:
        st.markdown("#### Upload Your Agreement")
        uploaded_file = st.file_uploader(
            "PDF, DOCX, or TXT (Scanned or Digital)",
            type=["pdf", "docx", "txt"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            st.session_state.sample_loaded = False
            st.success(f"✓ Loaded: **{uploaded_file.name}**")

    with col2:
        st.markdown("#### Pre-Loaded Specimen Agreements")
        st.caption("Select a standard specimen to benchmark:")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Bachelor Specimen", use_container_width=True):
                st.session_state.sample_loaded = True
                st.session_state.sample_text = SAMPLE_CONTRACT
                st.session_state.uploaded_file = None
                st.success("Loaded: Bachelor Specimen")
        with b2:
            if st.button("Corporate Specimen", use_container_width=True):
                st.session_state.sample_loaded = True
                st.session_state.sample_text = SAMPLE_CONTRACT_LONG
                st.session_state.uploaded_file = None
                st.success("Loaded: Corporate Specimen")

    st.write("")
    can_analyze = st.session_state.uploaded_file is not None or st.session_state.sample_loaded
    if st.button("🔍 Analyze Contract Now", type="primary", use_container_width=True, disabled=not can_analyze):
        with st.spinner("Analyzing contract clauses..."):
            analyze_contract()
            st.rerun()


def analyze_contract() -> None:
    if st.session_state.sample_loaded:
        text = st.session_state.get("sample_text", SAMPLE_CONTRACT)
        filename = "Mumbai Bachelor Rental Specimen" if text == SAMPLE_CONTRACT else "Corporate Residential Specimen"
    else:
        file = st.session_state.uploaded_file
        text = extract_text(file)
        filename = file.name

    result = analyze(text)
    save_scan(filename, result, st.session_state.get("user_id"))

    st.session_state.analysis_done = True
    st.session_state.findings = result.get("findings", [])
    st.session_state.contract_text = text
    st.session_state.filename = filename
    st.session_state.result = result


def render_results_tab() -> None:
    if not st.session_state.analysis_done:
        st.info("💡 Upload your agreement above or click **'⚡ Run Instant Specimen Scan'** to see the analysis.")
        return

    result = st.session_state.result
    findings = result.get("findings", [])
    filename = st.session_state.filename
    s = result.get("summary", {})

    high = s.get("high", 0)
    medium = s.get("medium", 0)
    low = s.get("low", 0)
    total = s.get("flagged", len(findings))
    score = s.get("risk_score", 0)
    band = s.get("risk_band", "Moderate")

    # Risk Summary Metrics
    st.markdown(f"### Contract Audit: **{filename}**")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Risk Score", f"{score} / 100", f"Status: {band}")
    m2.metric("Critical Redlines", f"{high} Issues", "High Priority")
    m3.metric("Moderate Gaps", f"{medium} Issues", "Negotiable")
    m4.metric("Total Items", f"{total} Flags", "Checked")

    st.write("")

    # Filter & Findings Display
    st.markdown("### ⚖️ Detected Clauses & AI Balanced Redlines")
    st.caption("Review each flagged clause below. The AI provides a balanced, ready-to-use replacement clause.")

    filter_choice = st.radio(
        "Filter Redlines:",
        ["All Issues", "Critical Only (High Priority)", "Moderate Only (Negotiable)"],
        horizontal=True,
    )

    flagged_findings = [f for f in findings if f.get("status") == "flagged"]
    if filter_choice == "Critical Only (High Priority)":
        flagged_findings = [f for f in flagged_findings if f.get("severity") == "high"]
    elif filter_choice == "Moderate Only (Negotiable)":
        flagged_findings = [f for f in flagged_findings if f.get("severity") == "medium"]

    redline_addendum_items = []
    whatsapp_summary_items = []

    for i, finding in enumerate(flagged_findings):
        sev = finding.get("severity", "low").upper()
        c_type = finding.get("clause_type", "General")
        title = finding.get("title", "Clause Issue")
        quote = finding.get("matches", ["(This protective clause is missing from the agreement)"])[0] if finding.get("matches") else "(Missing protective clause)"
        rule_id = finding.get("id", "")

        redline_clause = None
        for k, v in BALANCED_REDLINES.items():
            if k in rule_id or k in c_type.lower():
                redline_clause = v
                break
        if not redline_clause:
            redline_clause = DEFAULT_REDLINE

        redline_addendum_items.append((c_type, title, redline_clause))
        whatsapp_summary_items.append(f"• {title}: Requesting standard cap / bilateral cure period under statutory norms.")

        with st.container(border=True):
            hdr_left, hdr_right = st.columns([3, 1.2])
            with hdr_left:
                st.markdown(f"**{i + 1}. {title}** · <span class='badge-locality'>{c_type}</span>", unsafe_allow_html=True)
            with hdr_right:
                if sev == "HIGH":
                    st.markdown("<div style='text-align:right;'><span class='badge-pending' style='background:#fef2f2; color:#b91c1c; border-color:#fecaca;'>CRITICAL RISK</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align:right;'><span class='badge-pending'>MODERATE GAP</span></div>", unsafe_allow_html=True)

            # In Contract Section
            st.markdown(
                f"""
                <div style="background:#fff1f2; border-left:4px solid #f43f5e; padding:0.6rem 0.9rem; border-radius:6px; margin:0.4rem 0;">
                    <strong style="color:#9f1239;">Draft Clause in Contract:</strong><br/>
                    <span style="font-family:monospace; font-size:0.88rem; color:#881337;">"{quote}"</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Clean Redline Box
            st.markdown(
                f"""
                <div class="pros-box" style="margin-top:0.4rem;">
                    <strong>⚖️ Balanced Replacement Clause (Copy-Ready):</strong><br/>
                    <span style="font-family:monospace; font-size:0.9rem; color:#14532d;">"{redline_clause}"</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Theory tucked into dropdown
            with st.expander("📖 Why this matters (Legal Theory & Indian Precedents)"):
                st.markdown(f"**Statutory Problem:** {finding.get('rationale', 'This clause creates an unbalanced unilateral obligation under Indian Contract Act Section 23.')}")
                st.markdown(f"**Recommended Action:** {finding.get('recommendation', 'Clarify with landlord in writing before signing.')}")

    st.markdown("---")

    # 1-Click Export Negotiation Addendum & WhatsApp Draft
    st.markdown("### 📄 1-Click Negotiation Exports")
    st.caption("Generate ready-to-share negotiation drafts for your landlord or broker.")

    addendum_content = f"""ADDENDUM TO LEAVE AND LICENSE AGREEMENT
(Proposed Contract Modifications & Statutory Protective Terms)

Date: {date.today().strftime('%d %B %Y')}
Document Ref: {filename}
Prepared via The Dossier Legal Risk Intelligence Platform

WHEREAS the Licensor and Licensee have reviewed the draft Leave & License Agreement, 
the parties hereby mutually agree to incorporate the following amendments and supervening terms:

"""
    for idx, (ctype, ctitle, ctext) in enumerate(redline_addendum_items, 1):
        addendum_content += f"""{idx}. AMENDMENT TO CLAUSE: {ctype.upper()} ({ctitle})
The parties agree that the following replacement language shall govern and supersede any contradictory clause:
"{ctext}"

"""

    addendum_content += """All other terms and conditions of the principal Agreement not modified herein shall remain in full force and effect.

_____________________________                _____________________________
LICENSOR (LANDLORD)                          LICENSEE (TENANT)
"""

    whatsapp_msg = f"""Hi! We have reviewed the draft Leave & License agreement via The Dossier legal risk audit. We are excited to move forward, but we noticed a few standard points that need minor adjustment to align with standard Model Tenancy and Maharashtra Rent Control practice:

{chr(10).join(whatsapp_summary_items[:4])}

Could we please incorporate these balanced clauses in a simple 1-page addendum before registration? We have ready copy-paste wording that protects both parties. Thanks!"""

    e1, e2, e3 = st.columns([1.2, 1.2, 1])
    with e1:
        st.download_button(
            "📥 Download Formal Addendum (.txt)",
            data=addendum_content,
            file_name=f"contract-addendum-{date.today().isoformat()}.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True,
        )
    with e2:
        st.download_button(
            "📱 Download WhatsApp Draft (.txt)",
            data=whatsapp_msg,
            file_name=f"whatsapp-negotiation-{date.today().isoformat()}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with e3:
        if st.button("Check Another Contract", use_container_width=True):
            st.session_state.analysis_done = False
            st.session_state.uploaded_file = None
            st.session_state.sample_loaded = False
            st.rerun()

    # Dropdown for full underlying rulebook
    with st.expander("📋 View The 15 Statutory Contract Rules (Playbook Reference)"):
        st.caption("The analyzer uses an explainable deterministic rulebook under the Indian Contract Act, 1872:")
        for r in get_rules():
            st.markdown(f"**{r['title']}** ({r['severity'].upper()}) · *{r['clause_type']}*")
            st.write(r["rationale"])
            st.divider()


def render_genz_riders_tab() -> None:
    st.markdown("### 🚀 2026 Evolving Generation Lease Riders")
    st.markdown(
        "By 2026, Gen Z and young millennial tenants in India represent over 64% of urban rental moves. "
        "These ready-to-insert lease riders address emerging issues: **EV charging rights, remote work SLAs, digital escrow, pet equality, and co-living succession**."
    )

    with st.expander("📖 Why Leases Must Evolve in 2026 (Theoretical Rationale)"):
        st.write(
            "Traditional Indian Leave & License agreements drafted in the 1990s assume single-earner offline employment and zero electric mobility. "
            "In 2026, urban tenants require digital connectivity guarantees, legal protection for companion animals under AWBI precedents, "
            "and statutory EV charger socket access under Ministry of Power 2025 guidelines. The Dossier modernizes Indian rental contracts."
        )

    for rider in GENZ_2026_RIDERS:
        with st.container(border=True):
            st.markdown(f"#### {rider['title']}")
            st.caption(f"Category: **{rider['category']}**")
            st.markdown(
                f"""
                <div class="pros-box">
                    <strong>Recommended 2026 Rider Language:</strong><br/>
                    <span style="font-family:monospace; font-size:0.9rem; color:#14532d;">"{rider['clause']}"</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("📖 Problem Solved & Legal Context"):
                st.write(rider["rationale"])
