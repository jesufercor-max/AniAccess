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


# Vista 6 Animes Favoritos del Usuario
def animes_favoritos(request, nombre):
    """
    Muestra los animes favoritos de un usuario.
    Permite buscar por título o título original.
    """

    usuario = get_object_or_404(
        Usuario,
        nombre_usuario=nombre
    )

    buscar = request.GET.get('buscar', '')

    # QUERYSET ORM:
    # Obtiene los animes relacionados con el usuario mediante
    # la relación ManyToMany usuarios_favoritos y filtra por búsqueda.
    # Carga también sus plataformas y disponibilidades.
    animes = Anime.objects.filter(
        Q(usuarios_favoritos=usuario) &
        (
            Q(titulo__icontains=buscar) |
            Q(titulo_original__icontains=buscar)
        )
    ).prefetch_related(
        'plataformas',
        'disponibilidades__idioma'
    ).order_by('titulo')

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     """
    #     SELECT a.*
    #     FROM AniAccess_anime a
    #     INNER JOIN AniAccess_anime_usuarios_favoritos f
    #     ON f.anime_id = a.id
    #     WHERE f.usuario_id = %s
    #     AND (a.titulo LIKE %s OR a.titulo_original LIKE %s)
    #     ORDER BY a.titulo
    #     """,
    #     [usuario.id, f'%{buscar}%', f'%{buscar}%']
    # )

    return render(
        request,
        'AniAccess/animes_favoritos.html',
        {
            'usuario': usuario,
            'animes': animes,
            'buscar': buscar
        }
    )