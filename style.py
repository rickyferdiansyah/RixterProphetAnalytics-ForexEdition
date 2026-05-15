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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #2c3e50;
        font-weight: 700 !important;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: #34495e;
        font-weight: 600 !important;
    }
    
    /* ============ CARDS & CONTAINERS ============ */
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid #e0e0e0;
    }
    
    .note-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left: 4px solid #e67e22;
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
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .prediction-table table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }
    
    .prediction-table th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
    }
    
    .prediction-table td {
        padding: 10px 15px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .prediction-table tr:hover {
        background-color: #f8f9ff;
    }
    
    .prediction-table tr:last-child {
        font-weight: 600;
        background-color: #f8f9ff;
    }
    
    /* ============ METRIC CARDS ============ */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    /* ============ BUTTONS ============ */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* ============ SIDEBAR ============ */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #f8f9fa;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* ============ INFO/SUCCESS BOXES ============ */
    .stAlert {
        border-radius: 8px !important;
    }
    
    /* ============ SPINNER ============ */
    .stSpinner > div {
        border-top-color: #667eea !important;
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
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* ============ TOOLTIP ============ */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        border-bottom: 1px dotted #667eea;
    }
    
    /* ============ FOREX SPECIFIC STYLES ============ */
    .pip-indicator {
        background: #f0f0f0;
        padding: 8px 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
    }
    
    .rate-display {
        font-size: 2rem;
        font-weight: 800;
        color: #2c3e50;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        margin: 1rem 0;
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
    """Generate insight card HTML with color coding"""
    variants = {
        "positive": {"bg": "#d4edda", "border": "#28a745", "icon": "✅", "text": "#155724"},
        "warning": {"bg": "#fff3cd", "border": "#ffc107", "icon": "⚠️", "text": "#856404"},
        "danger": {"bg": "#f8d7da", "border": "#dc3545", "icon": "🔴", "text": "#721c24"},
        "default": {"bg": "#e2e3e5", "border": "#6c757d", "icon": "ℹ️", "text": "#383d41"},
    }
    
    v = variants.get(variant, variants["default"])
    
    return f"""
    <div style="
        background-color: {v['bg']};
        border-left: 4px solid {v['border']};
        padding: 1rem 1.2rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: {v['text']};
    ">
        <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">
            {v['icon']} {title}
        </div>
        <div style="font-size: 0.95rem; line-height: 1.6;">
            {content}
        </div>
    </div>
    """


def get_highlight_box(value, label, trend="neutral"):
    """Generate highlight box for key metrics"""
    colors = {
        "up": {"bg": "#d4edda", "border": "#28a745", "text": "#155724", "emoji": "📈"},
        "down": {"bg": "#f8d7da", "border": "#dc3545", "text": "#721c24", "emoji": "📉"},
        "neutral": {"bg": "#fff3cd", "border": "#ffc107", "text": "#856404", "emoji": "➡️"},
    }
    
    c = colors.get(trend, colors["neutral"])
    
    return f"""
    <div style="
        background-color: {c['bg']};
        border: 2px solid {c['border']};
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: {c['text']};
    ">
        <div style="font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem;">
            {label}
        </div>
        <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.3rem;">
            {c['emoji']} {value}
        </div>
    </div>
    """


def get_forex_rate_card(pair, rate, change, symbol):
    """Special card for displaying forex rates"""
    change_color = "#27ae60" if change >= 0 else "#e74c3c"
    change_sign = "+" if change >= 0 else ""
    
    return f"""
    <div class="rate-display">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">
            {pair}
        </div>
        <div style="font-size: 2.5rem; font-weight: 800; color: #2c3e50;">
            {symbol} {rate:,.2f}
        </div>
        <div style="font-size: 1.1rem; color: {change_color}; margin-top: 0.3rem;">
            {change_sign}{change:.2f}
        </div>
    </div>
    """
