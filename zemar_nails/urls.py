from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse

# Health-check simple para Railway
def health_check(request):
    return HttpResponse("OK")  # status 200


urlpatterns = [
    # Ruta para el cambio de idioma
    path('i18n/', include('django.conf.urls.i18n')),  
    path('', health_check, name='health'),
]

# Patrón principal de URLS
urlpatterns += i18n_patterns(
    path("", health_check, name="health"),  
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('servicios/', include('services.urls')),
    path('reviews/', include('reviews.urls')),
    path('reports/', include('reports.urls')),
)

if settings.DEBUG:  # Solo sirve archivos de medios en desarrollo
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
