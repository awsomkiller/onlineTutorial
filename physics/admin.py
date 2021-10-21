from django.contrib import admin
from .models import chapter, course, onlinecontent, thought
# Register your models here.

class chapterAdmin(admin.ModelAdmin):
    list_display = ('chapterId','chapterName','orderBy')

class courseAdmin(admin.ModelAdmin):
    list_display = ('courseId','topicName','chapterName','orderBy')
    list_filter = ('chapterName',)

class onlinecontentAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','topic','dataType','orderBy')
    list_filter = ('topic',)


admin.site.register(chapter, chapterAdmin)
# admin.site.register(content)
admin.site.register(course, courseAdmin)
admin.site.register(onlinecontent, onlinecontentAdmin)
admin.site.register(thought)