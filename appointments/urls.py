from django.urls import path
from .views import book_appointment, my_appointments, edit_appointment, confirm_delete_appointment, delete_appointment

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('my/', my_appointments, name='my_appointments'),
    path('edit/<int:appointment_id>/', edit_appointment, name='edit_appointment'),
    path('delete/<int:appointment_id>/confirm/', confirm_delete_appointment, name='confirm_delete_appointment'),
    path('delete/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
]
