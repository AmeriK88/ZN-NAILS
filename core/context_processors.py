import random
from django.utils import timezone
from django.db.models import Q
from .models import MensajeEspecial, ContadorVisitas

def mensaje_especial_context(request):
    """
    Provee:
    - special_message: MensajeEspecial activo (si existe)
    - contador_actualizado: visitas almacenadas
    - header_message: texto corto y creativo para mostrar en el encabezado
    """
    hoy = timezone.now().date()
    
    # Mensaje especial (si aplica)
    mensaje = MensajeEspecial.objects.filter(
        activo=True
    ).filter(
        Q(fecha_inicio__lte=hoy) | Q(fecha_inicio__isnull=True)
    ).filter(
        Q(fecha_fin__gte=hoy) | Q(fecha_fin__isnull=True)
    ).order_by('-fecha_inicio', '-id').first()

    # Contador de visitas (si usas; igual puedes mantenerlo o eliminarlo si ya no lo necesitas aquí)
    try:
        contador = ContadorVisitas.objects.get(pk=1)
        visitas = contador.total
    except ContadorVisitas.DoesNotExist:
        visitas = 0

    # Opciones cortas y creativas para el encabezado
    header_options = [
        "Uñas que... ✨| hablan",
        "Brilla ✨| en cada detalle",
        "Estilo ✨| a medida",
        "Tu estilo ✨| tu esencia",
        "Belleza ✨| sin complicaciones",
        "Manicura ✨| con magia",
        "Confía ✨| en tus manos",
        "Diseña ✨| tu huella",
        "Siente ✨| la diferencia",
    ]
    header_message = random.choice(header_options)

    return {
        'special_message': mensaje,
        'contador_actualizado': visitas,
        'header_message': header_message,
    }
