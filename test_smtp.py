import smtplib
import ssl
import certifi

context = ssl.create_default_context(cafile=certifi.where())

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls(context=context)
    server.login('chenchito88@gmail.com', 'xiej jibh hjks thjj')
    print("Conexión SMTP exitosa.")
    server.quit()
except Exception as e:
    print(f"Error en la conexión SMTP: {e}")
