"""
Replicability and transparency in topic modelling: developing best practice guidelines for the digital humanities
Copyright (c) 2023 [Andressa Gomide, Mathew Gillings, Diego Gimenez]
This file is part of Gomide et al. 2023.
This project is licensed under the terms of the MIT license.
"""

""" @get_gutemberg
This script download books from the Gutemberg Project (https://www.gutenberg.org/), 
removes unecessary elements (e.g. boilerplates, page numbers),
extract the metadata for each book
and saves:
- the original book file (html)
- the cleaned content (txt)
- the metadata (tsv)


Functions in this file
    * download_url - it takes an argument: 
    a string with with url path
    and returns the content of the url as bytes
"""

# import libraries
import re # for regular expressions
from urllib.request import urlopen # to request the content from the internet
from bs4 import BeautifulSoup # to work with html files (bs4 is known to be user friendly)
import pandas as pd # to store metadata as dataframe

def download_url(urlpath):
    ''' 
    download content from an url address
    Args: 
        urlpath (str): the url path
    Returns:
        connection.read() (bytes): the content of the page 
    '''
    try:
        # open a connection to the server
        with urlopen(urlpath, timeout=3) as connection:
            # return content of the url read as bytes
            return connection.read()
    except:
        # return None
        print(f"There was an issue when trying to download{urlpath}")


# create a list with the books id

# book_id = "44540" # cinco minutos j de alencar
# book_id = "55682" # quincas borba machado
# book_id = "31971" # o crime do padre amaro eca de queiros

book_id_list = ["44540", "55682", "31971"]


'''
- sometimes the same data content is available in different formats. it is a good idea to test extracting two different formats to get an idea which one will be better for the project.
- it is almost always easier to work with plain text, but preserving section breaks can lead to further analysis
- in our case, getting the data from html format sounds better and easier to (a) preserve the sections boundaries (b) to make cleaning easier
'''

# to get the books from the plain format

# create empty df to store the metadata

df = pd.DataFrame(columns = ['author', 'title', 'lang', 'subj', 'datepub'])

for book_id in book_id_list:
    # url for plain text book
    url_plain = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'

    # download the content
    data_plain = download_url(url_plain)

    # plain text link doesnt include metadata. 
    # we have to go to the previous page
    url_meta = f'https://www.gutenberg.org/ebooks/{book_id}'
    metadata = download_url(url_meta)

    # parse document 
    soup = BeautifulSoup(metadata, 'html.parser')

    # get metadata
    author = soup.find('a', {'about': re.compile(r'\/authors\/.*')}).text
    lang = soup.find('a', {'href': re.compile(r'\/browse\/languages\/.*')}).text
    subj = soup.find('a', {'href': re.compile(r'\/ebooks\/subject\/*')}).text
    title = soup.find('td', {'itemprop': 'headline'}).text
    datepub = soup.find('td', {'itemprop': 'datePublished'}).text

    # remove line breaks
    meta_list = [sub.replace('\n', '') for sub in [author, title, lang, subj, datepub]]


    # df.loc[book_id] = [book_id, meta_list[0], meta_list[1], meta_list[2], meta_list[3], meta_list[4]]
    df.loc[book_id] = [meta_list[0], meta_list[1], meta_list[2], meta_list[3], meta_list[4]]

    # write book content to file
    with open(f"input/plain/{book_id}.txt", 'wb') as file:
        file.write(data_plain)


# write metadata to file
df.to_csv('output/books_metadata.tsv', sep='\t', encoding='utf-8')
    





# to get the books from html
# create empty df to store the metadata

df = pd.DataFrame(columns = ['author', 'title', 'lang', 'subj', 'datepub'])

for book_id in book_id_list:
    url_html = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html'
    data_html = download_url(url_html)

    # parse
    soup = BeautifulSoup(data_html, 'html.parser')

    # get metadata
    author = soup.find('meta', {'name' : 'AUTHOR'})['content']
    lang = soup.find('meta', {'name' : 'dc.language'})['content']
    subj = soup.find('meta', {'name' : 'dc.subject'})['content']
    title = soup.find('meta', {'property' : 'og:title'})['content']
    datepub = soup.find('meta', {'name' : 'dcterms.created'})['content']

    ## remove unnecessary elements
    # style
    for i in soup.find_all('style'):
        i.decompose()

    # boiler plates
    for i in soup.find_all('section', {'class': re.compile('.*boilerplate.*')}):
        i.decompose()

    # editor comments
    for i in soup.find_all('div', {'class': 'fbox'}):
        i.decompose()

    # page numbers
    for i in soup.find_all('span', {'class': 'pagenum'}):
        i.decompose()

    # remove br tags
    for i in soup.find_all('br'):
        i.unwrap()

    # remove head
    soup.find('head').decompose()

    # get metadata
    df.loc[book_id] = [author, title, lang, subj, datepub]


    # write to file with tags
    with open(f'input/{book_id}.html', 'w', encoding = 'utf-8') as file:
        file.write(str(soup.prettify()))
    # write to file without tags
    with open(f'input/{book_id}.txt', 'w', encoding = 'utf-8') as file:
        file.write(soup.text)




# parse
soup = BeautifulSoup(data_html, 'html.parser')

# get metadata
author = soup.find('meta', {'name' : 'AUTHOR'})
lang = soup.find('meta', {'name' : 'dc.language'})
subj = soup.find('meta', {'name' : 'dc.subject'})
title = soup.find('meta', {'property' : 'og:title'})
datepub = soup.find('meta', {'name' : 'dcterms.created'})


for i in [author, lang, subj, title, datepub]:
    try:
        i = i['content']
    except:
        i = 'NA'





with open(f'input/{book_id}.html', 'w', encoding = 'utf-8') as file:
    file.write(str(soup.prettify()))

