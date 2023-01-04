"""
Replicability and transparency in topic modelling: developing best practice guidelines for the digital humanities
Copyright (c) 2023 [Andressa Gomide, Mathew Gillings, Diego Gimenez]
This file is part of Gomide et al. 2023.
This project is licensed under the terms of the MIT license.
"""

""" @get_gutemberg.py
This script downloads books from the Gutemberg Project (https://www.gutenberg.org/), 
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
from urllib.error import HTTPError # to raise errors when connecting to the sites
from bs4 import BeautifulSoup # to work with html files (bs4 is known to be user friendly)
import pandas as pd # to store metadata as dataframe

# def download_url(urlpath):
#     ''' 
#     download content from an url address
#     Args: 
#         urlpath (str): the url path
#     Returns:
#         connection.read() (bytes): the content of the page 
#     '''
#     try:
#         # open a connection to the server
#         with urlopen(urlpath, timeout=3) as connection:
#             # return content of the url read as bytes
#             return connection.read()
#     except:
#         # return None
#         print(f"There was an issue when trying to download{urlpath}")

def download_url(urlpath):
    ''' 
    download content from an url address
    Args: 
        urlpath (str): the url path
    Returns:
        connection.read() (bytes): the content of the page 
    '''
    # open a connection to the server
    with urlopen(urlpath, timeout=3) as connection:
        # return content of the url read as bytes
        return connection.read()

# create a list with the books id

# book_id = "44540" # cinco minutos j de alencar
# book_id = "55682" # quincas borba machado
# book_id = "31971" # o crime do padre amaro eca de queiros
# book_id_list = ["44540", "55682", "31971"]

'''
54829   Memorias Posthumas de Braz Cubas
55682   Quincas Borba
55752   Dom Casmurro
55797   Memorial de Ayres
56737   Esau e Jacob
57001   Papeis Avulsos
67935   Reliquias de Casa Velha
33056   Historias Sem Data
53101   A Mao e A Luva
67162   Helena
67780   Yayá Garcia
61653   Poesias Completas
'''


book_id_list = ["54829", "55682", "55752", "55797", "56737", "57001", "67935", "33056", "53101", "67162", "67780", "61653"]


'''
- sometimes the same data content is available in different formats. it is a good idea to test extracting two different formats to get an idea which one will be better for the project.
- it is almost always easier to work with plain text, but preserving section breaks can lead to further analysis
- in our case, getting the data from html format sounds better and easier to (a) preserve the sections boundaries (b) to make cleaning easier
'''

# to get the books from the plain format

# create empty df to store the metadata

df = pd.DataFrame(columns = ['author', 'title', 'lang', 'subj', 'datepub'])

for book_id in book_id_list:
    # # url for plain text book
    # url_plain = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'

    # # download the content
    # print(f'downloading content for {book_id}...')
    # data_plain = download_url(url_plain)

    # getting the content
    try:
        connection = urlopen(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
        data_plain = connection.read()
        print(f'downloading data for {book_id}, from link 1')
    except HTTPError as err:
        if err.code == 404: # not found error (link doesnt exist)
            connection = urlopen(f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt')
            data_plain = connection.read()
            print(f'downloading data for {book_id}, from link 2')
        else:
            print(f'error {err.code} when downloading file {book_id}')
            continue

    # plain text link doesnt include metadata. 
    # we have to go to the previous page
    # TODO add try exept to metadata 
    # if it doesnt exist, add NA to the respective row
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
    with open(f"input/{book_id}.txt", 'wb') as file:
        file.write(data_plain)


# write metadata to file
df.to_csv('output/books_metadata.tsv', sep='\t', encoding='utf-8')
    
###############à
# teste comeca
book_id = '55797'
url_plain = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'
# TODO add an try excep here
url_plain = f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt'
data_plain = download_url(url_plain)



def download_url(urlpath):
    with urlopen(urlpath, timeout=3) as connection:
        # return content of the url read as bytes
        return connection.read()


a = download_url(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')





from urllib.error import HTTPError




try:
    a = urlopen(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
    b = a.read()
    print('first')
except HTTPError as err:
    if err.code == 404: # not found error (link doesnt exist)
        a = urlopen(f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt')
        b = a.read()
        print('second')
    else:
        print(f'error {err.code} when downloading file')





for book_id in book_id_list:

    # getting the content
    try:
        connection = urlopen(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
        data_plain = connection.read()
        print(f'downloading data for {book_id}, from link 1')
    except HTTPError as err:
        if err.code == 404: # not found error (link doesnt exist)
            connection = urlopen(f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt')
            data_plain = connection.read()
            print(f'downloading data for {book_id}, from link 2')
        else:
            print(f'error {err.code} when downloading file {book_id}')
            continue

    
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
    with open(f"input/{book_id}.txt", 'wb') as file:
        file.write(data_plain)

df

# https://www.gutenberg.org/cache/epub/54829/pg54829.txt
# https://www.gutenberg.org/files/54829/54829-0.txt
# https://www.gutenberg.org/files/55797/55797-0.txt

# teste termina
###########àà####

# to get the books from html
# create empty df to store the metadata

df = pd.DataFrame(columns = ['author', 'title', 'lang', 'subj', 'datepub'])

for book_id in book_id_list:
    url_html = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}-images.html'
    data_html = download_url(url_html)

    # parse
    soup = BeautifulSoup(data_html, 'html.parser')

    # get metadata
    author = soup.find('meta', {'name' : 'AUTHOR'})['content'] if soup.find('meta', {'name' : 'AUTHOR'}) is not None else 'NA'
    lang = soup.find('meta', {'name' : 'dc.language'})['content'] if soup.find('meta', {'name' : 'dc.language'}) is not None else 'NA'
    subj = soup.find('meta', {'name' : 'dc.subject'})['content'] if soup.find('meta', {'name' : 'dc.subject'}) is not None else 'NA'
    title = soup.find('meta', {'property' : 'og:title'})['content'] if soup.find('meta', {'property' : 'og:title'}) is not None else 'NA'
    datepub = soup.find('meta', {'name' : 'dcterms.created'})['content'] if soup.find('meta', {'name' : 'dcterms.created'}) is not None else 'NA'

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
    with open(f'input/html/{book_id}.html', 'w', encoding = 'utf-8') as file:
        file.write(str(soup.prettify()))
    # write to file without tags
    with open(f'input/plain/{book_id}.txt', 'w', encoding = 'utf-8') as file:
        file.write(soup.text)


# write metadata to file
df.to_csv('output/books_metadata.tsv', sep='\t', encoding='utf-8')

