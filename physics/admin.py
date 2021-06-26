from django.contrib import admin
from .models import chapter, content, course
# Register your models here.

admin.site.register(chapter)
admin.site.register(content)
admin.site.register(course)