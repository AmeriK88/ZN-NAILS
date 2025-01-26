from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.utils.timezone import make_aware
from .models import ReporteMensual, ReporteDiario
from appointments.models import Appointment
from dateutil.relativedelta import relativedelta

def calcular_reporte_diario(fecha):
    """
    Genera el reporte diario solo para la fecha especificada.
    """
    fecha_inicio = make_aware(datetime.combine(fecha, datetime.min.time()))
    fecha_fin = fecha_inicio + timedelta(days=1)
    citas = Appointment.objects.filter(date__gte=fecha_inicio, date__lt=fecha_fin)

    total_citas = citas.count()
    total_ingresos = citas.aggregate(
        total=Sum(F('service__precio'))
    )['total'] or 0

    ReporteDiario.objects.update_or_create(
        dia=fecha,
        defaults={
            'total_citas': total_citas,
            'ingresos_totales': total_ingresos,
        }
    )
    print(f"✅ Reporte diario generado para {fecha.strftime('%d/%m/%Y')}")


def calcular_reporte_mensual(fecha):
    """
    Genera el reporte mensual basado en la fecha proporcionada.
    """
    mes_inicio = make_aware(datetime.combine(fecha.replace(day=1), datetime.min.time()))
    mes_fin = mes_inicio + relativedelta(months=1)
    citas = Appointment.objects.filter(date__gte=mes_inicio, date__lt=mes_fin)

    total_citas = citas.count()
    total_ingresos = citas.aggregate(
        total=Sum(F('service__precio'))
    )['total'] or 0

    ReporteMensual.objects.update_or_create(
        mes=mes_inicio.date(),
        defaults={
            'total_citas': total_citas,
            'ingresos_totales': total_ingresos,
            'ingresos_proyectados': total_ingresos,
        }
    )
    print(f"✅ Reporte mensual generado para {mes_inicio.strftime('%B %Y')}")

def limpiar_reportes():
    """
    Elimina todos los reportes existentes (mensuales y diarios).
    """
    ReporteMensual.objects.all().delete()
    ReporteDiario.objects.all().delete()
    print("✅ Todos los reportes fueron eliminados.")
