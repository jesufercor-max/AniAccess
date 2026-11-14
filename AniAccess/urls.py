from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('usuarios/<str:nombre>/favoritos/',views.animes_favoritos,name='animes_favoritos'),
]