import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="QUANT-AI Hedge Fund",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Render the elite TradingView / Bloomberg Terminal UI directly
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QUANT-AI Hedge Fund Terminal</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: #0d1117; color: #c9d1d9; padding: 15px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #161b22; padding: 12px 20px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 15px; }
        .logo { font-weight: 800; font-size: 15px; color: #58a6ff; display: flex; align-items: center; gap: 8px; }
        .controls { display: flex; gap: 10px; align-items: center; }
        input[type="text"] { background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 12px; border-radius: 6px; font-size: 13px; width: 280px; }
        button { padding: 6px 14px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; font-size: 12px; }
        .btn-start { background: #238636; color: white; }
        .btn-stop { background: #da3633; color: white; }
        .status-pill { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; background: #21262d; color: #8b949e; }
        .status-active { background: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid #238636; }
        
        .kpi-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-bottom: 15px; }
        .kpi-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; text-align: center; }
        .kpi-title { font-size: 10px; color: #8b949e; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
        .kpi-value { font-size: 18px; font-weight: 700; margin-top: 4px; }
        .green { color: #3fb950; }
        .red { color: #f85149; }

        .tabs { display: flex; gap: 5px; background: #161b22; padding: 6px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 15px; }
        .tab { padding: 8px 16px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; color: #8b949e; background: transparent; border: none; }
        .tab.active { background: #21262d; color: #58a6ff; border: 1px solid #30363d; }
        
        .panel { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; display: none; }
        .panel.active { display: block; }
        .panel-title { font-size: 14px; font-weight: 700; margin-bottom: 10px; color: #e6edf3; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #30363d; }
        th { color: #8b949e; font-weight: 600; }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo">🏛️ QUANT-AI <span style="font-weight:400; color:#8b949e; font-size:12px;">HEDGE FUND v3.2</span></div>
        <div class="controls">
            <input type="text" id="backendUrl" value="https://ai-hedge-fund-7sl1.onrender.com" />
            <button class="btn-start" onclick="startTrading()">▶ START</button>
            <button class="btn-stop" onclick="stopTrading()">⏹ STOP</button>
            <div id="statusIndicator" class="status-pill">STOPPED</div>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-title">Portfolio</div><div class="kpi-value" id="kpiPortfolio">$100,000</div></div>
        <div class="kpi-card"><div class="kpi-title">Return</div><div class="kpi-value green" id="kpiReturn">+0.00%</div></div>
        <div class="kpi-card"><div class="kpi-title">SPY Benchmark</div><div class="kpi-value green">+0.45%</div></div>
        <div class="kpi-card"><div class="kpi-title">Excess Return</div><div class="kpi-value red" id="kpiExcess">-0.45%</div></div>
        <div class="kpi-card"><div class="kpi-title">Sharpe Ratio</div><div class="kpi-value">1.84</div></div>
        <div class="kpi-card"><div class="kpi-title">Max Drawdown</div><div class="kpi-value red">-1.12%</div></div>
    </div>

    <div class="tabs">
        <button class="tab active" onclick="switchTab(0)">📈 Portfolio & Equity Curve</button>
        <button class="tab" onclick="switchTab(1)">🤖 Agent Intelligence & Thoughts</button>
        <button class="tab" onclick="switchTab(2)">📊 Live Market Watch</button>
        <button class="tab" onclick="switchTab(3)">📜 Executed Trades Log</button>
    </div>

    <div class="panel active" id="panel0">
        <div class="panel-title">Equity Curve Performance vs SPY Benchmark</div>
        <div style="height: 320px;"><canvas id="equityChart"></canvas></div>
    </div>

    <div class="panel" id="panel1">
        <div class="panel-title">Multi-Agent Consensus & Reasoning Log</div>
        <div id="agentLogsContainer" style="max-height: 320px; overflow-y: auto;">Loading agent thoughts...</div>
    </div>

    <div class="panel" id="panel2">
        <div class="panel-title">Live Market Watchlist & Asset Grid</div>
        <p style="color: #8b949e; font-size: 13px;">Monitoring top tier tech equities (AAPL, NVDA, MSFT, TSLA, GOOGL, AMZN, META, AMD).</p>
    </div>

    <div class="panel" id="panel3">
        <div class="panel-title">Chronological Execution History</div>
        <div id="tradesContainer">No trades executed yet.</div>
    </div>

    <script>
        function switchTab(index) {
            document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === index));
            document.querySelectorAll('.panel').forEach((p, i) => p.classList.toggle('active', i === index));
        }

        const ctx = document.getElementById('equityChart').getContext('2d');
        const equityChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Oct 1', 'Oct 4', 'Oct 8', 'Oct 12', 'Oct 15', 'Oct 18', 'Oct 20'],
                datasets: [
                    { label: 'Fund Growth', data: [100000, 101200, 103500, 102000, 105900, 104100, 104518], borderColor: '#3fb950', backgroundColor: 'rgba(63,185,80,0.1)', fill: true, tension: 0.3 },
                    { label: 'SPY Baseline', data: [100000, 100800, 102000, 101100, 103200, 103900, 104500], borderColor: '#58a6ff', borderDash: [5,5], tension: 0.3 }
                ]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#c9d1d9' } } }, scales: { x: { grid: { color: '#21262d' } }, y: { grid: { color: '#21262d' } } } }
        });

        async function startTrading() {
            const url = document.getElementById('backendUrl').value.replace(/\/$/, '');
            try {
                let res = await fetch(url + '/start', { method: 'POST' });
                let data = await res.json();
                document.getElementById('statusIndicator').innerText = "ACTIVE";
                document.getElementById('statusIndicator').className = "status-pill status-active";
            } catch(e) { alert("Connection error"); }
        }

        async function stopTrading() {
            const url = document.getElementById('backendUrl').value.replace(/\/$/, '');
            try {
                let res = await fetch(url + '/stop', { method: 'POST' });
                document.getElementById('statusIndicator').innerText = "STOPPED";
                document.getElementById('statusIndicator').className = "status-pill";
            } catch(e) { alert("Connection error"); }
        }

        async function fetchData() {
            const url = document.getElementById('backendUrl').value.replace(/\/$/, '');
            try {
                let res = await fetch(url + '/dashboard');
                if(res.ok) {
                    let d = await res.json();
                    document.getElementById('kpiPortfolio').innerText = '$' + d.metrics.portfolio_value.toLocaleString();
                    document.getElementById('kpiReturn').innerText = (d.metrics.total_return_pct >= 0 ? '+' : '') + d.metrics.total_return_pct.toFixed(2) + '%';
                    
                    if(d.agent_logs && d.agent_logs.length > 0) {
                        let html = '<table><tr><th>Time</th><th>Symbol</th><th>Quant Consensus</th><th>Sentiment</th><th>Decision</th></tr>';
                        d.agent_logs.forEach(l => {
                            html += `<tr><td>${l.timestamp}</td><td><b>${l.symbol}</b></td><td>${l.quant}</td><td>${l.sentiment}</td><td style="color:#3fb950;">${l.decision}</td></tr>`;
                        });
                        html += '</table>';
                        document.getElementById('agentLogsContainer').innerHTML = html;
                    }
                    
                    if(d.trade_history && d.trade_history.length > 0) {
                        let thtml = '<table><tr><th>Time</th><th>Symbol</th><th>Action</th><th>Price</th><th>Status</th></tr>';
                        d.trade_history.forEach(t => {
                            thtml += `<tr><td>${t.timestamp || 'Live'}</td><td><b>${t.symbol}</b></td><td style="color:#3fb950;">${t.action}</td><td>$${t.price}</td><td>${t.status}</td></tr>`;
                        });
                        thtml += '</table>';
                        document.getElementById('tradesContainer').innerHTML = thtml;
                    }
                }
            } catch(e) {}
        }
        setInterval(fetchData, 5000);
        fetchData();
    </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)
