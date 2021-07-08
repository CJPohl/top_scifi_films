# scraping top50 movie details from imdb and writing it to a csv

# imports for scraping and parsing
from bs4 import BeautifulSoup
import requests
import lxml

# import pandas for table creation and csv writing
import pandas as pd


# save url as a variable and execute get request
# change as needed
base_url = 'https://www.imdb.com'
url = 'https://www.imdb.com/search/title/?title_type=feature&genres=sci-fi&explore=genres'

# create data structure for data
data = {
'Rank': [],
'Title': [],
'Year': [],
'Rating': [],
'Runtime': [],
'Genre': [],
'User Rating': [],
'Metacritic': [],
}

def export_and_print():
    # use pandas to clean data and create table
    table = pd.DataFrame(data, columns=[
    'Rank',
    'Title',
    'Year',
    'Rating',
    'Runtime',
    'Genre',
    'User Rating',
    'Metacritic'])
    table.index = table.index + 1

    # create csv file with comma as separator
    # change filename as needed
    table.to_csv(f'topscifi.csv', sep=',', encoding='utf-8', index=False)
    print(table)
    return 0

def get_attributes(movie):
    # get attributes from html tags of choice
    # set conditions if object is NoneType
    rank = movie.find('h3', class_='lister-item-header').find('span',
     class_='lister-item-index unbold text-primary').text.replace('.', '')
    title = movie.find('h3', class_='lister-item-header').find('a').text
    year = movie.find('h3', class_='lister-item-header').find('span',
     class_='lister-item-year text-muted unbold').text
    year = year.replace('(', '').replace(')', '')
    if movie.find('p', class_='text-muted').find('span', class_='certificate') is not None:
        rating = movie.find('p', class_='text-muted').find('span', class_='certificate').text
    else:
        rating = ' '
    if movie.find('p', class_='text-muted').find('span', class_='runtime') is not None:
        runtime = movie.find('p', class_='text-muted').find('span', class_='runtime').text
    else:
        runtime = ' '
    genre = movie.find('p', class_='text-muted').find('span', class_='genre').text.rstrip().replace('\n', '')
    if movie.find('div', class_='ratings-bar') is not None:
        if movie.find('div', class_='ratings-bar').find('div', class_=
        'inline-block ratings-imdb-rating') is not None:
            user_rating = movie.find('div', class_='ratings-bar').find('div', class_=
            'inline-block ratings-imdb-rating').find('strong').text
        else:
            user_rating = ' '
    else:
        user_rating = ' '
    if movie.find('div', class_='ratings-bar') is not None:
        if movie.find('div', class_='ratings-bar').find('div', class_=
        'inline-block ratings-metascore') is not None:
            metacritic = movie.find('div', class_='ratings-bar').find('div', class_=
            'inline-block ratings-metascore').find('span').text.rstrip()
        else:
            metacritic = ' '
    else:
        metacritic = ' '

    # store data
    data['Rank'].append(rank)
    data['Title'].append(title)
    data['Year'].append(year)
    data['Rating'].append(rating)
    data['Runtime'].append(runtime)
    data['Genre'].append(genre)
    data['User Rating'].append(user_rating)
    data['Metacritic'].append(metacritic)

def parse_page(next_url):
    page = requests.get(next_url)
    # check if get requests returns 200 code and parse with bs/lxml
    if page.status_code == requests.codes.ok:
        bs = BeautifulSoup(page.text, 'lxml')

        # select elements from html
        all_movies = bs.findAll('div', class_='lister-item mode-advanced')

        for movie in all_movies:
            get_attributes(movie)

        # off to next page 40 other times
        if bs.find('a', class_='lister-page-next next-page') is not None:
            next_page = bs.find('a', class_=
            'lister-page-next next-page').text.replace(' »', '')
        else:
            next_page = 'Null'
        if next_page == 'Next':
            partial_url = bs.find('a', class_=
            'lister-page-next next-page')['href']
            next_page_url = base_url + partial_url
            print(f'Parsing {next_page_url}...')
            parse_page(next_page_url)
        else:
            export_and_print()

parse_page(url)
