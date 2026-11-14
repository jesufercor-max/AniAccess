from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('ranking-accesibilidad/',views.ranking_accesibilidad,name='ranking_accesibilidad'),
]