# clean investment and acquisition data files for displaying with Question 2. 
import pandas as pd

investment_data = pd.read_csv('investments.csv')
aq_data = pd.read_csv('acquisitions.csv')
# convert the existing date column into a TimeSeries for easier manipulation and calculations
investment_data['funded_at'] = pd.to_datetime(investment_data['funded_at'])

# new column that specifies the quarter of the year the investment was made
investment_data['quarter'] = investment_data.funded_at.dt.quarter

# new column that specifies the name of the month that the investment was made
investment_data['month'] = investment_data.funded_at.dt.month_name()

# Clean acquisition data by converting dates to DateTime objects and dropping NA values
aq_data.dropna(subset=['acquired_at'], inplace=True)
aq_data['acquired_at'] = pd.to_datetime(aq_data.acquired_at, errors='coerce')
aq_data.dropna(subset=['acquired_at'], inplace=True)

# new column; month the acquisition was made
aq_data['month'] = aq_data.acquired_at.dt.month_name()
#new column; quarter the acquisition was made
aq_data['quarter'] = aq_data.acquired_at.dt.quarter

investment_data.to_csv('clean_investments.csv')
aq_data.to_csv('clean_acquisitions.csv')

