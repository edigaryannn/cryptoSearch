from django.shortcuts import render
from django.views import generic
from searchengine.models import Document
from searchindex.query import run_query
from searchindex.query_completion import complete_query
from django.http import JsonResponse

import re

# Create your views here.


def formats_doc(doc_id, title, text):
    return f'<h3><a href="https://bitcoin.stackexchange.com/questions/{doc_id}">{title}</a></h3><br><p>{text}</p>'

class Index(generic.TemplateView):
    template_name = "search.html"

class Search(generic.ListView):
    template_name = "search.html"
    context_object_name = 'searchresults'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET['query']
        doc_ids, words_to_highlight = run_query(query)

        if not doc_ids:
            return ['No results']
        

        docs = [Document.objects.get(doc_id=doc) for doc in doc_ids]

        ndocs = []
        for doc in docs:
            # First highlight the title
            title = highlight_text(doc.title, words_to_highlight)

            # Then highlight the text
            text = highlight_text(doc.text, words_to_highlight)

            formatted_doc = formats_doc(doc.doc_id, title, text)
            ndocs.append(formatted_doc)

        # for doc in docs:
    
        if len(ndocs) >= 50:
            return ndocs[:50]

        return ndocs

def highlight_text(doc_req, words):
    for i in words:
        html = f'<b><span class="query">{i}</span></b>'
        doc_req = re.sub(f"([^\\w])({i})([^\\w])", f"\\1{html}\\3",doc_req)
    return doc_req

def complete(request):
    query = request.GET['q']

    completions = complete_query(query)
    return JsonResponse(completions,safe=False)