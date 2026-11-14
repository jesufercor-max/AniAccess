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


# Vista 9 Información de las colaboraciones 
def detalle_colaboracion(request, id, estado):
    """
    Muestra la información completa de una colaboración,
    identificándola mediante su ID y su estado.
    """

    # QUERYSET ORM:
    # Busca la colaboración por su identificador y estado.
    # select_related carga el voluntario y el usuario asociado
    # en la misma consulta mediante JOIN.
    colaboracion = get_object_or_404(
        Colaboracion.objects.select_related(
            'voluntario__usuario'
        ),
        id=id,
        estado=estado
    )

    # SQL RAW:
    # colaboracion = Colaboracion.objects.raw(
    #     "SELECT c.* "
    #     "FROM AniAccess_colaboracion c "
    #     "INNER JOIN AniAccess_voluntario v "
    #     "ON v.id = c.voluntario_id "
    #     "INNER JOIN AniAccess_usuario u "
    #     "ON u.id = v.usuario_id "
    #     "WHERE c.id = %s AND c.estado = %s",
    #     [id, estado]
    # )

    return render(
        request,
        'AniAccess/detalle_colaboracion.html',
        {'colaboracion': colaboracion}
    )