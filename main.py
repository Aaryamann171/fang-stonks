import streamlit as st
import pandas as pd
import altair as alt
import yfinance as yf
import urllib
from datetime import datetime, timedelta

st.title("FANG Stock Price")

st.sidebar.write("""
## Select the number of days
""")
# days_to_subtract = 20
days_to_subtract = st.sidebar.slider("Days", 1, 50, 20)

st.write(f"""
### Stock prices for Various FANG companies over the last **{days_to_subtract} days** 
""")

@st.cache
def get_data(tickers):
    global days_to_subtract
    data = []
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days_to_subtract}d")
        dates = list(hist.index)
        stock_data = hist['Close'].tolist()
        stock_data = [round(x, 2) for x in stock_data]
        stock_data.insert(0, company)
        data.append(stock_data)
    c = [x.strftime("%d %B %Y") for x in dates]
    c.insert(0, 'Name')
    df = pd.DataFrame(data, columns=c) 
    return df.set_index('Name')

try:
    tickers = {'apple':'AAPL', 'facebook':'FB', 'google': 'GOOGL', 'microsoft': 'MSFT', 'netflix': 'NFLX', 'amazon':'AMZN'}
    df = get_data(tickers)
    companies = st.multiselect(
        "Choose companies", list(df.index), ["google", "amazon", "facebook"]
    )
    if not companies:
        st.error("Please select at least one country.")
    else:
        data = df.loc[companies]
        st.write("### Stock Prices (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "Date", "value": "Stock Prices (USD)"}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8)
            .encode(
                x="Date:O",
                y=alt.Y("Stock Prices (USD):Q", stack=None),
                color="Name:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)

except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
