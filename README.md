# How to Make Movies (and Get Rich Trying!)

## Predicting box office revenue.

For this project, I scraped data from the IMDb pages for the top 100 grossing movies for each year from 2009 to 2018 and then analyzed things that might be predictive of box office revenue.

Files in this repository include:

**scraper.py**: This file contains the code to scrape the IMDb pages for each movie for potential features.  After scraping is completed and the data collected is stored in a dataframe, it will save the dataframe to a picklefile called _movie_dataframe.pkl_ in the present working directory.

**analysis.py**: This file performs analysis on the data and outputs visuals to represent the data analyzed.