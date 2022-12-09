import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import datetime
from datetime import date

import requests
import urllib.parse

from PIL import Image
from io import BytesIO
import json




'''
# Welcome to our stock prediction model.

On the following page we'll make you rich. You are welcome!
'''

options_8000 = pd.read_csv('nasdaq_current_list_12112012.csv')
options = list(options_8000['Name'])
options.insert(0, '')

stock_name = st.selectbox("Start typing a stock name", options, index = 1)


'''
#### You requested prediction for the following stock: 
'''

st.write(stock_name)


'''
### Here is some fake data to use for testing (with date display relative to today): 
'''

# get price prediction from UI
url = "http://127.0.0.1:8000/predict"
# url = 'https://gcloud-5cp25n2jkq-ew.a.run.app'
params = {'stock' : stock_name
            }
response = requests.get(url, params = params)
stock_prediction = response.json() 


st.write(stock_prediction)


# get price of stock for the last 7 days
today = date.today()

stock_prices_past = {
        f'{today - datetime.timedelta(days = 7)}' : stock_prediction['stock_price'][-7], 
        f'{today - datetime.timedelta(days = 6)}' : stock_prediction['stock_price'][-6],
        f'{today - datetime.timedelta(days = 5)}' : stock_prediction['stock_price'][-5],
        f'{today - datetime.timedelta(days = 4)}' : stock_prediction['stock_price'][-4],
        f'{today - datetime.timedelta(days = 3)}' : stock_prediction['stock_price'][-3],
        f'{today - datetime.timedelta(days = 2)}' : stock_prediction['stock_price'][-2],
        f'{today - datetime.timedelta(days = 1)}' : stock_prediction['stock_price'][-1]
    }

data_stock_prices_past = pd.DataFrame.from_dict(stock_prices_past, 
                                                columns = ['stock_price'], 
                                                orient = 'index')
data_stock_prices_past = data_stock_prices_past.reset_index()

# st.write(data_stock_prices_past)


'''
### Visualise predictions
'''


fig, ax = plt.subplots(figsize=(11, 5))
# ax.plot(stock_prediction_fake['date'], stock_prediction_fake['stock_price'])

ax.scatter(data_stock_prices_past['index'], data_stock_prices_past['stock_price'])
# plt.style.use('fast')
st.pyplot(fig)

'''
### Visualisation using R
'''
image = requests.post("http://localhost:8079/plot", json = {'stock_prediction': stock_prediction})

st.image(Image.open(BytesIO(image.content)), output_format='png')



