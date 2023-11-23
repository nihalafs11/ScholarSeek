from django.db import models

class arXiv(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    submitter = models.CharField(max_length=255, blank=True, null=True)
    authors = models.TextField()
    title = models.TextField()
    comments = models.TextField(blank=True, null=True)
    journal_ref = models.CharField(max_length=255, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
    report_no = models.CharField(max_length=100, blank=True, null=True)
    categories = models.CharField(max_length=255)
    license = models.URLField(blank=True, null=True)
    abstract = models.TextField()
    versions = models.JSONField()  # Storing versions as JSON
    update_date = models.DateField()
    authors_parsed = models.JSONField()  # Storing parsed authors as JSON

    def __str__(self):
        return self.title
