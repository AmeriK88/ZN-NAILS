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
        start_time = datetime.time(9, 0)  # 09:00 AM
        end_time = datetime.time(20, 0)   # 08:00 PM
        step = service.duracion  # Duración en minutos según el servicio

        times = []
        current_time = datetime.datetime.combine(datetime.date.today(), start_time)

        while current_time.time() <= end_time:
            # Validar si el horario ya está reservado
            if not Cita.objects.filter(date=selected_date, time=current_time.time()).exists():
                times.append((current_time.time().strftime('%H:%M'), current_time.time().strftime('%H:%M')))
            # Incrementar por la duración del servicio
            current_time += datetime.timedelta(minutes=step)

        return times
    
      #  MÉTODO DE VALIDACIÓN DE LA HORA
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
