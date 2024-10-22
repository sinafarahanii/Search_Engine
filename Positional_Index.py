import itertools
from parsivar import FindStems
import json
import re
import math
from utils import *


def tf_idf_maker(pos_index_raw, number_of_docs):
    tf_idf = {}
    tmp = {}
    for t in pos_index_raw.keys():
        tf_idf[t] = {}
        postings = pos_index_raw.__getitem__(t)
        t_df = postings[0]
        t_idf = math.log(number_of_docs/t_df, 10)

        for doc_id in postings[1].keys():
            t_tf = postings[1].__getitem__(doc_id)[0]
            t_tf = 1 + math.log(t_tf, 10)
            w_td = t_idf * t_tf
            tf_idf[t][doc_id] = w_td

    with open('tf_idf.json', 'w') as tf_idf_dic:
        tf_idf_dic.truncate(0)
        tf_idf_dic.write(json.dumps(tf_idf))
    doc_length(tf_idf)
    return


def doc_length(tf_idf):
    docs_length = {}
    for document in tf_idf.values():
        for doc_id in document:
            if doc_id in docs_length:
                docs_length[doc_id] += document[doc_id]**2
            else:
                docs_length[doc_id] = document[doc_id] ** 2
    for doc_id in docs_length:
        docs_length[doc_id] = math.sqrt(docs_length[doc_id])
    with open('doc_length.json', 'w') as docdoc:
        docdoc.truncate(0)
        docdoc.write(json.dumps(docs_length))
    return


def champions_list_maker(pos_index_tf_sorted):
    champions_list = {}
    for key in pos_index_tf_sorted:
        document = pos_index_tf_sorted[key]
        champions_list[key] = []
        champions_list[key].append(document[0])
        document[1] = dict(sorted(document[1].items(), key=lambda x: x[1][0], reverse=True))
        champions_list[key].append(dict(itertools.islice(document[1].items(), 100)))
    with open('champions_list.json', 'w') as champ:
        champ.truncate(0)
        champ.write(json.dumps(champions_list))
    return


stuff = docs
number_of_documents = len(stuff)


pos_index = {}
stemmer = FindStems()

for doc in stuff:

    normalized_text = normalize(stuff[doc]["content"])
    final_token_list = tokenizer(normalized_text.strip())
    for pos, term in enumerate(final_token_list):
        # First stem the term.
        tmp = term
        term = stemmer.convert_to_stem(term).split("&")[0]

        if term in pos_index:

            if doc in pos_index[term][1]:
                pos_index[term][1][doc][1].append(pos)
                pos_index[term][1][doc][0] += 1

            else:
                pos_index[term][0] = pos_index[term][0] + 1
                pos_index[term][1][doc] = []
                pos_index[term][1][doc].append(1)
                pos_index[term][1][doc].append([pos])
        else:
            pos_index[term] = []
            pos_index.__getitem__(term).append(1)
            pos_index[term].append({})
            pos_index[term][1][doc] = []
            pos_index[term][1][doc].append(1)
            pos_index[term][1][doc].append([pos])


pos_index = dict(sorted(pos_index.items(), key=lambda x: x[1][0], reverse=True))

count = 1
for element in list(pos_index.keys()):
    if count <= 50:
        #print(element, f" {pos_index[element][0]}")
        pos_index.pop(element)
        count += 1


with open('pos_index.json', 'w') as positional_index:
    positional_index.truncate(0)
    positional_index.write(json.dumps(pos_index))
tf_idf_maker(pos_index, number_of_documents)


champions_list_maker(pos_index)
