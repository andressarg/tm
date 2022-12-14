# import libraries
import spacy
# import re
import utilsNLP
import pandas as pd
from gensim.corpora.dictionary import Dictionary
# from gensim.models import LdaMulticore
# import importlib
# import pyLDAvis.gensim_models
# import pyLDAvis

# from pprint import pprint


# load language model
# for tests, i'm using the small model
nlp = spacy.load('pt_core_news_sm')

# get list with files
# i think its better to separate the notebook in 2/3 different files, according to their function
# the folder input has the files prepared with gutemberg
file_list = utilsNLP.get_file_list('input')


# Cleaning
# list of POS to be removed
# we can add here our own
# stop list
# and use the NER to remove name of places
removal= ['PUNCT', 'DET', 'SPACE', 'NUM', 'SYM']

# create empty df
df = pd.DataFrame(columns = ['tokens'])


for val in file_list:
    # read file
    with open(val, 'r', encoding='utf-8') as f:
        text_org = f.read()
    
    # apply model
    nlp_text = nlp(text_org)

    # TODO consider creating different bags of words (with stop words, without NER names, etc...)

    # get all tokens that are not in the removel list neither in the stop list and that is alpha
    tok = [token.lemma_.lower() for token in nlp_text if token.pos_ not in removal and not token.is_stop and token.is_alpha]

    df.loc[val.stem] = [tok]


# map each token to a unique ID (applying the Dictionary Object from Gensim)
dictionary = Dictionary(df['tokens'])

# see toknes and ids
print(dictionary.token2id)


# filter dictionary
# dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=1000)
dictionary.filter_extremes(no_below=1, no_above=0.8, keep_n=None)
'''
no_below: remove tokens that appear in less than n documents
no_above: remove tokens that appear in more than n% of the corpus
keep_n: keep the N most frequent token (‘None’ keeps all)
'''