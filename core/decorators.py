from functools import wraps
from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.conf import settings
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

def handle_exceptions(view_func):
    """
    Decorador para manejar excepciones comunes en vistas y redirigir a plantillas personalizadas.
    En modo DEBUG, mostrará el rastreo completo de errores para facilitar el desarrollo.
    En producción, redirige a plantillas personalizadas y registra los errores.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Llamar a la vista original
            return view_func(request, *args, **kwargs)
        except Http404:
            # Manejar errores 404 (Página no encontrada)
            logger.warning("Error 404: Página no encontrada. URL: %s", request.path)
            if settings.DEBUG:  # Mostrar rastreo completo en desarrollo
                raise
            return render(request, 'errors/404.html', status=404)
        except PermissionDenied:
            # Manejar errores 403 (Acceso denegado)
            logger.warning("Error 403: Acceso denegado. URL: %s", request.path)
            if settings.DEBUG:
                raise
            return render(request, 'errors/403.html', status=403)
        except Exception as e:
            # Manejar errores 500 (Errores inesperados)
            logger.error("Error 500: Error inesperado. URL: %s. Detalles: %s", request.path, str(e))
            if settings.DEBUG:
                raise
            return render(request, 'errors/500.html', status=500)
    return _wrapped_view
