"""Rulebook — read-only view of the active playbook."""

import html
import streamlit as st

from core.rulebook import get_rules, rule_count
from core.premium_theme import apply_premium_theme


def render() -> None:
    apply_premium_theme()
    
    st.markdown("""
    <div class="page-header">
        <h1>📋 Rulebook</h1>
        <p>All playbook rules in plain language. Completely transparent - nothing hidden.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="dcard" style="background:#fbfaf5;margin-bottom:1.25rem;">
          <div class="overline">Transparency</div>
          <p style="color:var(--charcoal);margin:0.5rem 0 0 0;line-height:1.6;">
            The engine applies <b>{rule_count()} rules</b>. Each one either flags a clause
            that is risky when <i>present</i>, or a protection that is risky when
            <i>absent</i>. In-app editing of these rules is in progress; for now the
            playbook is fixed and shown here in full.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(f"**{rule_count()} Active Rules**")
    
    for r in get_rules():
        mode = "Flags when present" if r["mode"] == "flag_if_present" else "Flags when absent"
        st.markdown(f"""
        <div class="finding {r['severity']}">
            <div class="finding-header">
                <div class="finding-icon">📌</div>
                <div>
                    <div class="finding-tag">{r['clause_type']} · {mode}</div>
                    <h3 class="finding-title">{html.escape(r['title'])}</h3>
                </div>
            </div>
            <p style="margin: 0.5rem 0; color: #6b7280;">{html.escape(r['rationale'])}</p>
            <div class="finding-meaning">
                <strong>Guidance:</strong> {html.escape(r['recommendation'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
