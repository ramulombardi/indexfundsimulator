import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("📈Index Fund Simulator")
st.subheader("📊Average Annual Returns (Last 20 Years)")
st.markdown("##### Extracting data...")

# Defino tickers para simulacion
tickers = {
    "S&P 500 (SPY)": "SPY",
    "NASDAQ 100 (QQQ)": "QQQ",
    "Dow Jones (DIA)": "DIA",
    "Russell 2000 (IWM)": "IWM",
    "Total US Market (VTI)": "VTI",
    "MSCI Emerging Markets (EEM)": "EEM",
    "MSCI Developed Markets (VEA)": "VEA",
    "Global Market (VT)": "VT",
    "Technology Sector (XLK)": "XLK",
    "Healthcare Sector (XLV)": "XLV"
}



#
end_date = datetime.today()
start_date = end_date - timedelta(days=20 * 365)

returns_data = []
avg_returns = {} #


for name, symbol in tickers.items():

    data = yf.download(symbol, start=start_date, end=end_date, interval='1d', progress=False)

    if 'Close' in data.columns:
        prices = data['Close']
        prices = prices.resample('Y').last()

        # Calculo de retornos anuales
        annual_returns = prices.pct_change().dropna()
        avg_return = float(annual_returns.mean() * 100) #Float

        returns_data.append({
            "Index": name,
            "Average Annual Return (%)": round(avg_return, 2)
        })

        avg_returns[symbol] = avg_return
    else:
        st.warning(f"❌'Close' not found for {symbol}")


# Tabla
if returns_data:
    returns_df = pd.DataFrame(returns_data)
    st.success("✅Data correctly extracted from Yahoo Finance API")
    st.dataframe(returns_df)
else:
    st.error("No return could be calculated.")
    st.stop()


# Compound Interest Calculator
st.subheader("🔢Compound Interest Calculator")

# Inputs
selected_index = st.selectbox("Select an index", options=list(avg_returns.keys()))
initial_amount = st.number_input("Initial amount (USD)", min_value=0.0, value=1000.0, step=100.0)
years = st.slider("Years to invest", min_value=1, max_value=50, value=20)

rate = avg_returns[selected_index] / 100

final_amount = initial_amount * (1 + rate) ** years

# Resultado
st.markdown(f"### 💰Estimated final amount **USD ${final_amount:,.2f}**")
st.caption(f"*Based on an average annual rate of {avg_returns[selected_index]:.2f}% {selected_index}*")


st.markdown("""
---
<p style='text-align: center; color: gray;'>
    Made by Ramu🧑🏻‍💻
</p>
""", unsafe_allow_html=True)