from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from appointments.models import Cita  
from core.decorators import handle_exceptions 
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from datetime import date

@csrf_protect
def register_view(request):
    """
    Procesa POST de registro:
    - GET: instancia RegisterForm vacío, show_register_modal=False.
    - POST inválido: show_register_modal=True y re-renderiza la plantilla con errores.
    - POST válido: crea usuario, lo autentica y redirige (por ejemplo a home o next).
    """
    show_register_modal = False
    # Mantener un LoginForm vacío en contexto para que el modal de login también exista
    login_form = LoginForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # Crear el usuario a partir del formulario
            user = register_form.save(commit=False)
            # Si tu formulario incluye first_name/last_name/email, asignarlos:
            user.first_name = register_form.cleaned_data.get('first_name', '')
            user.last_name  = register_form.cleaned_data.get('last_name', '')
            user.email      = register_form.cleaned_data.get('email', '')
            user.save()

            # Autenticación automática
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"¡Bienvenido/a {user.username}! Tu cuenta ha sido creada e iniciada sesión con éxito.")
                # Puedes usar un campo hidden 'next' en el formulario si quieres redirigir a la página origen:
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')  # o la ruta que estimes apropiada
            else:
                messages.error(request, "Hubo un problema al iniciar sesión automáticamente. Intenta iniciar sesión manualmente.")
                return redirect('login')
        else:
            # Si hay errores, abrir modal de registro
            show_register_modal = True
    else:
        register_form = RegisterForm()

    # Renderiza la plantilla (por ejemplo home) con ambos formularios y flags
    return render(request, 'core/home.html', {
        'register_form':      register_form,
        'login_form':         login_form,
        'show_register_modal': show_register_modal,
        'show_login_modal':    False,  
    })

@csrf_protect
def login_view(request):
    """
    Procesa el POST de login.
    - En GET: instancia LoginForm vacío, show_login_modal=False.
    - En POST: si válido, hace login y redirige; si inválido, show_login_modal=True y re-renderiza con errores.
    """
    show_login_modal = False
    # Instancia LoginForm con datos POST o vacío
    login_form = LoginForm(request, data=request.POST or None)
    # Preparamos también un RegisterForm vacío para el contexto, de modo que el modal de registro siga disponible en la plantilla
    register_form = RegisterForm()

    if request.method == 'POST':
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}!")
            # Si en el formulario viene un campo oculto 'next', redirige allí; si no, a la vista por defecto
            next_url = request.POST.get('next')
            return redirect(next_url or 'my_appointments')
        else:
            # Validación falló: abrimos el modal con errores
            show_login_modal = True

    # En GET o POST inválido, renderiza la plantilla base (ej. home) con login_form (con o sin errores),
    # register_form vacío, y flags adecuados para abrir o no modales.
    return render(request, 'core/home.html', {
        'login_form':        login_form,
        'register_form':     register_form,
        'show_login_modal':  show_login_modal,
        'show_register_modal': False,
    })


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('home')

@login_required
@handle_exceptions
def user_profile(request):
    # Citas activas
    active_appointments = Cita.objects.filter(user=request.user, date__gte=date.today()).order_by('date', 'time')
    # Historial de citas
    past_appointments = Cita.objects.filter(user=request.user, date__lt=date.today()).order_by('-date', '-time')

    context = {
        'active_appointments': active_appointments,
        'past_appointments': past_appointments,
    }
    return render(request, 'accounts/user_profile.html', context)

@login_required
@handle_exceptions
def update_profile_view(request):
    """
    Vista para actualizar los datos personales del usuario (nombre, apellidos, email).
    """
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu perfil se ha actualizado correctamente!')
            return redirect('user_profile')  
        else:
            messages.error(request, 'Por favor revisa los errores en el formulario.')
    else:
        form = UpdateUserForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/update_profile.html', context)