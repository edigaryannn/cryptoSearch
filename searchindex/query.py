from searchindex.build_index import index
from searchindex.preprocessing import preprocess_line_en
from searchengine.models import Document
import math
import re
def run_query(query):
    # Build the index
    words = preprocess_line_en(query)
    words_to_highlight = query.split(' ')
    results = []
    if not words:
        return [], words
    
    if len(words) == 1:
       res = index.get(words[0],[])

       res = run_ranked_search(query)
       return res, [words_to_highlight[0]]
    


    if 'AND NOT' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))
        for i in res1 :
            if i not in res2 :
                results.append(i)

    elif 'AND' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))
        for i in res1:
            if i in res2:
                results.append(i)

    elif 'OR NOT' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        all_doc_ids = set([str(doc.doc_id) for doc in Document.objects.all()])
        not_res2 = all_doc_ids.difference(res2)

        results = res1.union(not_res2)
        results = [int(i) for i in results]

    elif 'OR' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))
        first_word_resu_set = set(res1)
        sec_word_resu_set = set(res2)
        results = first_word_resu_set.union(sec_word_resu_set)

    # Run the query
    else:
        ind = index.get(query,[])
        results = run_ranked_search(query)
    return results, words_to_highlight

    # return index.get(query,["No Results"])

def run_ranked_search(query):
    words = preprocess_line_en(query)
    scores = {}
    for term in words:
        if term in index:
            doc_ids = index[term]
            for doc_id in doc_ids:
                term_freq = index[term][doc_id].freq
                doc_freq = index[term].docFreq
                weight = (1 + math.log10(term_freq)) * math.log10(index.docCount / doc_freq)
                if doc_id in scores:
                    scores[doc_id] += weight
                else:
                    scores[doc_id] = weight
                scores_values = sorted(scores, key=scores.get, reverse=True)
        print(index.docCount)
    return dict(sorted(scores.items() ,key = lambda x : x[1] ,reverse=True))
    # return results, words