# style.py - RixterProphet Analytics: Forex Edition
# Dark Luxury Professional Styling & Theme

import streamlit as st

def get_theme_css():
    """Return comprehensive dark luxury CSS theme"""
    return """
    <style>
    /* ============ GLOBAL THEME ============ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* ============ MAIN CONTAINER ============ */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* ============ HEADERS ============ */
    h1 {
        background: linear-gradient(135deg, #c9a84c 0%, #f0d78c 50%, #c9a84c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #e6edf3;
        font-weight: 700 !important;
        border-bottom: 2px solid #c9a84c;
        padding-bottom: 0.5rem;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: #c9d1d9;
        font-weight: 600 !important;
        letter-spacing: -0.2px;
    }
    
    h4 {
        color: #e6edf3;
        font-weight: 600 !important;
    }
    
    /* ============ CAPTIONS & TEXT ============ */
    .stCaption {
        color: #8b949e !important;
    }
    
    p, li, span {
        color: #c9d1d9;
    }
    
    /* ============ CARDS & CONTAINERS ============ */
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid #21262d;
    }
    
    .note-box {
        background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
        border-left: 4px solid #c9a84c;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        color: #c9d1d9;
    }
    
    .note-box b {
        color: #c9a84c;
    }
    
    /* ============ PREDICTION TABLE ============ */
    .prediction-table {
        overflow-x: auto;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.3);
    }
    
    .prediction-table table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        background-color: #161b22;
    }
    
    .prediction-table th {
        background: linear-gradient(135deg, #21262d 0%, #30363d 100%);
        color: #c9a84c;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #c9a84c;
    }
    
    .prediction-table td {
        padding: 10px 15px;
        border-bottom: 1px solid #21262d;
        color: #c9d1d9;
    }
    
    .prediction-table tr:hover {
        background-color: #21262d;
    }
    
    .prediction-table tr:last-child {
        font-weight: 600;
        background-color: #1a1f27;
    }
    
    /* ============ METRIC CARDS ============ */
    .metric-card {
        background: #161b22;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border: 1px solid #21262d;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(201, 168, 76, 0.15);
        border-color: #c9a84c;
    }
    
    .metric-card h4 {
        color: #c9a84c;
    }
    
    .metric-card p, .metric-card li {
        color: #c9d1d9;
    }
    
    /* ============ BUTTONS ============ */
    .stButton > button {
        background: linear-gradient(135deg, rgb(105 77 0) 0%, #000c31 100%) !important
        color: #0d1117 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(201, 168, 76, 0.4) !important;
        background: linear-gradient(135deg, #d4b35c 0%, #c9a84c 100%) !important;
    }
    
    /* ============ SIDEBAR ============ */
    .css-1d391kg, .css-1lcbmhc, [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #21262d;
    }
    
    .sidebar .sidebar-content {
        background-color: #161b22;
    }
    
    .sidebar .stHeader {
        color: #c9a84c !important;
    }
    
    /* ============ SIDEBAR TEXT ============ */
    [data-testid="stSidebar"] label {
        color: #c9d1d9 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stCaption {
        color: #8b949e !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #8b949e;
    }
    
    /* ============ INFO/SUCCESS/WARNING BOXES ============ */
    .stAlert {
        border-radius: 8px !important;
        background-color: #161b22 !important;
        border: 1px solid #21262d !important;
    }
    
    .stSuccess {
        border-left: 4px solid #27ae60 !important;
    }
    
    .stInfo {
        border-left: 4px solid #c9a84c !important;
    }
    
    .stWarning {
        border-left: 4px solid #f39c12 !important;
    }
    
    .stError {
        border-left: 4px solid #e74c3c !important;
    }
    
    /* ============ SPINNER ============ */
    .stSpinner > div {
        border-top-color: #c9a84c !important;
    }
    
    /* ============ DATA METRICS ============ */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #e6edf3 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
    }
    
    /* ============ INPUTS ============ */
    .stTextInput input, .stSelectbox select, .stDateInput input {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #0d1117 !important;
    }
    
    /* ============ SLIDER ============ */
    .stSlider > div > div > div {
        background-color: #c9a84c !important;
    }
    
    /* ============ CUSTOM SCROLLBAR ============ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #161b22;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #c9a84c 0%, #b8963e 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #d4b35c;
    }
    
    /* ============ FOREX SPECIFIC STYLES ============ */
    .pip-indicator {
        background: #21262d;
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        color: #c9d1d9;
    }
    
    .rate-display {
        font-size: 2rem;
        font-weight: 800;
        color: #e6edf3;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #30363d;
    }
    
    /* ============ EXPANDER ============ */
    .streamlit-expanderHeader {
        background-color: #161b22 !important;
        border: 1px solid #21262d !important;
        color: #c9d1d9 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0d1117 !important;
        border: 1px solid #21262d !important;
    }
    
    /* ============ CODE BLOCKS ============ */
    code {
        color: #c9a84c !important;
        background-color: #21262d !important;
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    pre {
        background-color: #161b22 !important;
        border: 1px solid #21262d !important;
    }
    
    /* ============ PROGRESS BAR ============ */
    .stProgress > div > div > div {
        background-color: #c9a84c !important;
    }
    
    /* ============ TABS ============ */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22;
        border-bottom: 1px solid #21262d;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
    }
    
    .stTabs [aria-selected="true"] {
        color: #c9a84c !important;
        border-bottom-color: #c9a84c !important;
    }
    </style>
    """


def apply_plot_style(fig, axes=None):
    """Apply dark professional style to matplotlib plots"""
    plt_style = {
        'figure.facecolor': '#0d1117',
        'axes.facecolor': '#161b22',
        'axes.grid': True,
        'grid.alpha': 0.15,
        'grid.color': '#30363d',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': True,
        'axes.spines.bottom': True,
        'axes.edgecolor': '#30363d',
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'text.color': '#c9d1d9',
        'axes.labelcolor': '#c9d1d9',
        'xtick.color': '#8b949e',
        'ytick.color': '#8b949e',
    }
    
    import matplotlib.pyplot as plt
    plt.rcParams.update(plt_style)
    
    if axes is not None:
        if not isinstance(axes, list):
            axes = [axes]
        
        for ax in axes:
            ax.set_facecolor('#161b22')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#30363d')
            ax.spines['bottom'].set_color('#30363d')
            ax.tick_params(colors='#8b949e')
            ax.xaxis.label.set_color('#c9d1d9')
            ax.yaxis.label.set_color('#c9d1d9')
            ax.title.set_color('#e6edf3')


def get_insight_card(title, content, variant="default"):
    """Generate insight card HTML for dark theme"""
    variants = {
        "positive": {
            "bg": "#0d1f14", 
            "border": "#27ae60", 
            "text": "#7ddb9e", 
            "accent": "#27ae60",
            "title_color": "#27ae60"
        },
        "warning": {
            "bg": "#1f180a", 
            "border": "#f39c12", 
            "text": "#f5d78c", 
            "accent": "#f39c12",
            "title_color": "#f39c12"
        },
        "danger": {
            "bg": "#1f0d0d", 
            "border": "#e74c3c", 
            "text": "#f5a09c", 
            "accent": "#e74c3c",
            "title_color": "#e74c3c"
        },
        "default": {
            "bg": "#161b22", 
            "border": "#c9a84c", 
            "text": "#c9d1d9", 
            "accent": "#c9a84c",
            "title_color": "#c9a84c"
        },
    }
    
    v = variants.get(variant, variants["default"])
    
    return f"""
    <div style="
        background-color: {v['bg']};
        border-left: 4px solid {v['border']};
        padding: 1.2rem 1.5rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: {v['text']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    ">
        <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.6rem; color: {v['title_color']}; letter-spacing: 0.3px; text-transform: uppercase;">
            {title}
        </div>
        <div style="font-size: 0.92rem; line-height: 1.7;">
            {content}
        </div>
    </div>
    """


def get_highlight_box(value, label, trend="neutral"):
    """Generate highlight box for key metrics in dark theme"""
    colors = {
        "up": {
            "bg": "#0d1f14", 
            "border": "#27ae60", 
            "text": "#7ddb9e", 
            "indicator": "▲",
            "label_color": "#27ae60"
        },
        "down": {
            "bg": "#1f0d0d", 
            "border": "#e74c3c", 
            "text": "#f5a09c", 
            "indicator": "▼",
            "label_color": "#e74c3c"
        },
        "neutral": {
            "bg": "#161b22", 
            "border": "#c9a84c", 
            "text": "#c9a84c", 
            "indicator": "■",
            "label_color": "#c9a84c"
        },
    }
    
    c = colors.get(trend, colors["neutral"])
    
    return f"""
    <div style="
        background-color: {c['bg']};
        border: 1.5px solid {c['border']};
        padding: 1.2rem;
        border-radius: 8px;
        text-align: center;
        color: {c['text']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    ">
        <div style="font-size: 0.8rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px; color: {c['label_color']};">
            {label}
        </div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; letter-spacing: -0.5px;">
            {c['indicator']} {value}
        </div>
    </div>
    """


def get_forex_rate_card(pair, rate, change, symbol):
    """Special card for displaying forex rates in dark theme"""
    change_color = "#27ae60" if change >= 0 else "#e74c3c"
    change_sign = "+" if change >= 0 else ""
    trend_indicator = "▲" if change >= 0 else "▼"
    
    return f"""
    <div class="rate-display">
        <div style="font-size: 0.85rem; color: #8b949e; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
            {pair}
        </div>
        <div style="font-size: 2.8rem; font-weight: 800; color: #e6edf3; letter-spacing: -1px;">
            {symbol} {rate:,.2f}
        </div>
        <div style="font-size: 1rem; color: {change_color}; margin-top: 0.4rem; font-weight: 600;">
            {trend_indicator} {change_sign}{change:.2f}
        </div>
    </div>
    """
