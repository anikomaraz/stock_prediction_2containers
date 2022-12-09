FROM tensorflow/tensorflow:2.10.0

WORKDIR stock_prediction/

COPY requirements.txt requirements.txt
COPY fastapi_.py fastapi_.py
COPY .env .env
COPY nasdaq_current_list_12112012.csv nasdaq_current_list_12112012.csv
COPY model_combined_appl.h5 model_combined_appl.h5
COPY scripts/get_news_sentiment.py scripts/get_news_sentiment.py
COPY scripts/get_stock_price.py scripts/get_stock_price.py
COPY scripts/get_tweet_sentiment.py scripts/get_tweet_sentiment.py
COPY scripts/get_google_search.py scripts/get_google_search.py

RUN pip install -U pip
RUN pip install -r requirements.txt

RUN python -c 'from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv())'

CMD uvicorn fastapi_:app --host 0.0.0.0 --port 8080