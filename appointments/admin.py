from django.contrib import admin
from .models import Cita
from .models import BloqueoFecha, BloqueoIntervalo  
from django.urls import path
from .views import calendario_bloqueo

@admin.register(Cita)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'comment')  
    search_fields = ('user__username', 'service', 'comment')
    list_filter = ('date', 'service')

@admin.register(BloqueoFecha)
class BloqueoFechaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'motivo', 'creado_el')
    list_filter = ('fecha',)
    search_fields = ('fecha', 'motivo')
    ordering = ['-fecha']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('calendario-bloqueo/', self.admin_site.admin_view(calendario_bloqueo), name='calendario_bloqueo'),
        ]
        return custom_urls + urls
    
@admin.register(BloqueoIntervalo)
class BloqueoIntervaloAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'motivo', 'creado_el')
    list_filter = ('fecha',)
    ordering = ['-fecha', 'hora_inicio']
