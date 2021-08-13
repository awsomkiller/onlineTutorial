from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExaminationsHandel, name="ExaminationsHandel"),
    path('start_exam<int:cid>/', views.exam, name='examid'),
    # path('result<int:id>', views.getResult, name="get result",)
] 