from django.urls import path
from . import views

urlpatterns = [
    # path('', views.upload_image_view),
    path('/editorjs/image_upload/', views.upload_image_view),
] 