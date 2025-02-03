from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.utils.formats import date_format
from django.utils.translation import gettext as _
from django.utils.translation import activate
import smtplib
import ssl
import certifi

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
        activate('es')
        enviar_correo_smtp(admin_emails, asunto, mensaje)


def enviar_confirmacion_cita(usuario_email, cita):
    """
    Envía un correo de confirmación al usuario y notifica a los administradores.
    """
    usuario_nombre = cita.user.get_full_name() or cita.user.username
     # 🛠 Corrección: Formateo de fecha en español
    fecha_formateada = date_format(cita.date, format=r"l, d \d\e F \d\e Y", use_l10n=True)
    hora_formateada = date_format(cita.time, format='H:i', use_l10n=True)

    asunto_usuario = '📅 Confirmación de tu cita en Zemar Nails'
    mensaje_usuario = f"""
    Estimado/a {usuario_nombre},

    Tu cita en **Zemar Nails** ha sido confirmada con éxito. Aquí tienes los detalles:

    📌 **Servicio:** {cita.service.nombre}  
    📅 **Fecha:** {fecha_formateada}  
    ⏰ **Hora:** {hora_formateada}  

    Si necesitas modificar o cancelar tu cita, puedes hacerlo desde tu cuenta en nuestra plataforma.

    ¡Te esperamos!

    Atentamente,  
    **Equipo Zemar Nails**  
    """

    enviar_correo_smtp([usuario_email], asunto_usuario, mensaje_usuario)

    # Email para administradores
    asunto_admin = '📢 Nueva cita reservada en Zemar Nails'
    mensaje_admin = f"""
    Se ha registrado una nueva cita:

    👤 **Cliente:** {usuario_nombre} ({usuario_email})  
    📌 **Servicio:** {cita.service.nombre}  
    📅 **Fecha:** {fecha_formateada}  
    ⏰ **Hora:** {hora_formateada}  

    **Información del usuario:**  
    🆔 **Nombre de usuario:** {cita.user.username}  
    📧 **Correo electrónico:** {usuario_email}  
    📞 **Teléfono:** {cita.user.profile.phone if hasattr(cita.user, 'profile') else 'No proporcionado'}  

    Esta cita ha sido agendada a través del sistema en línea.

    **Panel de administración de Zemar Nails**
    """

    enviar_correo_admin(asunto_admin, mensaje_admin)


def enviar_notificacion_modificacion_cita(usuario_email, cita):
    """
    Notifica al usuario y a los administradores cuando se modifica una cita.
    """
    usuario_nombre = cita.user.get_full_name() or cita.user.username
     # 🛠 Corrección: Formateo de fecha en español
    fecha_formateada = date_format(cita.date, format=r"l, d \d\e F \d\e Y", use_l10n=True)
    hora_formateada = date_format(cita.time, format='H:i', use_l10n=True)
    asunto_usuario = '📝 Modificación de tu cita en Zemar Nails'
    mensaje_usuario = f"""
    Estimado/a {usuario_nombre},

    Tu cita ha sido modificada. A continuación, los detalles actualizados:

    📌 **Servicio:** {cita.service.nombre}  
    📅 **Nueva fecha:** {cita.date.strftime('%A, %d de %B de %Y')}  
    ⏰ **Nueva hora:** {cita.time.strftime('%I:%M %p')}  

    Si no realizaste esta modificación, por favor contáctanos lo antes posible.

    Atentamente,  
    **Equipo Zemar Nails**  
    """

    enviar_correo_smtp([usuario_email], asunto_usuario, mensaje_usuario)

    asunto_admin = '🔄 Cita modificada en Zemar Nails'
    mensaje_admin = f"""
    Se ha modificado una cita:

    👤 **Cliente:** {usuario_nombre} ({usuario_email})  
    📌 **Servicio:** {cita.service.nombre}  
    📅 **Nueva fecha:** {fecha_formateada}  
    ⏰ **Nueva hora:** {hora_formateada}  

    **Información del usuario:**  
    🆔 **Nombre de usuario:** {cita.user.username}  
    📧 **Correo electrónico:** {usuario_email}  
    📞 **Teléfono:** {cita.user.profile.phone if hasattr(cita.user, 'profile') else 'No proporcionado'}  

    Esta actualización fue realizada a través del sistema en línea.

    **Panel de administración de Zemar Nails**
    """

    enviar_correo_admin(asunto_admin, mensaje_admin)


def enviar_notificacion_eliminacion_cita(usuario_email, cita):
    """
    Notifica al usuario y a los administradores cuando se cancela una cita.
    """
    usuario_nombre = cita.user.get_full_name() or cita.user.username
     # 🛠 Corrección: Formateo de fecha en español
    fecha_formateada = date_format(cita.date, format=r"l, d \d\e F \d\e Y", use_l10n=True)
    hora_formateada = date_format(cita.time, format='H:i', use_l10n=True)
    asunto_usuario = '❌ Cancelación de tu cita en Zemar Nails'
    mensaje_usuario = f"""
    Estimado/a {usuario_nombre},

    Tu cita ha sido cancelada con éxito. Aquí tienes los detalles:

    📌 **Servicio:** {cita.service.nombre}  
    📅 **Fecha:** {fecha_formateada}  
    ⏰ **Hora:** {hora_formateada}  

    Si deseas reservar una nueva cita, puedes hacerlo desde nuestra plataforma.

    Atentamente,  
    **Equipo Zemar Nails**  
    """

    enviar_correo_smtp([usuario_email], asunto_usuario, mensaje_usuario)

    asunto_admin = '⚠️ Cita cancelada en Zemar Nails'
    mensaje_admin = f"""
    Se ha cancelado una cita:

    👤 **Cliente:** {usuario_nombre} ({usuario_email})  
    📌 **Servicio:** {cita.service.nombre}  
    📅 **Fecha:** {fecha_formateada}  
    ⏰ **Hora:** {hora_formateada}  

    **Información del usuario:**  
    🆔 **Nombre de usuario:** {cita.user.username}  
    📧 **Correo electrónico:** {usuario_email}  
    📞 **Teléfono:** {cita.user.profile.phone if hasattr(cita.user, 'profile') else 'No proporcionado'}  

    Esta cancelación fue procesada a través del sistema en línea.

    **Panel de administración de Zemar Nails**
    """

    enviar_correo_admin(asunto_admin, mensaje_admin)
