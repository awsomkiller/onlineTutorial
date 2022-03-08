from django.contrib import admin
from jeeMain.models import qa_question, question
# Register your models here.

admin.site.register(question)
admin.site.register(qa_question)
