# Michael J. Franco, Jr.
# September 18, 2019
#
# Scraper tool for retrieving data from the Internet Movie Database website.
# Data sought will include release date, box office revenue, and ratings.
# The data will then be analyzed to see if there are any clear patterns that
# emerge showing correlations between these data points.  This algorithm will
# use the HTML code present in the webpage to determine which elements to
# scrape.

import requests
import urllib.request
import time
import pandas as pd
from bs4 import BeautifulSoup
import pickle
import re

# Set the URLs for collecting the links to the 100 highest-grossing
# films for each year from 2009 to 2018 listed on the IMDb website.
# This is done by first creating the list of strings url[] and then
# setting the value of each element to the string representing the
# respective URL.
#
# NB: IMDb only shows 50 results per page, so there are 2 links for
# each year of movies.

# Create the list url[] with 20 elements.
url = [None] * 20

# 2018
url[0] = 'https://www.imdb.com/search/title/?title_type=feature&year=2018-01-01,2018-12-31&sort=boxoffice_gross_us,desc'
url[1] = 'https://www.imdb.com/search/title/?title_type=feature&year=2018-01-01,2018-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2017
url[2] = 'https://www.imdb.com/search/title/?title_type=feature&year=2017-01-01,2017-12-31&sort=boxoffice_gross_us,desc'
url[3] = 'https://www.imdb.com/search/title/?title_type=feature&year=2017-01-01,2017-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2016
url[4] = 'https://www.imdb.com/search/title/?title_type=feature&year=2016-01-01,2016-12-31&sort=boxoffice_gross_us,desc'
url[5] = 'https://www.imdb.com/search/title/?title_type=feature&year=2016-01-01,2016-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2015
url[6] = 'https://www.imdb.com/search/title/?title_type=feature&year=2015-01-01,2015-12-31&sort=boxoffice_gross_us,desc'
url[7] = 'https://www.imdb.com/search/title/?title_type=feature&year=2015-01-01,2015-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2014
url[8] = 'https://www.imdb.com/search/title/?title_type=feature&year=2014-01-01,2014-12-31&sort=boxoffice_gross_us,desc'
url[9] = 'https://www.imdb.com/search/title/?title_type=feature&year=2014-01-01,2014-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2013
url[10] = 'https://www.imdb.com/search/title/?title_type=feature&year=2013-01-01,2013-12-31&sort=boxoffice_gross_us,desc'
url[11] = 'https://www.imdb.com/search/title/?title_type=feature&year=2013-01-01,2013-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2012
url[12] = 'https://www.imdb.com/search/title/?title_type=feature&year=2012-01-01,2012-12-31&sort=boxoffice_gross_us,desc'
url[13] = 'https://www.imdb.com/search/title/?title_type=feature&year=2012-01-01,2012-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2011
url[14] = 'https://www.imdb.com/search/title/?title_type=feature&year=2011-01-01,2011-12-31&sort=boxoffice_gross_us,desc'
url[15] = 'https://www.imdb.com/search/title/?title_type=feature&year=2011-01-01,2011-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2010
url[16] = 'https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2010-12-31&sort=boxoffice_gross_us,desc'
url[17] = 'https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2010-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# 2009
url[18] = 'https://www.imdb.com/search/title/?title_type=feature&year=2009-01-01,2009-12-31&sort=boxoffice_gross_us,desc'
url[19] = 'https://www.imdb.com/search/title/?title_type=feature&year=2009-01-01,2009-12-31&sort=boxoffice_gross_us,desc&start=51&ref_=adv_nxt'

# Each webpage linked to by each element of url[] is itself just a list
# of movies, ranked by box office revenue, and each of those listings
# contains another link, this time to the IMDb page with information about
# the individual movie.  The next step is to iterate through url[] and
# collect and follow these links, after which we scrape the information
# for each movie.

base_url = 'https://www.imdb.com'

movie_link_list = [] # List of webpages to be scraped for movie data

movie_features = []  # List of tuples returned by the getMovieData() function,
                     # which will then be converted to a pandas dataframe for
                     # analasys.

unscraped_pages = [] # A list of pages that did not scrape properly on the
                     # first pass.  They will be attempted one more time
                     # after the other pages have been scraped.

i = 0                # Index value for use in the while loop below.

# Verbose output
print('Initiating movie URL collection...')

# Iterate through the list of URLs 
while(i < len(url)):
    # Obtain the response to the request for the URLs from above (response
    # 200 means the request was successful).  The HTML contents of the page
    # can be found in page_response.text
    page_response = requests.get(url[i])

    # Convert the HTML code found in page_response.text to a BeautifulSoup
    # object, which makes for easier web scraping
    page_soup = BeautifulSoup(page_response.text, 'html.parser')

    # Create a list of tags which contain the link subdirectory for the movie
    # to be scraped.
    link_list = page_soup.find_all('span', class_='lister-item-index unbold text-primary')

    i += 1 # Increment the index for the current loop
    
    j = 0  # Index for the nested while loop below.

    # For each film listed on the page stored in url[i],
    # pull the link to that particular film and store it
    # in the list 'movie_link_list'.
    while(j < len(link_list)):
        # The tag that includes the string for the
        # page related to the movie.
        link_subdirectory_tag = link_list[j].find_next_sibling()

        # Pull the specific string for the link subdirectory
        # out of the tag.
        link_subdirectory = link_subdirectory_tag['href']

        # Append the string for the link subdirectory
        # to the base url 'https://www.imdb.com',
        # which assigns the full URL string to the
        # variable 'movie_link'.
        movie_link = base_url + link_subdirectory

        # Append the string value of 'movie_link' to the list
        # movie_link_list[].  This will be the list of pages
        # that will be scraped for movie data in the next
        # part of this program.
        movie_link_list.append(movie_link)

        # Verbose output: confirm each time 50 movie URLs have
        # been scraped.
        if((j+1) % 50 == 0):
            scraped_url_count = (j + 1) * (i + 1) # Number of URLs scraped
            total_url_count = len(url) * 50       # Total length of url[]

            # Verbose output
            print('Collected {} out of {} URLs.'\
                  .format(scraped_url_count, total_url_count)
                  )
            
        j += 1 # Increment the index of the current nested loop.
        
def getMPAArating(movie_soup):
    '''
    Take the BeautifulSoup object movie_soup
    and extract the MPAA rating string from
    the object by stripping away extraneous
    information and whitespace until the only
    thing left is the rating.
    '''

    # Extract the tag soup containing the title block
    # of the page.
    rating_soup = movie_soup.find('div', class_='subtext').text
    
    rating = str(rating_soup)       # Convert the tag soup to a string
                                              
    rating = re.sub('\n','',rating) # Remove newline characters because Regex
                                    # does not define the wildcard '.' so as
                                    # to include '\n'.
                                              
    rating = re.sub('\|.*','',rating).strip() # Capture the remaining
                                              # characters from the beginning
                                              # of what's left of the string
                                              # to the first pipe, and then
                                              # strip away the whitespace.

    return rating

def getMovieBudget(movie_soup):
    '''
    Use regex to strip non-numerical characters
    out of the budget string and then use int()
    to convert it to an integer.
    '''

    # Navigate to the section that contains box
    # office information.
    box_office_soup = movie_soup.find('h3', class_='subheading')\
                                .find_next_sibling()

    budget = re.sub('\n','',box_office_soup.text)  # Use regex to strip the
    budget = re.sub('.*\$','',budget)              # budget value down to
    budget = re.sub(',','',budget)                 # numerical characters.
    budget = re.sub('\(estimated\)','',budget).strip()

    budget = int(budget) # Convert the budget value from a string
                         # to an integer.

    return budget

def fetchOpeningWeekendGross(movie_soup):
    '''
    Obtain the opening weekend gross revenue.
    '''

    box_office_soup = movie_soup.find('h3', class_='subheading')\
                                .find_next_sibling()\
                                .find_next_sibling()

    # Remove the first newline character in order to enable other
    # irrelevant information to be more easily removed.
    opening_weekend_gross = re.sub('\nO','',box_office_soup.text)

    opening_weekend_gross = re.search('.*',opening_weekend_gross)
    opening_weekend_gross = str(opening_weekend_gross)
    opening_weekend_gross = re.sub('.*\$','',opening_weekend_gross)
    opening_weekend_gross = re.sub('[^0-9]','',opening_weekend_gross)

    opening_weekend_gross = int(opening_weekend_gross) # Convert opening
                                                       # weekend gross string
                                                       # to integer.

    return opening_weekend_gross

def fetchReleaseMonth(movie_soup):
    '''
    After finding the section of the page containing
    the release month, the re.search() function is
    used to search for the string for each month.  If
    the name of the month is found, that is the movie's
    release month and its respective string value is
    returned.
    '''

    # Obtain the section of the page containing the release date.
    release_date = movie_soup.find('div', class_='subtext')\
                             .find(title='See more release dates').text

    # Each if() statement corresponds to a release month.  If that string
    # has a match within the section of the page found in release_date,
    # this function will return the string for that month.
    if(re.search('January', release_date) != None):
        return 'January'
    if(re.search('February', release_date) != None):
        return 'February'
    if(re.search('March', release_date) != None):
        return 'March'
    if(re.search('April', release_date) != None):
        return 'April'
    if(re.search('May', release_date) != None):
        return 'May'
    if(re.search('June', release_date) != None):
        return 'June'
    if(re.search('July', release_date) != None):
        return 'July'
    if(re.search('August', release_date) != None):
        return 'August'
    if(re.search('September', release_date) != None):
        return 'September'
    if(re.search('October', release_date) != None):
        return 'October'
    if(re.search('November', release_date) != None):
        return 'November'
    if(re.search('December', release_date) != None):
        return 'December'

def getMovieData(movie_url):
    '''
    This function takes an IMDb URL as an
    argument and scrapes the page for movie
    attributes.
    '''

    # Obtain a response object for the IMDb page of the individual movie.
    movie_response = requests.get(movie_url)

    # Convert the response object for the page to a BeautifulSoup object.
    movie_soup = BeautifulSoup(movie_response.text, 'html.parser')

    # Get the MPAA rating of the movie.
    mpaa_rating = getMPAArating(movie_soup)

    # Set dummy variables initially to 0.
    dummy_g = 0
    dummy_pg = 0
    dummy_pg13 = 0
    dummy_r = 0

    # Now set the dummy variable that corresponds to rating to 1.
    if(mpaa_rating == 'G'):
        dummy_g = 1
    if(mpaa_rating == 'PG'):
        dummy_pg = 1
    if(mpaa_rating == 'PG-13'):
        dummy_pg13 = 1
    if(mpaa_rating == 'R'):
        dummy_r = 1
        
    release_month = fetchReleaseMonth(movie_soup) # Obtain the string value
                                                  # of the release month
                                                  
    # Set dummy variables for months of the year to 0
    jan_dummy = 0
    feb_dummy = 0
    mar_dummy = 0
    apr_dummy = 0
    may_dummy = 0
    jun_dummy = 0
    jul_dummy = 0
    aug_dummy = 0
    sep_dummy = 0
    oct_dummy = 0
    nov_dummy = 0
    dec_dummy = 0

    # Based on the value of the string release_month, set the corresponding
    # dummy variable to 1.
    if(release_month == 'January'):
        jan_dummy = 1
    if(release_month == 'February'):
        feb_dummy = 1
    if(release_month == 'March'):
        mar_dummy = 1
    if(release_month == 'April'):
        apr_dummy = 1
    if(release_month == 'May'):
        may_dummy = 1
    if(release_month == 'June'):
        jun_dummy = 1
    if(release_month == 'July'):
        jul_dummy = 1
    if(release_month == 'August'):
        aug_dummy = 1
    if(release_month == 'September'):
        sep_dummy = 1
    if(release_month == 'October'):
        oct_dummy = 1
    if(release_month == 'November'):
        nov_dummy = 1
    if(release_month == 'December'):
        dec_dummy = 1

    # The movie title being scraped from the page
    title = movie_soup.find('div', class_='subtext')\
                      .find_previous_sibling().text.strip()

    
    # The runtime of the movie.  This is found by taking the
    # second element on the page tagged on the page as 'time'
    # and then using regex to strip all non-numeric values from
    # the string.  The regex function is itself passed into the
    # int() function, leaving 'runtime' as an integer value of
    # the runtime of the movie in minutes.
    tech_spec_soup = movie_soup.find_all('time')[1]
    runtime = int(re.sub('[^0-9]','',tech_spec_soup.text))

    # Obtain the budget of the movie.
    budget = getMovieBudget(movie_soup)

    # opening_weekend_gross is opening weekend gross
    opening_weekend_gross = fetchOpeningWeekendGross(movie_soup)

    # Fetch total domestic gross revenue for movie.
    box_office_soup = movie_soup.find('h3', class_='subheading')\
                                .find_next_sibling()\
                                .find_next_sibling()\
                                .find_next_sibling()

    # Strip non-numeric characters from string and convert what remains
    # to integer.
    total_domestic_gross = int(re.sub('[^0-9]','',box_office_soup.text))

    # Obtain the worldwide gross
    box_office_soup = movie_soup.find('h3', class_='subheading')\
                                .find_next_sibling()\
                                .find_next_sibling()\
                                .find_next_sibling()\
                                .find_next_sibling()

    # Strip non-numeric characters from worldwide gross string and then
    # convert to integer value.
    worldwide_gross = int(re.sub('[^0-9]','',box_office_soup.text))

    # Obtain the user ratings of the movie
    rating_soup = movie_soup.find('div', class_='ratingValue')
    user_rating = re.sub('\n','',rating_soup.text)
    user_rating = float(re.sub('/.*','',user_rating))

    # The features to be analyzed are stored in a tuple, which
    # will be returned by the function and then appended to a
    # list which will be converted to a dataframe.
    feature_tuple = (title, release_month, mpaa_rating, dummy_g,
                     dummy_pg, dummy_pg13, dummy_r, jan_dummy,
                     feb_dummy, mar_dummy, apr_dummy, may_dummy,
                     jun_dummy, jul_dummy, aug_dummy, sep_dummy,
                     oct_dummy, nov_dummy, dec_dummy, runtime,
                     budget, opening_weekend_gross,
                     total_domestic_gross, worldwide_gross,
                     user_rating)

    return feature_tuple

i = 0
scraped_movie_count = 0
failed_scrapes = 0

total_movie_count = len(movie_link_list)

# Verbose output
print('Initiating scraping process...')

# Now for the fun part: scraping the actual movie
# data from the individual movie webpages.
while(i < len(movie_link_list)):

    # Error handling.  If anything goes wrong in the getMovieData()
    # function, the exception is handled so that it doesn't derail the
    # whole algorithm and force the scraping process to be restarted.
    try:
        movie_tuple = getMovieData(movie_link_list[i])

        movie_features.append(movie_tuple)

        # Verbose output
        scraped_movie_count += 1
        print('Scraped movie {} of {}.'.format(i+1, total_movie_count))
    
    except:
        failed_scrapes += 1

        # Verbose output
        print('Failed to scrape movie {} of {}.'.format(i+1, total_movie_count))
    
    i += 1

# Verbose output showing how many pages were able to be scraped and also
# how many failed.
print('Successfully scraped {} out of {} movies.  {} pages failed to scrape.'\
      .format(scraped_movie_count, total_movie_count, failed_scrapes))

# Take the list movie_features and convert to a pandas dataframe.
df = pd.DataFrame(movie_features)

# Pickle the dataframe so that it can simply be read into another file
# without having to re-scrape IMDb each time I want to tweak something!
df.to_pickle('movie_dataframe.pkl')
