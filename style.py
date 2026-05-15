# style.py - RixterProphet Analytics: Forex Edition
# Professional Styling & Theme for Streamlit App

import streamlit as st

def get_theme_css():
    """Return comprehensive CSS theme for the forex analytics app"""
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
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #1a1a2e;
        font-weight: 700 !important;
        border-bottom: 2px solid #1a1a2e;
        padding-bottom: 0.5rem;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: #2c3e50;
        font-weight: 600 !important;
        letter-spacing: -0.2px;
    }
    
    /* ============ CARDS & CONTAINERS ============ */
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid #e0e0e0;
    }
    
    .note-box {
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
        border-left: 4px solid #555;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1.5rem 0;
        color: #2c3e50;
    }
    
    /* ============ PREDICTION TABLE ============ */
    .prediction-table {
        overflow-x: auto;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.08);
    }
    
    .prediction-table table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }
    
    .prediction-table th {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .prediction-table td {
        padding: 10px 15px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .prediction-table tr:hover {
        background-color: #f8f9fa;
    }
    
    .prediction-table tr:last-child {
        font-weight: 600;
        background-color: #fafafa;
    }
    
    /* ============ METRIC CARDS ============ */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid #eee;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.10);
    }
    
    /* ============ BUTTONS ============ */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26, 26, 46, 0.3) !important;
    }
    
    /* ============ SIDEBAR ============ */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #fafafa;
    }
    
    .sidebar .sidebar-content {
        background-color: #fafafa;
    }
    
    /* ============ INFO/SUCCESS BOXES ============ */
    .stAlert {
        border-radius: 8px !important;
    }
    
    /* ============ SPINNER ============ */
    .stSpinner > div {
        border-top-color: #1a1a2e !important;
    }
    
    /* ============ DATA METRICS ============ */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    
    /* ============ CUSTOM SCROLLBAR ============ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f5f5f5;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 10px;
    }
    
    /* ============ FOREX SPECIFIC STYLES ============ */
    .pip-indicator {
        background: #f5f5f5;
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
    }
    
    .rate-display {
        font-size: 2rem;
        font-weight: 800;
        color: #1a1a2e;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    </style>
    """


def apply_plot_style(fig, axes=None):
    """Apply professional style to matplotlib plots"""
    plt_style = {
        'figure.facecolor': 'white',
        'axes.facecolor': '#fafafa',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
    }
    
    import matplotlib.pyplot as plt
    plt.rcParams.update(plt_style)
    
    if axes is not None:
        if not isinstance(axes, list):
            axes = [axes]
        
        for ax in axes:
            ax.set_facecolor('#fafafa')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cccccc')
            ax.spines['bottom'].set_color('#cccccc')
            ax.tick_params(colors='#666666')


def get_insight_card(title, content, variant="default"):
    """Generate insight card HTML with color coding - no emojis"""
    variants = {
        "positive": {"bg": "#f0f4f0", "border": "#2d4a2d", "text": "#1a2e1a", "accent": "#2d4a2d"},
        "warning": {"bg": "#faf8f0", "border": "#8a7a2e", "text": "#4a3e1a", "accent": "#8a7a2e"},
        "danger": {"bg": "#faf0f0", "border": "#8a2e2e", "text": "#4a1a1a", "accent": "#8a2e2e"},
        "default": {"bg": "#f5f5f5", "border": "#555", "text": "#2a2a2a", "accent": "#555"},
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
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    ">
        <div style="font-weight: 700; font-size: 1rem; margin-bottom: 0.6rem; color: {v['accent']}; letter-spacing: 0.3px; text-transform: uppercase;">
            {title}
        </div>
        <div style="font-size: 0.92rem; line-height: 1.7;">
            {content}
        </div>
    </div>
    """


def get_highlight_box(value, label, trend="neutral"):
    """Generate highlight box for key metrics - no emojis"""
    colors = {
        "up": {"bg": "#f0f4f0", "border": "#2d4a2d", "text": "#1a2e1a", "indicator": "▲"},
        "down": {"bg": "#faf0f0", "border": "#8a2e2e", "text": "#4a1a1a", "indicator": "▼"},
        "neutral": {"bg": "#faf8f0", "border": "#8a7a2e", "text": "#4a3e1a", "indicator": "■"},
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
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 0.8rem; font-weight: 500; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.5px;">
            {label}
        </div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; letter-spacing: -0.5px;">
            {c['indicator']} {value}
        </div>
    </div>
    """


def get_forex_rate_card(pair, rate, change, symbol):
    """Special card for displaying forex rates - no emojis"""
    change_color = "#2d4a2d" if change >= 0 else "#8a2e2e"
    change_sign = "+" if change >= 0 else ""
    
    return f"""
    <div class="rate-display">
        <div style="font-size: 0.85rem; color: #888; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">
            {pair}
        </div>
        <div style="font-size: 2.8rem; font-weight: 800; color: #1a1a2e; letter-spacing: -1px;">
            {symbol} {rate:,.2f}
        </div>
        <div style="font-size: 1rem; color: {change_color}; margin-top: 0.4rem; font-weight: 600;">
            {change_sign}{change:.2f}
        </div>
    </div>
    """
