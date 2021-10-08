from django.contrib import admin
from .models import chapter, course, onlinecontent, thought
# Register your models here.

admin.site.register(chapter)
# admin.site.register(content)
admin.site.register(course)
admin.site.register(onlinecontent)
admin.site.register(thought)