from .forms import LoginForm, RegisterForm

def auth_forms(request):
    """
    Inyecta instancias de LoginForm y RegisterForm en el contexto
    de todas las plantillas, con flags por defecto para apertura de modal.
    """
    return {
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
        'show_login_modal': False,
        'show_register_modal': False,
    }
