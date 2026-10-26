from django.conf import settings
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# ==========================================================
# 1. ANIME
# Información básica de cada anime.
# ==========================================================

class Anime(models.Model):

    titulo = models.CharField(max_length=150, unique=True)
    titulo_original = models.CharField(max_length=150)
    sinopsis = models.TextField(max_length=1000)
    anio_estreno = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    num_episodios = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50, default="En emisión")
    imagen = models.ImageField(
        upload_to="animes/",
        null=True,
        blank=True
    )

    # Muchos animes pueden estar disponibles en muchas plataformas.
    # Disponibilidad será la tabla intermedia con atributos propios.
    plataformas = models.ManyToManyField(
        "Plataforma",
        through="Disponibilidad",
        related_name="animes"
    )

    # Un usuario puede marcar muchos animes como favoritos
    # y un anime puede ser favorito de muchos usuarios.
    usuarios_favoritos = models.ManyToManyField(
        "Usuario",
        related_name="animes_favoritos",
        blank=True
    )

    def __str__(self):
        return self.titulo


# ==========================================================
# 2. PLATAFORMA
# Plataformas donde se puede consumir anime.
# ==========================================================

class Plataforma(models.Model):

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=500)
    web = models.URLField()
    logo = models.ImageField(
        upload_to="plataformas/",
        null=True,
        blank=True
    )
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ==========================================================
# 3. DISPONIBILIDAD
# Relaciona animes, plataformas e idiomas.
# Actúa como tabla intermedia de Anime y Plataforma.
# ==========================================================

class Disponibilidad(models.Model):

    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name="disponibilidades"
    )

    plataforma = models.ForeignKey(
        Plataforma,
        on_delete=models.CASCADE,
        related_name="disponibilidades"
    )

    idioma = models.ForeignKey(
        "Idioma",
        on_delete=models.PROTECT,
        related_name="disponibilidades"
    )

    subtitulos = models.BooleanField(default=False)
    doblaje = models.BooleanField(default=False)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["anime", "plataforma", "idioma"],
                name="disponibilidad_unica_anime_plataforma_idioma"
            )
        ]

    def __str__(self):
        return f"{self.anime} - {self.plataforma} - {self.idioma}"


# ==========================================================
# 4. ACCESIBILIDAD
# Características de accesibilidad de cada anime.
# ==========================================================

class Accesibilidad(models.Model):

    # Cada anime tendrá como máximo una ficha de accesibilidad.
    anime = models.OneToOneField(
        Anime,
        on_delete=models.CASCADE,
        related_name="accesibilidad"
    )

    subtitulos_accesibles = models.BooleanField(default=False)
    audiodescripcion = models.BooleanField(default=False)
    descripcion_sonidos = models.BooleanField(default=False)
    lengua_signos = models.BooleanField(default=False)
    doblaje = models.BooleanField(default=False)
    contraste_visual = models.BooleanField(default=False)
    observaciones = models.TextField(max_length=1000, blank=True)

    # Un tipo de necesidad puede estar relacionado con muchas fichas
    # de accesibilidad y una ficha puede cubrir varios tipos.
    tipos_discapacidad = models.ManyToManyField(
        "TipoDiscapacidad",
        related_name="accesibilidades",
        blank=True
    )

    def __str__(self):
        return f"Accesibilidad de {self.anime}"


# ==========================================================
# 5. TIPODISCAPACIDAD
# Clasifica las necesidades de accesibilidad.
# ==========================================================

class TipoDiscapacidad(models.Model):

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=500)
    icono = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ==========================================================
# 6. IDIOMA
# Idiomas disponibles en la aplicación.
# ==========================================================

class Idioma(models.Model):

    nombre = models.CharField(max_length=50, unique=True)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


# ==========================================================
# 7. USUARIO
# Información básica de los usuarios de AnimeAccess.
# ==========================================================

class Usuario(models.Model):

    nombre_usuario = models.CharField(
        max_length=50,
        unique=True
    )
    email = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_usuario


# ==========================================================
# 8. PERFILACCESIBILIDAD
# Preferencias de accesibilidad de cada usuario.
# ==========================================================

class PerfilAccesibilidad(models.Model):

    # Cada usuario tendrá como máximo un perfil de accesibilidad.
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_accesibilidad"
    )

    descripcion = models.TextField(max_length=500, blank=True)
    preferencia_subtitulos = models.BooleanField(default=False)
    preferencia_audiodescripcion = models.BooleanField(default=False)
    preferencia_lengua_signos = models.BooleanField(default=False)
    preferencia_doblaje = models.BooleanField(default=False)
    preferencia_descripcion_sonidos = models.BooleanField(
        default=False
    )

    # El perfil puede asociarse a varios tipos de necesidades.
    tipos_discapacidad = models.ManyToManyField(
        TipoDiscapacidad,
        related_name="perfiles",
        blank=True
    )

    def __str__(self):
        return f"Perfil de {self.usuario}"


# ==========================================================
# 9. VALORACION
# Valoraciones de los usuarios sobre los animes.
# ==========================================================

class Valoracion(models.Model):

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="valoraciones"
    )

    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name="valoraciones"
    )

    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comentario = models.TextField(max_length=1000, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    subtitulos_valoracion = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    audio_valoracion = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    accesibilidad_general = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # Ejemplo de campo decimal para una puntuación más precisa.
    precision_accesibilidad = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=3.00,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario} - {self.anime}: {self.puntuacion}"


# ==========================================================
# 10. VOLUNTARIO
# Información de las personas que colaboran en el proyecto.
# ==========================================================

class Voluntario(models.Model):

    # Cada voluntario corresponde a una cuenta de usuario.
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="voluntario"
    )

    nombre_publico = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500, blank=True)
    especialidad = models.CharField(max_length=100)
    fecha_alta = models.DateField(auto_now_add=True)
    disponible = models.BooleanField(default=True)
    puntos = models.PositiveIntegerField(default=0)
    colaboraciones_completadas = models.PositiveIntegerField(
        default=0
    )

    # Muchos voluntarios pueden tener muchas insignias.
    insignias = models.ManyToManyField(
        "Insignia",
        related_name="voluntarios",
        blank=True
    )

    def __str__(self):
        return self.nombre_publico


# ==========================================================
# 11. COLABORACION
# Trabajos realizados por los voluntarios.
# ==========================================================

class Colaboracion(models.Model):

    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("En proceso", "En proceso"),
        ("En revisión", "En revisión"),
        ("Aprobada", "Aprobada"),
        ("Rechazada", "Rechazada"),
    ]

    TIPOS = [
        ("Audiodescripción", "Audiodescripción"),
        ("Subtítulos", "Subtítulos accesibles"),
        ("Lengua de signos", "Lengua de signos"),
        ("Revisión", "Revisión de accesibilidad"),
    ]

    voluntario = models.ForeignKey(
        Voluntario,
        on_delete=models.CASCADE,
        related_name="colaboraciones"
    )

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(max_length=1000)
    tipo = models.CharField(max_length=100, choices=TIPOS)
    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="Pendiente"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)

    comentarios_revision = models.TextField(
        max_length=1000,
        blank=True
    )

    puntos_obtenidos = models.PositiveIntegerField(default=0)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    # Permite adjuntar un archivo como resultado de la colaboración.
    archivo_entrega = models.FileField(
        upload_to="colaboraciones/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.titulo


# ==========================================================
# 12. INSIGNIA
# Premios y logros de los voluntarios.
# ==========================================================

class Insignia(models.Model):

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=500)
    icono = models.ImageField(
        upload_to="insignias/",
        null=True,
        blank=True
    )

    puntos_necesarios = models.PositiveIntegerField(default=0)

    colaboraciones_necesarias = models.PositiveIntegerField(
        default=0
    )

    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
