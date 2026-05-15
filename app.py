# app.py - RixterProphet Analytics: Forex Edition
# LSTM Predictor for Forex with Deep Insights & Clear Emphasis
import os
import sys

# Pastikan current directory ada di path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import warnings

from style import get_theme_css, apply_plot_style, get_insight_card, get_highlight_box, get_forex_rate_card
from models import VanillaLSTM, BidirectionalLSTM

warnings.filterwarnings('ignore')

# Set seed for reproducibility
SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

# Page config
st.set_page_config(
    page_title="RixterProphet Analytics - Forex Edition",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FOREX PAIRS CONFIGURATION ====================
FOREX_PAIRS = {
    'USD/IDR': {'ticker': 'USDIDR=X', 'base': 'USD', 'quote': 'IDR', 'symbol': 'Rp', 'pip_size': 1.0},
    'EUR/USD': {'ticker': 'EURUSD=X', 'base': 'EUR', 'quote': 'USD', 'symbol': '$', 'pip_size': 0.0001},
    'GBP/USD': {'ticker': 'GBPUSD=X', 'base': 'GBP', 'quote': 'USD', 'symbol': '$', 'pip_size': 0.0001},
    'USD/JPY': {'ticker': 'USDJPY=X', 'base': 'USD', 'quote': 'JPY', 'symbol': '¥', 'pip_size': 0.01},
    'AUD/USD': {'ticker': 'AUDUSD=X', 'base': 'AUD', 'quote': 'USD', 'symbol': '$', 'pip_size': 0.0001},
    'USD/SGD': {'ticker': 'USDSGD=X', 'base': 'USD', 'quote': 'SGD', 'symbol': 'S$', 'pip_size': 0.0001},
    'EUR/JPY': {'ticker': 'EURJPY=X', 'base': 'EUR', 'quote': 'JPY', 'symbol': '¥', 'pip_size': 0.01},
    'GBP/JPY': {'ticker': 'GBPJPY=X', 'base': 'GBP', 'quote': 'JPY', 'symbol': '¥', 'pip_size': 0.01},
}

# ==================== HELPER FUNCTIONS ====================
@st.cache_data(ttl=3600)
def download_forex_data(ticker, start, end):
    """Download data forex dari Yahoo Finance dengan caching"""
    try:
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        if df.empty:
            return None
        
        # Handle MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df = df.reset_index()
        
        # Standardize column names
        rename_map = {}
        for col in df.columns:
            col_lower = str(col).lower()
            if 'date' in col_lower or col_lower == 'index':
                rename_map[col] = 'Date'
            elif 'close' in col_lower:
                rename_map[col] = 'Close'
            elif 'high' in col_lower:
                rename_map[col] = 'High'
            elif 'low' in col_lower:
                rename_map[col] = 'Low'
            elif 'open' in col_lower:
                rename_map[col] = 'Open'
        
        df = df.rename(columns=rename_map)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Ensure required columns exist
        required_cols = ['Date', 'Close', 'High', 'Low', 'Open']
        for col in required_cols:
            if col not in df.columns:
                df[col] = df.get('Close', df.iloc[:, 1] if len(df.columns) > 1 else 0)
        
        return df[required_cols].dropna()
    except Exception as e:
        st.error(f"Download error: {e}")
        return None


def create_sequences(data, seq_length):
    """Membuat sequences untuk time series forecasting"""
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i])
        y.append(data[i, 0])  # Predict Close price
    return np.array(X), np.array(y)


def inverse_scale(value, scaler, n_features=4):
    """Inverse transform scaled value ke actual price"""
    dummy = np.zeros((1, n_features))
    dummy[0, 0] = value
    return scaler.inverse_transform(dummy)[0, 0]


def is_trading_day(date):
    """Cek apakah tanggal adalah hari trading (Senin-Jumat)"""
    return date.weekday() < 5


def get_next_trading_days(last_date, n_days=14):
    """Generate list of next trading days"""
    trading_days = []
    current = last_date + timedelta(days=1)
    while len(trading_days) < n_days:
        if is_trading_day(current):
            trading_days.append(current)
        current += timedelta(days=1)
    return trading_days


def train_model(model, train_loader, val_loader, epochs, lr=0.001, patience=15):
    """Training loop dengan early stopping"""
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)
    
    train_losses, val_losses = [], []
    best_val_loss = float('inf')
    patience_counter = 0
    best_model_state = None
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        train_losses.append(train_loss)
        
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        val_losses.append(val_loss)
        scheduler.step(val_loss)
        
        progress = (epoch + 1) / epochs
        progress_bar.progress(progress)
        status_text.text(f"Epoch {epoch+1}/{epochs} -- Train Loss: {train_loss:.6f} | Val Loss: {val_loss:.6f}")
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_model_state = model.state_dict().copy()
        else:
            patience_counter += 1
            if patience_counter >= patience:
                status_text.text(f"Early stopping triggered at epoch {epoch+1}")
                break
    
    progress_bar.empty()
    status_text.empty()
    if best_model_state:
        model.load_state_dict(best_model_state)
    return model, train_losses, val_losses, len(train_losses)


def calculate_technical_indicators(df):
    """Hitung technical indicators untuk forex"""
    indicators = {}
    
    recent = df.tail(30)
    indicators['current_price'] = df['Close'].iloc[-1]
    indicators['price_30d_ago'] = df['Close'].iloc[-30] if len(df) >= 30 else df['Close'].iloc[0]
    indicators['change_30d'] = ((indicators['current_price'] - indicators['price_30d_ago']) / indicators['price_30d_ago']) * 100
    
    # Moving Averages
    indicators['ma_20'] = df['Close'].rolling(20).mean().iloc[-1]
    indicators['ma_50'] = df['Close'].rolling(50).mean().iloc[-1]
    indicators['ma_200'] = df['Close'].rolling(200).mean().iloc[-1] if len(df) >= 200 else None
    
    # Volatility
    returns = df['Close'].pct_change().dropna()
    indicators['volatility_20d'] = returns.tail(20).std() * 100
    indicators['volatility_60d'] = returns.tail(60).std() * 100 if len(returns) >= 60 else indicators['volatility_20d']
    
    # Support & Resistance
    recent_low = recent['Low'].min()
    recent_high = recent['High'].max()
    indicators['support_30d'] = recent_low
    indicators['resistance_30d'] = recent_high
    
    # Price position
    price_range = recent_high - recent_low
    if price_range > 0:
        indicators['price_position'] = ((indicators['current_price'] - recent_low) / price_range) * 100
    else:
        indicators['price_position'] = 50
    
    # Trend strength
    highs = recent['High'].values
    lows = recent['Low'].values
    higher_highs = sum(1 for i in range(1, len(highs)) if highs[i] > highs[i-1])
    higher_lows = sum(1 for i in range(1, len(lows)) if lows[i] > lows[i-1])
    indicators['trend_strength'] = ((higher_highs + higher_lows) / (2 * (len(highs)-1))) * 100
    
    # Forex specific
    indicators['avg_daily_range'] = (recent['High'] - recent['Low']).mean()
    indicators['current_spread_estimate'] = indicators['avg_daily_range'] * 0.05
    
    return indicators


def generate_forex_insights(model_name, pair_name, metrics, indicators, future_preds, future_dates, pip_size, symbol='Rp'):
    """Generate comprehensive forex insights"""
    insights = []
    
    mape = metrics['mape']
    r2 = metrics['r2']
    
    # Model Performance
    if mape < 1:
        perf_rating = "SANGAT BAIK"
        perf_class = "positive"
        perf_desc = f"Model {model_name} menunjukkan performa sangat akurat dengan MAPE {mape:.2f}%. Untuk forex, akurasi di bawah 1% sangat impresif."
    elif mape < 3:
        perf_rating = "BAIK"
        perf_class = "positive"
        perf_desc = f"Model {model_name} bekerja dengan baik (MAPE {mape:.2f}%). Error di bawah 3% cukup baik untuk pasar forex yang dinamis."
    elif mape < 5:
        perf_rating = "CUKUP"
        perf_class = "warning"
        perf_desc = f"Model {model_name} memiliki akurasi cukup (MAPE {mape:.2f}%). Forex sangat sulit diprediksi karena banyak faktor eksternal."
    else:
        perf_rating = "RENDAH"
        perf_class = "danger"
        perf_desc = f"Model {model_name} menunjukkan MAPE tinggi ({mape:.2f}%). Pasar forex sangat volatile, pertimbangkan faktor fundamental."
    
    insights.append({
        'title': f'Kualitas Model: {perf_rating}',
        'content': perf_desc + f"<br><br>R-squared: <b>{r2:.4f}</b> -- {'model dapat menjelaskan ' + str(int(r2*100)) + '% variasi harga' if r2 > 0 else 'model tidak lebih baik dari prediksi rata-rata'}.",
        'variant': perf_class
    })
    
    # Current Position
    pos = indicators['price_position']
    if pos > 70:
        position_desc = f"{pair_name} di <b>{pos:.0f}% dari range 30 hari</b> -- mendekati <b>RESISTANCE</b> di {symbol}{indicators['resistance_30d']:,.2f}. Waspada potensi reversal."
        position_class = "warning"
    elif pos < 30:
        position_desc = f"{pair_name} di <b>{pos:.0f}% dari range 30 hari</b> -- mendekati <b>SUPPORT</b> di {symbol}{indicators['support_30d']:,.2f}. Potensi rebound jika support bertahan."
        position_class = "positive"
    else:
        position_desc = f"{pair_name} di <b>mid-range</b> ({pos:.0f}%), support {symbol}{indicators['support_30d']:,.2f}, resistance {symbol}{indicators['resistance_30d']:,.2f}."
        position_class = "default"
    
    insights.append({
        'title': 'Posisi Harga Terkini',
        'content': position_desc + f"<br><br>Range harian rata-rata: <b>{symbol}{indicators['avg_daily_range']:,.2f}</b> ({indicators['avg_daily_range']/indicators['current_price']*100:.2f}% dari harga)",
        'variant': position_class
    })
    
    # Trend Analysis
    trend_strength = indicators['trend_strength']
    change_30d = indicators['change_30d']
    
    if change_30d > 1 and trend_strength > 60:
        trend_desc = f"<b>UPTREND KUAT</b> terdeteksi. {pair_name} menguat <b>{change_30d:+.2f}%</b> dalam 30 hari."
        trend_class = "positive"
    elif change_30d > 0 and trend_strength > 50:
        trend_desc = f"<b>UPTREND MODERAT</b>. Penguatan {change_30d:+.2f}% dalam 30 hari."
        trend_class = "positive"
    elif change_30d < -1 and trend_strength > 60:
        trend_desc = f"<b>DOWNTREND KUAT</b>. {pair_name} melemah <b>{change_30d:+.2f}%</b> dalam 30 hari."
        trend_class = "danger"
    elif change_30d < 0 and trend_strength > 50:
        trend_desc = f"<b>DOWNTREND MODERAT</b>. Pelemahan {change_30d:+.2f}% dalam 30 hari."
        trend_class = "warning"
    else:
        trend_desc = f"<b>SIDEWAYS / KONSOLIDASI</b>. Perubahan 30 hari: {change_30d:+.2f}%."
        trend_class = "default"
    
    insights.append({
        'title': 'Analisis Tren',
        'content': trend_desc + f"<br><br>MA20: {symbol}{indicators['ma_20']:,.2f} | MA50: {symbol}{indicators['ma_50']:,.2f}" + 
                  (f" | MA200: {symbol}{indicators['ma_200']:,.2f}" if indicators['ma_200'] else ""),
        'variant': trend_class
    })
    
    # Volatility
    vol_20 = indicators['volatility_20d']
    vol_60 = indicators['volatility_60d']
    
    if vol_20 > 1:
        vol_desc = f"<b>VOLATILITAS TINGGI</b>: {vol_20:.2f}% (20-hari). Pasar forex sedang sangat dinamis -- pergerakan besar mungkin terjadi."
        vol_class = "warning"
    elif vol_20 > 0.5:
        vol_desc = f"<b>VOLATILITAS MODERAT</b>: {vol_20:.2f}% (20-hari). Kondisi pasar normal untuk forex."
        vol_class = "default"
    else:
        vol_desc = f"<b>VOLATILITAS RENDAH</b>: {vol_20:.2f}% (20-hari). Pasar tenang, mungkin menunggu katalis."
        vol_class = "positive"
    
    if vol_20 > vol_60 * 1.3:
        vol_desc += " Volatilitas jangka pendek <b>meningkat</b> -- pantau berita ekonomi penting."
    elif vol_20 < vol_60 * 0.7:
        vol_desc += " Volatilitas jangka pendek <b>menurun</b> -- pasar stabil."
    
    insights.append({
        'title': 'Volatilitas Pasar',
        'content': vol_desc,
        'variant': vol_class
    })
    
    # Future Projection
    future_start = future_preds[0]
    future_end = future_preds[-1]
    future_change = ((future_end - future_start) / future_start) * 100
    pip_movement = abs(future_end - future_start) / pip_size
    
    if abs(future_change) > 1:
        fut_class = "positive" if future_change > 0 else "danger"
        fut_desc = f"Model memproyeksikan <b>{'PENGUATAN' if future_change > 0 else 'PELEMAHAN'} SIGNIFIKAN</b> sebesar <b>{future_change:+.2f}%</b> (~{pip_movement:,.0f} pips). "
    elif abs(future_change) > 0.3:
        fut_class = "positive" if future_change > 0 else "warning"
        fut_desc = f"Proyeksi <b>{'penguatan' if future_change > 0 else 'pelemahan'} moderat</b> {future_change:+.2f}% (~{pip_movement:,.0f} pips). "
    else:
        fut_class = "default"
        fut_desc = f"Proyeksi relatif <b>flat</b> ({future_change:+.2f}%, ~{pip_movement:,.0f} pips) -- konsolidasi. "
    
    fut_desc += f"Range: <b>{symbol}{future_preds.min():,.2f} -- {symbol}{future_preds.max():,.2f}</b>."
    
    insights.append({
        'title': f'Proyeksi {len(future_preds)} Hari ke Depan',
        'content': fut_desc,
        'variant': fut_class
    })
    
    # Forex specific
    insights.append({
        'title': 'Karakteristik Pasar Forex',
        'content': f"Forex beroperasi <b>24 jam/5 hari</b>. {pair_name} paling aktif selama sesi overlap London-New York (19:00-23:00 WIB). "
                   f"Spread estimasi: <b>{symbol}{indicators['current_spread_estimate']:,.2f}</b> per unit. "
                   f"Gunakan risk management ketat: max 1-2% risk per trade.",
        'variant': 'default'
    })
    
    return insights


def plot_forex_test_zoom(df, train_size, val_size, seq_len, y_test_actual, y_pred_test_actual,
                         model_name, pair_name, mape_val, r2, symbol='Rp',
                         future_dates_list=None, future_actual=None):
    """Plot zoom-in khusus data testing untuk forex"""
    
    test_start_idx = train_size + val_size
    test_dates = df['Date'].iloc[test_start_idx:].values
    
    min_len = min(len(test_dates), len(y_test_actual), len(y_pred_test_actual))
    test_dates = test_dates[-min_len:]
    y_test_actual = y_test_actual[-min_len:]
    y_pred_test_actual = y_pred_test_actual[-min_len:]
    
    errors = np.abs(y_test_actual - y_pred_test_actual)
    mae_line = np.mean(errors)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 9), gridspec_kw={'height_ratios': [3, 1]})
    apply_plot_style(fig, [ax1, ax2])
    
    ax1.plot(test_dates, y_test_actual, '#1f77b4', label='Actual Rate', linewidth=2.2, 
             marker='o', markersize=5, markerfacecolor='white', markeredgewidth=1.5)
    ax1.plot(test_dates, y_pred_test_actual, '#ff7f0e', label='Predicted Rate', linewidth=2, 
             marker='s', markersize=5, markerfacecolor='white', markeredgewidth=1.5)
    
    if future_dates_list is not None and future_actual is not None:
        ax1.plot(future_dates_list, future_actual, '#2ca02c', 
                label=f'Future Projection ({len(future_actual)} days)', 
                linewidth=3, marker='o', markersize=7, markerfacecolor='white', markeredgewidth=2)
        
        last_test_date = test_dates[-1]
        ax1.axvline(x=last_test_date, color='#666', linestyle='--', alpha=0.5, linewidth=1)
        ax1.text(last_test_date, ax1.get_ylim()[1]*0.95, 'Test | Future', 
                ha='center', fontsize=9, color='#666')
    
    ax1.fill_between(test_dates, y_test_actual, y_pred_test_actual, alpha=0.15, 
                     color='#ff7f0e', label='Prediction Error Gap')
    
    # Highlight max error
    max_err_idx = np.argmax(errors)
    y_max_err = max(y_test_actual[max_err_idx], y_pred_test_actual[max_err_idx])
    ax1.annotate(f'Max Error\n{symbol}{errors[max_err_idx]:,.2f}',
                xy=(test_dates[max_err_idx], y_test_actual[max_err_idx]),
                xytext=(test_dates[max_err_idx], y_max_err * 1.02),
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5),
                fontsize=9, color='#e74c3c', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#e74c3c', alpha=0.8),
                ha='center')
    
    ax1.set_ylabel(f'Exchange Rate ({symbol})', fontweight='bold')
    ax1.set_title(f'Zoom: Test Data Only -- {model_name} | {pair_name}\n'
                  f'MAPE: {mape_val:.2f}% | R-squared: {r2:.4f} | Avg Error: {symbol}{mae_line:,.2f}',
                  fontweight='bold', fontsize=13)
    
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(), loc='upper left', framealpha=0.9, fontsize=10)
    ax1.grid(True, alpha=0.4)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{symbol}{x:,.2f}'))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
    
    colors = ['#e74c3c' if e > mae_line * 1.5 else '#f39c12' if e > mae_line else '#27ae60' for e in errors]
    ax2.bar(test_dates, errors, color=colors, alpha=0.85, width=0.8)
    ax2.axhline(y=mae_line, color='#333', linestyle='--', linewidth=1.5, 
                label=f'Avg Error: {symbol}{mae_line:,.2f}')
    ax2.set_ylabel(f'Absolute Error ({symbol})', fontweight='bold')
    ax2.set_xlabel('Date', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{symbol}{x:,.2f}'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
    
    legend_elements = [
        Patch(facecolor='#27ae60', alpha=0.85, label='Below Avg'),
        Patch(facecolor='#f39c12', alpha=0.85, label='Moderate'),
        Patch(facecolor='#e74c3c', alpha=0.85, label='High Error'),
    ]
    ax2.legend(handles=legend_elements, loc='upper right', fontsize=8, ncol=3)
    
    fig.autofmt_xdate()
    plt.tight_layout(pad=2)
    
    return fig


# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("Forex Parameters")
    
    # Forex pair selection
    pair_options = list(FOREX_PAIRS.keys())
    selected_pair = st.selectbox(
        "Currency Pair",
        pair_options,
        index=0,
        help="Select currency pair for analysis"
    )
    
    pair_info = FOREX_PAIRS[selected_pair]
    ticker = pair_info['ticker']
    base_currency = pair_info['base']
    quote_currency = pair_info['quote']
    currency_symbol = pair_info['symbol']
    pip_size = pair_info['pip_size']
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                color: white; padding: 0.8rem; border-radius: 8px; text-align: center; margin: 0.5rem 0;">
        <div style="font-size: 0.8rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 1px;">{base_currency}/{quote_currency}</div>
        <div style="font-size: 1.3rem; font-weight: 700;">{currency_symbol} -- {selected_pair}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2020, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    st.markdown("---")
    st.subheader("Model & Training")
    
    model_type = st.selectbox(
        "LSTM Architecture",
        ["Vanilla LSTM", "Bidirectional LSTM"],
        index=0,
        help="Vanilla: Fast & efficient. Bidirectional: Better pattern recognition"
    )
    
    seq_len = st.selectbox(
        "Sequence Length (days)",
        [3, 5, 7, 10, 14, 20],
        index=3,
        help="Historical days used for 1 prediction. Forex: 10-14 days optimal"
    )
    
    epochs = st.slider("Epochs", 10, 200, 100, 10)
    batch_size = st.selectbox("Batch Size", [16, 32], index=0)
    hidden_units = st.slider("Hidden Units", 16, 256, 128, 8)
    lr = st.selectbox(
        "Learning Rate",
        [0.01, 0.001, 0.0005],
        index=1,
        format_func=lambda x: f"{x:.4f}"
    )
    
    st.markdown("---")
    st.subheader("Prediction")
    future_days = st.slider("Forecast Days", 5, 30, 14, 1)
    
    predict_btn = st.button("START FOREX ANALYSIS", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.caption("Powered by PyTorch + Yahoo Finance")
    st.caption("Forex Edition v1.0")

# Apply theme
st.markdown(get_theme_css(), unsafe_allow_html=True)

# ==================== HEADER ====================
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.title("RixterProphet Analytics")
    st.caption("Forex Edition -- LSTM-Based Predictive Analytics with Deep Insights")

# ==================== MAIN LOGIC ====================
if predict_btn:
    try:
        with st.spinner(f"Downloading {selected_pair} data from Yahoo Finance..."):
            df = download_forex_data(ticker, start_date, end_date)
            if df is None or len(df) < 100:
                st.error(f"Data insufficient. Minimum 100 rows required for valid analysis.")
                st.stop()
        
        # Display current rate
        current_rate = df['Close'].iloc[-1]
        previous_rate = df['Close'].iloc[-2]
        rate_change = current_rate - previous_rate
        
        st.markdown(get_forex_rate_card(selected_pair, current_rate, rate_change, currency_symbol), 
                   unsafe_allow_html=True)
        
        st.success(f"**{len(df):,} data rows** ({df['Date'].min().strftime('%d %b %Y')} -- {df['Date'].max().strftime('%d %b %Y')})")
        
        # Split data
        n = len(df)
        train_size = int(n * 0.7)
        val_size = int(n * 0.15)
        test_size = n - train_size - val_size
        
        indicators = calculate_technical_indicators(df)
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("Data Split")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Training", f"{train_size:,} rows", f"{train_size/n*100:.0f}%")
        col2.metric("Validation", f"{val_size:,} rows", f"{val_size/n*100:.0f}%")
        col3.metric("Test", f"{test_size:,} rows", f"{test_size/n*100:.0f}%")
        col4.metric("Forecast", f"{future_days} days", "ahead")
        
        with st.spinner("Processing data & scaling..."):
            features = ['Close', 'High', 'Low', 'Open']
            data_full = df[features].values
            scaler = MinMaxScaler()
            scaled_full = scaler.fit_transform(data_full)
            
            scaled_train = scaled_full[:train_size]
            scaled_val = scaled_full[train_size-seq_len:train_size+val_size]
            scaled_test = scaled_full[train_size+val_size-seq_len:]
            
            X_train, y_train = create_sequences(scaled_train, seq_len)
            X_val, y_val = create_sequences(scaled_val, seq_len)
            X_test, y_test = create_sequences(scaled_test, seq_len)
            
            train_dataset = TensorDataset(torch.FloatTensor(X_train), torch.FloatTensor(y_train).reshape(-1, 1))
            val_dataset = TensorDataset(torch.FloatTensor(X_val), torch.FloatTensor(y_val).reshape(-1, 1))
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
            val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        with st.spinner("Building model architecture..."):
            if model_type == "Vanilla LSTM":
                model = VanillaLSTM(4, hidden_units, 1, 0.1)
            else:
                model = BidirectionalLSTM(4, hidden_units, 1, 0.1)
            
            total_params = sum(p.numel() for p in model.parameters())
            trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        st.info(f"**{model_type}** | Total Parameters: **{total_params:,}** | Trainable: **{trainable_params:,}**")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("Training Process")
        
        model, train_losses, val_losses, actual_epochs = train_model(model, train_loader, val_loader, epochs, lr)
        st.success(f"Training complete -- **{actual_epochs} epochs** executed")
        
        # Loss plot
        fig_loss, ax_loss = plt.subplots(figsize=(10, 3))
        apply_plot_style(fig_loss, ax_loss)
        ax_loss.plot(range(1, len(train_losses)+1), train_losses, '#1a1a2e', label='Train Loss', linewidth=1.5)
        ax_loss.plot(range(1, len(val_losses)+1), val_losses, '#8a2e2e', label='Val Loss', linewidth=1.5)
        ax_loss.set_xlabel('Epoch')
        ax_loss.set_ylabel('Loss (MSE)')
        ax_loss.set_title('Training & Validation Loss Curve', fontweight='bold')
        ax_loss.legend()
        ax_loss.grid(alpha=0.3)
        st.pyplot(fig_loss)
        
        with st.spinner("Generating predictions..."):
            model.eval()
            X_test_t = torch.FloatTensor(X_test)
            X_train_t = torch.FloatTensor(X_train)
            X_val_t = torch.FloatTensor(X_val)
            
            with torch.no_grad():
                y_pred_test = model(X_test_t).numpy().flatten()
                y_pred_train = model(X_train_t).numpy().flatten()
                y_pred_val = model(X_val_t).numpy().flatten()
            
            y_test_actual = np.array([inverse_scale(v, scaler, 4) for v in y_test])
            y_pred_test_actual = np.array([inverse_scale(v, scaler, 4) for v in y_pred_test])
            y_train_actual = np.array([inverse_scale(v, scaler, 4) for v in y_train])
            y_pred_train_actual = np.array([inverse_scale(v, scaler, 4) for v in y_pred_train])
            y_val_actual = np.array([inverse_scale(v, scaler, 4) for v in y_val])
            y_pred_val_actual = np.array([inverse_scale(v, scaler, 4) for v in y_pred_val])
            
            mae = mean_absolute_error(y_test_actual, y_pred_test_actual)
            rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred_test_actual))
            mape_val = np.mean(np.abs((y_test_actual - y_pred_test_actual) / y_test_actual)) * 100
            ss_res = np.sum((y_test_actual - y_pred_test_actual) ** 2)
            ss_tot = np.sum((y_test_actual - np.mean(y_test_actual)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("Model Performance Metrics")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MAE", f"{currency_symbol} {mae:,.2f}")
        c2.metric("RMSE", f"{currency_symbol} {rmse:,.2f}")
        c3.metric("MAPE", f"{mape_val:.2f}%", 
                 delta="Excellent" if mape_val < 1 else ("Good" if mape_val < 3 else "Fair"))
        c4.metric("R-squared", f"{r2:.4f}", delta="Strong" if r2 > 0.7 else "Moderate")
        
        # Future prediction
        with st.spinner(f"Forecasting {future_days} days ahead..."):
            last_sequence = scaled_full[-seq_len:]
            current_seq = torch.FloatTensor(last_sequence).unsqueeze(0)
            
            last_actual_price = y_test_actual[-1]
            daily_changes = np.diff(y_test_actual[-30:]) if len(y_test_actual) >= 30 else np.diff(y_test_actual)
            avg_change = np.mean(daily_changes)
            std_change = np.std(daily_changes)
            
            recent_data = df[features].iloc[-30:]
            avg_hcr = (recent_data['High'] / recent_data['Close']).mean()
            avg_lcr = (recent_data['Low'] / recent_data['Close']).mean()
            avg_ocr = (recent_data['Open'] / recent_data['Close']).mean()
            
            future_preds = []
            model.eval()
            
            with torch.no_grad():
                for i in range(future_days):
                    pred_scaled = model(current_seq).item()
                    pred_actual = inverse_scale(pred_scaled, scaler, 4)
                    
                    blend = min(0.3, i / future_days)
                    trend = last_actual_price + avg_change * (i + 1)
                    corrected = pred_actual * (1 - blend) + trend * blend
                    
                    max_ch = abs(avg_change) * 2 + std_change * 1.5
                    upper = min(last_actual_price + max_ch * (i+1), last_actual_price * 1.1)
                    lower = max(last_actual_price - max_ch * (i+1), last_actual_price * 0.9)
                    
                    final_price = np.clip(corrected, lower, upper)
                    future_preds.append(final_price)
                    
                    sc = (final_price - scaler.data_min_[0]) / (scaler.data_max_[0] - scaler.data_min_[0])
                    new_row = np.zeros((1, 4))
                    new_row[0, 0] = sc
                    new_row[0, 1] = sc * avg_hcr
                    new_row[0, 2] = sc * avg_lcr
                    new_row[0, 3] = sc * avg_ocr
                    
                    last_sequence = np.vstack([last_sequence[1:], new_row])
                    current_seq = torch.FloatTensor(last_sequence).unsqueeze(0)
            
            future_actual = np.array(future_preds)
            last_date = df['Date'].max()
            future_dates_list = get_next_trading_days(last_date, future_days)
        
        # ========== FULL OVERVIEW PLOT ==========
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader(f"Prediction Chart -- {model_type} | {selected_pair}")
        
        all_dates = np.concatenate([
            df['Date'].iloc[seq_len:train_size].values,
            df['Date'].iloc[train_size:train_size+val_size].values,
            df['Date'].iloc[train_size+val_size:].values
        ])
        all_actual = np.concatenate([y_train_actual, y_val_actual, y_test_actual])
        all_pred = np.concatenate([y_pred_train_actual, y_pred_val_actual, y_pred_test_actual])
        
        fig1, ax1 = plt.subplots(figsize=(18, 7))
        apply_plot_style(fig1, ax1)
        
        ax1.plot(all_dates, all_actual, '#1f77b4', label='Actual Rate', linewidth=1.8)
        ax1.plot(all_dates, all_pred, '#ff7f0e', label='Model Prediction', linewidth=1.2, alpha=0.7)
        
        ax1.plot(future_dates_list, future_actual, '#2ca02c', 
                label=f'Future Projection ({future_days} days)',
                linewidth=3, marker='o', markersize=7, markerfacecolor='white', markeredgewidth=2)
        
        future_std = std_change * np.sqrt(np.arange(1, future_days+1))
        ax1.fill_between(future_dates_list,
                         future_actual - future_std,
                         future_actual + future_std,
                         alpha=0.15, color='green', label='Projection Band (+/-1 std)')
        
        test_start_date = df['Date'].iloc[train_size + val_size]
        ax1.axvspan(test_start_date, last_date, alpha=0.08, color='#ff7f0e', label='Test Period')
        ax1.axvline(x=last_date, color='#666', linestyle='--', alpha=0.5, linewidth=1)
        ax1.text(last_date, ax1.get_ylim()[1]*0.95, 'Past | Future', ha='center', fontsize=9, color='#666')
        
        ax1.set_title(f'{model_type} -- {selected_pair} Exchange Rate Prediction\n'
                     f'R-squared: {r2:.4f} | MAPE: {mape_val:.2f}%', fontweight='bold', fontsize=14)
        
        handles, labels = ax1.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax1.legend(by_label.values(), by_label.keys(), loc='upper left', framealpha=0.9)
        ax1.grid(alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{currency_symbol}{x:,.2f}'))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax1.set_ylabel(f'Exchange Rate ({currency_symbol})', fontweight='bold')
        
        fig1.autofmt_xdate()
        st.pyplot(fig1)
        
        # ========== TEST ZOOM ==========
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader(f"Test Data Zoom -- Actual vs Predicted")
        
        st.caption(f"Test Period: {df['Date'].iloc[train_size+val_size].strftime('%d %b %Y')} -- "
                  f"{df['Date'].iloc[-1].strftime('%d %b %Y')} ({len(y_test_actual):,} data points)")
        
        fig_zoom = plot_forex_test_zoom(
            df, train_size, val_size, seq_len,
            y_test_actual, y_pred_test_actual,
            model_type, selected_pair, mape_val, r2, currency_symbol,
            future_dates_list, future_actual
        )
        
        st.pyplot(fig_zoom)
        
        # ========== PREDICTION TABLE ==========
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader(f"Forecast Table -- Next {future_days} Days | {selected_pair}")
        
        pred_data = []
        for i, (date, price) in enumerate(zip(future_dates_list, future_actual)):
            day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}
            day_id = day_names.get(date.weekday(), '')
            
            if i == 0:
                ch_pct = 0
                ch_str = "--"
                pip_change = 0
            else:
                ch_pct = ((price - future_actual[0]) / future_actual[0]) * 100
                ch_str = f"{ch_pct:+.4f}%"
                pip_change = (price - future_actual[0]) / pip_size
            
            pip_str = f"{pip_change:+.0f} pips" if i > 0 else "--"
            
            ch_html = f'<span style="color:#2d4a2d;font-weight:600;">{ch_str}</span>' if ch_pct > 0 else \
                     f'<span style="color:#8a2e2e;font-weight:600;">{ch_str}</span>' if ch_pct < 0 else ch_str
            
            pred_data.append({
                'Day': i+1,
                'Date': date.strftime('%d %b %Y'),
                'Weekday': day_id,
                'Forecast Rate': f"{currency_symbol}{price:,.2f}",
                'Change %': ch_html,
                'Pips': pip_str
            })
        
        pred_df = pd.DataFrame(pred_data)
        st.markdown(
            f"""<div class="prediction-table">{pred_df.to_html(index=False, escape=False)}</div>""",
            unsafe_allow_html=True
        )
        
        # ========== INSIGHTS ==========
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.header("Deep Insights & Analysis")
        
        metrics = {
            'mae': mae,
            'rmse': rmse,
            'mape': mape_val,
            'r2': r2
        }
        
        insights = generate_forex_insights(
            model_type, selected_pair, metrics, indicators, 
            future_actual, future_dates_list, pip_size, currency_symbol
        )
        
        future_change = ((future_actual[-1] - future_actual[0]) / future_actual[0]) * 100
        
        st.subheader("Executive Summary")
        
        emph_col1, emph_col2, emph_col3 = st.columns(3)
        
        with emph_col1:
            st.markdown(
                get_highlight_box(
                    f"{future_change:+.2f}%",
                    f"{future_days}-Day Forecast",
                    "up" if future_change > 0.5 else ("down" if future_change < -0.5 else "neutral")
                ),
                unsafe_allow_html=True
            )
        
        with emph_col2:
            st.markdown(
                get_highlight_box(
                    f"{mape_val:.2f}%",
                    "Error Rate (MAPE)",
                    "up" if mape_val < 1 else ("down" if mape_val > 5 else "neutral")
                ),
                unsafe_allow_html=True
            )
        
        with emph_col3:
            st.markdown(
                get_highlight_box(
                    f"{indicators['volatility_20d']:.3f}%",
                    "Volatility (20-Day)",
                    "up" if indicators['volatility_20d'] < 0.5 else ("down" if indicators['volatility_20d'] > 1 else "neutral")
                ),
                unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.subheader("Detailed Analysis")
        
        for i in range(0, len(insights), 2):
            col1, col2 = st.columns(2)
            with col1:
                ins = insights[i]
                st.markdown(get_insight_card(ins['title'], ins['content'], ins['variant']), unsafe_allow_html=True)
            with col2:
                if i + 1 < len(insights):
                    ins = insights[i+1]
                    st.markdown(get_insight_card(ins['title'], ins['content'], ins['variant']), unsafe_allow_html=True)
        
        # ========== DISCLAIMER ==========
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="note-box">
            <b>Disclaimer:</b> This prediction is generated by a machine learning model and is <b>for informational purposes only</b>. 
            The forex market is highly volatile and influenced by numerous fundamental factors such as interest rates, economic data, 
            and geopolitical events that cannot be predicted by technical models alone.<br><br>
            <b>This is NOT trading advice.</b> Always practice strict risk management 
            (max 1-2% risk per trade), monitor the economic calendar, and consult with a qualified financial professional 
            before making any trading decisions. Forex trading involves substantial risk and is not suitable for all investors.
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        with st.expander("Error Details (for debugging)"):
            import traceback
            st.code(traceback.format_exc())

else:
    # Welcome screen
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to RixterProphet Forex Analytics
        
        A **Deep Learning (LSTM)** based currency exchange rate prediction platform 
        delivering in-depth analysis with actionable insights for forex trading.
        
        #### Key Features:
        - **8 Major Forex Pairs**: USD/IDR, EUR/USD, GBP/USD, and more
        - **2 LSTM Architectures**: Vanilla & Bidirectional
        - **Technical Indicators**: Support/Resistance, MA, Volatility
        - **Forex-Specific Metrics**: Pip movement, spread estimation
        - **Deep Insights**: 5 automated analysis categories
        - **Clear Emphasis**: Key metrics & projection highlights
        - **Professional Visualization**: Interactive charts with projection bands
        """)
    
    with col2:
        st.markdown("""
        #### How to Use:
        
        1. **Select a Forex Pair** (default: USD/IDR)
        2. **Set the Date Range** for historical data
        3. **Choose Model Architecture** (Vanilla/Bidirectional)
        4. **Configure Hyperparameters** (or use defaults)
        5. **Set the Number of Days** to forecast
        6. **Click "Start Forex Analysis"**
        
        ---
        
        #### Available Pairs:
        | Pair | Description |
        |------|-------------|
        | `USD/IDR` | US Dollar - Indonesian Rupiah |
        | `EUR/USD` | Euro - US Dollar |
        | `GBP/USD` | Pound Sterling - USD |
        | `USD/JPY` | US Dollar - Japanese Yen |
        | `AUD/USD` | Australian Dollar - USD |
        | `USD/SGD` | US Dollar - Singapore Dollar |
        | `EUR/JPY` | Euro - Japanese Yen |
        | `GBP/JPY` | Pound Sterling - Yen |
        """)
    
    st.info("""
    **Ready to begin?** Select a forex pair in the left sidebar, configure your parameters, then click **START FOREX ANALYSIS**.
    
    The model will download historical data, train the LSTM, and generate exchange rate predictions with deep insights to support your analysis.
    
    **Tip**: For optimal results, use at least 1-2 years of data and a sequence length of 10-14 days for forex.
    """)
    
    # Quick start cards
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.subheader("Quick Start Examples")
    
    qcol1, qcol2, qcol3 = st.columns(3)
    
    with qcol1:
        st.markdown("""
        <div class="metric-card">
            <h4>USD/IDR Analysis</h4>
            <p>Pair: <b>USD/IDR</b><br>
            Model: Bidirectional LSTM<br>
            Period: 2020-2024<br>
            Seq Length: 14<br>
            Forecast: 14 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with qcol2:
        st.markdown("""
        <div class="metric-card">
            <h4>EUR/USD Analysis</h4>
            <p>Pair: <b>EUR/USD</b><br>
            Model: Vanilla LSTM<br>
            Period: 2021-2024<br>
            Seq Length: 10<br>
            Forecast: 7 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with qcol3:
        st.markdown("""
        <div class="metric-card">
            <h4>USD/JPY Analysis</h4>
            <p>Pair: <b>USD/JPY</b><br>
            Model: Bidirectional LSTM<br>
            Period: 2020-2024<br>
            Seq Length: 20<br>
            Forecast: 21 days</p>
        </div>
        """, unsafe_allow_html=True)
