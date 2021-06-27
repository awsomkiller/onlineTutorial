from django.contrib import admin
from .models import chapter, content, course, onlinecontent
# Register your models here.

admin.site.register(chapter)
admin.site.register(content)
admin.site.register(course)
admin.site.register(onlinecontent)