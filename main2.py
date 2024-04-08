import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt

tickers = {
    "apple":"AAPL",
    "disney":"DIS",
    "Coca-Cola":"KO",
    "NIKE":"NKE",
    "Rani Therapeutics":"RANI",
    "Unity":"U",
}

st.title("鈴木の株価")
st.balloons()
st.sidebar.write("表示日数選択")

days = st.sidebar.slider("日数",1,365,30)

st.write(f"過去{days}日間の株価")

@st.cache_data
def get_data(days,tickers):
    df = pd.DataFrame()

    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f"{days}d")
        hist.index = hist.index.strftime("%d %B %y")
        hist = hist[["Close"]]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"
        df = pd.concat([df, hist])
    return df

st.sidebar.write("株価の範囲指定")
ymin, ymax = st.sidebar.slider(
    "範囲を指定してください",0.0,500.0,(0.0, 500.0)
)

df = get_data(days, tickers)

companies = st.multiselect(
    "会社名を選択してください",list(df.index),["Unity"],
)

data = df.loc[companies]

st.write("株価",data.sort_index())
data = data.T.reset_index()
data = pd.melt(data, id_vars=["Date"]).rename(columns={"value":"Stock Prices"})

chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices:Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
        color="Name:N"
    )
)

st.altair_chart(chart, use_container_width = True)