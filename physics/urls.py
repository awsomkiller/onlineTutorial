from django.urls import path
from . import views

urlpatterns = [
    path('jee/', views.jeeChapterView, name='physicsview'),
    path('neet/', views.neetChapterView, name='physicsview'),
    path('jee/chapterId=<int:cid>/', views.jeeCourseView, name='physicsview'),
    path('jee/chapterId=<int:cid>/courseId=<int:coid>/', views.jeeContentView, name='contentView'),
    path('neet/chapterId=<int:cid>/', views.jeeCourseView, name='physicsview'),
    path('neet/chapterId=<int:cid>/courseId=<int:coid>/', views.neetContentView, name='contentView'),
    path('practicepaper/', views.commingSoon),
    path('hcverma/chapterId=<int:cid>/', views.hcVermaContent),
    path('advancearchieve/chapterId=<int:cid>/', views.advanceArchieve),
    path('ncert/', views.commingSoon),
]