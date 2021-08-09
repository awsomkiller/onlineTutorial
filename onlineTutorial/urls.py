from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('physics/',include('physics.urls')),
    path('accounts/',include('accounts.urls')),
    path('chemistry/',views.commingsoon, name='commingsoon'),
    path('maths/',include('physics.urls')),
    path('finance/',include('finance.urls')),
    path('examinations/', include('questionbank.urls')),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('support/', views.contact, name="support"),
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # path('imageUpload/', include('questionbank.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

