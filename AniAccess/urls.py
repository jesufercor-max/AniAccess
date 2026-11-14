from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('animes/', views.catalogo_animes, name='catalogo_animes'),
    path('animes/<int:id>/', views.detalle_anime, name='detalle_anime'),
    path('plataformas/', views.comparador_plataformas, name='comparador_plataformas'),
    path('accesibilidad/', views.buscador_accesibilidad, name='buscador_accesibilidad'),
    path('usuarios/<str:nombre>/favoritos/', views.animes_favoritos, name='animes_favoritos'),
    path('usuarios/<str:nombre>/', views.perfil_usuario, name='perfil_usuario'),
    path('ranking-accesibilidad/', views.ranking_accesibilidad, name='ranking_accesibilidad'),
    path('voluntariado/', views.ranking_voluntarios, name='ranking_voluntarios'),
    path('voluntariado/insignias/', views.catalogo_insignias, name='catalogo_insignias'),
    path('voluntariado/colaboraciones/<int:id>/<str:estado>/', views.detalle_colaboracion, name='detalle_colaboracion'),
]