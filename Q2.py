import pandas as pd
import numpy as np 
# switch output_file with output_notebook if rendering in jupyter notebook
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Panel, Tabs
from bokeh.models.tools import HoverTool

output_file("q2.html")
# read from data sources
investment_data = pd.read_csv('clean_investments.csv')
aq_data = pd.read_csv('clean_acquisitions.csv')

# how many investments occur per month
monthly_investments_total = investment_data.groupby('month')['company_name'].count()

# order that we want the months to be displayed on figure's x-axis
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

d_monthly = monthly_investments_total.to_dict()
l_monthly = [d_monthly.get(x) for x in months]

monthly_source = ColumnDataSource(data=dict(months=months, counts=l_monthly))

# figure displaying monthly number of investments
p1 = figure(x_range=months, toolbar_location=None, title="Investments per Month", width=800)
p1.vbar(x='months', top='counts', width=0.5, source=monthly_source, color="firebrick")
p1.xaxis.axis_label = 'Month'
p1.yaxis.axis_label = 'Number of Investments'

hover = HoverTool()
hover.tooltips = [('Total # of Investments', '@counts')]
p1.add_tools(hover)

tab1 = Panel(child=p1, title="Investments")

# do the same for monthly acquisitions
monthly_acquisitions = aq_data.groupby('month')['company_name'].count()
temp = monthly_acquisitions.to_dict()
aq_values = [temp.get(x) for x in months]

aq_source = ColumnDataSource(data=dict(months=months, counts=aq_values))

p2 = figure(x_range=months, title="Acquisitions per Month", width=800, toolbar_location=None)
p2.vbar(x='months', top='counts', width=0.5, source=aq_source, color="firebrick")
p1.xaxis.axis_label = 'Month'
p1.yaxis.axis_label = 'Number of Acquisitions'
hover2 = HoverTool()
hover2.tooltips = [('Total # of Acquisitions', '@counts')]
p2.add_tools(hover2)

tab2 = Panel(child=p2, title="Acquisitions")


tabs = Tabs(tabs=[tab1, tab2])
show(tabs)
