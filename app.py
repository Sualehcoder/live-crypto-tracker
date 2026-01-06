import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# 1. API Setup
URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,dogecoin,solana,ripple",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": "false"
}

st.title("📈 Live Crypto Dashboard")
st.write("Tracking real-time prices...")

# Create empty slots for the Table and the Chart
table_placeholder = st.empty()
chart_placeholder = st.empty()

# Initialize a list to save the history of Bitcoin prices
# We need this to draw the line!
bitcoin_history = []

if st.button("Start Live Feed"):
    st.info("Fetching data... (This chart will grow every 10 seconds)")
    
    while True:
        try:
            # --- API CALL ---
            response = requests.get(URL, params=PARAMS)
            data = response.json()
            
            # Process Data
            crypto_list = []
            for coin in data:
                crypto_list.append({
                    "Name": coin['name'],
                    "Price ($)": coin['current_price'],
                    "24h Change (%)": coin['price_change_percentage_24h']
                })
            
            df = pd.DataFrame(crypto_list)
            
            # --- 4. CHARTING ENGINE ---
            # Find Bitcoin's current price
            btc_data = next(item for item in crypto_list if item["Name"] == "Bitcoin")
            current_price = btc_data["Price ($)"]
            
            # Add to history with the current time
            now = datetime.now().strftime("%H:%M:%S")
            bitcoin_history.append({"Time": now, "Bitcoin Price ($)": current_price})
            
            # Create a dataframe specifically for the chart
            chart_data = pd.DataFrame(bitcoin_history)
            
            # --- DISPLAY UPDATES ---
            
            # 1. Update the Table
            table_placeholder.dataframe(df.style.format({"Price ($)": "{:.2f}"}))
            
            # 2. Update the Chart
            # We tell Streamlit to chart the 'Bitcoin Price' column
            if not chart_data.empty:
                chart_placeholder.line_chart(
                    chart_data.set_index("Time")["Bitcoin Price ($)"]
                )
            
            # 3. Alert Logic (Your Algo Trader)
            if current_price < 95000:
                st.toast(f"📉 ALERT: BTC Drop! ${current_price}", icon="⚠️")
            
            time.sleep(10) # Update every 10s
            
        except Exception as e:
            st.error(f"Error: {e}")
            break
else:
    st.write("Click to start.")