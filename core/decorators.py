from functools import wraps
from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

def handle_exceptions(view_func):
    """
    Decorador para manejar excepciones comunes en vistas y redirigir a plantillas personalizadas.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Http404:
            logger.warning("Error 404: Página no encontrada. URL: %s", request.path)
            return render(request, 'errors/404.html', status=404)
        except PermissionDenied:
            logger.warning("Error 403: Acceso denegado. URL: %s", request.path)
            return render(request, 'errors/403.html', status=403)
        except Exception as e:
            logger.error("Error 500: Error inesperado. URL: %s. Detalles: %s", request.path, str(e))
            return render(request, 'errors/500.html', status=500)
    return _wrapped_view
