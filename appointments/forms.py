from django import forms
from .models import Cita
from services.models import Servicio
from django.utils.translation import gettext_lazy as _
import datetime

class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Servicio.objects.filter(disponible=True),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'id_service'}),
        empty_label=_("Selecciona un servicio"),
        label=_("📌 Servicio")
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-lg',
            'min': datetime.date.today().strftime('%Y-%m-%d')
        }),
        label=_("📅 Fecha")
    )

    # VALIDACIÓN: no permitir sábados ni domingos
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date.weekday() in (5, 6):  # 5 = sábado, 6 = domingo
            raise forms.ValidationError(_("No se pueden reservar citas en fin de semana."))
        return date

    time = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        label=_("⏰ Hora")
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'rows': 3,
            'placeholder': _("Escribe algún comentario o instrucción especial (opcional)")
        }),
        required=False,
        label=_("📝 Comentario")
    )

    class Meta:
        model = Cita
        fields = ['service', 'date', 'time', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay un servicio seleccionado, generar los horarios
        if 'service' in self.data and 'date' in self.data:
            try:
                service_id = int(self.data.get('service'))
                service = Servicio.objects.get(id=service_id)
                selected_date = self.data.get('date')
                self.fields['time'].choices = self.get_available_times(service, selected_date)
            except (ValueError, Servicio.DoesNotExist):
                self.fields['time'].choices = []
        elif self.instance.pk:
            # Si estamos editando, cargar los horarios del servicio existente
            self.fields['time'].choices = self.get_available_times(self.instance.service, self.instance.date)
        else:
            self.fields['time'].choices = []

    def get_available_times(self, service, selected_date):
        start_time = datetime.time(9, 0)
        end_time = datetime.time(20, 0)
        service_duration_td = datetime.timedelta(minutes=service.duracion)
        times = []
        step_increment = datetime.timedelta(minutes=5)
        candidate_start = datetime.datetime.combine(datetime.date.today(), start_time)
        end_datetime = datetime.datetime.combine(datetime.date.today(), end_time)

        while candidate_start + service_duration_td <= end_datetime:
            candidate_end = candidate_start + service_duration_td
            # Verificar solapamientos con citas ya existentes
            if not Cita.objects.filter(date=selected_date, time=candidate_start.time()).exists():
                times.append((candidate_start.time().strftime('%H:%M'), candidate_start.time().strftime('%H:%M')))
            candidate_start += step_increment

        return times

    # MÉTODO DE VALIDACIÓN DE LA HORA
    def clean_time(self):
        time = self.cleaned_data.get('time')
        service = self.cleaned_data.get('service')
        date = self.cleaned_data.get('date')

        if service and date:
            available_times = [t[0] for t in self.get_available_times(service, date)]
            
            if time not in available_times:
                raise forms.ValidationError("⚠️ La hora seleccionada no es válida. Elige otra disponible.")

        return time

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Validar disponibilidad
        if Cita.objects.filter(service=service, date=date, time=time).exists():
            self.add_error('time', _("⚠️ Ya hay una cita reservada para esta hora."))

        return cleaned_data
