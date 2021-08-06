from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.loginview, name='loginView'),
    path('register/', views.registerview, name='resgisterView'),
    path('logout/', views.logoutview, name='logoutview'),
    path('forgotpassword/', views.changepassword, name='forgotPassword'),
    path('changepassword/', views.changepassword, name='changePassword'),
    # path('changepassword/', views.passwordchangeview.as_view(template_name='changepassword.html')),
    path('resetpassword/',views.otpgeneration, name='passwordReset'),
    path('profile/', views.profileview, name='profileview'),
    path('resetpass/', views.changepass, name='profileview'),
]