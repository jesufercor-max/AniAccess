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


# Vista 8 Ranking de Voluntarios
def ranking_voluntarios(request):
    """
    Muestra un ranking de voluntarios disponibles,
    ordenados por sus puntos y colaboraciones aprobadas.
    """

    # QUERYSET ORM:
    # Filtra voluntarios disponibles, cuenta sus colaboraciones aprobadas
    # mediante Count con filtro Q, y precarga usuario, insignias y colaboraciones.
    voluntarios = Voluntario.objects.filter(
        disponible=True
    ).select_related(
        'usuario'
    ).prefetch_related(
        'insignias',
        'colaboraciones'
    ).annotate(
        total_colaboraciones=Count(
            'colaboraciones',
            filter=Q(colaboraciones__estado='Aprobada'),
            distinct=True
        )
    ).order_by(
        '-puntos',
        '-total_colaboraciones'
    )[:10]

    # SQL RAW:
    # voluntarios = Voluntario.objects.raw(
    #     """
    #     SELECT v.*,
    #     COUNT(DISTINCT CASE WHEN c.estado = 'Aprobada' THEN c.id END) AS total_colaboraciones
    #     FROM AniAccess_voluntario v
    #     INNER JOIN AniAccess_usuario u ON u.id = v.usuario_id
    #     LEFT JOIN AniAccess_colaboracion c ON c.voluntario_id = v.id
    #     WHERE v.disponible = 1
    #     GROUP BY v.id
    #     ORDER BY v.puntos DESC, total_colaboraciones DESC
    #     LIMIT 10
    #     """
    # )

    return render(
        request,
        'AniAccess/ranking_voluntarios.html',
        {'voluntarios': voluntarios}
    )