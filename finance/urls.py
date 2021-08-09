from django.urls import path
from . import views

urlpatterns = [
path('', views.checkout, name="checkout"),
path('create-checkout-session', views.create_checkout_session, name="payment"),
path('success/', views.success_url, name="Payment Success"),
path('cancel/', views.cancel_url, name="payment failed"),
]