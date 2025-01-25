import ssl
import certifi
from django.core.mail import send_mail
from django.conf import settings


def enviar_correo_admin(asunto, mensaje):
    """
    Envía un correo electrónico a los administradores configurados en settings.ADMINS.
    """
    if settings.ADMINS:
        admin_emails = [admin[1] for admin in settings.ADMINS]
        send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, admin_emails, fail_silently=False)


def enviar_confirmacion_cita(usuario_email, cita):
    """
    Envía un correo de confirmación al usuario y notifica a los administradores.
    """
    asunto = 'Confirmación de tu cita en Zemar Nails'
    mensaje_usuario = f"""
    Hola {cita.user.get_full_name()},

    Gracias por reservar una cita con nosotros. Aquí están los detalles de tu cita:

    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}

    En caso de no poder asistir, puedes modificar o cancelar tu cita desde nuestra app.

    ¡Te esperamos!
    """

    # Crear un contexto SSL usando el certificado de certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    send_mail(
        asunto,
        mensaje_usuario,
        settings.EMAIL_HOST_USER,
        [usuario_email],
        fail_silently=False,
    )

    # Notificar a los administradores
    mensaje_admin = f"""
    Nueva cita reservada:

    Usuario: {cita.user.get_full_name()} ({usuario_email})
    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}
    """
    enviar_correo_admin('Nueva cita en Zemar Nails', mensaje_admin)


def enviar_notificacion_modificacion_cita(usuario_email, cita):
    """
    Envía una notificación al usuario y a los administradores al modificar una cita.
    """
    asunto = 'Tu cita en Zemar Nails ha sido modificada'
    mensaje_usuario = f"""
    Hola {cita.user.get_full_name()},

    Tu cita ha sido modificada. Aquí están los nuevos detalles:

    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}

    Atentamente,
    Zemar Nails
    """
    # Crear un contexto SSL usando el certificado de certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    send_mail(
        asunto,
        mensaje_usuario,
        settings.EMAIL_HOST_USER,
        [usuario_email],
        fail_silently=False,
    )

    # Notificar a los administradores
    mensaje_admin = f"""
    Una cita ha sido modificada:

    Usuario: {cita.user.get_full_name()} ({usuario_email})
    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}
    """
    enviar_correo_admin('Cita modificada en Zemar Nails', mensaje_admin)


def enviar_notificacion_eliminacion_cita(usuario_email, cita):
    """
    Envía una notificación al usuario y a los administradores al eliminar una cita.
    """
    asunto = 'Tu cita en Zemar Nails ha sido eliminada'
    mensaje_usuario = f"""
    Hola {cita.user.get_full_name()},

    Tu cita para el servicio {cita.service.nombre} el {cita.date} a las {cita.time} ha sido eliminada.

    Si lo deseas, puedes volver a agendar una cita desde nuestra app.

    Atentamente,
    Zemar Nails
    """
    # Crear un contexto SSL usando el certificado de certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    send_mail(
        asunto,
        mensaje_usuario,
        settings.EMAIL_HOST_USER,
        [usuario_email],
        fail_silently=False,
    )

    # Notificar a los administradores
    mensaje_admin = f"""
    Una cita ha sido eliminada:

    Usuario: {cita.user.get_full_name()} ({usuario_email})
    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}
    """
    enviar_correo_admin('Cita eliminada en Zemar Nails', mensaje_admin)
