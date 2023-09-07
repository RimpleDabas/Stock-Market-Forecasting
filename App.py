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
st.write(adfuller(get_data[column_select])[1]<0.05)

st.header('Decomposition')
decompose = seasonal_decompose(get_data[column_select],model='additive',period= 12)
# st.write(decompose.plot())

st.write("Decomposed Plots")
st.plotly_chart(px.line(x= get_data["Date"],y =decompose.trend,title='Trend',width=1200,height=400,labels={"x":"Date",'y':"Price"}).update_traces(line_color = 'Blue'))
st.plotly_chart(px.line(x= get_data["Date"],y =decompose.seasonal,title='Seasonality',width=1200,height=400,labels={"x":"Date",'y':"Price"}).update_traces(line_color = 'Green'))
st.plotly_chart(px.line(x= get_data["Date"],y =decompose.resid,title='Residuals',width=1200,height=400,labels={"x":"Date",'y':"Price"}).update_traces(line_color = 'Red',line_dash='dot'))
p = st.slider('Select the value of p',0,5,2)
d= st.slider('Select the value of d',0,5,1)
q = st.slider('Select the value of q',0,5,2)
seasonal_order  = st.number_input('Select the value of seasonal p',0,24,12)
model = sm.tsa.statespace.SARIMAX(get_data[column_select],order=(p,d,q),seasonal_order= (p,d,q,seasonal_order))
model= model.fit()
st.header('Model Summary')
st.write(model.summary())
forecast = st.number_input('Select days for forcasting',1,365,10)
predict = model.get_prediction(start=len(get_data),end = len(get_data)+forecast)
predict = predict.predicted_mean
predict.index = pd.date_range(start=end_date, periods = len(predict),freq = "D")
predict = pd.DataFrame(predict)
predict.insert(0,'Date',predict.index)
predict.reset_index(drop=True,inplace= True)
st.write("Predictions",predict)
st.write("Actual Data",get_data)
fig = go.Figure()

fig.add_trace(go.Scatter(x=get_data["Date"],y = get_data[column_select],mode = 'lines',name = 'Actual',line = dict(color= 'blue')))
fig.add_trace(go.Scatter(x=predict["Date"],y = predict['predicted_mean'],mode = 'lines',name = 'Predicted',line = dict(color= 'red')))
fig.update_layout(title='Actual vs Predicted',xaxis_title = 'Date',yaxis_title= 'Price',width = 1200,height = 400)
st.plotly_chart(fig)