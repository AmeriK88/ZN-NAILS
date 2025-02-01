from datetime import timedelta, datetime
from .models import Appointment
from appointments.models import BloqueoFecha

def verificar_disponibilidad(fecha, hora_inicio, duracion_servicio):
    hora_fin = hora_inicio + timedelta(minutes=duracion_servicio)
    
    citas_existentes = Appointment.objects.filter(date=fecha)

    for cita in citas_existentes:
        cita_fin = datetime.combine(cita.date, cita.time) + timedelta(minutes=cita.service.duracion)

        # Comprobar si hay solapamiento
        if (hora_inicio < cita_fin) and (hora_fin > datetime.combine(cita.date, cita.time)):
            return False  

    return True  

def verificar_disponibilidad(fecha, hora_inicio, duracion_servicio):
    """
    Verifica si la fecha y hora seleccionadas están disponibles.
    """
    # Bloquear fechas que estén en BloqueoFecha
    if BloqueoFecha.objects.filter(fecha=fecha).exists():
        return False

    hora_fin = hora_inicio + timedelta(minutes=duracion_servicio)
    citas_existentes = Appointment.objects.filter(date=fecha)

    for cita in citas_existentes:
        cita_fin = datetime.combine(cita.date, cita.time) + timedelta(minutes=cita.service.duracion)
        if (hora_inicio < cita_fin) and (hora_fin > datetime.combine(cita.date, cita.time)):
            return False  # Hay solapamiento

    return True  