import pathlib
import re
import random

'''
reading files
'''

def get_file_list(files_path):
    '''
    create a list and append the files names to it
    '''
    workingDir = pathlib.Path(files_path)
    file_list = []
    for f in workingDir.iterdir():
        file_list.append(f)
    return file_list


# def generate_ngrams(text, gram_n=3):
#     tokens = re.findall(r'\w+|[^\s\w]+', text)
#     ngrams = []  
#     for i in range(len(tokens) - gram_n + 1):
#         ngram = '_'.join(tokens[i:i + gram_n])
#         ngrams.append(ngram)
#     return ngrams


# '''
# text as dicts
# '''
# # create a dictionary
# # def create_dict(str):
# #     dicio = dict()
# #     tokens = re.findall(r'\w+|[^\s\w]+', str)
# #     for t in tokens:
# #         if t in dicio:
# #             dicio[t] += 1
# #         else:
# #             dicio[t] = 1
# #     return dicio



# def create_dict(text, gram_n=1):
#     dicio = dict()
#     if gram_n > 1:
#         tokens = generate_ngrams(text, gram_n)
#     else:
#         tokens = re.findall(r'\w+|[^\s\w]+', text)
#     for t in tokens:
#         if t in dicio:
#             dicio[t] += 1
#         else:
#             dicio[t] = 1
#     return dicio

# # get token count 
# def sum_dict_values(dicio):
#     val_list = []
#     for i in dicio:
#         val_list.append(dicio[i])
#     sum_val = sum(val_list)
#     return sum_val

# '''
# slicing corpus
# '''
# def get_text_sample(filename, slice='middle', perc=10):
#     with open(filename, 'r', encoding="utf-8") as f:
#         text_str = f.read()
    
#     # TODO remove extra \n'
    
#     # get size of parts
#     n_parts = 3
#     chars_text_part = round(len(text_str) / n_parts)

#     # get % of text
#     perc_text = round(len(text_str) * perc / 100)

#     if slice == 'middle':
#         text_part = text_str[chars_text_part:chars_text_part*2]
#     elif slice == 'end':
#         text_part = text_str[chars_text_part*2:]
#         return text_part[:perc_text]
#     elif slice == 'start':
#         text_part = text_str[:chars_text_part]
#     elif slice == 'random':
#         text_list = text_str.splitlines()
#         rl = random.sample(text_list, len(text_list))
#         text_str = ' '.join(rl)
#         text_part = text_str[:chars_text_part]
#     else:
#         print("slicing method not recognized")
       
#     # get only a percentage of text
#     return text_part[:perc_text]