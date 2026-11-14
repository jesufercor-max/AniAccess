from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Avg
from .models import (
    Anime, Plataforma, Disponibilidad, Accesibilidad,
    TipoDiscapacidad, Idioma, Usuario, PerfilAccesibilidad,
    Valoracion, Voluntario, Colaboracion, Insignia
)


# Index
def index(request):
    return render(request, 'AniAccess/index.html')


# Vista 1: Catálogo de Animes
def catalogo_animes(request):
    buscar = request.GET.get('buscar', '')
    animes = Anime.objects.filter(
        Q(estado='En emisión') &
        (Q(titulo__icontains=buscar) | Q(titulo_original__icontains=buscar))
    ).order_by('-anio_estreno')[:20]

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     "SELECT * FROM AniAccess_anime WHERE estado = %s AND (titulo LIKE %s OR titulo_original LIKE %s) ORDER BY anio_estreno DESC LIMIT 20",
    #     ['En emisión', f'%{buscar}%', f'%{buscar}%']
    # )

    return render(request, 'AniAccess/catalogo_animes.html', {
        'animes': animes,
        'buscar': buscar
    })


# Vista 2: Detalle del Anime
def detalle_anime(request, id):
    anime = get_object_or_404(
        Anime.objects
        .select_related('accesibilidad')
        .prefetch_related(
            'plataformas',
            'disponibilidades__idioma',
            'disponibilidades__plataforma',
            'valoraciones__usuario',
            'accesibilidad__tipos_discapacidad'
        )
        .annotate(
            total_valoraciones=Count('valoraciones', distinct=True),
            media_valoraciones=Avg('valoraciones__accesibilidad_general')
        ),
        id=id
    )

    # SQL RAW:
    # anime = Anime.objects.raw(
    #     "SELECT a.*, COUNT(DISTINCT v.id) AS total_valoraciones, AVG(v.accesibilidad_general) AS media_valoraciones "
    #     "FROM AniAccess_anime a LEFT JOIN AniAccess_valoracion v ON v.anime_id = a.id WHERE a.id = %s GROUP BY a.id",
    #     [id]
    # )

    return render(request, 'AniAccess/detalle_anime.html', {'anime': anime})


# Vista 3: Comparador de Plataformas
def comparador_plataformas(request):
    plataformas = Plataforma.objects.filter(
        activa=True
    ).prefetch_related(
        'disponibilidades__anime',
        'disponibilidades__idioma'
    ).annotate(
        total_animes=Count('animes', distinct=True)
    ).order_by('nombre')

    return render(request, 'AniAccess/comparador_plataformas.html', {'plataformas': plataformas})


# Vista 4: Buscador de Accesibilidad
def buscador_accesibilidad(request):
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
    #     "SELECT DISTINCT a.* FROM AniAccess_anime a INNER JOIN AniAccess_accesibilidad ac ON ac.anime_id = a.id "
    #     "WHERE ac.subtitulos_accesibles = 1 OR ac.audiodescripcion = 1 OR ac.lengua_signos = 1 ORDER BY a.titulo"
    # )

    return render(request, 'AniAccess/buscador_accesibilidad.html', {'animes': animes})


# Vista 5: Perfil de Usuario
def perfil_usuario(request, nombre):
    usuario = get_object_or_404(
        Usuario.objects
        .select_related('perfil_accesibilidad', 'voluntario')
        .prefetch_related(
            'perfil_accesibilidad__tipos_discapacidad',
            'valoraciones__anime',
            'voluntario__insignias',
            'voluntario__colaboraciones'
        ),
        nombre_usuario=nombre
    )
    return render(request, 'AniAccess/perfil_usuario.html', {'usuario': usuario})


# Vista 6: Animes Favoritos del Usuario
def animes_favoritos(request, nombre):
    usuario = get_object_or_404(Usuario, nombre_usuario=nombre)
    buscar = request.GET.get('buscar', '')

    animes = Anime.objects.filter(
        Q(usuarios_favoritos=usuario) &
        (Q(titulo__icontains=buscar) | Q(titulo_original__icontains=buscar))
    ).prefetch_related(
        'plataformas',
        'disponibilidades__idioma'
    ).order_by('titulo')

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     "SELECT a.* FROM AniAccess_anime a INNER JOIN AniAccess_anime_usuarios_favoritos f ON f.anime_id = a.id "
    #     "WHERE f.usuario_id = %s AND (a.titulo LIKE %s OR a.titulo_original LIKE %s) ORDER BY a.titulo",
    #     [usuario.id, f'%{buscar}%', f'%{buscar}%']
    # )

    return render(request, 'AniAccess/animes_favoritos.html', {
        'usuario': usuario,
        'animes': animes,
        'buscar': buscar
    })


# Vista 7: Ranking de Accesibilidad
def ranking_accesibilidad(request):
    animes = Anime.objects.annotate(
        total_valoraciones=Count('valoraciones', distinct=True),
        media_puntuacion=Avg('valoraciones__accesibilidad_general')
    ).filter(
        total_valoraciones__gte=1,
        media_puntuacion__gte=3
    ).order_by('-media_puntuacion', '-total_valoraciones')[:10]

    # SQL RAW:
    # animes = Anime.objects.raw(
    #     "SELECT a.*, COUNT(DISTINCT v.id) AS total_valoraciones, AVG(v.accesibilidad_general) AS media_puntuacion "
    #     "FROM AniAccess_anime a INNER JOIN AniAccess_valoracion v ON v.anime_id = a.id "
    #     "GROUP BY a.id HAVING COUNT(DISTINCT v.id) >= 1 AND AVG(v.accesibilidad_general) >= 3 "
    #     "ORDER BY media_puntuacion DESC, total_valoraciones DESC LIMIT 10"
    # )

    return render(request, 'AniAccess/ranking_accesibilidad.html', {'animes': animes})


# Vista 8: Ranking de Voluntarios
def ranking_voluntarios(request):
    voluntarios = Voluntario.objects.filter(
        disponible=True
    ).select_related('usuario').prefetch_related(
        'insignias', 'colaboraciones'
    ).annotate(
        total_colaboraciones=Count(
            'colaboraciones',
            filter=Q(colaboraciones__estado='Aprobada'),
            distinct=True
        )
    ).order_by('-puntos', '-total_colaboraciones')[:10]

    # SQL RAW:
    # voluntarios = Voluntario.objects.raw(
    #     "SELECT v.*, COUNT(DISTINCT CASE WHEN c.estado = 'Aprobada' THEN c.id END) AS total_colaboraciones "
    #     "FROM AniAccess_voluntario v INNER JOIN AniAccess_usuario u ON u.id = v.usuario_id "
    #     "LEFT JOIN AniAccess_colaboracion c ON c.voluntario_id = v.id WHERE v.disponible = 1 "
    #     "GROUP BY v.id ORDER BY v.puntos DESC, total_colaboraciones DESC LIMIT 10"
    # )

    return render(request, 'AniAccess/ranking_voluntarios.html', {'voluntarios': voluntarios})


# Vista 9: Detalle de Colaboración
def detalle_colaboracion(request, id, estado):
    colaboracion = get_object_or_404(
        Colaboracion.objects.select_related('voluntario__usuario'),
        id=id,
        estado=estado
    )

    # SQL RAW:
    # colaboracion = Colaboracion.objects.raw(
    #     "SELECT c.* FROM AniAccess_colaboracion c INNER JOIN AniAccess_voluntario v ON v.id = c.voluntario_id "
    #     "INNER JOIN AniAccess_usuario u ON u.id = v.usuario_id WHERE c.id = %s AND c.estado = %s",
    #     [id, estado]
    # )

    return render(request, 'AniAccess/detalle_colaboracion.html', {'colaboracion': colaboracion})


# Vista 10: Catálogo de Insignias
def catalogo_insignias(request):
    insignias = Insignia.objects.filter(
        activa=True
    ).annotate(
        total_voluntarios=Count('voluntarios', distinct=True)
    ).prefetch_related('voluntarios__usuario').order_by('puntos_necesarios')

    # SQL RAW:
    # insignias = Insignia.objects.raw(
    #     "SELECT i.*, COUNT(DISTINCT vi.voluntario_id) AS total_voluntarios FROM AniAccess_insignia i "
    #     "LEFT JOIN AniAccess_voluntario_insignias vi ON vi.insignia_id = i.id WHERE i.activa = 1 "
    #     "GROUP BY i.id ORDER BY i.puntos_necesarios"
    # )

    return render(request, 'AniAccess/catalogo_insignias.html', {'insignias': insignias})


# Manejadores de Error HTTP
def error_400(request, exception):
    return render(request, 'AniAccess/400.html', status=400)


def error_403(request, exception):
    return render(request, 'AniAccess/403.html', status=403)


def error_404(request, exception):
    return render(request, 'AniAccess/404.html', status=404)


def error_500(request):
    return render(request, 'AniAccess/500.html', status=500)
