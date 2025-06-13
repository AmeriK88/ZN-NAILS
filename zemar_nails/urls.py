from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse

# Importa tu vista de home real
from core.views import home as home_view

def root(request):
    # Si es un HEAD (health-check de Railway), devolvemos OK
    if request.method == 'HEAD':
        return HttpResponse("OK")
    # Si es GET (o cualquier otro), renderizamos tu home de verdad
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

# El resto de tu app bajo i18n_patterns
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('servicios/', include('services.urls')),
    path('reviews/', include('reviews.urls')),
    path('reports/', include('reports.urls')),
    # ¡No vuelvas a poner path('', ...) aquí!
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
