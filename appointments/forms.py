from django import forms
from .models import Appointment
from services.models import Service

class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(disponible=True),  # Solo servicios disponibles
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        empty_label="Selecciona un servicio"
    )

    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-lg'}),
        }
