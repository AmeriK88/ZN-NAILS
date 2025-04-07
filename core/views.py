from django.shortcuts import render
from core.models import ContadorVisitas

def home(request):
    contador, _ = ContadorVisitas.objects.get_or_create(pk=1)
    contador.total += 1
    contador.save()

    # Refrescar datos
    contador.refresh_from_db()

    # Aquí defines la variable "contador_global" o como la quieras llamar.
    contador_global = 1234  # O algún otro valor, si así lo deseas

    # Renderizar la plantilla con ambas variables en el contexto
    response = render(
        request,
        'core/home.html',
        {
            'contador_actualizado': contador.total,
            'contador_global': contador_global,
        }
    )

    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


