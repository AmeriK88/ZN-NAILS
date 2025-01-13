from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control form-control-lg'}),
        }
