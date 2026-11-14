from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('accesibilidad/',views.buscador_accesibilidad,name='buscador_accesibilidad'),
]