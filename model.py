import pandas as pd
import datetime
from datetime import date

# get features 
from scripts.get_stock_price import get_stock_prices
from scripts.get_google_search import get_google_search
from scripts.get_news_sentiment import get_news_sentiment
from scripts.get_tweet_sentiment import get_tweet_sentiment

# get model 
from keras.models import load_model
model = load_model('model_combined_1.h5')

stock_ticker = 'MSFT'

# pull stocks price data from API
df_stocks = get_stock_prices(stock_ticker)

# get the right column names
X_train_stocks = df_stocks.rename(columns = {'Open':'open', 
                                             'High':'high', 
                                             'Low':'low',
                                             'Close':'close', 
                                             'Adj Close':'adjusted_close',
                                             'Volume':'volume'})

X_train_stocks

# fill missing price data (for the weekends) with the last known price for the stock 
date_range = pd.date_range((date.today() - datetime.timedelta(days=29)),
                           date.today())

# first replace with zeros
X_train_stocks.index = pd.DatetimeIndex(X_train_stocks.index)
X_train_stocks = X_train_stocks.reindex(date_range, fill_value=0)

# then replace zeros with the values above them 
# (implying that the previous day's price is the best predictor for the next day)
def replace_missing_with_one_above(column): 
    for index, number in enumerate(column):
        if column[index] != 0: 
            if number == 0:
                 column[index] = column[index-1]
        return column

X_train_stocks.apply(replace_missing_with_one_above)

X_train_stocks.head()

api_key = '6373e059e5d049.13587213'

news = get_news_sentiment(stock_ticker, api_key = api_key)
tweets = get_tweet_sentiment(stock_ticker, api_key = api_key)
# google = get_google_search(stock_ticker).drop(['isPartial'], axis = 1).reset_index()

merged_features = pd.merge(news, tweets, 
                           left_on='Date', 
                           right_on='Date', 
                           how='left')\
                    .drop(columns=['Date'])

X_train_sentiments = merged_features.rename(columns= {'News_Count':'news_count', 
                                                         'News_Sentiment': 'news_sentiment', 
                                                         'Tweet_Count': 'tweet_count', 
                                                         'Tweet_Sentiment': 'tweet_sentiment'})
# X_train_sentiments should contain ["news_count", "news_sentiment", "tweet_count", "tweet_sentiment"]], shape is (batch_size, 30, 4)
X_train_sentiments.shape
# model = load_model("model_combined_1.h5")
stock_prediction_14 = model.predict([X_train_stocks, X_train_sentiments])[0].tolist()
stock_prediction_14
# X_train_stocks should contain ["open", "high", "low", "close", "adjusted_close", "volume"], shape is (batch_size, 30, 6)
# X_train_sentiments should contain ["news_count", "news_sentiment", "tweet_count", "tweet_sentiment"]], shape is (batch_size, 30, 4)

# Data should be for the last 30 days