from django.db import models
from django.contrib.auth.models import User
from services.models import Service 
from django.utils.translation import gettext_lazy as _

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    comment = models.TextField(blank=True, null=True, help_text="Añade un comentario o instrucción especial") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.nombre} - {self.date} {self.time}"

class BloqueoFecha(models.Model):
    fecha = models.DateField(unique=True, verbose_name=_("Fecha Bloqueada"))
    motivo = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Motivo"))
    creado_el = models.DateTimeField(auto_now_add=True, verbose_name=_("Creado el"))

    class Meta:
        verbose_name = _("Bloqueo de Fecha")
        verbose_name_plural = _("Bloqueos de Fechas")
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha} - {self.motivo if self.motivo else 'Sin motivo'}"