from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time')
    search_fields = ('user__username', 'service')
    list_filter = ('date', 'service')
