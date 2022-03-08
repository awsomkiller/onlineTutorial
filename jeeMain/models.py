from django.db import models
from physics.models import chapter
from accounts.models import subscriptionplan
from tinymce.models import HTMLField

# Create your models here.
class question(models.Model):
    id = models.AutoField(primary_key=True)
    chapter = models.ForeignKey(chapter, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    description = HTMLField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    comprehension = models.BooleanField()
    multiselect = models.BooleanField()

class qa_question(models.Model):
    id = models.AutoField(primary_key=True, editable=True)
    title = models.CharField(max_length=50)
    questiondescription = HTMLField()
    answer =models.TextField(max_length=100)
    def __str__(self):
        return self.title

# class exam_portal(models.Model):
#     id = models.AutoField(primary_key=True, editable=True)
#     title = models.CharField(max_length=100)
#     exam_time = models.DateTimeField()
#     Durations = models.IntegerField()
#     question = models.ManyToManyField(question)
#     qa_question = models.ManyToManyField(qa_question)
#     plans = models.ManyToManyField(subscriptionplan)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.title