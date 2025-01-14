from django.db import models

class Service(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='static/imagenes/', null=True, blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
