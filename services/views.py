from django.shortcuts import render
from .models import Service

def lista_servicios(request):
    servicios = Service.objects.filter(disponible=True)
    return render(request, 'services/service_list.html', {'servicios': servicios})
