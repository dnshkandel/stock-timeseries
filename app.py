import os
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show
from bokeh.embed import components 
import matplotlib.pyplot as plt
import streamlit as st

def get_stock_price(symbol):
    API_KEY= os.getenv("API_KEY", "optional-default")
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta_data = ts.get_weekly_adjusted(symbol=symbol)
    aapl = np.array(data['5. adjusted close'])
    aapl_dates = np.array(data.index, dtype=np.datetime64)

    window_size = 4
    window = np.ones(window_size)/float(window_size)
    aapl_avg = np.convolve(aapl, window, 'same')

    p2 = figure(x_axis_type="datetime", title=symbol+ " Weekly data with One-Month Average")
    p2.grid.grid_line_alpha = 0
    p2.xaxis.axis_label = 'Date'
    p2.yaxis.axis_label = 'Price'
    p2.ygrid.band_fill_color = "olive"
    p2.ygrid.band_fill_alpha = 0.1

    p2.scatter(aapl_dates, aapl, size=4, legend_label='close',
               color='darkgrey', alpha=0.8)

    p2.line(aapl_dates, aapl_avg, legend_label='avg', color='navy')
    p2.legend.location = "top_left"

    st.pyplot(p2)

def main():
    #Setup plot
    name = st.text_input("Enter Stock Name (required)")
    get_stock_price(name)
    

if __name__ == '__main__':
    main()

