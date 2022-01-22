from django.urls import path
from . import views

urlpatterns = [
    path('', views.physicsChapterView, name='physicsview'),
    path('chapterId=<int:cid>/', views.physicsCourseView, name='physicsview'),
    path('chapterId=<int:cid>/courseId=<int:coid>/', views.physicsContentView, name='contentView'),
    path('practicepaper/', views.commingSoon),
    path('hcverma/chapterId=<int:cid>/', views.hcVermaContent),
    path('advancearchieve/chapterId=<int:cid>/', views.advanceArchieve),
    path('ncert/', views.commingSoon),
]