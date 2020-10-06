from django.urls import path

from api import views

urlpatterns = [
    path('getNumber/', views.get_number, name='get_number'),
    path('number/', views.number_status, name='number_status')
]