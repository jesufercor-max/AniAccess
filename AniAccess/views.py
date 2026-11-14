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


# Vista 3 Plataformas de Animes 
def comparador_plataformas(request):
    """
    Muestra las plataformas activas y los animes que tienen
    disponibles actualmente, incluyendo los idiomas.
    """

    # QUERYSET ORM:
    # Filtra plataformas activas con disponibilidades activas
    # que todavía no tienen fecha de finalización.
    # Cuenta los animes distintos asociados a cada plataforma.
    plataformas = Plataforma.objects.filter(
        activa=True,
        disponibilidades__activo=True,
        disponibilidades__fecha_fin__isnull=True
    ).annotate(
        total_animes=Count(
            'disponibilidades__anime',
            distinct=True
        )
    ).prefetch_related(
        'disponibilidades__anime',
        'disponibilidades__idioma'
    ).order_by('nombre')

    # SQL RAW:
    # plataformas = Plataforma.objects.raw(
    #     "SELECT p.*, "
    #     "COUNT(DISTINCT d.anime_id) AS total_animes "
    #     "FROM AniAccess_plataforma p "
    #     "INNER JOIN AniAccess_disponibilidad d "
    #     "ON d.plataforma_id = p.id "
    #     "WHERE p.activa = 1 "
    #     "AND d.activo = 1 "
    #     "AND d.fecha_fin IS NULL "
    #     "GROUP BY p.id "
    #     "ORDER BY p.nombre"
    # )

    return render(
        request,
        'AniAccess/comparador_plataformas.html',
        {'plataformas': plataformas}
    )