from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Avg
from django.urls import reverse
from django.core.exceptions import PermissionDenied, SuspiciousOperation
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


# Vista de Errores
def error_400(request, exception):
    return render(request, 'AniAccess/400.html', status=400)


def error_403(request, exception):
    return render(request, 'AniAccess/403.html', status=403)


def error_404(request, exception):
    return render(request, 'AniAccess/404.html', status=404)


def error_500(request):
    return render(request, 'AniAccess/500.html', status=500)