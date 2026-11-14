from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('usuarios/<str:nombre>/',views.perfil_usuario,name='perfil_usuario'),
]