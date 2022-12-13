############
# TM paper #
############

1.	Data pre-processing
1.1.	Data collection
1.2.	Data cleaning
1.3.	Tokenization and tagging


2.	Data analysis
2.1.	Data “manipulation”:
2.1.1.	Removing stop words 
2.1.2.	Lemmatizing
2.1.3.	Grouping texts differently

2.2.	Applying statistics
2.2.1.	Choosing a method and setting parameters


# ==================== #
# 1.1. Data collection #
# 1.2. Data cleaning   #

@get_gutemberg.py

- keep original data (as obtained from source)
- keep as much metadata as possible
- if it doesn't require a lot of work, it might be a better idea to use your own code, as you have more awareness and avoid having a lot of dependencies. In this example, its better to use our own codes than importing https://pypi.org/project/Gutenberg/
- it is always easier to work with plain text, but preserving section breaks can lead to better analysis
- sometimes the same data content is available in different formats. it is a good idea to test extracting two different formats to get an idea which one will be better for the project.
- in our case, getting the data from html format sounds better and easier to (a) preserve the sections boundaries (b) to make cleaning easier


# ============================= #
# 1.3. Tokenization and Tagging #

- There are better ways to perform preprocessing than just lower-casing and splitting by space. Effective preprocessing is beyond the scope of this tutorial: if you’re interested, check out the gensim.utils.simple_preprocess() function.


# ================= #
# 2.2. Applying TM #

@apply_tm.py