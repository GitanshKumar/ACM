from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha', include('captcha.urls')),
    path('', include('base.urls'))
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        # Add a URL pattern for serving media files
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]

handler404 = "base.views.error_404"
handler500 = "base.views.error_500"