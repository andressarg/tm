# import libraries
import spacy
#import re
import utilsNLP
import pandas as pd
#from gensim.corpora.dictionary import Dictionary
# from gensim.models import LdaMulticore
# import importlib
# import pyLDAvis.gensim_models
# import pyLDAvis
# from pprint import pprint


# load language model
# for tests, i'm using the small model
nlp = spacy.load('pt_core_news_sm')

# get list with files
# the folder input has the files prepared with @get_gutemberg.py
file_list = utilsNLP.get_file_list('input')


# Cleaning
# list of elements to be removed
# we can add here our own
pos_rm = ['PUNCT', 'DET', 'SPACE', 'NUM', 'SYM']
ner_rm = ['PER', 'LOC']
wrd_rm = ['ella', 'elle']

# create empty df to store the different bows
df = pd.DataFrame(columns = ['all_tokens', 'full_clean', 'custom_tok'])


for val in file_list:
    # read file
    with open(val, 'r', encoding='utf-8') as f:
        text_org = f.read()
    
    # remove line breaks
    text_oneline = text_org.replace("\n", " ")

    # apply model
    nlp_text = nlp(text_org)

    # create a list to store the NER labes to be 
    ne2rm = []
    for ent in nlp_text.ents:
        if ent.label_ in ner_rm:
            ne2rm.append(ent.text.lower())

    # get lis of unique values for the ner found
    ne2rm = list(set(ne2rm))

    # other possibilities
    # - remove numbers, but not words that contain numbers...
    # - Remove words that are only one character...

    # # get all tokens that are not in the removel list neither in the stop list and that is alpha
    # tok = [token.lemma_.lower() for token in nlp_text if token.pos_ not in pos_rm and not token.is_stop and token.is_alpha]

    # all tokens (no space)
    all_tokens = [token.text.lower() for token in nlp_text if token.pos_ != 'SPACE']

    # get all lemma that are not in the removel list neither in the stop list and that is alpha (not letters)
    full_clean = [token.lemma_.lower() for token in nlp_text if token.pos_ not in pos_rm and not token.is_stop and token.is_alpha]

    # remove locations and named person/family
    # custom_tok = [token.text.lower() for token in nlp_text if token.text.lower() not in ne2rm and token.pos_ != 'SPACE']
    custom_tok = [token.text.lower() for token in nlp_text if token.text.lower() not in ne2rm and token.text.lower() not in wrd_rm and token.pos_ != 'SPACE' and not token.is_stop]

    df.loc[val.stem] = [all_tokens, full_clean, custom_tok]

#write df to file
df.to_csv('output/bows.tsv', sep='\t', encoding='utf-8')


# come back here and try to solve it
# Compute bigrams.
from gensim.models import Phrases
import copy
dfcopy = copy.deepcopy(df)


bow = dfcopy['all_tokens']
bigrams = Phrases(bow, min_count=5)

len(bow[0]) # 169310 | 180609
len(df['all_tokens'][0])


for idx in range(len(bow)):
    for token in bigrams[bow[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            bow[idx].append(token)





