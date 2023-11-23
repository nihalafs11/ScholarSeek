from django.contrib import admin
from .models import arXiv

class arXivAdmin(admin.ModelAdmin):
    list_display = ('id', 'submitter', 'authors', 'title', 'comments', 'journal_ref',  'doi', 'report_no', 'categories', 'license', 'abstract', 'versions', 'update_date', 'authors_parsed')  # Add other fields you want to display


admin.site.register(arXiv, arXivAdmin)