from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'comment')  
    search_fields = ('user__username', 'service', 'comment')
    list_filter = ('date', 'service')
