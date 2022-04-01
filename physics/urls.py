from django.urls import path
from . import views

urlpatterns = [
    path('jee/', views.jeeChapterView, name='physicsview'),
    path('neet/', views.neetChapterView, name='physicsview'),
    
    path('jee/chapterId=<int:cid>/', views.jeeCourseView, name='physicsview'),
    path('jee/chapterId=<int:cid>/courseId=<int:coid>/', views.jeeContentView, name='contentView'),
    
    path('neet/chapterId=<int:cid>/', views.neetCourseView, name='physicsview'),
    path('neet/chapterId=<int:cid>/courseId=<int:coid>/', views.neetContentView, name='contentView'),
    
    path('jee/hcverma/chapterId=<int:cid>/', views.hcVermaJeeCourseView, name='physicsview'),
    path('jee/hcverma/chapterId=<int:cid>/courseId=<int:coid>/', views.hcVermaJeeContent),

    # path('neet/hcverma/chapterId=<int:cid>/', views.hcVermaNeetCourseView, name='physicsview'),
    path('neet/hcverma/chapterId=<int:cid>/courseId=<int:coid>/', views.hcVermaNeetContent),
    
    path('jee/advancearchieve/chapterId=<int:cid>/', views.advancearchiveCourseView, name='physicsview'),
    path('jee/advancearchieve/chapterId=<int:cid>/courseId=<int:coid>/', views.advanceArchieve),

    # path('neet/archieve/chapterId=<int:cid>/', views.archiveCourseView, name='physicsview'),
    path('neet/archieve/chapterId=<int:cid>/courseId=<int:coid>/', views.advanceArchieve),

    path('jee/ncert/chapterId=<int:cid>/', views.ncertJeeCourseView, name='physicsview'),
    path('jee/ncert/chapterId=<int:cid>/courseId=<int:coid>/', views.ncertJeeContent),

    # path('neet/ncert/chapterId=<int:cid>/', views.ncertNeetCourseView, name='physicsview'),
    # path('neet/ncert/chapterId=<int:cid>/courseId=<int:coid>/', views.ncertNeetContent),
]