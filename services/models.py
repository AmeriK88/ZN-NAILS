from django.db import models

class Service(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='static/imagenes/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    duracion = models.PositiveIntegerField(default=30, help_text="Duración del servicio en minutos")

    def __str__(self):
        return self.nombre
