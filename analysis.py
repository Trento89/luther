# Michael J. Franco, Jr.
# October 6, 2019
#
# Analysis tool for working with the data scraped from IMDb.  Will read in
# the pickle file movie_dataframe.pkl created by the scraper.py program.

import requests
import urllib.request
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pickle
import re

import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score

df = pd.read_pickle('movie_dataframe.pkl') # Load file 'movie_dataframe.pkl'
                                           # which was created in 'scraper.py'
                                           # and read it in as dataframe 'df'.

# Name the columns of df.
df.columns = ['Title', 'Release Month', 'MPAA Rating', 'G Dummy', 'PG Dummy',
              'PG-13 Dummy', 'R Dummy', 'January', 'February', 'March',
              'April', 'May', 'June', 'July', 'August', 'September',
              'October', 'November', 'December', 'Runtime', 'Budget',
              'Opening Weekend Box Office Earnings',
              'Total Domestic Gross Earnings',
              'Total Worldwide Gross Earnings', 'IMDb User Ratings']

# Linear Regression

# Target dataframe
y = df['Total Worldwide Gross Earnings']

# Feature dataframe
X = df[['Budget', 'Runtime', 'January', 'February', 'March',
        'April', 'May', 'June', 'July', 'August', 'September',
        'October', 'November', 'December', 'G Dummy','PG Dummy',
        'PG-13 Dummy', 'R Dummy']]

# Perform train-test split.  X_test and y_test are holdout test sets.
X, X_test, y, y_test = train_test_split(X, y, test_size=.2, random_state=10)

linreg_model = LinearRegression() # Create an object for linear regression
linreg_model.fit(X,y)             # Fit linear model

# Use cross validation on the training set, segmenting it into 5
# subsets to validate the linear regression.  The mean of those
# values will then be stored in cv_score.
cv_list = cross_val_score(linreg_model, X, y, cv=5)
cv_score = np.mean(cv_list)

# R^2 value for test set
r_squared = linreg_model.score(X_test,y_test)

print('r^2 = {}'.format(r_squared))                   # Print r^2 value

print('Cross validation score = {}'.format(cv_score)) # Print cv score

# Create dataframes based on rating
df_g = df.loc[df['MPAA Rating'] == 'G']
df_pg = df.loc[df['MPAA Rating'] == 'PG']
df_pg13 = df.loc[df['MPAA Rating'] == 'PG-13']
df_r = df.loc[df['MPAA Rating'] == 'R']

# Save scatterplot of worldwide gross earnings as a function of budget
# to a .png file.
sns.scatterplot(x='Budget',y='Total Worldwide Gross Earnings',data=df)\
   .figure.savefig('budget_worldwide_gross_scatterplot.png')

# Verbose output
print('Saved scatterplot as \'budget_worldwide_gross_scatterplot.png\'.')

# Save scatterplot of worldwide gross earnings as a function of budget
# and with line of best fit to a .png file.
sns.lmplot('Budget','Total Worldwide Gross Earnings',
           data=df, fit_reg=True)\
   .savefig('budget_worldwide_gross_linreg.png')

# Verbose output
print('Saved \'budget_worldwide_gross_linreg.png\'.')

sns.lmplot('Budget','Total Worldwide Gross Earnings',
           data=df_g, fit_reg=True).savefig('earnings_g.png')

print('Saved \'earnings_g.png\'.') # Verbose output

sns.lmplot('Budget','Total Worldwide Gross Earnings',
           data=df_pg, fit_reg=True).savefig('earnings_pg.png')

print('Saved \'earnings_pg.png\'.') # Verbose output

sns.lmplot('Budget','Total Worldwide Gross Earnings',
           data=df_pg13, fit_reg=True).savefig('earnings_pg13.png')

print('Saved \'earnings_pg13.png\'.') # Verbose output

sns.lmplot('Budget','Total Worldwide Gross Earnings',
           data=df_r, fit_reg=True).savefig('earnings_r.png')

print('Saved \'earnings_r.png\'.') # Verbose output
