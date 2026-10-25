"""Interactive legal learning area for non-lawyers."""
import streamlit as st
from core.premium_theme import apply_premium_theme
from core.nav import go_to

ARTICLES = {
    "contract-basics": {"title": "Contract basics", "section": "Start here", "summary": "Understand what makes an agreement enforceable in India.", "read": "6 min", "body": [("The simple definition", "A contract is an agreement that the law can enforce. It records who must do what, when they must do it, and what happens if something goes wrong."), ("The five checks", "Look for offer, acceptance, consideration, intention to create legal relations, and free consent. If one is missing, enforceability may be affected."), ("Before you sign", "Confirm the legal names, scope of work, payment dates, renewal terms, termination notice, dispute forum, and who is authorised to sign.")]},
    "risky-clauses": {"title": "Clauses that change your risk", "section": "Read smarter", "summary": "Learn how liability, indemnity, renewal and termination affect you.", "read": "8 min", "body": [("Liability caps", "A cap limits the maximum amount payable after a breach. Compare it with the contract value and check carve-outs for confidentiality, IP, fraud or data loss."), ("Indemnity", "Indemnity shifts the cost of specified claims. Check whether it is mutual, limited to fault, and controlled by a notice and defence process."), ("Auto-renewal", "An evergreen term renews unless notice is given in a narrow window. Record the notice deadline and ask for a clear cancellation route."), ("Termination", "A balanced contract gives both parties termination rights, a cure period, and clear consequences for work already delivered.")]},
    "indian-law": {"title": "Indian law essentials", "section": "Know the framework", "summary": "A practical map of laws and forums commonly seen in business contracts.", "read": "7 min", "body": [("Indian Contract Act, 1872", "The central statute for agreements, consent, performance, breach and remedies."), ("Arbitration and Conciliation Act, 1996", "Check the arbitration seat, venue, number of arbitrators, language and governing rules."), ("Information Technology Act, 2000", "Electronic records and signatures can have legal relevance. Read data-handling clauses carefully."), ("Consumer Protection Act, 2019", "Consumer-facing businesses should understand unfair terms, service deficiency and complaint mechanisms.")]},
    "disputes": {"title": "When something goes wrong", "section": "Take action", "summary": "A calm response plan for missed payments, breach and contract disputes.", "read": "5 min", "body": [("Create a record", "Save the signed contract, invoices, emails, delivery evidence and notices in one folder."), ("Send a precise notice", "State the obligation, breach, evidence, cure period and next action. Avoid unsupported threats or admissions."), ("Choose the forum", "Read governing law, jurisdiction and arbitration clauses before filing anything.")]},
}


def render():
    apply_premium_theme()
    key = st.session_state.get("learn_article")
    if key in ARTICLES:
        render_article(key)
        return
    st.markdown('<div class="page-header"><div class="eyebrow">Knowledge centre</div><h1>Learn contract law</h1><p>Practical guidance for founders, freelancers and teams who sign agreements without a law degree.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="notice"><strong>Learn, then apply.</strong><br/>Open a topic, finish the short lesson, then scan a real contract to see the idea in context.</div>', unsafe_allow_html=True)
    st.markdown("### Learning paths")
    for key, article in ARTICLES.items():
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f'<div class="article-row"><div><div class="eyebrow">{article["section"]} · {article["read"]}</div><h3>{article["title"]}</h3><p>{article["summary"]}</p></div></div>', unsafe_allow_html=True)
        with c2:
            if st.button("Open", key=f"open-{key}", use_container_width=True):
                st.session_state.learn_article = key
                st.rerun()
    st.markdown("### Continue with your document")
    if st.button("Open Scan Contract", type="primary"):
        go_to("scan")
    st.caption("Educational information only. Consult a qualified Indian advocate for your facts.")


def render_article(key):
    article = ARTICLES[key]
    if st.button("Back to Learn"):
        st.session_state.learn_article = None
        st.rerun()
    st.markdown(f'<div class="page-header"><div class="eyebrow">{article["section"]} · {article["read"]}</div><h1>{article["title"]}</h1><p>{article["summary"]}</p></div>', unsafe_allow_html=True)
    done = st.session_state.get(f"done-{key}", False)
    st.progress(1.0 if done else 0.25, text="Completed" if done else "In progress")
    for heading, body in article["body"]:
        st.markdown(f'<div class="lesson-block"><h3>{heading}</h3><p>{body}</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Mark as completed", use_container_width=True):
            st.session_state[f"done-{key}"] = True
            st.rerun()
    with c2:
        if st.button("Apply to a contract", use_container_width=True):
            go_to("scan")
    st.markdown("### Related topics")
    for related_key, related in ARTICLES.items():
        if related_key != key and st.button(related["title"], key=f"related-{related_key}"):
            st.session_state.learn_article = related_key
            st.rerun()
    st.caption("Sources to verify: Indian Contract Act, 1872; Arbitration and Conciliation Act, 1996; Information Technology Act, 2000.")
