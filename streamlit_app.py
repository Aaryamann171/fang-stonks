import streamlit as st
import pandas as pd
import altair as alt
import yfinance as yf
import urllib
from datetime import datetime, timedelta
from currency_converter import CurrencyConverter

st.title("FANG Stock Prices")
st.write(f"""
#### developed by [aaryamann171](https://github.com/aaryamann171)
""")

# currency selector
st.sidebar.write("""
## Select the Currency
""")
c = CurrencyConverter()
currency_options = ('USD', 'INR', 'EUR', 'GBP', 'CAD')
currency_choice = st.sidebar.selectbox("Currency", currency_options, index=0)

# get exchange rate 
exchange_rate = round(c.convert(1, 'USD', currency_choice), 2)
st.sidebar.write(f"""
Exchange Rate (USD -> {currency_choice}): **{exchange_rate}**
""")

# past `x` days slider and display
st.sidebar.write("""
## Select the number of days
""")
days_to_subtract = st.sidebar.slider("Days", 1, 50, 20)
st.write(f"""
### Stock prices for Various FANG companies over the last **{days_to_subtract} days** 
""")

@st.cache
def get_data(tickers):
    global days_to_subtract
    global exchange_rate
    data = []
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days_to_subtract}d")
        dates = list(hist.index)
        stock_prices = hist['Close'].tolist()
        stock_prices_converted = [round(x * exchange_rate, 2) for x in stock_prices]
        stock_prices_converted.insert(0, company)
        data.append(stock_prices_converted)
    cols = [d.strftime("%d %B %Y") for d in dates]
    cols.insert(0, 'Name')
    df = pd.DataFrame(data, columns=cols) 
    return df.set_index('Name')

try:
    tickers = {'apple':'AAPL', 'facebook':'FB', 'google': 'GOOGL', 'microsoft': 'MSFT', 'netflix': 'NFLX', 'amazon':'AMZN'}
    df = get_data(tickers)
    companies = st.multiselect(
        "Choose companies", list(df.index), ["facebook", "amazon", "netflix", "google"]
    )
    if not companies:
        st.error("Please select at least one country.")
    else:
        data = df.loc[companies]
        st.write(f"### Stock Prices ({currency_choice})", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "Date", "value": f"Stock Prices ({currency_choice})"}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8)
            .encode(
                x="Date:T",
                y=alt.Y(f"Stock Prices ({currency_choice}):Q", stack=None),
                color="Name:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)

except:
    st.error(
        """
        **OOPS! Something went wrong.** :(
    """
    )
