from django.contrib import admin
from .models import question, qa_question, exam_portal, result

# Register your models here.
admin.site.register(question)
admin.site.register(qa_question)
admin.site.register(exam_portal)

@admin.register(result)
class UserAdmin(admin.ModelAdmin):
    exclude = ( 'id')
    list_display = ('studentId', 'result', 'exam_details')
    list_filter = ('studentId', 'exam_details')
