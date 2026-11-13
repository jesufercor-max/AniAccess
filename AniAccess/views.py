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


# Vista 1 Catálogos de Animes 
def catalogo_animes(request):
    """
    Muestra un catálogo de animes en emisión.
    Permite buscar por título o título original.
    """

    buscar = request.GET.get('buscar', '')

    # QUERYSET:
    # Filtra animes en emisión y permite buscar por dos títulos.
    # Utiliza AND y OR, ordena por año y limita a 20 resultados.
    animes = Anime.objects.filter(
        Q(estado='En emisión') &
        (
            Q(titulo__icontains=buscar) |
            Q(titulo_original__icontains=buscar)
        )
    ).order_by('-anio_estreno')[:20]

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     """
    #     SELECT *
    #     FROM AniAccess_anime
    #     WHERE estado = %s
    #     AND (titulo LIKE %s OR titulo_original LIKE %s)
    #     ORDER BY anio_estreno DESC
    #     LIMIT 20
    #     """,
    #     ['En emisión', f'%{buscar}%', f'%{buscar}%']
    # )
    
    return render(request, 'AniAccess/catalogo_animes.html', {
        'animes': animes,
        'buscar': buscar
    })