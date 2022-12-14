# TM paper


1. Data pre-processing
    1. Data collection
    2. Data cleaning

2. Data preparation
    1. Tokenization and tagging (POS, lematization, NER)
    2. Removing stop words and other unwanted tokens
    3. Grouping texts differently

3. Applying statistics
    1. Choosing a method and setting parameters


-----

## Data collection and Data cleaning
@get_gutemberg.py

- keep original data (as obtained from source)
- keep as much metadata as possible
- if it doesn't require a lot of work, it might be a better idea to use your own code, as you have more awareness and avoid having a lot of dependencies. In this example, its better to use our own codes than importing https://pypi.org/project/Gutenberg/
- it is always easier to work with plain text, but preserving section breaks can lead to better analysis
- sometimes the same data content is available in different formats. it is a good idea to test extracting two different formats to get an idea which one will be better for the project.
- in our case, getting the data from html format sounds better and easier to (a) preserve the sections boundaries (b) to make cleaning easier

-----
## Tokenization and Tagging with Spacy and removing unwanted words (creating bag of words)
@create_bow.py
- generate bag of words
- filter on the fly, to be more efficient?


## 2.2. Applying TM #
@apply_tm.py