from django.contrib import admin
from . models import User, contactus

# Register your models here.
admin.site.register(contactus)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

