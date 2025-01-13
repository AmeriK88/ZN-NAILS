from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment
from django.contrib import messages

@login_required()
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.user = request.user
                appointment.save()
                messages.success(request, "¡Cita reservada con éxito!")
                return redirect('my_appointments')
            except Exception as e:
                messages.error(request, f"Error al guardar la cita: {e}")
        else:
            messages.error(request, "Error al reservar la cita. Revisa los campos.")
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required(login_url='login')
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    if not appointments.exists():
        messages.info(request, "No tienes citas registradas.")
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})

