
import requests
import urllib.parse
import pandas as pd
import datetime
from datetime import date


def get_news_sentiment(stock, 
                       api_key):
    url = 'https://eodhistoricaldata.com/api/sentiments?'
    
    start_date = (date.today() - datetime.timedelta(days=29))
    end_date = date.today()
       
    params = {'s':stock,
              'from':start_date,
              'to':end_date,
              'api_token':api_key}
    news_url = url + urllib.parse.urlencode(params)
    company_key = f'{stock}.US'
    request = requests.get(news_url).json()[company_key]
    df = pd.DataFrame(request).rename(columns={"date": "Date",
                                               'count':'News_Count',
                                               'normalized':'News_Sentiment'})
    df['Date'] = pd.to_datetime(df['Date'])
    return df
