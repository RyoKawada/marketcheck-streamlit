import altair as alt
import pandas as pd
import yfinance as yf
import streamlit as st

st.title("USA・Japan Stock Price、Exchange Rate View App.")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])

        hist = tkr.history(period=f"{days}d")
        hist.index = hist.index.strftime("%d %B %Y")
        hist = hist[["Close"]]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Name"
        df = pd.concat([df, hist])
    return df

st.sidebar.write("""
# Choose number of days displayed.
""")

days = st.sidebar.slider("day", 1, 50, 25)

# ----- USA -----
st.sidebar.write(f"""
# US Stock Price Last ***{days}*** days.
""")

st.sidebar.write("""
## Choose US stock price range.
""")

usymin, usymax = st.sidebar.slider(
  "stock price range", 0, 300, (80, 280)
)

# ----- Japan -----
st.sidebar.write(f"""
# Japan Stock Price Last ***{days}*** days.
""")

st.sidebar.write("""
## Choose Japan stock price range.
""")

jaymin, jaymax = st.sidebar.slider(
  "stock price range", 0, 50000, (500, 6000)
)

# ----- Exchange Rate -----
st.sidebar.write(f"""
# Exchange Rate Last ***{days}*** days.
""")

st.sidebar.write("""
## Choose exchange rate range.
""")

exymin, exymax = st.sidebar.slider(
  "exchange rate range", 0, 200, (140, 170)
)

us_tickers = {
    "apple"   : "AAPL",
    "facebook": "Meta",
    "amazon"  : "AMZN",
    "google"  : "GOOGL",
    "microsoft"  : "MSFT"
}

ja_tickers = {
    "toyota"  : "7203.T",
    "softbank": "9984.T",
    "ufjbank" : "8306.T",
    "keyence" : "6861.T"
}

exchange = {
    "ドル": "USDJPY=X",
    "ポンド": "GBPJPY=X",
    "元": "CNYJPY=X",
    "ペソ": "PHPJPY=X"
}

df_us = get_data(days, us_tickers)
df_ja = get_data(days, ja_tickers)
df_ex = get_data(days, exchange)


try:
  # ----- USA -----
  us_company = st.multiselect(
    "Choose below options.(US company)",
    list(df_us.index),
    ["apple", "facebook", "amazon", "google", "microsoft"]
  )

  if not us_company:
    st.error("Choose some companies!")
  else:
    data = df_us.loc[us_company].sort_index()
    st.write("### USA Stock Price ###", data)
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["Date"]).rename(
      columns={"value": "US Stock Price"}
    )
    chart = (
      alt.Chart(data)
      .mark_line(opacity=0.8, clip=True)
      .encode(
          x="Date:T",
          y=alt.Y("US Stock Price", scale=alt.Scale(domain=[usymin, usymax])),
          color="Name"
      )
    )
    st.altair_chart(chart, use_container_width=True)

  # ----- Japan -----
  ja_company = st.multiselect(
    "Choose below options.(Japan company)",
    list(df_ja.index),
    ["toyota", "softbank", "ufjbank", "keyence"]
  )

  if not ja_company:
    st.error("Choose some companies!")
  else:
    data = df_ja.loc[ja_company].sort_index()
    st.write("### Japan Stock Price ###", data)
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["Date"]).rename(
      columns={"value": "Japan Stock Price"}
    )
    chart = (
      alt.Chart(data)
      .mark_line(opacity=0.8, clip=True)
      .encode(
          x="Date:T",
          y=alt.Y("Japan Stock Price", scale=alt.Scale(domain=[jaymin, jaymax])),
          color="Name"
      )
    )
    st.altair_chart(chart, use_container_width=True)

  # ----- Exchange Rate -----
  exchange = st.multiselect(
    "Choose below options.(Exchange rate)",
    list(df_ex.index),
    ["ドル", "ポンド"]
  )

  if not exchange:
    st.error("Choose some currency!")
  else:
    data = df_ex.loc[exchange].sort_index()
    st.write("### Exchange Price ###", data)
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["Date"]).rename(
      columns={"value": "Exchange Price"}
    )
    chart = (
      alt.Chart(data)
      .mark_line(opacity=0.8, clip=True)
      .encode(
          x="Date:T",
          y=alt.Y("Exchange Price", scale=alt.Scale(domain=[exymin, exymax])),
          color="Name"
      )
    )
    st.altair_chart(chart, use_container_width=True)
except:
  st.error(
    "Wshat happend! There is an error."
  )