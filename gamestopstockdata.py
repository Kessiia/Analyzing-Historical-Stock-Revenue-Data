# Uploading all the needed libraries
!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat==4.2.0

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

#Defining the make_graph function. A piece of code they let us copy and paste in the course.
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Using yfinance to Extract Stock Data. We look at GameStop Stock.
gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period = "max")
#Resetting the index and showing the first 5 rows of the dataframe
gme_data.reset_index(inplace=True)
gme_data.head()

#Using webscraping to extract GameStop Revenue Data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

html_data = requests.get(url).text

#Parse the html data using beautiful_soup
soup = BeautifulSoup(html_data)

#Using read_html to extract the table, store it in a df, clean up the table by removing comma and dollar sign and show the first 5 rows.

html_data = pd.DataFrame(columns =["Date", "Revenue"])

read_html_pd_data = pd.read_html(url)

gme_revenue = read_html_pd_data[1]
gme_revenue.rename(columns={gme_revenue.columns[0]: "Date"}, inplace = True)
gme_revenue.rename(columns={gme_revenue.columns[1]: "Revenue"}, inplace = True)
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.head()

#To display the last 5 rows
gme_revenue.tail()

#Plotting GameStop Stock Graph
make_graph(gme_data, gme_revenue, 'GameStop')
