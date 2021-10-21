from django.contrib import admin
from . models import User, subscriptionplan

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('active', 'admin', 'staff', 'emailConfirm', 'timestamp', 'expiry', 'mobileConfirm')
    list_display = ('name', 'mobile', 'mobileConfirm', 'institute')
    list_filter = ('plan', 'institute', 'mobileConfirm', 'timestamp')

admin.site.register(subscriptionplan)