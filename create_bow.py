# import libraries
import spacy
import re
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
    # examples:
    # - remove numbers, but not words that contain numbers.
    # - Remove words that are only one character.

    # get all tokens that are not in the removel list neither in the stop list and that is alpha
    tok = [token.lemma_.lower() for token in nlp_text if token.pos_ not in removal and not token.is_stop and token.is_alpha]

    df.loc[val.stem] = [tok]


# # map each token to a unique ID (applying the Dictionary Object from Gensim)
# dictionary = Dictionary(df['tokens'])

# # see toknes and ids
# print(dictionary.token2id)


# # filter dictionary
# # dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=1000)
# dictionary.filter_extremes(no_below=1, no_above=0.8, keep_n=None)
# '''
# no_below: remove tokens that appear in less than n documents
# no_above: remove tokens that appear in more than n% of the corpus
# keep_n: keep the N most frequent token (‘None’ keeps all)
# '''


# rascunho

# create empty df
df = pd.DataFrame(columns = ['all_tokens', 'full_clean', 'custom_tok'])


val = 'input/book31971.txt'
with open(val, 'r', encoding='utf-8') as f:
    text_org = f.read()

# remove line breaks
text_oneline = text_org.replace("\n", " ")

# apply model
nlp_text = nlp(text_oneline)

# get NER for person
'''
to see named entity labels and their explanation
nlp.get_pipe("ner").labels
spacy.explain('LOC')
spacy.explain('MISC')
spacy.explain('ORG')
spacy.explain('PER')
'''

ner_rm = []
for ent in nlp_text.ents:
    if ent.label_ == 'PER':
        ner_rm.append(ent.text.lower())

# get lis of unique values for the ner found
ner_rm = list(set(ner_rm))


# all tokens (no space)
all_tokens = [token.text.lower() for token in nlp_text if token.pos_ != 'SPACE'] #

# get all lemma that are not in the removel list neither in the stop list and that is alpha (not letters)
full_clean = [token.lemma_.lower() for token in nlp_text if token.pos_ not in removal and not token.is_stop and token.is_alpha]

# remove locations and named person/family
custom_tok = [token.text.lower() for token in nlp_text if token.text.lower() not in ner_rm and token.pos_ != 'SPACE']



# df.loc[val.stem] = [tok]
df.loc[val[10:15]] = [all_tokens, full_clean, custom_tok]


bow_coll = []
bow_coll.append(bow)
len(bow)
len(bow_coll)




bigrams = Phrases(bow, min_count=5)

for idx in range(len(bow_coll)):
    print(idx)
    for token in bigrams[bow_coll[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            print(token)
            bow_coll[idx].append(token)



# adicionar phrases later?

# bow_coll.append(bow)

bigrams = Phrases(bow_coll, min_count=5)

for idx in range(len(bow_coll)):
    print(idx)
    for token in bigrams[bow_coll[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            print(token)
            bow_coll[idx].append(token)


# df.loc[val.stem] = [bow]
df.loc[val[10:15]] = [bow, '1']
df.loc[val[10:15]] = [bow, bow_coll]
len(bow_coll[0])
len(bow)
bow_coll[0][-3:]
bow[-3:]

for token in bigrama[bow]:
    if '_' in token:
        # Token is a bigram, add to document.
        print(token)



# bow_1 = df['tokens']['book31971'] 

bigrama = Phrases(bow, min_count=5)

for idx in range(len(bow)):
    print(idx)
    # print(bow[idx])
    for token in bigrama[bow[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            print(token)
            bow[idx].append(token)

len(bow)
bigrama

bow[0][5]

