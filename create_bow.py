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
# list of elements to be removed
# we can add here our own
pos_rm = ['PUNCT', 'DET', 'SPACE', 'NUM', 'SYM']
ner_rm = ['PER', 'LOC']

# create empty df to store the different bow
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
    custom_tok = [token.text.lower() for token in nlp_text if token.text.lower() not in ne2rm and token.pos_ != 'SPACE']

    df.loc[val.stem] = [all_tokens, full_clean, custom_tok]

#write df
df




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

