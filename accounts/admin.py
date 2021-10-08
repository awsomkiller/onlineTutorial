from django.contrib import admin
from . models import User, subscriptionplan

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(subscriptionplan)