# TODO check which libraries i need
# import libraries
import spacy
# import re
import utilsNLP
import pandas as pd
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
# import importlib
import pyLDAvis.gensim_models
import pyLDAvis

from pprint import pprint



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


corpus = [dictionary.doc2bow(doc) for doc in df['tokens']]
# "doc2bow() simply counts the number of occurrences of each distinct word, converts the word to its integer word id and returns the result as a sparse vector"

lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, iterations=50, num_topics=5, workers = 4, passes=10)
'''
"As input, I give the model our corpus and dictionary from before; besides, I choose to iterate over the corpus 50 times to optimize the model parameters (this is the default value). I select the number of topics to be ten and the workers to be 4 (find the number of cores on your PC by pressing the ctr+shift+esc keys). The pass is 10, which means the model will pass through the corpus ten times during training."
'''

lda_model.print_topics(-1)
pprint(lda_model.print_topics())


lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

pyLDAvis.enable_notebook()
# pyLDAvis.display(lda_display)
pyLDAvis.save_html(lda_display, 'index.html')



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
- "In practice, corpora may be very large, so loading them into memory may be impossible. Gensim intelligently handles such corpora by streaming them one document at a time. See https://radimrehurek.com/gensim/auto_examples/core/run_corpora_and_vector_spaces.html#corpus-streaming-tutorial for details."

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