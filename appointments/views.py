from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Cita
from services.models import Servicio
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
    servicio = get_object_or_404(Servicio, id=service_id) if service_id else None
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
    cita = get_object_or_404(Cita, id=appointment_id, user=request.user)

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
    cita = get_object_or_404(Cita, id=appointment_id, user=request.user)

    if request.method == 'POST':
        cita_detalle = {
            'email': request.user.email,
            'servicio': cita.service.nombre,
            'fecha': cita.date,
            'hora': cita.time,
        }
        enviar_notificacion_eliminacion_cita(cita_detalle['email'], cita)
        cita.delete()
        messages.success(request, "¡Cita eliminada correctamente! Se ha enviado un correo de confirmación. ✅")
        return redirect('my_appointments')

    return render(request, 'appointments/confirm_delete.html', {'appointment': cita})


@login_required
@handle_exceptions
def confirm_delete_appointment(request, appointment_id):
    """
    Vista para confirmar la eliminación de una cita antes de proceder.
    """
    appointment = get_object_or_404(Cita, id=appointment_id, user=request.user)
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})


@login_required
@handle_exceptions
def my_appointments(request):
    """
    Vista para mostrar las citas del usuario autenticado.
    """
    appointments = Cita.objects.filter(user=request.user)
    if not appointments.exists():
        messages.info(request, "No tienes citas registradas.")
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
@handle_exceptions
def load_available_times(request):
    """
    Devuelve los horarios disponibles para un servicio y una fecha,
    garantizando que el intervalo completo del servicio no se solape con citas existentes
    ni con intervalos de bloqueo definidos.
    """
    service_id = request.GET.get('service_id')
    selected_date_str = request.GET.get('date')

    if not service_id or not selected_date_str:
        return JsonResponse({'error': 'Parámetros inválidos ⚠️'}, status=400)

    try:
        service = Servicio.objects.get(id=service_id)
        selected_date = datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except Servicio.DoesNotExist:
        return JsonResponse({'error': 'Servicio no encontrado ⚠️'}, status=404)

    # Verificar bloqueo total del día
    bloqueo_dia = BloqueoFecha.objects.filter(fecha=selected_date).first()
    if bloqueo_dia:
        return JsonResponse({'blocked': True, 'motivo': bloqueo_dia.motivo}, status=200)

    start_time = datetime.time(9, 0)
    end_time = datetime.time(20, 0)
    step = service.duracion  # Duración en minutos según el servicio

    # Obtener intervalos ocupados por citas existentes
    citas = Cita.objects.filter(date=selected_date)
    horarios_ocupados = []
    for cita in citas:
        inicio_cita = datetime.datetime.combine(selected_date, cita.time)
        fin_cita = inicio_cita + datetime.timedelta(minutes=cita.service.duracion)
        bloque_actual = inicio_cita
        while bloque_actual < fin_cita:
            horarios_ocupados.append(bloque_actual.time())
            bloque_actual += datetime.timedelta(minutes=service.duracion)

    # Obtener intervalos bloqueados por el admin (bloqueos parciales)
    blocked_intervals = get_blocked_intervals(selected_date)

    # Generar los horarios disponibles
    times = []
    current_time = datetime.datetime.combine(selected_date, start_time)
    end_datetime = datetime.datetime.combine(selected_date, end_time)
    service_duration_td = datetime.timedelta(minutes=service.duracion)

    while current_time + service_duration_td <= end_datetime:
        candidate_end = current_time + service_duration_td

        # Comprobar si el rango de horas se solapa con citas existentes
        citas_ocupadas = any(
            hora_ocupada >= current_time.time() and hora_ocupada < candidate_end.time()
            for hora_ocupada in horarios_ocupados
        )
        # Comprobar solapamiento con bloqueos parciales
        bloqueado = is_interval_blocked(current_time, candidate_end, blocked_intervals)

        if not citas_ocupadas and not bloqueado:
            times.append(current_time.time().strftime('%H:%M'))

        current_time += service_duration_td

    return JsonResponse({'blocked': False, 'times': times})


@staff_member_required
def calendario_bloqueo(request):
    """
    Vista del calendario de fechas bloqueadas accesible solo para administradores.
    """
    bloqueos = BloqueoFecha.objects.all()
    return render(request, 'admin/appointments/calendario_bloqueo.html', {'bloqueos': bloqueos})


def get_blocked_intervals(selected_date):
    """
    Devuelve una lista de tuplas (inicio, fin) de BloqueoIntervalo para la fecha dada.
    """
    from .models import BloqueoIntervalo  # Import local para evitar problemas circulares
    blocked = []
    for bloqueo in BloqueoIntervalo.objects.filter(fecha=selected_date):
        inicio = datetime.datetime.combine(selected_date, bloqueo.hora_inicio)
        fin = datetime.datetime.combine(selected_date, bloqueo.hora_fin)
        blocked.append((inicio, fin))
    return blocked

def is_interval_blocked(candidate_start, candidate_end, blocked_intervals):
    """
    Verifica si el intervalo candidato se solapa con alguno de los intervalos bloqueados.
    """
    for b_start, b_end in blocked_intervals:
        # Si candidate_start < b_end y candidate_end > b_start, hay solapamiento.
        if candidate_start < b_end and candidate_end > b_start:
            return True
    return False

