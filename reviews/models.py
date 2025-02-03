from django.db import models
from django.contrib.auth.models import User
from services.models import Servicio  


class Reseña(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.servicio} - {self.rating}⭐'

