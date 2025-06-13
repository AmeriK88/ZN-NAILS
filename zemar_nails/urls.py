from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")  # status 200

urlpatterns = [
    # 1) Ruta raíz para que Railway reciba un 200 OK
    path('', health_check, name='root_health'),
    # 2) Health-check dedicado
    path('healthz/', health_check, name='health'),
    # 3) Cambio de idioma
    path('i18n/', include('django.conf.urls.i18n')),
]

# Ahora las URLs principales con i18n
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('servicios/', include('services.urls')),
    path('reviews/', include('reviews.urls')),
    path('reports/', include('reports.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
