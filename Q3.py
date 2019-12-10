import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Tabs, FactorRange
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap


output_file('q3.html')

def markDomestic(row):
  return row.company_country_code == row.investor_country_code

investments = pd.read_csv('investments_clean.csv')
investments.drop(columns='Unnamed: 0', inplace=True)

investments.dropna(subset=['investor_name', 'raised_amount_usd', 'company_country_code'], inplace=True)

def makePlot(option='sum'):
  grouped_investors = investments.groupby('investor_name', sort=False)['raised_amount_usd']
  
  invested_by_each_vc = grouped_investors.sum()
  if option == 'count':
    invested_by_each_vc = grouped_investors.count()
  top_twenty = invested_by_each_vc.nlargest(5)
  top_twenty = top_twenty.index

  df_top_twenty = investments[investments.investor_name.isin(top_twenty)]

  domestic = df_top_twenty.apply(markDomestic, axis=1)

  df_top_twenty = df_top_twenty.assign(domestic=domestic)
  #print(df_top_twenty.head(2))

  groups = df_top_twenty.groupby('investor_name')

  ticks = ['Domestic', 'International']
  investor_names = []
  international = []
  domestic = []
  for company, data in groups:
    print(company)
    investor_names.append(company)
    temp = data.domestic.value_counts()
    international.append(temp[False])
    domestic.append(temp[True])

  data = {
    'investors' : investor_names,
    'International': international,
    'Domestic' : domestic
  } 

  palette = ["#c7251a", "#718dbf"]

  x = [(investor, tick) for investor in investor_names for tick in ticks]
  counts = sum(zip(data['Domestic'], data['International']), ())

  source = ColumnDataSource(data=dict(x=x, counts=counts))
  p1 = figure(x_range=FactorRange(*x), plot_height=600, plot_width=850,
  title="Domestic vs International Investment", toolbar_location=None)

  p1.vbar(x='x', top='counts', source=source, width=0.9, line_color='white',
  fill_color=factor_cmap('x', palette=palette, factors=ticks, start=1))

  hover = HoverTool()
  hover.tooltips = [('Total # of Investments', '@counts')]
  p1.add_tools(hover)

  p1.y_range.start = 0
  p1.x_range.range_padding = 0.0
  p1.xaxis.major_label_orientation = 1
  p1.xaxis.group_label_orientation = 1
  p1.xgrid.grid_line_color=None
  p1.xaxis.group_text_font_size = "7pt"
  p1.xaxis.group_text_line_height = 10
  p1.xaxis.axis_label = 'Investor Name'
  p1.yaxis.axis_label = 'Number of Investments'
  return p1

p1 = makePlot()
p2 = makePlot('count')

tab1 = Panel(child=p1, title="Top 5 VC Firms by USD Invested")
tab2 = Panel(child=p2, title="Top 5 VC Firms by Number of Investments")
tabs = Tabs(tabs=[tab1, tab2])
show(tabs)