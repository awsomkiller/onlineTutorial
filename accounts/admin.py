from django.contrib import admin
from . models import User, subscriptionplan, contactus

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ( 'admin', 'staff', 'emailConfirm', 'expiry' )
    list_display = ('name', 'mobile', 'mobileConfirm', 'plan')
    list_filter = ('plan', 'institute', 'mobileConfirm', 'timestamp')

admin.site.register(subscriptionplan)
admin.site.register(contactus)