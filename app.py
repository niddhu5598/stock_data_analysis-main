import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='stock data analysis')
st.sidebar.header("Stock Data Analysis")
st.sidebar.image("up.png",width=100)

# to run program, run on terminal
# 1st step:
# ..\Scripts\activate
# 2nd step:
# streamlit run app.py
# In case of an error, ensure the folder open is:-
# C:\Users\HP\py-venvs\stocks\stock_data_analysis-main

@st.cache
def load_data():
    return pd.read_csv('data/NIFTY50_all.csv',parse_dates=['Date'])

def home(title):
    df = load_data()
    st.title("Stock data Analysis")
    st.image('image.png',width=400)
    st.write(" ")
    st.header("Raw dataset")
    st.write(" ")
    st.write(df.head(10))
    st.markdown("<hr>", unsafe_allow_html= True)
    col1, col2 = st.beta_columns(2)
    col1.subheader("Number of Rows:")
    col1.write(df.shape[0])
    col2.subheader("Number of Columns:")
    col2.write(df.shape[1])
    st.markdown("<hr>", unsafe_allow_html= True)
    st.write(" ")
    st.header("Dataset Summary")
    st.write(" ")
    st.write(df.describe())

    st.header("Columns description")
    for i in df.columns:
        st.subheader(i)
        col1, col2 = st.beta_columns(2)
        col1.caption("Unique Values")
        col1.write(len(df[i].unique()))
        col2.caption("Type of Data")
        col2.write("String of Characters" if type(df[i].iloc[0]) is str else "Numerical")
        st.markdown("<hr>",unsafe_allow_html = True)


def page1(title):
    df = load_data()
    st.title(title)
    stock = st.sidebar.selectbox("Choose a stock:-", list(df.Symbol.unique()))
    sd = df[df.Symbol == stock]
    st.header("Close price Line graph")
    st.plotly_chart(px.line(sd, 'Date', 'Close'))
    st.header("Candlestick Plot")
    st.plotly_chart(go.Figure(data=[go.Candlestick(x=sd['Date'],open=sd['Open'],high=sd['High'],low=sd['Low'],close=sd['Close'])]))
    st.header("High price Histogram")
    st.plotly_chart(px.histogram(sd,x='Date',y='High'))
    st.header('VWAP over time')
    fig = go.Figure([go.Scatter(x=sd.index, y=sd['VWAP'])])
    fig.update_xaxes(title="Date")
    fig.update_yaxes(title="VWAP")
    st.plotly_chart(fig)
    st.header("Trades over time")
    st.plotly_chart(px.scatter(sd,'Date','Trades'))
    st.header("Volume over time")
    st.plotly_chart(px.line(sd,'Date','Volume'))
    st.header("Turnover")
    st.plotly_chart(px.scatter(sd,'Date','Turnover'))

def page2(title):
    data = load_data()
    st.title(title)
    st.header("Latest Close price comparison")
    st.plotly_chart(px.bar(data[data.Date==max(data.Date)],'Symbol','Close'))
    st.header("Latest VWAP comparison")
    st.plotly_chart(px.bar(data[data.Date==max(data.Date)],'Symbol','VWAP'))
    st.header("Highest Trades comparison")
    st.plotly_chart(px.bar(data.groupby('Symbol',as_index=False).max(),'Symbol','Trades'))
    st.header("Top 10 highest Volume")
    st.plotly_chart(px.pie(data[data.Date==max(data.Date)].head(10),'Symbol','Volume'))
    st.header("Top 10 All time highest Turnover")
    st.plotly_chart(px.pie(data.groupby('Symbol',as_index=False).max().head(10),'Symbol','Turnover'))


pages = {'Introduction':home,'Analysing a single stock':page1,'Comparison between Stocks':page2}
page = st.sidebar.selectbox('Choose a page:-',list(pages.keys()))

pages[page](page)
