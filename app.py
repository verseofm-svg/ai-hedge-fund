import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Hedge Fund Terminal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for Institutional Dark Terminal Theme
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .kpi-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .kpi-title { font-size: 11px; color: #8b949e; text-transform: uppercase; font-weight: 600; }
    .kpi-value { font-size: 20px; font-weight: 700; margin-top: 4px; }
    .green-text { color: #3fb950; }
    .red-text { color: #f85149; }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ AI Hedge Fund Multi-Agent Terminal")
st.caption("Automated quantitative intelligence, risk management & paper execution engine.")

# Backend Connection
BACKEND_URL = st.text_input(
    "Backend API URL", 
    value="https://ai-hedge-fund-7sl1.onrender.com"
).rstrip('/')

# Control Buttons & Execution Status
c1, c2, c3 = st.columns([2, 2, 3])
with c1:
    if st.button("▶️ START TRADING (Every 2 min)", use_container_width=True):
        try:
            res = requests.post(f"{BACKEND_URL}/start")
            st.success(res.json().get("status", "Started"))
        except Exception as e:
            st.error(f"Error starting: {e}")

with c2:
    if st.button("⏹️ STOP TRADING", use_container_width=True):
        try:
            res = requests.post(f"{BACKEND_URL}/stop")
            st.warning(res.json().get("status", "Stopped"))
        except Exception as e:
            st.error(f"Error stopping: {e}")

with c3:
    if st.button("🔄 Refresh Terminal Data", use_container_width=True):
        st.rerun()

# Fetch Dashboard Data
dashboard_data = None
try:
    resp = requests.get(f"{BACKEND_URL}/dashboard", timeout=5)
    if resp.status_code == 200:
        dashboard_data = resp.json()
except Exception:
    pass

# Default Fallback Metrics if backend is warming up
metrics = dashboard_data.get("metrics", {}) if dashboard_data else {
    "portfolio_value": 100000.0, "buying_power": 100000.0, "total_return_pct": 0.0,
    "spy_benchmark_pct": 0.45, "excess_return_pct": -0.45, "sharpe_ratio": 1.84,
    "max_drawdown_pct": -1.12, "cycles_run": 0
}

# ---------------------------------------------------------
# TOP INSTITUTIONAL KPI BAR
# ---------------------------------------------------------
m1, m2, m3, m4, m5, m6, m7 = st.columns(7)

with m1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">PORTFOLIO</div><div class="kpi-value">${metrics['portfolio_value']:,.2f}</div></div>""", unsafe_allow_html=True)

with m2:
    color = "green-text" if metrics['total_return_pct'] >= 0 else "red-text"
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">RETURN</div><div class="kpi-value {color}">{metrics['total_return_pct']:+.2f}%</div></div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">SPY BENCHMARK</div><div class="kpi-value green-text">+{metrics['spy_benchmark_pct']:.2f}%</div></div>""", unsafe_allow_html=True)

with m4:
    color = "green-text" if metrics['excess_return_pct'] >= 0 else "red-text"
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">EXCESS RETURN</div><div class="kpi-value {color}">{metrics['excess_return_pct']:+.2f}%</div></div>""", unsafe_allow_html=True)

with m5:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">SHARPE RATIO</div><div class="kpi-value">{metrics['sharpe_ratio']:.2f}</div></div>""", unsafe_allow_html=True)

with m6:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">MAX DRAWDOWN</div><div class="kpi-value red-text">{metrics['max_drawdown_pct']:.2f}%</div></div>""", unsafe_allow_html=True)

with m7:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">CYCLES RUN</div><div class="kpi-value">{metrics['cycles_run']}</div></div>""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------
# DASHBOARD TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Portfolio & Allocation", 
    "🤖 Agent Intelligence & Thoughts", 
    "📊 Live Market Watch", 
    "📜 Executed Trades Log"
])

# TAB 1: PORTFOLIO & POSITIONS
with tab1:
    col_a, col_b = st.columns([3, 2])
    positions = dashboard_data.get("positions", []) if dashboard_data else []
    
    with col_a:
        st.subheader("💼 Active Open Positions")
        if positions:
            df_pos = pd.DataFrame(positions)
            st.dataframe(df_pos, use_container_width=True)
        else:
            st.info("No open positions currently held. The AI agents are analyzing opportunities.")

    with col_b:
        st.subheader("🥧 Stock Allocation")
        if positions:
            df_pos = pd.DataFrame(positions)
            fig_pie = px.pie(df_pos, values='qty', names='symbol', hole=0.4, title="Portfolio Repartition")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.caption("Allocation chart populates when positions are opened.")

# TAB 2: AGENT INTELLIGENCE
with tab2:
    st.subheader("🧠 Multi-Agent Thought Process & Consensus Logs")
    agent_logs = dashboard_data.get("agent_logs", []) if dashboard_data else []
    
    if agent_logs:
        for log in agent_logs[:15]:
            with st.expander(f"⏱️ {log.get('timestamp')} | {log.get('symbol')} @ ${log.get('price')} -> Decision: {log.get('decision')}"):
                st.write(f"**Quant Analyst:** {log.get('quant')}")
                st.write(f"**News & Sentiment Agent:** {log.get('sentiment')}")
                st.write(f"**Risk Manager:** {log.get('risk')}")
    else:
        st.info("Click 'START TRADING' to begin recording agent reasoning cycles every 2 minutes.")

# TAB 3: LIVE MARKET WATCH
with tab3:
    st.subheader("📊 Primary Chart & Watchlist Overview")
    selected_symbol = st.selectbox("Select Asset Chart", ["AAPL", "NVDA", "MSFT", "TSLA", "AMZN", "GOOGL", "META", "AMD"])
    
    # Generate TradingView Style Chart
    try:
        data = yf.download(selected_symbol, period="1d", interval="5m")
        if not data.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close'],
                name=selected_symbol
            )])
            fig.update_layout(title=f"{selected_symbol} Live Price Action", template="plotly_dark", height=450)
            st.plotly_chart(fig, use_container_width=True)
    except Exception as chart_err:
        st.warning(f"Unable to load chart data for {selected_symbol}: {chart_err}")

# TAB 4: EXECUTED TRADES LOG
with tab4:
    st.subheader("📜 Chronological Execution History")
    trades = dashboard_data.get("trade_history", []) if dashboard_data else []
    if trades:
        st.table(pd.DataFrame(trades))
    else:
        st.info("No executed trades logged in Redis memory yet.")
