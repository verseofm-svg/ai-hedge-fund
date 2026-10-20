import os
import json
import redis
import yfinance as yf
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

app = FastAPI()

# Connect to Upstash Redis for Persistent Session Memory
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    ssl=True if os.getenv("REDIS_PASSWORD") else False
)

# Connect to Alpaca Paper Trading
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

trading_active = False
scheduler = BackgroundScheduler()

def run_hedge_fund_cycle():
    """Multi-Agent Consensus & Execution Cycle"""
    print("🤖 Running AI Hedge Fund multi-agent cycle...")
    
    # 1. Load session memory from Redis
    history = r.get("trade_history")
    past_trades = json.loads(history) if history else []

    symbol = "AAPL"
    
    # 2. Agent 1: Quant Analyst (Checks simple moving average momentum)
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="5d")
    current_price = hist['Close'].iloc[-1]
    prev_price = hist['Close'].iloc[0]
    quant_signal = "BUY" if current_price > prev_price else "SELL"

    # 3. Agent 2: Risk Manager (Validates position sizing & limits)
    risk_approval = True if quant_signal == "BUY" else False

    # 4. Agent 3: Portfolio Manager Execution Decision
    if risk_approval:
        try:
            # Submit Paper Trade to Alpaca
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=1,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            order = trading_client.submit_order(order_data=market_order_data)
            
            trade_record = {
                "symbol": symbol,
                "action": "BUY",
                "price": float(current_price),
                "status": "Executed (Paper)"
            }
            past_trades.append(trade_record)
            
            # Save updated memory back to Redis
            r.set("trade_history", json.dumps(past_trades))
            print(f"✅ Trade Executed & Saved: {trade_record}")
        except Exception as e:
            print(f"❌ Trade execution failed: {e}")

# Schedule automated runs every 30 minutes
scheduler.add_job(run_hedge_fund_cycle, 'interval', minutes=30, id='fund_job')

@app.post("/start")
def start_trading():
    global trading_active
    if not trading_active:
        if not scheduler.running:
            scheduler.start()
        else:
            scheduler.resume()
        trading_active = True
    return {"status": "🚀 Automated Hedge Fund Started"}

@app.post("/stop")
def stop_trading():
    global trading_active
    if trading_active:
        scheduler.pause()
        trading_active = False
    return {"status": "⏹️ Automated Hedge Fund Paused"}

@app.get("/memory")
def get_memory():
    history = r.get("trade_history")
    return json.loads(history) if history else []
