from django.contrib import admin
from django.utils.html import format_html
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion', 'disponible', 'preview_image')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('disponible',)

    def preview_image(self, obj):
        if obj.imagen:  # Asegúrate de que el campo se llame `imagen`
            return format_html('<img src="{}" style="width: 75px; height: auto; border-radius: 5px;" alt="{}" />', obj.imagen.url, obj.nombre)
        return "No image"

    preview_image.short_description = "Previsualización"  # Nombre de la columna en el admin
