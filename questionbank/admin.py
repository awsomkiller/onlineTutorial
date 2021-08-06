from django.contrib import admin
from .models import question, qa_question, exam_portal

# Register your models here.
admin.site.register(question)
admin.site.register(qa_question)
admin.site.register(exam_portal)