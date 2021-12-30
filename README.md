# Displaying time-series of Stock tickers

This project uses Streamlit configuration to build webapp showing time-series plot of stock prices on Heroku.


The webapp can be accesed here: https://dinesh-stock.herokuapp.com 

Some steps that have been deployed here are:

## Step 1: Gathering the stock data
-  Gathered stock data using Alpha Vantage API, which provides this data for free. Some data like adjusted daily price can only be accessed using premium version, so I have collected adjusted weekly data.
- A montly moving average is calculated/
- Users are allowed to input their custom ticker name, start date and end date.

## Step 2: Plotting pandas data
- We created an interactive plot from the dataframe using Bokeh.

Hope you enjoy using this simple app.
