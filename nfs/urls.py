from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('crm/', include('crm.urls')),
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('rest_framework/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
