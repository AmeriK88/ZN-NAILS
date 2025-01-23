from django.contrib import admin
from .models import Review, Service

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'servicio', 'rating', 'created_at')
    list_filter = ('servicio', 'rating', 'created_at')
    search_fields = ('user__username', 'servicio__nombre', 'comment')
    ordering = ('-created_at',)
