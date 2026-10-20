import streamlit as st
import requests

st.set_page_config(page_title="AI Hedge Fund", page_icon="🏛️", layout="centered")

st.title("🏛️ AI Hedge Fund Control Center")
st.markdown("Automated multi-agent trading team managed from your iOS device.")

# Enter your deployed backend URL here later
BACKEND_URL = st.text_input("Backend API URL", value="https://your-render-backend-url.onrender.com")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ START TRADING", use_container_width=True):
        try:
            res = requests.post(f"{BACKEND_URL}/start")
            st.success(res.json().get("status", "Started"))
        except Exception as e:
            st.error(f"Connection error: {e}")

with col2:
    if st.button("⏹️ STOP TRADING", use_container_width=True):
        try:
            res = requests.post(f"{BACKEND_URL}/stop")
            st.warning(res.json().get("status", "Stopped"))
        except Exception as e:
            st.error(f"Connection error: {e}")

st.divider()

st.subheader("🧠 Session Memory & Live Execution Log")
if st.button("🔄 Refresh Memory"):
    try:
        response = requests.get(f"{BACKEND_URL}/memory")
        if response.status_code == 200:
            trades = response.json()
            if trades:
                st.table(trades)
            else:
                st.info("No trades executed yet during this session.")
        else:
            st.error("Failed to fetch memory from backend.")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")
