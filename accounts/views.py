from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from appointments.models import Cita  
from core.decorators import handle_exceptions 
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UpdateUserForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from datetime import date

@csrf_protect
def register_view(request):
    show_register_modal = False

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Guardar el usuario
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            # 🔐 Autenticar al usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # 🔑 Iniciar sesión automáticamente
                login(request, user)
                messages.success(request, f"¡Bienvenido/a {user.username}! Tu cuenta ha sido creada e iniciada sesión con éxito.")
                return redirect('home')
            else:
                messages.error(request, "Hubo un problema al iniciar sesión automáticamente. Intenta iniciar sesión manualmente.")
                return redirect('login')
        else:
            show_register_modal = True  
    else:
        form = RegisterForm()

    return render(request, 'core/home.html', {'form': form, 'show_register_modal': show_register_modal})


@csrf_protect
def login_view(request):
    show_login_modal = False  

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}!")
            return redirect('my_appointments')
        else:
            show_login_modal = True 
    else:
        form = LoginForm()

    return render(request, 'core/home.html', {
        'form': form,
        'show_login_modal': show_login_modal
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