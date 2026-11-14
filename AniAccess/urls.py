from django.urls import path
from .import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('voluntariado/colaboraciones/<int:id>/<str:estado>/', views.detalle_colaboracion, name='detalle_colaboracion'),
]