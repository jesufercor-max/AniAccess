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


# Vista 10 Insignias de los voluntarios 
def catalogo_insignias(request):
    """
    Muestra las insignias activas y el número de voluntarios
    que han conseguido cada una.
    """

    # QUERYSET ORM:
    # Filtra las insignias activas.
    # Cuenta los voluntarios asociados mediante la relación ManyToMany.
    # Carga también los voluntarios y sus usuarios.
    insignias = Insignia.objects.filter(
        activa=True
    ).annotate(
        total_voluntarios=Count(
            'voluntarios',
            distinct=True
        )
    ).prefetch_related(
        'voluntarios__usuario'
    ).order_by(
        'puntos_necesarios'
    )

    # SQL RAW:
    # insignias = Insignia.objects.raw(
    #     "SELECT i.*, "
    #     "COUNT(DISTINCT vi.voluntario_id) AS total_voluntarios "
    #     "FROM AniAccess_insignia i "
    #     "LEFT JOIN AniAccess_voluntario_insignias vi "
    #     "ON vi.insignia_id = i.id "
    #     "WHERE i.activa = 1 "
    #     "GROUP BY i.id "
    #     "ORDER BY i.puntos_necesarios"
    # )

    return render(
        request,
        'AniAccess/catalogo_insignias.html',
        {'insignias': insignias}
    )