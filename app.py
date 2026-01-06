import streamlit as st
import requests
import pandas as pd
import time

# 1. The API Endpoint (The URL we ask for data)
# We are asking CoinGecko for data on Bitcoin, Ethereum, and Dogecoin in USD.
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
st.write("Fetching live data from CoinGecko API...")

# 2. Create a generic placeholder
# This allows us to update the table without refreshing the whole page
data_placeholder = st.empty()

# 3. The Loop (To simulate "Live" updates)
if st.button("Start Live Feed"):
    st.info("Tracking prices... (Stop by pressing the button again or refreshing)")
    
    while True:
        try:
            # --- THE API CALL ---
            response = requests.get(URL, params=PARAMS)
            data = response.json()  # Convert the response to JSON (Python List/Dict)
            
            # Extract specific data we care about
            crypto_list = []
            for coin in data:
                crypto_list.append({
                    "Name": coin['name'],
                    "Symbol": coin['symbol'].upper(),
                    "Price ($)": coin['current_price'],
                    "24h Change (%)": coin['price_change_percentage_24h'],
                    "Market Cap": coin['market_cap']
                })
            
            # Convert to DataFrame for a nice table
            df = pd.DataFrame(crypto_list)
            
            # Display it in the placeholder
            with data_placeholder.container():
                # Display the Table
                st.dataframe(df.style.format({
                    "Price ($)": "{:.2f}",
                    "24h Change (%)": "{:.2f}",
                    "Market Cap": "{:,.0f}"
                }))
                
                # Bonus: Add a visual Metric for Bitcoin
                btc = next(item for item in crypto_list if item["Name"] == "Bitcoin")
                st.metric(
                    label="Bitcoin Price", 
                    value=f"${btc['Price ($)']}", 
                    delta=f"{btc['24h Change (%)']}%"
                )
                # --- ALGO TRADING ALERT SYSTEM ---
                target_price = 95000  # Set this to a price close to current value
                
                if btc['Price ($)'] < target_price:
                    st.error(f"📉 ALERT: Bitcoin is below ${target_price}! CONSIDER BUYING.")
                else:
                    st.success(f"📈 Bitcoin is healthy (Above ${target_price}). Holding...")
                
                st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")

            # Wait for 10 seconds before fetching again (to avoid banning)
            time.sleep(10)
            
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            break
else:
    st.write("Click the button to start tracking.")