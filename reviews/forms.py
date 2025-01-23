from django import forms
from .models import Review
from services.models import Service 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['servicio', 'comment', 'rating']
        widgets = {
            'servicio': forms.Select(attrs={
                'class': 'form-control',
                'aria-label': 'Selecciona un servicio',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu reseña aquí...',
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'placeholder': 'Puntuación (1-5)',
            }),
        }
        labels = {
            'servicio': 'Servicio',
            'comment': 'Comentario',
            'rating': 'Puntuación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo servicios disponibles
        self.fields['servicio'].queryset = Service.objects.filter(disponible=True)
