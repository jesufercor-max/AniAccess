from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('voluntariado/insignias/', views.catalogo_insignias, name='catalogo_insignias'),
]