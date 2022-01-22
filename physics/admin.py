from django.contrib import admin
from .models import chapter, course, onlinecontent, thought, hcvermacontent, advancearchieve
# Register your models here.

class chapterAdmin(admin.ModelAdmin):
    list_display = ('chapterId','chapterName','orderBy')
    list_display_links = ('chapterId', 'chapterName')

class courseAdmin(admin.ModelAdmin):
    list_display = ('courseId','topicName','chapterName','orderBy')
    list_filter = ('chapterName',)
    list_display_links=('courseId','topicName')

class onlinecontentAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','topic','dataType','orderBy')
    list_filter = ('topic',)
    list_display_links=('contentId','title')

class hcvermacontentAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','chapter','dataType','orderBy')
    list_filter = ('chapter',)
    list_display_links=('contentId','title')

class advancearchieveAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','chapter','dataType','orderBy')
    list_filter = ('chapter',)
    list_display_links=('contentId','title')


admin.site.register(chapter, chapterAdmin)
admin.site.register(hcvermacontent, hcvermacontentAdmin)
admin.site.register(course, courseAdmin)
admin.site.register(onlinecontent, onlinecontentAdmin)
admin.site.register(advancearchieve, advancearchieveAdmin)
admin.site.register(thought)