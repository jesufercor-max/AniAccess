from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Avg
from django.urls import reverse
from .models import (
    Anime, Plataforma, Disponibilidad, Accesibilidad,
    TipoDiscapacidad, Idioma, Usuario, PerfilAccesibilidad,
    Valoracion, Voluntario, Colaboracion, Insignia
)

# Create your views here.

# Index 
def index(request):
    """
    Página principal de AniAccess.
    Permite acceder a las diez secciones de la aplicación.
    """

    return render(request, 'AniAccess/index.html')


# Vista 7 Ranking de Accesibilidad
def ranking_accesibilidad(request):
    """
    Muestra un ranking de animes ordenado por su puntuación
    media de accesibilidad.
    """

    # QUERYSET ORM:
    # Calcula el número de valoraciones y la media de accesibilidad.
    # El filter aplicado después de annotate filtra los resultados
    # agregados, equivalente a utilizar HAVING en SQL.
    animes = Anime.objects.annotate(
        total_valoraciones=Count(
            'valoraciones',
            distinct=True
        ),
        media_puntuacion=Avg(
            'valoraciones__accesibilidad_general'
        )
    ).filter(
        total_valoraciones__gte=1,
        media_puntuacion__gte=3
    ).order_by(
        '-media_puntuacion',
        '-total_valoraciones'
    )[:10]

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     "SELECT a.*, "
    #     "COUNT(DISTINCT v.id) AS total_valoraciones, "
    #     "AVG(v.accesibilidad_general) AS media_puntuacion "
    #     "FROM AniAccess_anime a "
    #     "INNER JOIN AniAccess_valoracion v "
    #     "ON v.anime_id = a.id "
    #     "GROUP BY a.id "
    #     "HAVING COUNT(DISTINCT v.id) >= 1 "
    #     "AND AVG(v.accesibilidad_general) >= 3 "
    #     "ORDER BY media_puntuacion DESC, "
    #     "total_valoraciones DESC "
    #     "LIMIT 10"
    # )

    return render(
        request,
        'AniAccess/ranking_accesibilidad.html',
        {'animes': animes}
    )