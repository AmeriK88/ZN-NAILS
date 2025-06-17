from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import login 
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
    - En GET: muestra home con register_form vacío y login_form vacío.
    - En POST con datos inválidos: re-renderiza home con register_form con errores y show_register_modal=True.
    - En registro exitoso: crea usuario, lo autentica, redirige.
    """
    show_register_modal = False
    # Prepara un LoginForm vacío para que el contexto siempre tenga login_form
    login_form = LoginForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # Guardar el usuario
            user = register_form.save(commit=False)
            # Asignar first_name, last_name, email si tu formulario los incluye:
            user.first_name = register_form.cleaned_data.get('first_name', '')
            user.last_name  = register_form.cleaned_data.get('last_name', '')
            user.email      = register_form.cleaned_data.get('email', '')
            user.save()

            # Autenticación automática tras registro
            username = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"¡Bienvenido/a {user.username}! Tu cuenta ha sido creada e iniciada sesión con éxito.")
                return redirect('home')
            else:
                messages.error(request, "Hubo un problema al iniciar sesión automáticamente. Intenta iniciar sesión manualmente.")
                return redirect('login')
        else:
            # Errores en registro: reabrir modal
            show_register_modal = True
    else:
        register_form = RegisterForm()

    # Renderiza la home con ambos formularios y flags
    return render(request, 'core/home.html', {
        'register_form':     register_form,
        'login_form':        login_form,
        'show_register_modal': show_register_modal,
        'show_login_modal':   False,
    })

@csrf_protect
def login_view(request):
    """
    Procesa POST de login. 
    - Si GET o POST sin datos, muestra home con login_form vacío.
    - Si POST con errores, re-renderiza home con login_form que incluye errores y show_login_modal=True.
    """
    show_login_modal = False
    # Prepara un formulario de registro vacío para el contexto (el modal de registro puede estar disponible)
    register_form = RegisterForm()

    if request.method == 'POST':
        login_form = LoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}!")
            # Redirige a la página que desees tras login exitoso
            return redirect('my_appointments')
        else:
            # Hay errores en el login: reabrir modal
            show_login_modal = True
    else:
        # GET: formulario vacío
        login_form = LoginForm()

    # Renderizamos la home pasando login_form (posible con errores), register_form vacío, y flags
    return render(request, 'core/home.html', {
        'login_form': login_form,
        'register_form': register_form,
        'show_login_modal': show_login_modal,
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