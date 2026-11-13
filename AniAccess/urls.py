from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('animes/', views.catalogo_animes, name='catalogo_animes'),
]