import json
from utils import *
from parsivar import FindStems
import math
from datetime import datetime

def pos_index_read():
    with open('pos_index.json', 'r', encoding="utf-8") as f:
        pos_index_dic = json.load(f)
    f.close()
    return pos_index_dic


def docs_tf_idf():
    with open('tf_idf.json', 'r', encoding="utf-8") as f:
        weights = json.load(f)
    f.close()
    return weights


def doc_length_read():
    with open('doc_length.json', 'r', encoding="utf-8") as f:
        dod = json.load(f)
    f.close()
    return dod


def champions_list_read():
    with open('champions_list.json', 'r', encoding="utf-8") as f:
        champs = json.load(f)
    f.close()
    return champs


def query_tf_idf(q_tokens, pos_index_dic):
    q_tf_idf = {}
    norm = 0
    for qt in q_tokens:
        qt_tf = q_tokens.count(qt)
        qt_tf = 1 + math.log(qt_tf, 10)
        try:
            qt_df = pos_index_dic.__getitem__(qt)[0]
            qt_idf = math.log(number_of_docs / qt_df, 10)
        except:
            qt_idf = 0
        qt_tf_idf = qt_idf * qt_tf
        q_tf_idf[qt] = qt_tf_idf
        norm += qt_tf_idf**2
    if norm != 0:
        norm = math.sqrt(norm)
        for a in q_tf_idf.keys():
            q_tf_idf[a] /= norm
    return q_tf_idf


def calculate_scores(q_weights, w_docs, champions_list, doc_length):
    res = {}
    for term in q_weights.keys():
        qt_weight = q_weights.__getitem__(term)
        if qt_weight > 0:
            token_postings = champions_list.__getitem__(term)[1]
            for doc_id in token_postings:
                if doc_id in res:
                    res[doc_id][0] += qt_weight * w_docs[term][doc_id]

                else:
                    res[doc_id] = []
                    res[doc_id].append(qt_weight * w_docs[term][doc_id])

    for doc_id in res:
        res[doc_id][0] /= doc_length[doc_id]

    return res


doc_length = doc_length_read()
pos_index = pos_index_read()
docs_weights = docs_tf_idf()
champ_list = champions_list_read()
query = input("Enter your query: ")
normalized_query = normalize(query)
query_tokens = tokenizer(normalized_query)
stemmer = FindStems()
for i in range(len(query_tokens)):
    query_tokens[i] = stemmer.convert_to_stem(query_tokens[i]).split("&")[0]

qw = query_tf_idf(query_tokens, pos_index)
if sum(qw.values()) == 0:
    print("No result matches the query :(")
    exit()

result = calculate_scores(qw, docs_weights, champ_list, doc_length)
result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
result_keys = []
k = 10

for key in result.keys():
    if k != 0:
        result_keys.append(key)
        k -= 1

for result_doc_key in result_keys:
    ans = docs[result_doc_key]
    print("####################################################################")
    print("")
    print("Title: ", ans["title"])
    print("URL: ", ans["url"])
    print("")

