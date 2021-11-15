from django.urls import path
from . import views

urlpatterns = [
path('checkout/', views.checkout, name="checkout"),
path('user-plan/',views.userplans, name="userPlans"),
path('user-plan/select-plan=<int:planid>/',views.selectplans, name="selectplans"),
path('create-checkout-session/', views.create_checkout_session, name="payment"),
path('success/', views.success_url, name="Payment Success"),
path('cancel/', views.cancel_url, name="payment failed"),
path('paymentconfirm/', views.my_webhook_view, name="stripe confirmation"),
path('trynow/', views.try_now, name="activate trial"),
]