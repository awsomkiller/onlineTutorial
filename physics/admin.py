from django.contrib import admin
from .models import chapter, lecturecourse, thought, hcvermacontent, advancearchievecourse, hcvermacourse, lecturecontent, advancearchievecontent
# Register your models here.

class chapterAdmin(admin.ModelAdmin):
    list_display = ('chapterId','chapterName','orderBy')
    list_display_links = ('chapterId', 'chapterName')

class courseAdmin(admin.ModelAdmin):
    list_display = ('courseId','topicName','chapterName','orderBy')
    list_filter = ('chapterName',)
    list_display_links=('courseId','topicName')

class onlinecontentAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','topic','dataType','orderBy', 'jee', 'neet')
    list_filter = ('topic','jee', 'neet')
    list_display_links=('contentId','title')

class hcvermacontentAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','topic','dataType','orderBy')
    list_filter = ('topic',)
    list_display_links=('contentId','title')

class advancearchieveAdmin(admin.ModelAdmin):
    list_display = ('contentId','title','topic','dataType','orderBy')
    list_filter = ('topic',)
    list_display_links=('contentId','title')

class hcVermaCoursesAdmin(admin.ModelAdmin):
    list_display = ('courseId','topicName','chapterName','orderBy')
    list_filter = ('chapterName',)
    list_display_links=('courseId','topicName')


admin.site.register(chapter, chapterAdmin)
admin.site.register(hcvermacontent, hcvermacontentAdmin)
admin.site.register(lecturecourse, courseAdmin)
admin.site.register(lecturecontent, onlinecontentAdmin)
admin.site.register(advancearchievecontent, advancearchieveAdmin)
admin.site.register(thought)
admin.site.register(advancearchievecourse)
admin.site.register(hcvermacourse, hcVermaCoursesAdmin)