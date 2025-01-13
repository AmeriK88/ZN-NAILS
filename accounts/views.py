from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def register_view(request):
    show_register_modal = False

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.success(request, f"¡Bienvenido/a {user.username}! Tu cuenta ha sido creada con éxito.")
            return redirect('home')
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
            return redirect('home')
        else:
            show_login_modal = True  
    else:
        form = LoginForm()

    return render(request, 'core/home.html', {'form': form, 'show_login_modal': show_login_modal})


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('home')
