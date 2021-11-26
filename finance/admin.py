from finance.models import payment, checkoutrecord, trynowrecord
from django.contrib import admin

# Register your models here.
@admin.register(payment)
class UserAdmin(admin.ModelAdmin):
    exclude = ('amount',)
    list_display = ('user', 'plan', 'amount', 'time')
    list_filter = ('plan', 'time')

@admin.register(checkoutrecord)
class UserAdmin(admin.ModelAdmin):
    exclude = ('amount', 'status', 'isactive', 'stripe_payment_intent')
    list_display = ('user', 'plan', 'amount', 'status', 'stripe_payment_intent')
    list_filter = ('plan', 'status')

@admin.register(trynowrecord)
class UserAdmin(admin.ModelAdmin):
    exclude = ( 'endtime', 'active')
    list_display = ('user', 'starttime', 'endtime')
    list_filter = ('active',)