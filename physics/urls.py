from django.urls import path
from . import views

urlpatterns = [
    path('', views.physicsChapterView, name='physicsview'),
    path('chapterId=<int:cid>/', views.physicsCourseView, name='physicsview'),
    path('chapterId=<int:cid>/courseId=<int:coid>/', views.physicsContentView, name='contentView'),
    path('practicepaper/', views.commingSoon),
    path('hcverma/', views.commingSoon),
    path('ncert/', views.commingSoon),
]