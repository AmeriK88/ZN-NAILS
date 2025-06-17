from django.shortcuts import render
from core.models import ContadorVisitas
from accounts.forms import LoginForm, RegisterForm  # importa tus formularios

def home(request):
    # Lógica de contador existente
    contador, _ = ContadorVisitas.objects.get_or_create(pk=1)
    contador.total += 1
    contador.save()
    contador.refresh_from_db()

    contador_global = 1234  # o tu lógica real

    # Prepara siempre ambos formularios y flags a False
    login_form = LoginForm()
    register_form = RegisterForm()
    show_login_modal = False
    show_register_modal = False

    # Renderiza la plantilla pasando los nuevos context vars
    response = render(
        request,
        'core/home.html',
        {
            'contador_actualizado': contador.total,
            'contador_global': contador_global,
            'login_form': login_form,
            'register_form': register_form,
            'show_login_modal': show_login_modal,
            'show_register_modal': show_register_modal,
        }
    )
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response
