# 📈 Live Crypto Price Tracker & Algo-Trader

A real-time financial dashboard that tracks live cryptocurrency prices, visualizes market trends, and simulates algorithmic trading alerts. Built with Python and Streamlit.

## 🚀 Features
- **Real-Time Data:** Fetches live market data (Price, Market Cap, 24h Change) via the [CoinGecko API](https://www.coingecko.com/en/api).
- **Live Charting:** Dynamic line chart that updates every 10 seconds to visualize price trends (Time Series Data).
- **Algo Trading Alerts:** Integrated logic that triggers a visual alert if Bitcoin drops below a specific threshold (Simulated Buy Signal).
- **Auto-Refresh:** Dashboard updates automatically without requiring a page reload.

## 🛠️ Tech Stack
- **Python:** Core logic and data processing.
- **Streamlit:** Frontend UI and real-time rendering.
- **Pandas:** Data manipulation and DataFrame management.
- **Requests:** Handling API GET requests to fetch JSON data.

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/live-crypto-tracker.git](https://github.com/YOUR_USERNAME/live-crypto-tracker.git)
   cd live-crypto-tracker