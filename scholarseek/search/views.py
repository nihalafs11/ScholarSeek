import pyterrier as pt
from django.shortcuts import render

if not pt.started():
    pt.init()

def index(request):
    return render(request, 'index.html')

def search_by_criteria(request):
    search_query = request.GET.get('searchQuery', '')
    
    index_path = "./index" 
    indexref = pt.IndexRef.of(index_path + "/data.properties")
    br = pt.BatchRetrieve(indexref, wmodel="BM25", metadata=["docno", "title", "authors", "text"])
    
    terrier_results = br.search(search_query)
    
    results = [{
        'docno': row.docno,
        'title': row.title or 'No Title',
        'authors': row.authors or 'Unknown Authors',
        'text': row.text or 'No Abstract',
        'score': row.score
    } for row in terrier_results.itertuples()]

    return render(request, 'search_results.html', {'results': results})