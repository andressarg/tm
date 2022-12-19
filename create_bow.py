"""
Replicability and transparency in topic modelling: developing best practice guidelines for the digital humanities
Copyright (c) 2023 [Andressa Gomide, Mathew Gillings, Diego Gimenez]
This file is part of Gomide et al. 2023.
This project is licensed under the terms of the MIT license.
"""

""" @create_bow.py
This script
- reads plain text files in a give folder
- applies Spacy Lang model
- creates different bags of words ('all_tokens', 'full_clean', 'custom_tok')
and saves:
- the original book file (html)
- the cleaned content (txt)
- the metadata (tsv)


"""

# import libraries
import spacy # to tokenize and annotate the data
import pandas as pd # to store metadata as dataframe
from gensim.models import Phrases # to compute the bigrams
import utilsNLP # our library with functions 


# load language model
# there are different models availables at https://spacy.io/models 
# we can also create our own
# here we will use a small model 
nlp = spacy.load('pt_core_news_sm')

# get list with files
# the folder input has the plain files prepared with @get_gutemberg.py
file_list = utilsNLP.get_file_list('input/plain')


# Cleaning
## list of elements to be removed (we can also here our own)
# POS tags to be removed
pos_rm = ['PUNCT', 'DET', 'SPACE', 'NUM', 'SYM']
# Named Entities tags to be removed
ner_rm = ['PER', 'LOC']
# words to be removed
wrd_rm = ['ella', 'elle']

# create empty df to store the different bag of words (BoWs)
df = pd.DataFrame(columns = ['all_tokens', 'full_clean', 'custom_tok'])

# iterate each file and create the 3 different BoWs
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

    # all tokens (no space)
    print('getting all tokens BoW...')
    all_tokens = [token.text.lower() for token in nlp_text if token.pos_ != 'SPACE']

    # get all lemma that are not in the removel list neither in the stop list and that is alpha (not letters)
    print("getting BoW with a 'full clean' approach ...")
    full_clean = [token.lemma_.lower() for token in nlp_text if token.pos_ not in pos_rm and not token.is_stop and token.is_alpha]

    # remove locations and named person/family
    print("getting customized BoW")
    custom_tok = [token.text.lower() for token in nlp_text if token.text.lower() not in ne2rm and token.text.lower() not in wrd_rm and token.pos_ not in pos_rm and not token.is_stop]

    # add BoWs to dataframe
    df.loc[val.stem] = [all_tokens, full_clean, custom_tok]

# write dataframe to file
df.to_csv('output/bows.tsv', sep='\t', encoding='utf-8')



# Compute bigrams.
# as this can be a very heavy (and slow) process, we make it separately 
# and save it in a seperate file

# get only the values from the all_tokens column
bow = df['all_tokens']

len(bow[0]) # 93208
len(df['all_tokens'][0]) # 1369489

# get bigrams that occur at least 5 times
bigrams = Phrases(bow, min_count=5)

# add bigrams to BoW
for idx in range(len(bow)):
    for token in bigrams[bow[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            bow[idx].append(token)

# save to file
bow.to_csv('output/bow_with2gram.tsv', sep='\t', encoding='utf-8')


