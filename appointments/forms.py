from django import forms
from .models import Appointment
from services.models import Service
from django.utils.translation import gettext_lazy as _

class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(disponible=True),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        empty_label=_("Selecciona un servicio"),
        label=_("📌 Servicio")
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
        label=_("📅 Fecha")
    )

    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-lg'}),
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
        model = Appointment
        fields = ['service', 'date', 'time', 'comment']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Validar si la combinación de fecha y hora ya existe, excluyendo la cita actual si es edición
        existing_appointments = Appointment.objects.filter(date=date, time=time)
        
        # Excluir la cita actual si se está editando
        if self.instance.pk:
            existing_appointments = existing_appointments.exclude(pk=self.instance.pk)

        if existing_appointments.exists():
            self.add_error(None, _("⚠️ Cita con esta fecha y hora ya existe."))  # ✅ Error general

        return cleaned_data

