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

class exam_portal(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    title = models.CharField(max_length=125)
    exam_time = models.DateTimeField()
    Durations = models.IntegerField()
    question = models.ManyToManyField(question)
    qa_question = models.ManyToManyField(qa_question)
    active = models.BooleanField(default=True)