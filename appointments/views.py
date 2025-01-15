from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment
from django.contrib import messages
from services.models import Service

@login_required()
def book_appointment(request):
    service_id = request.GET.get('service_id')  

    # Si hay un servicio, lo obtenemos
    if service_id:
        servicio = get_object_or_404(Service, id=service_id)
        form = AppointmentForm(initial={'service': servicio})  
    else:
        form = AppointmentForm()

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

    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required(login_url='login')
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cita actualizada con éxito!")
            return redirect('my_appointments')
        else:
            messages.error(request, "Error al actualizar la cita. Revisa los campos.")
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {'form': form, 'appointment': appointment})

@login_required(login_url='login')
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "¡Cita eliminada correctamente!")
        return redirect('my_appointments')
    return redirect('confirm_delete_appointment', appointment_id=appointment_id)


@login_required(login_url='login')
def confirm_delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})


@login_required(login_url='login')
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    if not appointments.exists():
        messages.info(request, "No tienes citas registradas.")
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})

