from django.utils import timezone
from django.db.models import Q
from .models import MensajeEspecial

def mensaje_especial_context(request):
    hoy = timezone.now().date()
    mensaje = MensajeEspecial.objects.filter(
        activo=True
    ).filter(
        Q(fecha_inicio__lte=hoy) | Q(fecha_inicio__isnull=True)
    ).filter(
        Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
    ).order_by('-fecha_inicio', '-id').first()
    return {
        'special_message': mensaje
    }
