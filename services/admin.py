from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion', 'disponible')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('disponible',)
