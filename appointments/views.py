from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
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
from appointments.models import BloqueoFecha
import datetime


@login_required
@handle_exceptions
def book_appointment(request):
    """
    Vista para reservar una nueva cita.
    Valida que la fecha seleccionada no esté bloqueada antes de permitir la reserva.
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

            # Verificar si la fecha está bloqueada antes de hacer cualquier otra validación
            bloqueo = BloqueoFecha.objects.filter(fecha=fecha).first()
            if bloqueo:
                messages.error(request, f"No puedes reservar en esta fecha ({fecha}), motivo: {bloqueo.motivo or 'Sin especificar'}. ⚠️")
                return render(request, 'appointments/appointment_form.html', {'form': form})

            # Verificar disponibilidad horaria
            hora_inicio = datetime.datetime.combine(fecha, cita.time)
            duracion_servicio = cita.service.duracion
            if verificar_disponibilidad(fecha, hora_inicio, duracion_servicio):
                cita.save()
                enviar_confirmacion_cita(request.user.email, cita)
                messages.success(request, "¡Cita reservada con éxito! Se ha enviado un correo de confirmación. ✅")
                return redirect('my_appointments')
            else:
                messages.error(request, "La hora seleccionada se solapa con otra cita. Elige otro horario. ⚠️")

    return render(request, 'appointments/appointment_form.html', {'form': form})


@login_required
@handle_exceptions
def edit_appointment(request, appointment_id):
    """
    Vista para editar una cita existente.
    Verifica si la fecha editada está bloqueada antes de permitir la modificación.
    """
    cita = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=cita)
        if form.is_valid():
            nueva_fecha = form.cleaned_data['date']

            # Verificar si la nueva fecha está bloqueada
            bloqueo = BloqueoFecha.objects.filter(fecha=nueva_fecha).first()
            if bloqueo:
                messages.error(request, f" No puedes cambiar la cita a esta fecha ({nueva_fecha}), motivo: {bloqueo.motivo or 'Sin especificar'}. ⚠️")
                return render(request, 'appointments/appointment_form.html', {'form': form, 'appointment': cita})

            # Si la fecha es válida, actualizar la cita
            cita = form.save()
            enviar_notificacion_modificacion_cita(request.user.email, cita)
            messages.success(request, "¡Cita actualizada con éxito! Se ha enviado un correo de notificación. ✅")
            return redirect('my_appointments')

    form = AppointmentForm(instance=cita)
    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'appointment': cita,
        'bloqueos': BloqueoFecha.objects.all()  
    })


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
        messages.success(request, "¡Cita eliminada correctamente! ✅")
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
    Si la fecha está bloqueada, devuelve un mensaje con la razón del bloqueo.
    """
    service_id = request.GET.get('service_id')
    selected_date = request.GET.get('date')

    if service_id and selected_date:
        try:
            service = Service.objects.get(id=service_id)
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()

            # Verificar si la fecha está bloqueada
            bloqueo = BloqueoFecha.objects.filter(fecha=selected_date).first()
            if bloqueo:
                return JsonResponse({'blocked': True, 'motivo': bloqueo.motivo}, status=200)

            start_time = datetime.time(9, 0)  
            end_time = datetime.time(20, 0)  
            step = service.duracion  

            # Obtener todas las citas de la fecha seleccionada
            citas = Appointment.objects.filter(date=selected_date)

            # Lista de horarios ocupados
            horarios_ocupados = []

            for cita in citas:
                inicio_cita = datetime.datetime.combine(selected_date, cita.time)
                fin_cita = inicio_cita + datetime.timedelta(minutes=cita.service.duracion)

                # Agregar a la lista de horarios ocupados todos los bloques que cubre la cita
                bloque_actual = inicio_cita
                while bloque_actual < fin_cita:
                    horarios_ocupados.append(bloque_actual.time())
                    bloque_actual += datetime.timedelta(minutes=service.duracion)

            # Generar los horarios disponibles
            times = []
            current_time = datetime.datetime.combine(selected_date, start_time)

            while current_time.time() < end_time:
                # Comprobar si el horario y su rango están ocupados
                fin_actual = current_time + datetime.timedelta(minutes=step)
                
                if not any(hora_ocupada >= current_time.time() and hora_ocupada < fin_actual.time() for hora_ocupada in horarios_ocupados):
                    times.append(current_time.time().strftime('%H:%M'))

                current_time += datetime.timedelta(minutes=step)

            return JsonResponse({'blocked': False, 'times': times})

        except Service.DoesNotExist:
            return JsonResponse({'error': 'Servicio no encontrado ⚠️'}, status=404)

    return JsonResponse({'error': 'Parámetros inválidos ⚠️'}, status=400)


@staff_member_required
def calendario_bloqueo(request):
    """
    Vista del calendario de fechas bloqueadas accesible solo para administradores.
    """
    bloqueos = BloqueoFecha.objects.all()
    return render(request, 'admin/appointments/calendario_bloqueo.html', {'bloqueos': bloqueos})