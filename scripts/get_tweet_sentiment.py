
import requests
import urllib.parse
import pandas as pd
import datetime
from datetime import date

def get_tweet_sentiment(stock, 
                        api_key):  
    url = 'https://eodhistoricaldata.com/api/tweets-sentiments?'
    
    start_date = (date.today() - datetime.timedelta(days=29))
    end_date = date.today()
    
    params = {'s':stock,
              'from':start_date,
              'to':end_date,
              'api_token':api_key}
    tweet_url = url + urllib.parse.urlencode(params)
    company_key = f'{stock}.US'
    request = requests.get(tweet_url).json()[company_key]
    df = pd.DataFrame(request).rename(columns={"date": "Date",
                                               'count':'Tweet_Count',
                                               'normalized':'Tweet_Sentiment'})
    df['Date'] = pd.to_datetime(df['Date'])
    return df
