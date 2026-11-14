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


# Vista 4 Accesibilidad de los Animes 
def buscador_accesibilidad(request):
    """
    Muestra los animes que disponen de alguna característica
    de accesibilidad.
    """

    # QUERYSET ORM:
    # Busca animes que tengan subtítulos CC, audiodescripción
    # o lengua de signos.
    # Se utiliza OR para aceptar cualquiera de las condiciones.
    animes = Anime.objects.filter(
        Q(accesibilidad__subtitulos_accesibles=True) |
        Q(accesibilidad__audiodescripcion=True) |
        Q(accesibilidad__lengua_signos=True)
    ).select_related(
        'accesibilidad'
    ).prefetch_related(
        'accesibilidad__tipos_discapacidad'
    ).distinct().order_by('titulo')

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     "SELECT DISTINCT a.* "
    #     "FROM AniAccess_anime a "
    #     "INNER JOIN AniAccess_accesibilidad ac "
    #     "ON ac.anime_id = a.id "
    #     "WHERE ac.subtitulos_cc = 1 "
    #     "OR ac.audiodescripcion = 1 "
    #     "OR ac.lengua_signos = 1 "
    #     "ORDER BY a.titulo"
    # )

    return render(
        request,
        'AniAccess/buscador_accesibilidad.html',
        {'animes': animes}
    )