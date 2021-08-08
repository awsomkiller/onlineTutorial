from django.urls import path
from .views import CreateCheckoutSessionView
from . import views

urlpatterns = [
path('', CreateCheckoutSessionView.as_view(), name="payment"),
path('success/', views.success, name="Payment Success"),
path('cancel/', views.cancel, name="payment failed"),
]