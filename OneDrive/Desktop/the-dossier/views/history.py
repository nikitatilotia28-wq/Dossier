"""Searchable review archive."""
import streamlit as st
from core.db import get_all_scans, get_scan, delete_scan, get_rental_records, delete_rental_record
from core.premium_theme import apply_premium_theme


def render():
    apply_premium_theme()
    st.markdown('<div class="page-header"><div class="eyebrow">Review archive</div><h1>History</h1><p>Find, reopen and manage every contract review saved on this device.</p></div>', unsafe_allow_html=True)
    user_id = st.session_state.get("user_id")
    rental_records = get_rental_records(user_id=user_id)
    if rental_records:
        st.markdown("### Rental records")
        st.caption("Repairs, receipts, and handover notes saved on this device.")
        for record in rental_records:
            with st.container(border=True):
                left, right = st.columns([5, 1])
                with left:
                    st.markdown(f"**{record['title'] or 'Rental record'}** · {record['status']}")
                    st.caption(f"{record['record_type'].title()} · {record['record_date']} · Saved {record['created_at'].replace('T', ' ')}")
                    st.write(record['details'])
                    if record.get('attachment_path'):
                        st.caption(f"Attachment saved: {record['attachment_path']}")
                with right:
                    if st.button("Delete", key=f"delete_record_{record['id']}"):
                        delete_rental_record(record['id'])
                        st.rerun()
        st.divider()

    rows = get_all_scans(user_id=user_id)
    if not rows:
        st.markdown('<div class="notice"><strong>No reviews yet.</strong><br/>Run a scan and the complete result will appear here.</div>', unsafe_allow_html=True)
        return
    q = st.text_input("Search reviews", placeholder="Search by filename")
    bands = ["All risk levels", "High risk", "Moderate risk", "Low risk"]
    band = st.selectbox("Risk level", bands)
    filtered = [r for r in rows if (not q or q.lower() in r["filename"].lower()) and (band == "All risk levels" or r["risk_band"] == band)]
    st.caption(f"Showing {len(filtered)} of {len(rows)} reviews")
    for row in filtered:
        with st.container(border=True):
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                display_name = row['filename'].replace('Sample MSA', 'Practice rental agreement').replace('Sample — Master Services Agreement', 'Practice rental agreement')
                st.markdown(f"**{display_name}**")
                st.caption(row['scanned_at'].replace('T', ' ') + f" · {row['flagged']} findings · score {row['risk_score']}")
            with c2:
                st.markdown(f"**{row['risk_band']}**")
            with c3:
                if st.button("Open", key=f"open-{row['id']}", use_container_width=True):
                    st.session_state.history_scan = row['id']
                    st.rerun()
                if st.button("Delete", key=f"delete-{row['id']}", use_container_width=True):
                    delete_scan(row['id'])
                    st.rerun()
    selected = st.session_state.get("history_scan")
    if selected:
        record = get_scan(selected)
        if record and record.get("result"):
            st.divider()
            display_name = record['filename'].replace('Sample MSA', 'Practice rental agreement').replace('Sample — Master Services Agreement', 'Practice rental agreement')
            st.markdown(f"### Review details: {display_name}")
            result = record['result']
            for finding in result.get('findings', []):
                if finding.get('status') == 'flagged':
                    st.markdown(f"**{finding.get('title', 'Finding')}** · {finding.get('severity', '').title()}")
                    st.write(finding.get('quote', finding.get('description', '')))
