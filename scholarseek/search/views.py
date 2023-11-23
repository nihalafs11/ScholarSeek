from django.shortcuts import render
from django.db.models import Q
from .models import arXiv

def index(request):
    return render(request, 'index.html')

def search_by_criteria(request):
    search_query = request.GET.get('searchQuery', '')
    search_type = request.GET.get('searchType', 'none')

    if search_type == 'author':
        results = arXiv.objects.filter(authors__icontains=search_query)
    elif search_type == 'title':
        results = arXiv.objects.filter(title__icontains=search_query)
    else:
        # Handle 'none' or default case
        results = arXiv.objects.filter(Q(title__icontains=search_query) | Q(authors__icontains=search_query))

    return render(request, 'search_results.html', {'results': results})
