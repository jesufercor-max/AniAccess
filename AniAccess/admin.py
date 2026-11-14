from django.contrib import admin
from .models import (
    Anime,
    Plataforma,
    Disponibilidad,
    Accesibilidad,
    TipoDiscapacidad,
    Idioma,
    Usuario,
    PerfilAccesibilidad,
    Valoracion,
    Voluntario,
    Colaboracion,
    Insignia
)

# Register your models here.
admin.site.register([
    Anime,
    Plataforma,
    Disponibilidad,
    Accesibilidad,
    TipoDiscapacidad,
    Idioma,
    Usuario,
    PerfilAccesibilidad,
    Valoracion,
    Voluntario,
    Colaboracion,
    Insignia
])