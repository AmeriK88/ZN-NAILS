from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse
from django.views.static import serve

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

# El resto de tu app bajo i18n_patterns, sin volver a declarar la raíz aquí
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('appointments/', include('appointments.urls')),
    path('servicios/', include('services.urls')),
    path('reviews/', include('reviews.urls')),
    path('reports/', include('reports.urls')),
    path('', include('core.urls')),  # core.urls define path('', views.home, name='home')
)

# Servir archivos media subidos por el admin / usuarios.
# Esta ruta sirve media desde MEDIA_ROOT en producción/pruebas. 
# Atención: en Railway el almacenamiento local es efímero (se perderán al redeploy).
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# En DEBUG podemos dejar que Django sirva también estáticos si lo deseamos
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
