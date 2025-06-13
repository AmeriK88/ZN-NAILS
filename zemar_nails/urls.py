from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse

# Importa aquí tu vista de la home; ajusta la ruta si tu función o app tienen otro nombre
from core.views import home as home_view

def root(request):
    # Railway marca sus health‐checks con este header
    if request.META.get('HTTP_X_RAILWAY_EDGE') is not None:
        return HttpResponse("OK")
    # Para cualquier otro request, devolvemos tu página principal
    return home_view(request)

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    # 1) Ruta raíz condicional
    path('', root, name='root'),
    # 2) Health-check dedicado (opcional)
    path('healthz/', health_check, name='health'),
    # 3) Cambio de idioma
    path('i18n/', include('django.conf.urls.i18n')),
]

# Ahora tus rutas principales bajo i18n_patterns (sin volver a declarar '')
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('servicios/', include('services.urls')),
    path('reviews/', include('reviews.urls')),
    path('reports/', include('reports.urls')),
    # Ya no hace falta: path('', include('core.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
