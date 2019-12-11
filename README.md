# Investmenting in Startups Over Time

## Running .ipynb files

In order to run the .ipynb files, you must first install Bokeh.

## Presentation Link
https://docs.google.com/presentation/d/1rfPX1cCwxa8rv7X7S3jaNn-0LlSF7eIPRxCoaAVeHsM/edit?usp=sharing


## Visualizations
https://people.ucsc.edu/~thjafox/


## Questions Asked

1) Do venture capitalists tend to diversify their investment portfolios, or do they tend to invest in a particular sector?

2) Which parts of the year are investments/acquisitions more active? Is there a part of the year where overall activity is greater?

3) Do leading venture capitalists tend to invest domestically or are their investments diversified with international investments?

4) Which cities, states, countries have the highest number of investments?

5) Which sectors garner the highest number of investments? How has this changed over time?

6) Do Investments tend to lead or lag behind the public’s interest?

## Results

Answers and visualizations to the question set can be found by running index.html which is found in the root level directory.

Finished code and necessary data files can be found in the folder titled /Submission. Each .ipynb file generates a standalone .html file which contains the visualization for the question being answered.

## Challenges

We faced challenges in regards to sourcing and binning our data.

Sourcing: Our data comes from a Github Repo that a third-party person compiled from Crunchbase. In order to actually source data from Crunchbase, we would need a premium account ($300 to make one). Furthermore, the free trial premium did not allow full access to the data (i.e. downloading .csv files) and any attempts to scrape Crunchbases webpages were immediately denied, so webscraping more data was extremely unfeasible.

Binning: A lot of our project revolves around analyzing investment habits based around various sectors of companies. Our dataset has a column that denotes the sector(s) that a company fall under, but this is presented in the form of a string with the format "(sector) | (sector) | (sector)". With this label, there were over 16,000 unique tags in this column, so a binning system had to be used instead. This was solved by separating the sectors, making them a column in our data, and having the data value be 1 if that company is in that sector, and 0 otherwise. Unfortunately, this causes some issues with how representative our data is because a singular investment can fall under multiple sectors.