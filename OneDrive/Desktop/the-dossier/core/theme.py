"""
DigiLocker-inspired purple theme.
Clean, minimal, professional. Purple brand, white canvas, traffic-light risk system.
"""

import streamlit as st

# Color palette
PRIMARY = "#6366f1"
PRIMARY_DARK = "#4f46e5"
PRIMARY_LIGHT = "#eef2ff"
RED = "#dc2626"
AMBER = "#ea580c"
GREEN = "#059669"
TEXT = "#111827"
TEXT_MUTED = "#6b7280"
BORDER = "#e5e7eb"
BG = "#ffffff"

def apply_theme():
    """Apply DigiLocker-style purple theme."""
    st.set_page_config(
        page_title="The Dossier",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    css = f"""
    <style>
    * {{ box-sizing: border-box; }}
    
    .stApp {{ background: {BG}; }}
    .main {{ padding: 0; }}
    .block-container {{ 
        max-width: 1200px; 
        margin: 0 auto;
        padding: 2rem 1.5rem;
    }}
    
    /* Typography */
    body, p, span, div {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    h1, h2, h3 {{ color: {TEXT}; font-weight: 600; }}
    h1 {{ font-size: 2rem; margin: 0 0 0.5rem 0; }}
    h2 {{ font-size: 1.5rem; margin: 0 0 1rem 0; }}
    p {{ color: {TEXT_MUTED}; margin: 0; }}
    
    /* Header with icon */
    .header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 2px solid {BORDER};
    }}
    .header-icon {{ font-size: 2.5rem; }}
    .header-content h1 {{ margin: 0; }}
    .header-sub {{ font-size: 0.9rem; color: {TEXT_MUTED}; }}
    
    /* Tabs */
    .tabs {{
        display: flex;
        gap: 2rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid {BORDER};
        padding-bottom: 0;
    }}
    .tab {{
        padding: 1rem 0;
        font-weight: 600;
        color: {TEXT_MUTED};
        cursor: pointer;
        border: none;
        background: none;
        border-bottom: 3px solid transparent;
        transition: all 0.2s;
    }}
    .tab:hover {{ color: {PRIMARY}; }}
    .tab.active {{
        color: {PRIMARY};
        border-bottom-color: {PRIMARY};
    }}
    
    /* Cards - metric grid */
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }}
    
    .metric-card {{
        background: {BG};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }}
    .metric-card:hover {{
        border-color: {PRIMARY};
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
    }}
    .metric-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {PRIMARY};
        margin: 0.5rem 0;
    }}
    .metric-label {{
        font-size: 0.85rem;
        color: {TEXT_MUTED};
    }}
    
    /* Risk banner - traffic light */
    .risk-banner {{
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        border: 2px solid;
    }}
    .risk-banner.high {{
        background: rgba(220, 38, 38, 0.05);
        border-color: {RED};
    }}
    .risk-banner.medium {{
        background: rgba(234, 88, 12, 0.05);
        border-color: {AMBER};
    }}
    .risk-banner.low {{
        background: rgba(5, 150, 105, 0.05);
        border-color: {GREEN};
    }}
    .risk-dot {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        flex-shrink: 0;
    }}
    .risk-banner.high .risk-dot {{ background: {RED}; }}
    .risk-banner.medium .risk-dot {{ background: {AMBER}; }}
    .risk-banner.low .risk-dot {{ background: {GREEN}; }}
    .risk-text h3 {{ margin: 0; font-size: 1.5rem; }}
    .risk-text p {{ margin: 0.5rem 0 0 0; }}
    
    /* Finding cards */
    .finding {{
        background: {BG};
        border: 1px solid {BORDER};
        border-left: 4px solid;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }}
    .finding.high {{ border-left-color: {RED}; }}
    .finding.medium {{ border-left-color: {AMBER}; }}
    .finding.low {{ border-left-color: {GREEN}; }}
    
    .finding-header {{
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }}
    .finding-icon {{
        font-size: 1.5rem;
        flex-shrink: 0;
    }}
    .finding-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: {TEXT};
        margin: 0;
    }}
    .finding-tag {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {TEXT_MUTED};
    }}
    
    .finding-quote {{
        background: #f9fafb;
        border-left: 3px solid {PRIMARY};
        padding: 0.75rem 1rem;
        margin: 1rem 0;
        border-radius: 6px;
        font-size: 0.9rem;
        font-family: 'Courier New', monospace;
        color: {TEXT};
        line-height: 1.5;
    }}
    
    .finding-meaning {{
        background: {PRIMARY_LIGHT};
        border-radius: 6px;
        padding: 0.75rem 1rem;
        margin-top: 1rem;
        font-size: 0.9rem;
        color: {TEXT};
    }}
    .finding-meaning strong {{ color: {PRIMARY}; }}
    
    /* Upload zone */
    .upload-zone {{
        border: 2px dashed {PRIMARY};
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        background: {PRIMARY_LIGHT};
        cursor: pointer;
    }}
    .upload-icon {{ font-size: 3rem; margin-bottom: 1rem; }}
    .upload-text {{ font-weight: 600; color: {PRIMARY}; }}
    .upload-sub {{ color: {TEXT_MUTED}; margin-top: 0.5rem; }}
    
    /* Buttons */
    .stButton > button {{
        background: {PRIMARY} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
    }}
    .stButton > button:hover {{
        background: {PRIMARY_DARK} !important;
    }}
    
    #MainMenu, footer {{ visibility: hidden; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
