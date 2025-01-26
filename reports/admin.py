from django.contrib import admin
from .models import ReporteMensual, ReporteDiario
from .utils import calcular_reporte_diario, calcular_reporte_mensual

@admin.register(ReporteMensual)
class ReporteMensualAdmin(admin.ModelAdmin):
    list_display = ('mes', 'total_citas', 'ingresos_totales', 'ingresos_proyectados', 'creado_el')
    readonly_fields = ('total_citas', 'ingresos_totales', 'ingresos_proyectados', 'creado_el')

    def has_add_permission(self, request):
        return True  # Adding reports manually

    def has_delete_permission(self, request, obj=None):
        return True # Allow delete

    def save_model(self, request, obj, form, change):
        calcular_reporte_mensual(obj.mes)
        self.message_user(request, f"✅ Reporte generado para el mes {obj.mes.strftime('%B %Y')}")


@admin.register(ReporteDiario)
class ReporteDiarioAdmin(admin.ModelAdmin):
    list_display = ('dia', 'total_citas', 'ingresos_totales', 'creado_el')
    readonly_fields = ('total_citas', 'ingresos_totales', 'creado_el')

    def has_add_permission(self, request):
        return True  # Adding reports manually

    def has_delete_permission(self, request, obj=None):
        return True  # Allow delete

    def save_model(self, request, obj, form, change):
        calcular_reporte_diario(obj.dia)
        self.message_user(request, f"✅ Reporte generado para el día {obj.dia.strftime('%d/%m/%Y')}")
