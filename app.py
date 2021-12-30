import os
import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from bokeh.layouts import gridplot, column
from bokeh.plotting import figure, curdoc
from bokeh.embed import components 
import streamlit as st
st.title('Your Stock Finder')
def get_stock_price(symbol, start_year, end_year):
    API_KEY= os.getenv("API_KEY", "optional-default")
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta_data = ts.get_weekly_adjusted(symbol=symbol)
    aapl = np.array(data['5. adjusted close'])
    aapl_dates = np.array(data.index, dtype=np.datetime64)
    year = pd.DatetimeIndex(data.index).year
    inds = np.where(np.logical_and(year>=start_year, year<=end_year))
    filtered_dates, filtered_prices = aapl_dates[inds], aapl[inds]
    window_size = 4
    window = np.ones(window_size)/float(window_size)
    aapl_avg = np.convolve(aapl, window, 'same')
    p2 = figure(x_axis_type="datetime", title=symbol+ " Weekly data with One-Month Average")
    p2.grid.grid_line_alpha = 0
    p2.xaxis.axis_label = 'Date'
    p2.yaxis.axis_label = 'Price'
    p2.ygrid.band_fill_color = "olive"
    p2.ygrid.band_fill_alpha = 0.1

    p2.scatter(filtered_dates, filtered_prices, size=4, legend_label='close',
               color='darkgrey', alpha=0.8)

    p2.line(filtered_dates[2:], aapl_avg[inds][2:], legend_label='avg', color='navy')
    p2.legend.location = "top_left"
    st.bokeh_chart(p2)

def main():
    #Setup plot
    name = st.sidebar.text_input("Stock Name", 'AAPL')
    start_year = st.sidebar.number_input("Start year", value=2012)
    end_year = st.sidebar.number_input("End year", value=2021)
    get_stock_price(name, start_year, end_year)
    

if __name__ == '__main__':
    main()

