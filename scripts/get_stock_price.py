# import necessary packages
import yfinance as yf
import pandas as pd
import datetime
from datetime import date

def get_stock_prices(stock_ticker): 
    
    '''
    Input a stock name (real stock names, not ticker names!), check if input is correct. 
    Get data from the yahoo cloud. 
    Return a csv file with the stock prices in the pre-specified period. 
    '''
    # get stock and ticker names (from current stocks only, list of ~ 8000)
    #stock_names = pd.read_csv('~/code/rahulvaity25/stock_prediction/stock_prediction/raw_data/nasdaq_current_list_12112012.csv')
    stock_names = pd.read_csv('nasdaq_current_list_12112012.csv')
    stock_names = stock_names[['Symbol', 'Name']]
    
    # create a dictionary of stocks
    stock_dictionary = dict(zip(stock_names['Name'], # keys, verbose name of stock
                                stock_names['Symbol'])) # values, Ticker name
    
    # check if input query exists: 
    if stock_ticker in stock_dictionary.values(): 
        # get stock ticker name from dictionary
        # stock_ticker = stock_dictionary[stock]
        
        # find and download price data
        start = (date.today() - datetime.timedelta(days=30))
        end = date.today()
        stock_price_historical = yf.download(stock_ticker, start=start, end=end)
        
        return stock_price_historical


