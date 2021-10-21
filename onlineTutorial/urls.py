from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


#Django Admin Customization
admin.site.site_header = "RKeduV Administration Panel"
admin.site.site_title = "Rkeduv Admin Panel"
admin.site.index_title = "Data Administration Portal"

urlpatterns = [
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
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # path('imageUpload/', include('questionbank.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

