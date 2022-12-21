"""
Replicability and transparency in topic modelling: developing best practice guidelines for the digital humanities
Copyright (c) 2023 [Andressa Gomide, Mathew Gillings, Diego Gimenez]
This file is part of Gomide et al. 2023.
This project is licensed under the terms of the MIT license.
"""

""" @apply_tm.py
This script
- reads bag of words saved as values in dataframes
- 
and saves:
- 


"""

# import libraries
import pandas as pd # for dataframes
from gensim.corpora.dictionary import Dictionary # to convert bows to dictionary
#from gensim.models import LdaModel # to apply the lda model
import pyLDAvis # for data visualization of the topic model
import pyLDAvis.gensim_models  
from pprint import pprint # to print the results in a better way
import matplotlib.pyplot as plt # for the plots
from gensim import models


'''
# Read in the data
'''
# read in dfs
df = pd.read_csv('output/bows.tsv',sep = '\t',  index_col=0)
df_2gram = pd.read_csv('output/bow_with2gram.tsv',sep = '\t',  index_col=0)

# see dfs columns
print(df.columns)
print(df_2gram.columns)

# convert values to lists
at_list = df['all_tokens'].apply(eval)
fc_list = df['full_clean'].apply(eval)
ct_list = df['custom_tok'].apply(eval)
bi_list = df_2gram['all_tokens'].apply(eval)



'''
# Prepare the bag of words
'''

# TODO put the below in a function? so it's easier to process different results

# map each token to a unique ID (applying the Dictionary Object from Gensim)
dictionary = Dictionary(bi_list)

# see tokens and ids
print(dictionary.token2id)


# filter dictionary
'''
no_below: remove tokens that appear in less than n documents
no_above: remove tokens that appear in more than n% of the corpus
keep_n: keep the N most frequent token (‘None’ keeps all)
'''
dictionary.filter_extremes(no_below=1, no_above=0.8, keep_n=None)



# make bag of words representation of the documents
# "doc2bow() simply counts the number of occurrences of each distinct word, converts the word to its integer word id and returns the result as a sparse vector"
corpus = [dictionary.doc2bow(doc) for doc in bi_list]

# Make an index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token


# see corpus
print('Number of types: %d' % len(dictionary))
print('Number of documents: %d' % len(corpus))

'''

# FINDING OPTIMAL NUMBER OF TOPICS

After training the model, we should evaluate it.
We can use coherence score for that

"The score measures the degree of semantic similarity between high scoring words in each topic." 

"In this fashion, a coherence score can be computed for each iteration by inserting a varying number of topics.

Algorithms to calculate coherence score: C_v, C_p, C_uci, C_umass, C_npmi, C_a, ...

gensim library makes this calculation easier

Coherence score for C_v ranges from 0 (complete incoherence) to 1 (complete coherence).
> 0.5 = fairly good (Doing Computational Social Science: A Practical Introduction By John McLevey)."

'''

# Calculating the coherence score using C_v and u_mass 
# we first create an empty list to iterate the number of the max numbers of topics to test
# and empty lists to store the cv and umass score

topics = []
score_cv = []
score_umass = []

for i in range(1,20,1):
    # lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=10, num_topics=i, workers = 4, passes=10, random_state=100)
    print(f'working with {i} topics...')
    lda_model = models.LdaModel(corpus=corpus, id2word=id2word, iterations=10, num_topics=i, passes=10, random_state=100)
    print('calculating cv')
    cv = models.CoherenceModel(model=lda_model, texts = bi_list, corpus=corpus, dictionary=dictionary, coherence='c_v')
    score_cv.append(cv.get_coherence())
    print('calculating umass')
    um = models.CoherenceModel(model=lda_model, corpus=corpus, dictionary=dictionary, coherence='u_mass')
    score_umass.append(um.get_coherence())
    topics.append(i)


plt.plot(topics, score_cv)
plt.xlabel('Number of Topics')
plt.ylabel('Coherence Score')
plt.show()


plt.plot(topics, score_umass)
plt.xlabel('Number of Topics')
plt.ylabel('Coherence Score')
plt.show()





############
# LdaModel #
############

# Set training parameters.
num_topics = 16
chunksize = 2000
passes = 20
iterations = 400
eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make an index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

lda_model = models.LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    # We set alpha = 'auto' and eta = 'auto'. Again this is somewhat technical, but essentially we are automatically learning two parameters in the model that we usually would have to specify explicitly.
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)

pprint(lda_model.print_topics())

# get top topics
top_topics = lda_model.top_topics(corpus)
pprint(top_topics)

# Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
print('Average topic coherence: %.4f.' % avg_topic_coherence)

# prepare visualization
lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)


# pyLDAvis.enable_notebook()
# pyLDAvis.display(lda_display)
pyLDAvis.save_html(lda_display, 'output/lda_vis.html')



####################à
# lsi model
'''
Latent Semantic Indexing, LSI (or sometimes LSA) transforms documents 
from either bag-of-words or (preferrably) TfIdf-weighted space 
into a latent space of a lower dimensionality. 


model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=300)


'''

tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]


lsi_model = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
pprint(lsi_model.print_topics())

lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
pprint(lsi_model.print_topics())










###############
# lda multicore comeca 
# ? qual a diferenca

lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=50, num_topics=5, workers = 4, passes=10)
'''
"As input, I give the model our corpus and dictionary from before; 
besides, I choose to iterate over the corpus 50 times to optimize the model parameters (this is the default value). 
I select the number of topics to be ten and the workers to be 4 (find the number of cores on your PC by pressing the ctr+shift+esc keys). 
The pass is 10, which means the model will pass through the corpus ten times during training."
'''
pprint(lda_model.print_topics())
lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
# pyLDAvis.enable_notebook()
pyLDAvis.display(lda_display)
pyLDAvis.save_html(lda_display, 'index.html')

# lda multicore termina
###############



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import spacy
from imp import reload # pode ser necesario
import pyLDAvis.gensim_models
pyLDAvis.enable_notebook()# Visualise inside a notebook
import en_core_web_sm
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
from gensim.models import CoherenceModel




'''
Notes


- "One of the main properties of the bag-of-words model is that it completely ignores the order of the tokens in the document that is encoded"
- "Depending on how the representation was obtained, two different documents may have the same vector representations."
- "The full power of Gensim comes from the fact that a corpus doesn’t have to be a list, or a NumPy array, or a Pandas dataframe, or whatever. Gensim accepts any object that, when iterated over, successively yields documents."
- document-level X sentence-level topic modeling

See
- https://omdena.com/blog/topic-modeling-python-libraries-nlp-projects/
- https://towardsdatascience.com/topic-modelling-in-python-with-spacy-and-gensim-dc8f7748bdbf
- https://radimrehurek.com/gensim/#
- https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html#sphx-glr-auto-examples-tutorials-run-lda-py
- https://neptune.ai/blog/pyldavis-topic-modelling-exploration-tool-that-every-nlp-data-scientist-should-know
'''