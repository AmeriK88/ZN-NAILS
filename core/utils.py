import smtplib
import ssl
import certifi
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

# Crear el contexto SSL utilizando certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

def enviar_correo_smtp(destinatarios, asunto, mensaje):
    """
    Envía un correo utilizando smtplib para entornos de desarrollo.
    """
    try:
        # Configurar el servidor SMTP
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.ehlo()
        server.starttls(context=ssl._create_unverified_context())
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Crear el mensaje MIME con codificación UTF-8
        mensaje_mime = MIMEMultipart()
        mensaje_mime['From'] = settings.EMAIL_HOST_USER
        mensaje_mime['To'] = ', '.join(destinatarios)
        mensaje_mime['Subject'] = asunto
        mensaje_mime.attach(MIMEText(mensaje, 'plain', 'utf-8'))  # Codifica el mensaje como UTF-8

        # Enviar el correo
        server.sendmail(settings.EMAIL_HOST_USER, destinatarios, mensaje_mime.as_string())
        server.quit()
        print(f"✅ Correo enviado exitosamente a {', '.join(destinatarios)}.")
    except smtplib.SMTPException as e:
        print(f"❌ Error SMTP: {e}")
        raise
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        raise

def enviar_correo_admin(asunto, mensaje):
    """
    Envía un correo electrónico a los administradores configurados en settings.ADMINS.
    """
    if settings.ADMINS:
        admin_emails = [admin[1] for admin in settings.ADMINS]
        enviar_correo_smtp(admin_emails, asunto, mensaje)

def enviar_confirmacion_cita(usuario_email, cita):
    """
    Envía un correo de confirmación al usuario y notifica a los administradores.
    """
    asunto_usuario = 'Confirmación de tu cita en Zemar Nails'
    mensaje_usuario = f"""
    Hola {cita.user.get_full_name()},

    Gracias por reservar una cita con nosotros. Aquí están los detalles:

    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}

    En caso de no poder asistir, puedes modificar o cancelar tu cita desde nuestra app.

    ¡Te esperamos!
    """
    enviar_correo_smtp([usuario_email], asunto_usuario, mensaje_usuario)

    # Correo para los administradores
    asunto_admin = 'Nueva cita en Zemar Nails'
    mensaje_admin = f"""
    Nueva cita reservada:

    Usuario: {cita.user.get_full_name()} ({usuario_email})
    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}
    """
    enviar_correo_admin(asunto_admin, mensaje_admin)

def enviar_notificacion_modificacion_cita(usuario_email, cita):
    """
    Envía una notificación al usuario y a los administradores al modificar una cita.
    """
    asunto_usuario = 'Tu cita en Zemar Nails ha sido modificada'
    mensaje_usuario = f"""
    Hola {cita.user.get_full_name()},

    Tu cita ha sido modificada. Aquí están los nuevos detalles:

    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}

    Atentamente,
    Zemar Nails
    """
    enviar_correo_smtp([usuario_email], asunto_usuario, mensaje_usuario)

    asunto_admin = 'Cita modificada en Zemar Nails'
    mensaje_admin = f"""
    Una cita ha sido modificada:

    Usuario: {cita.user.get_full_name()} ({usuario_email})
    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}
    """
    enviar_correo_admin(asunto_admin, mensaje_admin)

def enviar_notificacion_eliminacion_cita(usuario_email, cita):
    """
    Envía una notificación al usuario y a los administradores al eliminar una cita.
    """
    asunto_usuario = 'Tu cita en Zemar Nails ha sido eliminada'
    mensaje_usuario = f"""
    Hola {cita.user.get_full_name()},

    Tu cita para el servicio {cita.service.nombre} el {cita.date} a las {cita.time} ha sido eliminada.

    Si lo deseas, puedes volver a agendar una cita desde nuestra app.

    Atentamente,
    Zemar Nails
    """
    enviar_correo_smtp([usuario_email], asunto_usuario, mensaje_usuario)

    asunto_admin = 'Cita eliminada en Zemar Nails'
    mensaje_admin = f"""
    Una cita ha sido eliminada:

    Usuario: {cita.user.get_full_name()} ({usuario_email})
    Servicio: {cita.service.nombre}
    Fecha: {cita.date}
    Hora: {cita.time}
    """
    enviar_correo_admin(asunto_admin, mensaje_admin)
