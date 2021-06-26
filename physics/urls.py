from django.urls import path
from . import views

urlpatterns = [
    path('', views.physicsview, name='physicsview'),
    path('<int:cid>', views.physicsview, name='physicsview')
]