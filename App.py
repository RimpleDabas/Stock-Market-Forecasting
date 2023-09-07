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
import statsmodels.api as sm 

app = "Stock Market App"
st.title(app)
st.subheader("Select stock for forecasting")
st.image("data:image/jpeg;base64,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")
st.sidebar.header("Select parameters")
start_date = st.sidebar.date_input("Start Date",date(2022,1,1))
end_date = st.sidebar.date_input("End Date",date(2022,12,31))
ticker_symbols= ["AAPL", "AMZN", "MSFT", "GOOGL", "FB","TSLA", "NFLX", "JPM", "NVDA", "DIS", "V", "MA", "BRK.A", "PYPL", "PG", "VZ", "T", "KO", "BA"]
ticker =st.sidebar.selectbox('Make selection',ticker_symbols)
get_data = yf.download(ticker,start = start_date,end = end_date)
st.write(get_data)