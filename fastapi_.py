from fastapi import FastAPI
import requests
import pandas as pd
import datetime
from datetime import date

# api key for eodh
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
api_key = os.environ.get('api_key')

# features
from scripts.get_stock_price import get_stock_prices
from scripts.get_google_search import get_google_search
from scripts.get_news_sentiment import get_news_sentiment
from scripts.get_tweet_sentiment import get_tweet_sentiment

# load model 
from keras.models import load_model
model = load_model('model_combined_appl.h5')

# get stock as user input
def get_ticker(stock): 
    '''
    Function takes the stock verbose name from the UI as input and 
    outputs the corresponding ticker name (based on the current NASDAQ stock list)
    '''
    stock_names = pd.read_csv('nasdaq_current_list_12112012.csv')
    stock_names = stock_names[['Symbol', 'Name']]
    stock_dictionary = dict(zip(stock_names['Name'], # keys, verbose name of stock
                                stock_names['Symbol'])) # values, Ticker name
    # breakpoint()
    stock_ticker = stock_dictionary[stock] # to retrieve value (ticker) at key (stock verbose name)
    
    return stock_ticker



# get user requested stock name using stock ticker name

# stock = 'AAPL'
# stock_name = 'Agilent Technologies Inc. Common Stock'


# Define a root `/` endpoint
app = FastAPI()

# streamlit local host: http://localhost:8501
# http://127.0.0.1:8000/predict?stock='AAPL' 
# https://stockprediction.streamlit.app/predict?stock=AAPL
@app.get('/predict')

def predict(stock):     
    stock_ticker = get_ticker(stock) 
    
    # STOCK PRICE data from API
    df_stocks = get_stock_prices(stock_ticker)
    X_train_stocks = df_stocks.rename(columns = {'Open':'open', 
                                             'High':'high', 
                                             'Low':'low',
                                             'Close':'close', 
                                             'Adj Close':'adjusted_close',
                                             'Volume':'volume'})

    # fill missing price data (for the weekends) with the last known price for the stock 
    date_range = pd.date_range((date.today() - datetime.timedelta(days=29)),
                           date.today())

    X_train_stocks.index = pd.DatetimeIndex(X_train_stocks.index)
    X_train_stocks = X_train_stocks.reindex(date_range, fill_value=0)

    def replace_missing_with_one_above(column): 
        for index, number in enumerate(column):
            if column[index] != 0: 
                if number == 0:
                     column[index] = column[index-1]
            return column

    X_train_stocks.apply(replace_missing_with_one_above)
    
    # get SENTIMENT + COUNT data from twitter + news
    api_key = os.environ.get('api_key')
    news = get_news_sentiment(stock_ticker, api_key = api_key)
    tweets = get_tweet_sentiment(stock_ticker, api_key = api_key)
    google = get_google_search(stock_ticker).drop(['isPartial'], axis = 1).reset_index()
    google = google.rename(columns={google.columns[1]: 'google_count', google.columns[0]: 'Date'})

    merged_news_tweets = pd.merge(news, tweets, 
                           left_on='Date', 
                           right_on='Date', 
                           how='left')
    merged_features = pd.merge(merged_news_tweets, google,
                          left_on = 'Date', 
                          right_on = 'Date', 
                          how = 'left')
    merged_features = merged_features.set_index('Date')

    
    X_train_sentiments = merged_features.rename(columns= {'News_Count':'news_count', 
                                                         'News_Sentiment': 'news_sentiment', 
                                                         'Tweet_Count': 'tweet_count', 
                                                         'Tweet_Sentiment': 'tweet_sentiment',
                                                         'google_count': 'google_count'})

    # fill missing price data (for the weekends) with the last known price for the stock 
    date_range = pd.date_range((date.today() - datetime.timedelta(days=29)),
                               date.today())
    X_train_sentiments.index = pd.DatetimeIndex(X_train_sentiments.index)
    X_train_sentiments = X_train_sentiments.reindex(date_range, fill_value=0)
    X_train_sentiments['google_count'] = X_train_sentiments['google_count'].fillna(0) # google NAN values replaced by 0
    
    X_train_sentiments.apply(replace_missing_with_one_above)

    # CALL MODEL AND MAKE THE PREDICTION
    # breakpoint()
    stock_prediction_14 = model.predict([X_train_stocks, X_train_sentiments])[0].tolist()
    #X_processed = preprocess_featustockres(X_pred)
    
    # y_pred_raw = model.predict(X_pred)
    
    # y_pred = {'stock_price': pd.DataFrame(y_pred_raw)}
     
    #return {'stock_prediction': stock_prediction}

    
   
    
    return {
        'stock' : stock,
        'stock_prediction_14': stock_prediction_14, 
        'stock_date' : get_stock_prices(stock_ticker).index.values.tolist(),
        'stock_price' : get_stock_prices(stock_ticker)['Close'].to_list(),
        #'google_date' : get_google_search(stock_ticker)['date']\
                                                   # .to_list(),
        #'google_clicks' : get_google_search(stock_ticker)[stock_ticker]\
                                                    #.to_list(),

        # 'news_date' : get_news_sentiment(stock_ticker, 
        #                                  api_key = api_key)['Date']\
        #                                      .to_list(),
        # 'news_clicks' : get_news_sentiment(stock_ticker, 
        #                                    api_key = api_key)['News_Count']\
        #                                      .to_list(),
        # 'news_sentiment' : get_news_sentiment(stock_ticker, api_key)['News_Sentiment']\
        #                                     .to_list(),
       
        # 'tweet_date' : get_tweet_sentiment(stock_ticker, api_key = api_key)['Date']\
        #                                     .to_list(),
        # 'tweet_clicks' : get_tweet_sentiment(stock_ticker, api_key = api_key)['Tweet_Count']\
        #                                     .to_list(),
        # 'tweet_sentiment' : get_tweet_sentiment(stock_ticker, api_key = api_key)['Tweet_Sentiment']\
        #                                     .to_list()
    }
      
         
    
# app.state.model.predict(...)


