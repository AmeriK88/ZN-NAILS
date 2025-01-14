from django.urls import path
from .views import lista_servicios

urlpatterns = [
    path('', lista_servicios, name='lista_servicios'),
]
