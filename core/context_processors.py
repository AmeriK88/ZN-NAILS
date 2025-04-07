from django.utils import timezone
from django.db.models import Q
from .models import MensajeEspecial, ContadorVisitas

def mensaje_especial_context(request):
    hoy = timezone.now().date()
    
    mensaje = MensajeEspecial.objects.filter(
        activo=True
    ).filter(
        Q(fecha_inicio__lte=hoy) | Q(fecha_inicio__isnull=True)
    ).filter(
        Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
    ).order_by('-fecha_inicio', '-id').first()

    try:
        contador = ContadorVisitas.objects.get(pk=1)
        visitas = contador.total
    except ContadorVisitas.DoesNotExist:
        visitas = 0

    return {
        'special_message': mensaje,
        'contador_actualizado': visitas,
    }
