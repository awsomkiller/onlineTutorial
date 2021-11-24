from django.db import models
from django.db.models.deletion import PROTECT
from django_editorjs_fields import EditorJsJSONField
from accounts.models import User, subscriptionplan

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
    def __str__(self):
        return self.title

class exam_portal(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    title = models.CharField(max_length=125)
    exam_time = models.DateTimeField()
    Durations = models.IntegerField()
    question = models.ManyToManyField(question)
    qa_question = models.ManyToManyField(qa_question)
    plans = models.ManyToManyField(subscriptionplan)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class result(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    exam_details = models.ForeignKey(exam_portal, on_delete=PROTECT)
    studentId = models.ForeignKey(User, on_delete=PROTECT)
    studentResponse = models.JSONField()
    result = models.CharField(max_length=50, null=True)
    resultfile = models.FileField(upload_to='var/www/static/resultfiles', max_length=254, null=True)
