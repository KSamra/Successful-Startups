import pandas as pd
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Panel, Tabs, FactorRange
from bokeh.models.tools import HoverTool
from bokeh.transform import factor_cmap


output_file('q3.html')


def markDomestic(row):
  '''
  Marks an investment as domestic if countries are the same.
  '''
  return row.company_country_code == row.investor_country_code

investments = pd.read_csv('investments_clean.csv')
investments.drop(columns='Unnamed: 0', inplace=True)

investments.dropna(subset=['investor_name', 'raised_amount_usd', 'company_country_code'], inplace=True)

def makePlot(option='sum'):
  # First determine 'top investors'
  grouped_investors = investments.groupby('investor_name', sort=False)['raised_amount_usd']
  invested_by_each_vc = grouped_investors.sum()

  # if we want to determine top investors by overall number of investments made, then option == 'count
  if option == 'count':
    invested_by_each_vc = grouped_investors.count()

  # of the 'top' investors, take only the top 5
  top = invested_by_each_vc.nlargest(5)
  # top.index is list of investor names
  top = top.index

  df_top = investments[investments.investor_name.isin(top)]

  domestic = df_top.apply(markDomestic, axis=1)

  df_top = df_top.assign(domestic=domestic)

  groups = df_top.groupby('investor_name')

  # Prepare data for plotting
  ticks = ['Domestic', 'International']
  investor_names = []
  international = []
  domestic = []
  for company, data in groups:
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
  plot = figure(x_range=FactorRange(*x), plot_height=600, plot_width=850,
  title="Domestic vs International Investment", toolbar_location=None)

  plot.vbar(x='x', top='counts', source=source, width=0.9, line_color='white',
  fill_color=factor_cmap('x', palette=palette, factors=ticks, start=1))

  hover = HoverTool()
  hover.tooltips = [('Total # of Investments', '@counts')]
  plot.add_tools(hover)

  plot.y_range.start = 0
  plot.x_range.range_padding = 0.0
  plot.xaxis.major_label_orientation = 1
  plot.xaxis.group_label_orientation = 1
  plot.xgrid.grid_line_color=None
  plot.xaxis.group_text_font_size = "7pt"
  plot.xaxis.group_text_line_height = 10
  plot.xaxis.axis_label = 'Investor Name'
  plot.yaxis.axis_label = 'Number of Investments'
  return plot

# Make a plot in which the top investors are determined by USD invested
p1 = makePlot()
# Make a plot in which the top investors are determined by the num of investments made
p2 = makePlot('count')

tab1 = Panel(child=p1, title="Top 5 VC Firms by USD Invested")
tab2 = Panel(child=p2, title="Top 5 VC Firms by Number of Investments")
tabs = Tabs(tabs=[tab1, tab2])
show(tabs)