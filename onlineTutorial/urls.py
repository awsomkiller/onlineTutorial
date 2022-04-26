from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from filebrowser.sites import site

#Django Admin Customization
admin.site.site_header = "RKeduV Administration Panel"
admin.site.site_title = "Rkeduv Admin Panel"
admin.site.index_title = "Data Administration Portal"

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('physics/',include('physics.urls')),
    path('accounts/',include('accounts.urls')),
    path('chemistry/',views.commingsoon, name='commingsoon'),
    path('maths/',include('physics.urls')),
    path('finance/',include('finance.urls')),
    path('examinations/', include('questionbank.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('logos/favicon.ico'))),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('support/', views.contact, name="support"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('tinymce/', include('tinymce.urls')),
    path('privacy/', views.privacy, name="privacy"),
    path('disclaimer/', views.disclaimer, name="disclaimer"),
    path('cookies/', views.cookies, name="cookies"),
    path('termsandcondition/', views.terms, name="terms"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

