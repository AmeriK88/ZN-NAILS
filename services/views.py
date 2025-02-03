from django.shortcuts import render
from .models import Servicio

def lista_servicios(request):
    servicios = Servicio.objects.filter(disponible=True)
    return render(request, 'services/service_list.html', {'servicios': servicios})
