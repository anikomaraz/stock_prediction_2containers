In this project my aim was to deploy our final bootcamp project using two containers (Python and R). In our project we aimed to predict stock prices (2 weeks in advance) based on the public perception of the company (news representation and tweets - sentiment + count for both sources) plus of course historical prices of the given stock. We then added a non-sequential deep learning model to predict the prices. The final project is available at: 

https://stockprediction.streamlit.app

This Git repo contains the full deployment: two backend containers: (1) the Python container fetching data via API calls and contains the model weights + (2) the R container creating a beautiful visualisation in ggplot. The frontend is then displayed using Streamlit. To learn more about how I deployed this project using two containers (Python and R) and linking it to the Streamlit frontend, go to [blogpost/dockerize.md](https://github.com/anikomaraz/stock_prediction_2containers/blob/master/blogpost/dockerize.md)

**Final note:**  You are 100% correct: *my solution is a total overkill for the task.*  🤓


