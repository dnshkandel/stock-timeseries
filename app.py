import numpy as np
from alpha_vantage.timeseries import TimeSeries
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show
from bokeh.embed import components 
from flask import Flask, render_template


def get_stock_price(symbol):
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

    #show(gridplot([[p2]]))  
    return p2
@app.route('/')
def homepage():
    #Setup plot    
    p = get_plot(get_stock_price('AAPL))
    script, div = components(p)
    #Render the page
    return render_template('home.html', script=script, div=div)    

if __name__ == '__main__':
    app.run(debug=False) #Set to false when deploying
