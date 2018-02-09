#!/usr/bin/env python
# Name: Rolf Hofsink
# Student number: 11422831
"""
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
"""
import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    """
    Extract a list of highest rated TV series from DOM (of IMDB page).
    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """
    
    tvseries = []
    #search per movie
    find = dom.find_all('div', class_ = 'lister-item mode-advanced')
    findlength = len(find)

    #iterate over the movies
    for i in range(findlength):
        #find moviename
        movie = find[i]
        moviename = movie.h3.a.text

        #find ratings
        rating = float(movie.strong.text)

        #find genres
        genre = movie.find('span', class_ = 'genre').get_text(strip=True)

        #find runtime
        runtime = movie.find('span', 'runtime').contents[0]

        #find actors
        actors = movie.find('p', 'a', class_="")
        actors2 = actors.find_next_sibling('p', 'a', class_="").text[25:] 

        #copy the results to a list 
        tvseries.append([moviename, genre, runtime, rating, actors2])
        
    

    return tvseries

  
    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED TV-SERIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.



def save_csv(outfile, tvseries):
    """
    Output a CSV file containing highest rated TV-series.
    """
    #call the previous def
    tvseries = extract_tvseries(dom)

    #write the results to csv file
    writer = csv.writer(outfile)
    writer.writerow(['Title', 'Genre', 'Runtime', 'Rating', 'Actors'])
    for i in range(50):
        writer.writerow(tvseries[i])
        
  

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE TV-SERIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, tvseries)