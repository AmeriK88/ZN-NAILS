from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service} - {self.date} {self.time}"

    class Meta:
        unique_together = ('date', 'time')
