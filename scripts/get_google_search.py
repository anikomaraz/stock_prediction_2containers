import pandas as pd
import datetime
from datetime import date
import pytrends

# connect to google
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)


def get_google_search(company_ticker):

    # build payload
    kw_list = [company_ticker]
    
    start_date = (date.today() - datetime.timedelta(days=29))
    end_date = date.today()

    pytrends.build_payload(kw_list, cat=0, timeframe=f'{start_date} {end_date}')
    second_half = pytrends.interest_over_time()
    # second_half = second_half.reset_index()
    

    #pytrends.build_payload(kw_list, cat=0, timeframe=f'{start_date} 2022-05-27')
    #first_half = pytrends.interest_over_time()
    #first_half = first_half.reset_index()

    #data = pd.concat([first_half,second_half]).drop(['isPartial'], axis=1)

    #return data
    return second_half


