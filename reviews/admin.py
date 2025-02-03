from django.contrib import admin
from .models import Reseña, Servicio

@admin.register(Reseña)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'servicio', 'rating', 'created_at')
    list_filter = ('servicio', 'rating', 'created_at')
    search_fields = ('user__username', 'servicio__nombre', 'comment')
    ordering = ('-created_at',)
