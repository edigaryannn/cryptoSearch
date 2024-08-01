from django.db import models

# Create your models here.

class Document(models.Model):


    doc_id = models.IntegerField(db_index = True)
    # document text
    text = models.TextField()
    title = models.TextField()
