from django.db import models
from django.contrib.auth.models import User
from services.models import Service  # Importa el modelo Service

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    comment = models.TextField(blank=True, null=True, help_text="Añade un comentario o instrucción especial") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.nombre} - {self.date} {self.time}"

    class Meta:
        unique_together = ('date', 'time')
