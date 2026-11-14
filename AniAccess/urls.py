from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('voluntariado/',views.ranking_voluntarios,name='ranking_voluntarios'),
]