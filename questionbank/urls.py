from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExaminationsHandel, name="ExaminationsHandel"),
    path('<int:cid>/', views.exam, name='examid'),
    # path('editorjs/image_upload/', views.upload_image_view),
] 