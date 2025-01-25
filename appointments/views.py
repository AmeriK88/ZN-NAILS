from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Appointment
from services.models import Service
from core.utils import (
    enviar_confirmacion_cita,
    enviar_notificacion_modificacion_cita,
    enviar_notificacion_eliminacion_cita,
)
from .utils import verificar_disponibilidad
from core.decorators import handle_exceptions
import datetime


@login_required
@handle_exceptions
def book_appointment(request):
    """
    Vista para reservar una nueva cita.
    Envía un correo de confirmación al usuario después de reservar exitosamente.
    """
    service_id = request.GET.get('service_id')
    servicio = get_object_or_404(Service, id=service_id) if service_id else None
    form = AppointmentForm(initial={'service': servicio}) if servicio else AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.user = request.user

            fecha = cita.date
            hora_inicio = datetime.datetime.combine(fecha, cita.time)
            duracion_servicio = cita.service.duracion

            if verificar_disponibilidad(fecha, hora_inicio, duracion_servicio):
                cita.save()
                enviar_confirmacion_cita(request.user.email, cita)
                messages.success(request, "¡Cita reservada con éxito! Se ha enviado un correo de confirmación.")
                return redirect('my_appointments')
            else:
                messages.error(request, "La hora seleccionada se solapa con otra cita. Elige otro horario.")

    return render(request, 'appointments/appointment_form.html', {'form': form})


@login_required
@handle_exceptions
def edit_appointment(request, appointment_id):
    """
    Vista para editar una cita existente.
    Envía un correo de notificación al usuario después de modificar la cita.
    """
    cita = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save()
            enviar_notificacion_modificacion_cita(request.user.email, cita)
            messages.success(request, "¡Cita actualizada con éxito! Se ha enviado un correo de notificación.")
            return redirect('my_appointments')

    form = AppointmentForm(instance=cita)
    return render(request, 'appointments/appointment_form.html', {'form': form, 'appointment': cita})


@login_required
@handle_exceptions
def delete_appointment(request, appointment_id):
    """
    Vista para eliminar una cita.
    Envía un correo de notificación al usuario y a los administradores después de eliminar la cita.
    """
    cita = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        cita_detalle = {
            'email': request.user.email,
            'servicio': cita.service.nombre,
            'fecha': cita.date,
            'hora': cita.time,
        }
        enviar_notificacion_eliminacion_cita(cita_detalle['email'], cita)
        cita.delete()
        messages.success(request, "¡Cita eliminada correctamente!")
        return redirect('my_appointments')

    return render(request, 'appointments/confirm_delete.html', {'appointment': cita})


@login_required
@handle_exceptions
def confirm_delete_appointment(request, appointment_id):
    """
    Vista para confirmar la eliminación de una cita antes de proceder.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})


@login_required
@handle_exceptions
def my_appointments(request):
    """
    Vista para mostrar las citas del usuario autenticado.
    """
    appointments = Appointment.objects.filter(user=request.user)
    if not appointments.exists():
        messages.info(request, "No tienes citas registradas.")
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
@handle_exceptions
def load_available_times(request):
    """
    Carga los horarios disponibles para un servicio y una fecha específica.
    Devuelve los horarios como JSON.
    """
    service_id = request.GET.get('service_id')
    selected_date = request.GET.get('date')

    if service_id and selected_date:
        try:
            service = Service.objects.get(id=service_id)
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()

            start_time = datetime.time(9, 0)
            end_time = datetime.time(20, 0)
            step = service.duracion  # Duración del servicio en minutos

            times = []
            current_time = datetime.datetime.combine(selected_date, start_time)

            while current_time.time() <= end_time:
                hora_inicio = current_time
                duracion_servicio = service.duracion

                if verificar_disponibilidad(selected_date, hora_inicio, duracion_servicio):
                    times.append(current_time.time().strftime('%H:%M'))

                current_time += datetime.timedelta(minutes=step)

            return JsonResponse({'times': times})

        except Service.DoesNotExist:
            return JsonResponse({'error': 'Servicio no encontrado'}, status=404)

    return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
