from django.shortcuts import redirect
from django.conf import settings

class CustomRedirectionMiddleware:
    """
    Middleware que redirige cualquier petición cuyo host no sea el dominio canónico
    o que no use HTTPS, hacia https://carlamarqueznails.com<ruta>, preservando path y querystring.
    No aplica en entorno de desarrollo (DEBUG=True).

    Uso:
      - Colocar esta clase en un archivo accesible, p. ej. middleware/custom_redirection_middleware.py.
      - Añadirla en settings.py en MIDDLEWARE, justo después de SecurityMiddleware.
      - Ajustar settings para producción: SECURE_SSL_REDIRECT, SECURE_PROXY_SSL_HEADER, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, HSTS, etc.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Dominio canónico sin esquema ni puerto
        # Si cambias el dominio en el futuro, modifícalo aquí o pásalo por settings
        self.canonical_host = 'carlamarqueznails.com'

    def __call__(self, request):
        # 1) Saltar forzado en entorno de desarrollo
        #    Si DEBUG=True, no forzamos HTTPS ni host canónico, permitimos accesos por HTTP.
        if settings.DEBUG:
            # Devolver la respuesta sin alterar
            return self.get_response(request)

        # 2) Obtener el host de la petición (sin puerto)
        #    request.get_host() puede devolver "example.com" o "example.com:8000"
        host = request.get_host().split(':')[0]

        # 3) Comprobar si la solicitud es segura (HTTPS).
        #    Django usará settings.SECURE_PROXY_SSL_HEADER para determinar request.is_secure()
        is_secure = request.is_secure()

        # 4) Si el host no coincide con el dominio canónico, o no está en HTTPS, redirigir:
        if host != self.canonical_host or not is_secure:
            # Reconstruir la URL apuntando a HTTPS y al host canónico
            # request.get_full_path() incluye path y querystring (p. ej. "/ruta/?a=b")
            new_url = 'https://' + self.canonical_host + request.get_full_path()
            # Redirección permanente (301). Si prefieres temporal (302), quita permanent=True.
            return redirect(new_url, permanent=True)

        # 5) Si ya es el host canónico y HTTPS, continuar normalmente
        return self.get_response(request)
