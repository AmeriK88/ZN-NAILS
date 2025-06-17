from django.shortcuts import redirect
from django.conf import settings

class CustomRedirectionMiddleware:
    """
    Redirige cualquier request cuyo host no sea el dominio canónico
    o que no use HTTPS, hacia https://carlamarqueznails.com<ruta>,
    preservando path y querystring.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Dominio canónico sin esquema ni puerto
        self.canonical_host = 'carlamarqueznails.com'

    def __call__(self, request):
        # Opcional: no forzar en DEBUG
        if settings.DEBUG:
            return self.get_response(request)

        # Obtiene host sin puerto
        host = request.get_host().split(':')[0]
        # Comprueba si la petición ya viene como segura (HTTPS).
        # Django usa SECURE_PROXY_SSL_HEADER para request.is_secure()
        is_secure = request.is_secure()

        # Si el host no es el canónico o no está en HTTPS, redirige
        if host != self.canonical_host or not is_secure:
            # Reconstruye la URL en HTTPS y dominio canónico
            new_url = 'https://' + self.canonical_host + request.get_full_path()
            # permanent=True => 301
            return redirect(new_url, permanent=True)

        # Ya es el host canónico en HTTPS: continúa normalmente
        return self.get_response(request)