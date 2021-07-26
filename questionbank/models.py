from django.db import models
from django_editorjs_fields import EditorJsJSONField

# Create your models here.
class question(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    title = models.CharField(max_length=100)
    questiondescription = EditorJsJSONField()    
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    comprehension = models.BooleanField()
    multiselect = models.BooleanField()

class qa_question(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    title = models.CharField(max_length=100)
    questiondescription = EditorJsJSONField()
    answer =models.TextField(max_length=100)