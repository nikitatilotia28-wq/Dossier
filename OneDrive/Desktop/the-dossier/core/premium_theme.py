"""Premium, meaningful design for The Dossier - contract + education platform."""

import streamlit as st

# Professional color palette - Indigo + Teal + Gold
PRIMARY = "#1e3a8a"  # Deep indigo
SECONDARY = "#0d9488"  # Teal
ACCENT = "#d97706"  # Gold
LIGHT_BG = "#f0f9ff"  # Sky blue (very light)
CARD_BG = "#ffffff"
TEXT_PRIMARY = "#1f2937"
TEXT_SECONDARY = "#6b7280"
BORDER = "#e5e7eb"
RED_RISK = "#dc2626"
AMBER_RISK = "#ea580c"
GREEN_RISK = "#059669"

def apply_premium_theme():
    """Apply professional, educational design."""
    try:
        st.set_page_config(
            page_title="The Dossier - Mumbai Rental & Housing Intelligence",
            page_icon="🏢",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except Exception:
        pass
    
    css = f"""
    <style>
    * {{ box-sizing: border-box; }}
    
    /* Colors & Typography */
    .stApp {{ 
        background: #f5f7fb;
    }}
    
    body, p, span, div {{ 
        font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
    }}
    h1, h2, h3 {{ 
        color: {PRIMARY}; 
        font-weight: 700;
    }}
    p {{ color: {TEXT_SECONDARY}; }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {PRIMARY} 0%, #1e40af 100%);
    }}
    section[data-testid="stSidebar"] * {{ color: white; }}
    
    /* Main Container */
    .block-container {{ 
        max-width: 1400px; 
        padding: 2rem 2rem;
    }}
    
    /* Header with gradient */
    .page-header {{
        background: {PRIMARY};
        color: white;
        border-radius: 16px;
        padding: 3rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.15);
    }}
    .page-header h1 {{
        color: white;
        font-size: 2.5rem;
        margin: 0 0 0.5rem 0;
    }}
    .page-header p {{
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        border-bottom: 2px solid {BORDER};
        gap: 1rem;
        background: #ffffff;
        padding: 0 0.5rem;
        border-radius: 10px 10px 0 0;
        display: flex !important;
        visibility: visible !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 700;
        color: {TEXT_PRIMARY} !important;
        padding: 1rem 1.5rem;
        border-bottom: 3px solid transparent;
        background: #ffffff !important;
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {{ 
        color: {TEXT_PRIMARY} !important; 
        visibility: visible !important;
        opacity: 1 !important;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: {PRIMARY} !important;
        border-bottom-color: {PRIMARY};
        background: #ffffff !important;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] p,
    .stTabs [data-baseweb="tab"][aria-selected="true"] span {{ 
        color: {PRIMARY} !important; 
        visibility: visible !important;
        opacity: 1 !important;
    }}
    
    /* Cards */
    .card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s;
    }}
    .card:hover {{
        box-shadow: 0 10px 24px rgba(30, 58, 138, 0.12);
        border-color: {SECONDARY};
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: {CARD_BG};
        border-left: 4px solid {SECONDARY};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }}
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {PRIMARY};
        margin: 0.5rem 0;
    }}
    .metric-label {{
        font-size: 0.9rem;
        color: {TEXT_SECONDARY};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    /* Risk Banner */
    .risk-banner {{
        border-radius: 14px;
        padding: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        border: 2px solid;
        margin-bottom: 2rem;
    }}
    .risk-banner.high {{
        background: rgba(220, 38, 38, 0.08);
        border-color: {RED_RISK};
    }}
    .risk-banner.medium {{
        background: rgba(234, 88, 12, 0.08);
        border-color: {AMBER_RISK};
    }}
    .risk-banner.low {{
        background: rgba(5, 150, 105, 0.08);
        border-color: {GREEN_RISK};
    }}
    .risk-dot {{
        width: 70px;
        height: 70px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        flex-shrink: 0;
    }}
    .risk-banner.high .risk-dot {{ background: {RED_RISK}; }}
    .risk-banner.medium .risk-dot {{ background: {AMBER_RISK}; }}
    .risk-banner.low .risk-dot {{ background: {GREEN_RISK}; }}
    .risk-text h3 {{ margin: 0; color: {PRIMARY}; }}
    
    /* Finding Cards */
    .finding {{
        background: {CARD_BG};
        border-left: 5px solid;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .finding.high {{ border-left-color: {RED_RISK}; }}
    .finding.medium {{ border-left-color: {AMBER_RISK}; }}
    .finding.low {{ border-left-color: {GREEN_RISK}; }}
    
    .finding-title {{
        font-size: 1.2rem;
        font-weight: 600;
        color: {PRIMARY};
        margin: 0 0 0.5rem 0;
    }}
    .finding-tag {{
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {PRIMARY};
        background: rgba(30, 58, 138, 0.1);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 0.5rem;
    }}
    
    .finding-quote {{
        background: #f9fafb;
        border-left: 4px solid {SECONDARY};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        color: {TEXT_PRIMARY};
        line-height: 1.6;
        font-size: 0.9rem;
    }}
    
    .finding-meaning {{
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.08) 0%, rgba(217, 119, 6, 0.04) 100%);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        color: {TEXT_PRIMARY};
    }}
    .finding-meaning strong {{ color: {SECONDARY}; }}
    
    /* Buttons */
    .stButton > button, .stFormSubmitButton > button, [data-testid="stFormSubmitButton"] button {{
        background: {PRIMARY} !important;
        color: #ffffff !important;
        border: 1px solid {PRIMARY} !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2) !important;
    }}
    .stButton > button *, .stFormSubmitButton > button *, [data-testid="stFormSubmitButton"] button * {{
        color: #ffffff !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.3) !important;
    }}
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {{ color: #ffffff !important; }}
    .login-shell {{
        max-width: 680px;
        margin: 5rem auto 1.5rem;
        padding: 2.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #172554, #1e3a8a);
        color: #eff6ff;
        box-shadow: 0 24px 70px rgba(15,23,42,.25);
    }}
    .login-shell h1 {{ color: #ffffff !important; margin: .6rem 0; }}
    .login-shell p {{ color: #dbeafe !important; max-width: 560px; }}
    .language-card {{
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 0.75rem 0.9rem !important;
        margin: 0.5rem 0 0.35rem !important;
    }}
    .language-card strong, .language-card span {{
        display: block !important;
        color: #0f172a !important;
    }}
    .language-card span {{ font-size: 0.75rem !important; margin-top: 0.2rem !important; }}
    /* Language picker and all compact selectors */
    [data-testid="stSidebar"] [data-testid="stExpander"] summary,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] label,
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        color: #0f172a !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: #172554 !important;
        border: 1px solid #bfdbfe !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="select"] div,
    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] svg {{
        color: #ffffff !important;
        fill: #ffffff !important;
        opacity: 1 !important;
    }}
    [data-testid="stSidebar"] [role="combobox"] {{
        background: #172554 !important;
        color: #ffffff !important;
        border: 1px solid #bfdbfe !important;
    }}
    [data-testid="stSidebar"] [role="combobox"] * {{
        color: #ffffff !important;
        fill: #ffffff !important;
    }}
    [role="listbox"], [role="option"] {{
        background: #ffffff !important;
        color: #0f172a !important;
    }}
    .stButton > button:disabled {{
        background: #dbe3f0 !important;
        color: #334155 !important;
        border: 1px solid #cbd5e1 !important;
        opacity: 1 !important;
        box-shadow: none !important;
    }}
    .stDownloadButton > button {{
        background: #ffffff !important;
        color: {PRIMARY} !important;
        border: 1px solid {PRIMARY} !important;
    }}
    .stDownloadButton > button:hover {{
        background: #eef4ff !important;
        color: {PRIMARY} !important;
    }}
    
    /* Learn Section Cards */
    .learn-card {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 2rem;
        border: 2px solid {BORDER};
        transition: all 0.3s;
    }}
    .learn-card:hover {{
        border-color: {SECONDARY};
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(13, 148, 136, 0.15);
    }}
    .learn-card-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
    }}
    .learn-card h3 {{
        color: {PRIMARY};
        font-size: 1.4rem;
        margin: 0.5rem 0;
    }}
    .learn-card p {{
        color: {TEXT_SECONDARY};
        line-height: 1.6;
    }}
    
    /* Info Box */
    .info-box {{
        background: linear-gradient(135deg, {LIGHT_BG} 0%, #eff6ff 100%);
        border-left: 5px solid {SECONDARY};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }}
    .info-box strong {{ color: {PRIMARY}; }}
    
    /* Alert */
    .alert {{
        background: #fef3c7;
        border-left: 5px solid {ACCENT};
        border-radius: 10px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        color: #92400e;
    }}
    
    .eyebrow {{ color: {SECONDARY}; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }}
    .notice {{ background: #eef4ff; border: 1px solid #c8d7f2; border-radius: 10px; padding: 1rem 1.25rem; margin: 1rem 0 1.5rem; color: #243b63; }}
    .article-row {{ background: white; border: 1px solid {BORDER}; border-radius: 10px; padding: 1.1rem 1.25rem; margin-bottom: 0.75rem; }}
    .article-row h3 {{ margin: 0.25rem 0; color: {PRIMARY}; }}
    .article-row p {{ margin: 0; }}
    .lesson-block {{ background: white; border-left: 3px solid {SECONDARY}; border-radius: 8px; padding: 1rem 1.25rem; margin: 0.9rem 0; }}
    .lesson-block h3 {{ margin: 0 0 0.35rem; font-size: 1.08rem; }}

    /* Badges & Real Estate Styling */
    .badge-verified {{
        display: inline-flex;
        align-items: center;
        background: #ecfdf5;
        color: #065f46;
        border: 1px solid #a7f3d0;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
    }}
    .badge-pending {{
        display: inline-flex;
        align-items: center;
        background: #fffbeb;
        color: #92400e;
        border: 1px solid #fde68a;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
    }}
    .badge-locality {{
        display: inline-flex;
        align-items: center;
        background: #eff6ff;
        color: #1e40af;
        border: 1px solid #bfdbfe;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
    }}
    .badge-amenity {{
        display: inline-block;
        background: #f8fafc;
        color: #334155;
        font-size: 0.72rem;
        font-weight: 500;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        margin: 0.15rem 0.2rem 0.15rem 0;
        border: 1px solid #e2e8f0;
    }}
    .rating-pill {{
        display: inline-flex;
        align-items: center;
        background: #fffbeb;
        color: #b45309;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.25rem 0.6rem;
        border-radius: 8px;
        border: 1px solid #fde68a;
    }}
    .pros-box {{
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.88rem;
        color: #166534;
    }}
    .cons-box {{
        background: #fff7ed;
        border-left: 4px solid #ea580c;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 0.88rem;
        color: #9a3412;
    }}
    .kpi-card {{
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }}
    .kpi-num {{
        font-size: 1.85rem;
        font-weight: 800;
        color: #1e3a8a;
        margin: 0.2rem 0;
    }}
    .kpi-label {{
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.05em;
    }}

    /* Enforce Uniform Image Sizing across all cards & feeds */
    div[data-testid="stImage"] {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        overflow: hidden !important;
        border-radius: 10px !important;
        background: #f1f5f9 !important;
    }}
    div[data-testid="stImage"] img,
    .stImage img {{
        height: 200px !important;
        max-height: 200px !important;
        width: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 10px !important;
        aspect-ratio: 16 / 10.6 !important;
        transition: transform 0.25s ease-in-out !important;
    }}
    div[data-testid="stImage"] img:hover,
    .stImage img:hover {{
        transform: scale(1.02) !important;
    }}

    /* Theory Dropdown / Expander Styling */
    div[data-testid="stExpander"] {{
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        background: #f8fafc !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.8rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }}
    div[data-testid="stExpander"] details summary {{
        font-weight: 700 !important;
        color: #1e3a8a !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }}
    div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        padding: 1rem 1.25rem !important;
        background: #ffffff !important;
        border-radius: 0 0 11px 11px !important;
        border-top: 1px solid #e2e8f0 !important;
        line-height: 1.65 !important;
    }}

    /* Sidebar Navigation Enhancement */
    [data-testid="stSidebarNav"] {{
        padding-top: 0.5rem !important;
    }}
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] p,
    [data-testid="stSidebarNav"] a {{
        font-size: 0.96rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: rgba(255, 255, 255, 0.18) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }}

    #MainMenu, footer {{ visibility: hidden; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
