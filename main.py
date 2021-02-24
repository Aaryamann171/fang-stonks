import streamlit as st
import pandas as pd
import altair as alt
import yfinance as yf
import urllib

st.title("FANG Stock Price")
st.write("""
### Stock prices for Various FANG companies over the last **20 days** 
""")

@st.cache
def get_data(tickers):
    data = []
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period="20d")
        stock_data = hist['Close'].tolist()
        stock_data = [round(x, 2) for x in stock_data]
        stock_data.insert(0, company)
        data.append(stock_data)
    c = [x for x in range(1,21)]
    c.insert(0, 'Name')
    df = pd.DataFrame(data, columns = c) 
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
            columns={"index": "days", "value": "Stock Prices (USD)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="days:O",
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
