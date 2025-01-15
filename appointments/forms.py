from django import forms
from .models import Appointment
from services.models import Service

class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(disponible=True),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        empty_label="Selecciona un servicio"
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control form-control-lg',
            'rows': 3,
            'placeholder': 'Escribe algún comentario o instrucción especial (opcional)'
        }),
        required=False
    )

    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'comment']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-lg'}),
        }

