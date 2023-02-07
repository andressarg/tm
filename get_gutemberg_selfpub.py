
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
        with urlopen(urlpath, timeout=5) as connection:
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
1. METADADOS
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

# salvar os metadados
df.to_csv('output/self_pub.tsv', sep='\t', encoding='utf-8')

'''
2. BAIXAR OS LIVROS
'''
# pegar o link de download do livro
for l in df['link']:
    print(l)

    # formar o link
    # page_link = 'http://self.gutenberg.org/eBooks' + df['link'][0]
    page_link = 'http://self.gutenberg.org/eBooks' + l

    # baixar conteudo
    print(f"downloading {page_link}")
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
3. PDF 2 PLAIN TEXT
conversao para plain text
'''
from PyPDF2 import PdfReader
# https://pypdf2.readthedocs.io/en/stable/user/extract-text.html
import pathlib 

def get_file_list(files_path):
    '''
    create a list and append the files names to it
    '''
    workingDir = pathlib.Path(files_path)
    file_list = []
    for f in workingDir.iterdir():
        file_list.append(f)
    return file_list


file_list = get_file_list('input/self_pdf')

# for val in file_list:
    # pdf_reader = PdfReader(val)
    
    # pdf_text = ''

    # for n in range(len(pdf_reader.pages)):
    #     pdf_pages = pdf_reader.pages[n]
    #     pdf_text += pdf_pages.extract_text()

    # # write book content to file
    # with open(f"input/self_txt/{val.stem}.txt", 'w', encoding='utf-8') as file:
    #     file.write(pdf_text)



for val in file_list:
    pdf_reader = PdfReader(val)
    
    pdf_text = ''

    for n in range(len(pdf_reader.pages)):
        pdf_pages = pdf_reader.pages[n]
        try:
            pdf_text += pdf_pages.extract_text()
        except:
            print(f'error on page {n} of file: {val.stem}')
            continue

    # write book content to file
    try:
        with open(f"input/self_txt/{val.stem}.txt", 'w', encoding='utf-8') as file:
            file.write(pdf_text)
    except:
        print(f'error writing file {val.stem}')




