import streamlit as st
import pandas as pd 
import numpy as np 
import yfinance as yf 
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.graph_objects as go 
import plotly.express as px 
import datetime 
from datetime import date, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm 
app = "Stock Market App"
st.title(app)
st.subheader("Select stock for forecasting")
st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkzFTa0bjy9V7Kllf8INArhrmpsrLz7gQx2Q&usqp=CAU')
st.sidebar.header("Select parameters")
start_date = st.sidebar.date_input("Start Date",date(2022,1,1))
end_date = st.sidebar.date_input("End Date",date(2022,12,31))
ticker_symbols= ["AAPL", "AMZN", "MSFT", "GOOGL", "META","TSLA", "NFLX", "JPM", "NVDA", "DIS", "V", "MA", "BRK.A", "PYPL", "PG", "VZ", "T", "KO", "BA"]
ticker =st.sidebar.selectbox('Make selection',ticker_symbols)
get_data = yf.download(ticker,start = start_date,end = end_date)
get_data.insert(0,"Date",get_data.index,True)
get_data.reset_index(drop = True,inplace= True)
st.write("Data From",start_date,"to","end_date")
st.write(get_data)
st.header("Visualization")
st.subheader("Plot")
figure = px.line(get_data , x = "Date", y = get_data.columns, title= "Closing price",width=1000,height=600)
st.plotly_chart(figure)
column_select = st.selectbox("Select column for forecasting",get_data.columns[1:])
get_data =get_data[['Date',column_select]]
st.write('Selected Data')
st.write(get_data)

st.header("Check if data is stationary")
st.write(adfuller(get_data[column_select][1]<0.05))
