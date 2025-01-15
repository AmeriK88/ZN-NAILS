from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .models import Appointment
from django.contrib import messages
from services.models import Service
from django.http import JsonResponse
from .utils import verificar_disponibilidad
import datetime


@login_required()
def book_appointment(request):
    service_id = request.GET.get('service_id')
    
    if service_id:
        servicio = get_object_or_404(Service, id=service_id)
        form = AppointmentForm(initial={'service': servicio})
    else:
        form = AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user

            # Verificar disponibilidad antes de guardar
            fecha = appointment.date
            hora_inicio = datetime.datetime.combine(fecha, appointment.time)
            duracion_servicio = appointment.service.duracion

            if verificar_disponibilidad(fecha, hora_inicio, duracion_servicio):
                appointment.save()
                messages.success(request, "¡Cita reservada con éxito!")
                return redirect('my_appointments')
            else:
                messages.error(request, "La hora seleccionada se solapa con otra cita. Elige otro horario.")

    return render(request, 'appointments/appointment_form.html', {'form': form})



@login_required()
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cita actualizada con éxito!")
            return redirect('my_appointments')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/appointment_form.html', {'form': form, 'appointment': appointment})


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

@login_required
def load_available_times(request):
    service_id = request.GET.get('service_id')
    selected_date = request.GET.get('date')

    if service_id and selected_date:
        try:
            service = Service.objects.get(id=service_id)
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()

            start_time = datetime.time(9, 0)
            end_time = datetime.time(20, 0)
            step = 15  # Intervalo de 15 minutos

            times = []
            current_time = datetime.datetime.combine(selected_date, start_time)

            while current_time.time() <= end_time:
                hora_inicio = current_time
                duracion_servicio = service.duracion

                # Verificar si el horario está disponible
                if verificar_disponibilidad(selected_date, hora_inicio, duracion_servicio):
                    times.append(current_time.time().strftime('%H:%M'))

                current_time += datetime.timedelta(minutes=step)

            return JsonResponse({'times': times})

        except Service.DoesNotExist:
            return JsonResponse({'error': 'Servicio no encontrado'}, status=404)

    return JsonResponse({'error': 'Parámetros inválidos'}, status=400)