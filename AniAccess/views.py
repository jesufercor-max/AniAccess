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


# Vista 5 Perfil de Usuario 
def perfil_usuario(request, nombre):
    """
    Muestra el perfil de un usuario, sus preferencias de accesibilidad,
    valoraciones y datos de voluntariado.
    """

    # QUERYSET ORM:
    # select_related carga las relaciones OneToOne.
    # prefetch_related carga las valoraciones, preferencias,
    # insignias y colaboraciones.
    usuario = get_object_or_404(
        Usuario.objects
        .select_related(
            'perfil_accesibilidad',
            'voluntario',
        )
        .prefetch_related(
            'perfil_accesibilidad__tipos_discapacidad',
            'valoraciones__anime',
            'voluntario__insignias',
            'voluntario__colaboraciones',
        ),
        nombre_usuario=nombre
    )

    # SQL RAW:
    # usuario = Usuario.objects.raw(
    #     "SELECT u.* "
    #     "FROM AniAccess_usuario u "
    #     "LEFT JOIN AniAccess_perfilaccesibilidad pa "
    #     "ON pa.usuario_id = u.id "
    #     "LEFT JOIN AniAccess_voluntario v "
    #     "ON v.usuario_id = u.id "
    #     "WHERE u.nombre_usuario = %s",
    #     [nombre]
    # )

    return render(
        request,
        'AniAccess/perfil_usuario.html',
        {'usuario': usuario}
    )