import smtplib
import ssl
import certifi

# Configuración de email desde tus settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'chenchito88@gmail.com'
EMAIL_HOST_PASSWORD = 'xiej jibh hjks thjj'

# Crear el contexto SSL usando certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

try:
    # Iniciar conexión SMTP
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()  # Identificar cliente SMTP
    server.starttls(context=ssl._create_unverified_context())

    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # Inicia sesión con las credenciales

    print("✅ Conexión SMTP exitosa.")

    # Enviar un correo de prueba (opcional)
    from_email = EMAIL_HOST_USER
    to_email = 'chenchito88@gmail.com'  # Cambia esto por un correo válido
    subject = "Correo de prueba"
    body = "Este es un correo de prueba desde Zemar Nails."

    mensaje = f"Subject: {subject}\n\n{body}"
    server.sendmail(from_email, to_email, mensaje)

    print(f"✅ Correo enviado exitosamente a {to_email}.")
    server.quit()  # Cierra la conexión SMTP

except smtplib.SMTPException as e:
    print(f"❌ Error en la conexión SMTP: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
