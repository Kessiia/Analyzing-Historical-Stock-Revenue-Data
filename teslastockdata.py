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

#Using yfinance to Extract Stock Data. We look at Tesla Stock.
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period = "max")
#Resetting the index and showing the first 5 rows of the dataframe
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Using webscraping to extract Tesla Revenue Data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data)

#Using read_html to extract the table, store it in a df and show the first 5 rows.
html_data = pd.DataFrame(columns =["Date", "Revenue"])

read_html_pd_data = pd.read_html(url)

tesla_revenue = read_html_pd_data[1]
tesla_revenue.rename(columns={tesla_revenue.columns[0]: "Date"}, inplace = True)
tesla_revenue.rename(columns={tesla_revenue.columns[1]: "Revenue"}, inplace = True)
tesla_revenue.head()

#Cleaning up the table, removing the comma and dollar sign and remove null or empty strings.
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#To display the last 5 rows
tesla_revenue.tail()

#Plotting Tesla Stock Graph
make_graph(tesla_data, tesla_revenue, 'Tesla')

