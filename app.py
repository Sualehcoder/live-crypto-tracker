import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import streamlit as st
# DEBUG: Print all secret keys to the screen
st.write("Available Keys:", st.secrets.keys())
import alerts  # <--- IMPORT YOUR NEW FILE

# --- CONFIGURATION ---
URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,dogecoin,solana,ripple",
    "order": "market_cap_desc",
    "per_page": 10,
    "sparkline": "false"
}

# STATE MANAGEMENT (To track when we last sent an email)
if "last_alert_time" not in st.session_state:
    st.session_state["last_alert_time"] = 0

st.title("📈 Live Crypto Dashboard + Alerts")

# --- CREDIT SECTION ---
st.sidebar.title("Configuration")
st.sidebar.info("Developed by Sualeh")

# ----------------------

# ... rest of your code (inputs, buttons, etc.)

# Inputs for your Alert
target_price = st.number_input("Set Bitcoin Buy Price ($)", value=95000)

if st.button("Start Live Tracking"):
    st.info("Tracking started...")
    placeholder = st.empty()
    
    while True:
        try:
            response = requests.get(URL, params=PARAMS)
            data = response.json()
            
            # Find Bitcoin
            btc = next(item for item in data if item["name"] == "Bitcoin")
            current_price = btc["current_price"]
            
            # --- ALERT LOGIC ---
            if current_price < target_price:
                # Check if we sent an email recently (e.g., in the last 3600 seconds/1 hour)
                current_time = time.time()
                if current_time - st.session_state["last_alert_time"] > 3600:
                    
                    st.warning(f"📉 Price Drop Detected! Sending Email...")
                    
                    # Call the function from alerts.py
                    success = alerts.send_email_alert("Bitcoin", current_price)
                    
                    if success:
                        st.success("✅ Email Sent successfully!")
                        st.session_state["last_alert_time"] = current_time
                else:
                    st.caption("⚠️ Price is low, but email already sent recently (Cooldown active).")

            # Update UI
            with placeholder.container():
                st.metric(label="Bitcoin Price", value=f"${current_price}", delta=f"{btc['price_change_percentage_24h']}%")
                st.dataframe(pd.DataFrame(data)[['name', 'current_price', 'price_change_percentage_24h']])
            
            time.sleep(10)

        except Exception as e:
            st.error(f"Error: {e}")
            break