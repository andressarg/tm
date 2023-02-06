
""" @get_gutemberg_selfpub.py
This script downloads books from the Project Gutemberg Self-Publishing Press (http://self.gutenberg.org/Home),
extract the metadata for each book,
and saves:
- the original book file (pdf)
- the plain text (txt)
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



'''
Para baixar conteúdos de um site, usamos a funcao abaixo
'''

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




import requests
import os
def download_pdf_file(url):
    """Download PDF from given URL to local directory.

    :param url: The url of the PDF file to be downloaded
    :return: True if PDF file was successfully downloaded, otherwise False.
    """

    # Request URL and get response object
    response = requests.get(url, stream=True)

    # isolate PDF filename from URL
    pdf_file_name = os.path.basename(url)
    if response.status_code == 200:
        # Save in current working directory
        filepath = os.path.join(os.getcwd() + '/input', pdf_file_name)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{pdf_file_name} was successfully saved!')
            return True
    else:
        print(f'Uh oh! Could not download {pdf_file_name},')
        print(f'HTTP response status code: {response.status_code}')
        return False






'''
Para descobrir o que precisamos baixar do site,
realizei a busca manualmente em http://self.gutenberg.org/Home,
selecionando apenas livros em portugues.

A busca retornou 4 páginas de resultados.
O link para a página 1 é:
"http://self.gutenberg.org/Results.aspx?PageIndex=1&SearchCollection=Authors+Community&EverythingType=0&TitleType=0&AuthorType=0&SubjectType=0&PublisherType=0&LanguageDropDownValue=Portuguese&DisplayMode=List"

Para chegar nas outras páginas, basta alterar o número após PageIndex= para o número desejado

Precisamos salvar também os metadados desejados

textTitle
textAuthor
textPublisher
textId
textFormatType
textSubject
textCollections
textAbstracts

'''

# criar uma DF para salvar os metadados
df = pd.DataFrame(columns = ['bookid', 'title', 'author', 'lang', 'publisher', 'orgFormat', 'subj', 'collection', 'link'])

# estabelecer o numero de paginas
pages = [1, 2, 3, 4]

# ir pagina por pagina
for n in pages:
    val = f"http://self.gutenberg.org/Results.aspx?PageIndex={n}&SearchCollection=Authors+Community&EverythingType=0&TitleType=0&AuthorType=0&SubjectType=0&PublisherType=0&LanguageDropDownValue=Portuguese&DisplayMode=List"

    # baixar pagina
    page = download_url(val)
    print(f'getting page {n}')

    # html parser 
    soup = BeautifulSoup(page, 'html.parser')

    # pegar os metadados
    bookids    = soup.findAll('div', {'class': 'textId'})
    titles     = soup.findAll('div', {'class': 'textTitle'})
    authors    = soup.findAll('div', {'class': 'textAuthor'})
    publishers = soup.findAll('div', {'class': 'textPublisher'}) # tem dois
    srcformats = soup.findAll('div', {'class': 'textFormatType'})
    subjects   = soup.findAll('div', {'class': 'textSubject'})
    collects   = soup.findAll('div', {'class': 'textCollections'})

    # para cada livro identificado
    for i in range(len(bookids)):
        print(f'getting book {i+1} in page {n}')
        # criar uma lista com os metadados desejados
        # bookid, title, author, lang, publisher, orgFormat, subj, collection, link
        meta_list = [bookids[i].text, titles[i].text, authors[i].text, publishers[i*2].text, publishers[i*2 +1].text, srcformats[i].text, subjects[i].text, collects[i].text, bookids[i].a.attrs['href']]
        
        # remove line breaks, tabs and carriage returns
        meta_list = [sub.replace('\n', '') for sub in meta_list]
        meta_list = [sub.replace('\t', '') for sub in meta_list]
        meta_list = [sub.replace('\r', '') for sub in meta_list]

        # remove 'Book Id: ' from bookid
        meta_list[0] = meta_list[0][9:]

        # add list to DF
        df.loc[len(df)] = meta_list


df.to_csv('output/self_pub.tsv', sep='\t', encoding='utf-8')


# pegar o link de download do livro
for l in df['link']:
    print(l)

    # formar o link
    # page_link = 'http://self.gutenberg.org/eBooks' + df['link'][0]
    page_link = 'http://self.gutenberg.org/eBooks' + l

    # baixar conteudo
    page_book = download_url(page_link)

    # BS parser
    page_soup = BeautifulSoup(page_book, 'html.parser')

    # encontrar link para o pdf
    pdf_link1 = page_soup.find('iframe', {'id': 'bookViewer'}).attrs['src']
    pdf_link2 = re.search(r'.*file=\/uploads/pdf/(.*)', pdf_link1)[1]
    pdf_link3 = f'http://uploads.worldlibrary.net/uploads/pdf/{pdf_link2}'

    # baixar pdf
    download_pdf_file(pdf_link3)


'''
http://uploads.worldlibrary.net/uploads/pdf/20121014234847o_caminho_da_verdade_pdf.pdf
http://Uploads.WorldLibrary.org/uploads/userfiles/20121014235904o_caminho_da_verdade_jpg.jpg
'''


download_url("http://self.gutenberg.org/eBooks/eBooks/WPLBN0003468721-O-Mago-de-Camelot--A-saga-de-Merlin-para-coroar-um-drag-o-by-Hip-lito-Marcelo.aspx?&Words=")

from urllib.error import HTTPError




# getting the content
try:
    connection = urlopen("http://self.gutenberg.org/eBooks/eBooks/WPLBN0003468721-O-Mago-de-Camelot--A-saga-de-Merlin-para-coroar-um-drag-o-by-Hip-lito-Marcelo.aspx?&Words=")
    data_plain = connection.read()
    print(f'downloading ')
except HTTPError as err:
    print(err.code)


page_soup = BeautifulSoup(data_plain, 'html.parser')









######################àà
# teste
val = f"http://self.gutenberg.org/Results.aspx?PageIndex=2&SearchCollection=Authors+Community&EverythingType=0&TitleType=0&AuthorType=0&SubjectType=0&PublisherType=0&LanguageDropDownValue=Portuguese&DisplayMode=List"

# baixar pagina
page2 = download_url(val)

# parser 
soup = BeautifulSoup(page2, 'html.parser')

# get metadata

# bookid = soup.find('div', {'class': 'textId'}).text
# title = soup.find('div', {'class': 'textTitle'}).text
# author = soup.find('div', {'class': 'textAuthor'}).text
# publisher = soup.find('div', {'class': 'textPublisher'}).text # tem dois
# srcformat = soup.find('div', {'class': 'textFormatType'}).text
# subject = soup.find('div', {'class': 'textSubject'}).text
# collections = soup.find('div', {'class': 'textCollections'}).text
# bookpage = soup.find('div', {'class': 'textAbstracts'}).a.attrs['href']


bookids    = soup.findAll('div', {'class': 'textId'})
titles     = soup.findAll('div', {'class': 'textTitle'})
authors    = soup.findAll('div', {'class': 'textAuthor'})
publishers = soup.findAll('div', {'class': 'textPublisher'}) # tem dois
srcformats = soup.findAll('div', {'class': 'textFormatType'})
subjects   = soup.findAll('div', {'class': 'textSubject'})
collects   = soup.findAll('div', {'class': 'textCollections'})
# bookpages  = soup.findAll('div', {'class': 'textAbstracts'}).a.attrs['href']
# soup.findAll('div', {'class': 'textId'}).a.attrs['href']



# df = pd.DataFrame(columns = ['bookid', 'title', 'author', 'lang', 'publisher', 'orgFormat', 'subj', 'collection', 'link'])


# para cada livro identificado
for i in range(len(bookids)):
    # criar uma lista com os metadados desejados
    # bookid, title, author, lang, publisher, orgFormat, subj, collection, link
    lista = [bookids[i].text, titles[i].text, authors[i].text, publishers[i*2].text, publishers[i*2 +1].text, srcformats[i].text, subjects[i].text, collects[i].text, bookids[i].a.attrs['href']]
    
    # remove line breaks, tabs and carriage returns
    lista = [sub.replace('\n', '') for sub in lista]
    lista = [sub.replace('\t', '') for sub in lista]
    lista = [sub.replace('\r', '') for sub in lista]

    # remove 'Book Id: ' from bookid
    lista[0] = lista[0][9:]

    df.loc[len(df)] = lista


df.to_csv('output/self_pub.tsv', sep='\t', encoding='utf-8')

bookids[0].a.attrs['href']

count = 1
for i in publishers:
    print(count)
    print(i.text)
    count += 1





# # df.loc[book_id] = [book_id, meta_list[0], meta_list[1], meta_list[2], meta_list[3], meta_list[4]]
# df.loc[book_id] = [meta_list[0], meta_list[1], meta_list[2], meta_list[3], meta_list[4]]



for i in range(len(titles)):
    # print(bookids[i].text)
    # df.loc[len(df)] = [bookids[i].text, titles[i].text, authors[i].text, publishers[i].text, srcformats[i].text, subjects[i].text, collects[i].text]
    print([bookids[i].text, titles[i].text, authors[i].text, publishers[i].text, srcformats[i].text, subjects[i].text, collects[i].text])
    
    # pd.concat([new_row, df.loc[:]]).reset_index(drop=True)


df
bookids[0].text

lista = [bookids[i].text, titles[i].text, authors[i].text, publishers[i].text, publishers[i*2].text, srcformats[i].text, subjects[i].text, collects[i].text, 'link']
len(lista)
df
df.loc[len(df)] = lista






#div textTitle

#####################à
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

