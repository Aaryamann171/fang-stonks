import streamlit as st
import pandas as pd
import altair as alt
import yfinance as yf
import urllib

@st.cache
def get_UN_data(tickers):
    data = []
    # data = [['tom', 10, 9, 12, 14, 42, 98], ['nick', 15, 89, 9, 21, 2, 4], ['juli', 14, 20, 12, 44, 22, 90]] 
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period="7d")
        stock_data = hist['Close'].tolist()
        stock_data.insert(0, company)
        data.append(stock_data)

    # Create the pandas DataFrame 
    df = pd.DataFrame(data, columns = ['Name', '2018-10-01', '2018-11-01', '2018-12-01', '2018-13-01', '2018-14-01', '2018-15-01', '2018-16-01']) 
    return df.set_index('Name')

try:
    tickers = {'apple':'AAPL','facebook':'FB'}
    df = get_UN_data(tickers)
    countries = st.multiselect(
        "Choose countries", list(df.index), ["apple", "facebook"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        st.write("### Stock Prices", data)

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "day", "value": "Stock Prices"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="day:T",
                y=alt.Y("Stock Price:Q", stack=None),
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
