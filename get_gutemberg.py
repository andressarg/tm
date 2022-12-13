"""
get text straight from gutemberg
look at:
- https://pypi.org/project/Gutenberg/
- https://superfastpython.com/threadpoolexecutor-download-books/
- 
"""
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup # chose this libary for its user friendliness

'''
download content
'''
def download_url(urlpath):
    try:
        # open a connection to the server
        with urlopen(urlpath, timeout=3) as connection:
            # return content of the url read as bytes
            return connection.read()
    except:
        # return None
        print(f"There was an issue when trying to download{urlpath}")


# set the book id
book_id = "44540" # cinco minutos j de alencar
book_id = "55682" # quincas borba machado
book_id = "31971" # o crime do padre amaro eca de queiros
##########################
# from plain text
# url for plain text book
url_plain = f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt'

# download the content
data_plain = download_url(url_plain)

# plain text link doesnt include metadata. we have to go to the previous page
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

# write content to file
with open(f"input/book{book_id}.txt", 'wb') as file:
    file.write(data_plain)

# TODO
# write metadata


##########################
# from html
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


# write to file with tags
with open(f'input/book{book_id}.html', 'w', encoding = 'utf-8') as file:
    file.write(str(soup.prettify()))

with open(f'input/book{book_id}_fromhtml.txt', 'w', encoding = 'utf-8') as file:
    file.write(soup.text)