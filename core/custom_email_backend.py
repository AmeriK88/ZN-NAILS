from django.core.mail.backends.base import BaseEmailBackend
from .utils import enviar_correo_smtp  # Importa tu función personalizada

class CustomEmailBackend(BaseEmailBackend):
    """
    Backend de correo personalizado que utiliza la lógica de `enviar_correo_smtp`.
    """
    def send_messages(self, email_messages):
        sent_count = 0
        for message in email_messages:
            try:
                enviar_correo_smtp(
                    destinatarios=message.to,
                    asunto=message.subject,
                    mensaje=message.body
                )
                sent_count += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        return sent_count
