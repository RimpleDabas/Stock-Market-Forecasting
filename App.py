#import dependencies
import streamlit as st
import pandas as pd 
import yfinance as yf 
import seaborn as sns 
import plotly.graph_objects as go 
import plotly.express as px 
import datetime 
from datetime import date, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm 
#add title and color
app = ":orange[Stock Market App]"
st.title(app)
st.subheader(':orange[Select stock]')
## help taken from streamlit discussion to add background image
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url('data:image/jpeg;base64,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');
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()
#st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkzFTa0bjy9V7Kllf8INArhrmpsrLz7gQx2Q&usqp=CAU')
st.sidebar.header(":orange[Select parameters]")
#add start and end date
start_date = st.sidebar.date_input(":orange[Start Date]",date(2022,1,1))
end_date = st.sidebar.date_input(":orange[End Date]",date(2022,12,31))
#add ticker symbols
ticker_symbols= ["AAPL", "AMZN", "MSFT", "GOOGL", "META","TSLA", "NFLX", "JPM", "NVDA", "DIS", "V", "MA", "BRK.A", "PYPL", "PG", "VZ", "T", "KO", "BA"]
ticker =st.sidebar.selectbox(':orange[Make selection]',ticker_symbols)
#pull data from yahoo finance
get_data = yf.download(ticker,start = start_date,end = end_date)
#reset indices to get date in the column
get_data.insert(0,"Date",get_data.index,True)
get_data.reset_index(drop = True,inplace= True)
#print and plot the data
st.write(":orange[Data From]",start_date,":orange[to]",end_date)
st.write(get_data)
st.header(":orange[Visualization]")
st.subheader(":orange[Plot]")
#get column names to make selection in the next step
figure = px.line(get_data , x = "Date", y = get_data.columns, title= "Closing price",width=1000,height=600)
st.plotly_chart(figure)
column_select = st.selectbox(":orange[Select column for forecasting]",get_data.columns[1:])
get_data =get_data[['Date',column_select]]
st.write(':orange[Selected Data]')
st.write(get_data)
#check for the stationarity
st.header(":orange[Check if data is stationary]")
st.write(adfuller(get_data[column_select])[1]<0.05)

st.header(':orange[Decomposition]')
decompose = seasonal_decompose(get_data[column_select],model='additive',period= 12)
# st.write(decompose.plot())
#decompose to get seasonality and trends
st.write(":orange[Decomposed Plots]")
st.plotly_chart(px.line(x= get_data["Date"],y =decompose.trend,title='Trend',width=1200,height=400,labels={"x":"Date",'y':"Price"}).update_traces(line_color = 'Blue'))
st.plotly_chart(px.line(x= get_data["Date"],y =decompose.seasonal,title='Seasonality',width=1200,height=400,labels={"x":"Date",'y':"Price"}).update_traces(line_color = 'Green'))
st.plotly_chart(px.line(x= get_data["Date"],y =decompose.resid,title='Residuals',width=1200,height=400,labels={"x":"Date",'y':"Price"}).update_traces(line_color = 'Red',line_dash='dot'))
p = st.slider(':orange[Select the value of p]',0,3,1)
d= st.slider(':orange[Select the value of d]',0,3,1)
q = st.slider(':orange[Select the value of q]',0,3,1)
seasonal_order  = st.number_input(':orange[Select the value of seasonal p]',0,24,12)
model = sm.tsa.statespace.SARIMAX(get_data[column_select],order=(p,d,q),seasonal_order= (p,d,q,seasonal_order))
model= model.fit()
#st.header(':orange[Model Summary]')
#st.write(model.summary())
forecast = st.number_input(':orange[Select days for forcasting]',1,365,10)
predict = model.get_prediction(start=len(get_data),end = len(get_data)+forecast)
predict = predict.predicted_mean
predict.index = pd.date_range(start=end_date, periods = len(predict),freq = "D")
predict = pd.DataFrame(predict)
predict.insert(0,'Date',predict.index)
predict.reset_index(drop=True,inplace= True)
st.write(":orange[Predictions]",predict)
st.write(":orange[Actual Data]",get_data)
fig = go.Figure()

fig.add_trace(go.Scatter(x=get_data["Date"],y = get_data[column_select],mode = 'lines',name = 'Actual',line = dict(color= 'blue')))
fig.add_trace(go.Scatter(x=predict["Date"],y = predict['predicted_mean'],mode = 'lines',name = 'Predicted',line = dict(color= 'red')))
fig.update_layout(title='Actual vs Predicted',xaxis_title = 'Date',yaxis_title= 'Price',width = 1200,height = 400)
st.plotly_chart(fig)