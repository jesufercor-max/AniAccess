import random
import uuid
from datetime import timedelta
from decimal import Decimal

from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone

from AniAccess.models import (
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
    Insignia,
)


fake = Faker("es_ES")


class Command(BaseCommand):
    help = "Genera 10 registros de prueba para cada modelo de AnimeAccess."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE("Generando datos de prueba para AnimeAccess...")
        )

        # 1. Crear los modelos independientes.
        self.crear_idiomas()
        self.crear_tipos_discapacidad()
        self.crear_insignias()
        self.crear_plataformas()
        self.crear_usuarios()
        self.crear_animes()

        # 2. Crear los modelos que dependen de otros.
        self.crear_disponibilidades()
        self.crear_accesibilidades()
        self.crear_perfiles()
        self.crear_valoraciones()
        self.crear_voluntarios()
        self.crear_colaboraciones()

        # 3. Asociar relaciones muchos a muchos.
        self.asociar_relaciones()

        self.stdout.write(
            self.style.SUCCESS(
                "\nProceso terminado. Resumen de registros:"
            )
        )

        # Mostrar el número final de registros de cada modelo.
        modelos = [
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
            Insignia,
        ]

        for modelo in modelos:
            self.stdout.write(
                f"  {modelo.__name__}: {modelo.objects.count()} registros"
            )

    # MÉTODOS AUXILIARES

    def sufijo_unico(self):
        """Genera un identificador para evitar duplicados."""
        return uuid.uuid4().hex[:8]

    def fecha_aleatoria(self, inicio="2020-01-01", fin=None):
        """Genera una fecha aleatoria dentro de un intervalo."""
        fecha_inicio = timezone.datetime.fromisoformat(inicio).date()
        fecha_fin = fin or timezone.localdate()

        if fecha_fin < fecha_inicio:
            fecha_fin = fecha_inicio

        dias = (fecha_fin - fecha_inicio).days

        return fecha_inicio + timedelta(
            days=random.randint(0, dias)
        )

    def fecha_hora_aleatoria(self):
        """Genera una fecha y hora de prueba con zona horaria."""
        fecha = self.fecha_aleatoria()

        fecha_hora = timezone.datetime.combine(
            fecha,
            timezone.datetime.min.time().replace(
                hour=random.randint(8, 20),
                minute=random.choice([0, 15, 30, 45]),
            ),
        )

        return timezone.make_aware(
        fecha_hora,
        timezone.get_current_timezone(),
        )

    # 1. IDIOMA

    def crear_idiomas(self):
        idiomas = [
            ("Español", "es"),
            ("Inglés", "en"),
            ("Japonés", "ja"),
            ("Francés", "fr"),
            ("Alemán", "de"),
            ("Italiano", "it"),
            ("Portugués", "pt"),
            ("Coreano", "ko"),
            ("Chino", "zh"),
            ("Catalán", "ca"),
        ]

        for nombre, codigo in idiomas:
            if Idioma.objects.count() >= 10:
                break

            Idioma.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "codigo": codigo,
                    "descripcion": f"Idioma {nombre} para AnimeAccess.",
                    "activo": True,
                },
            )

    # 2. TIPODISCAPACIDAD

    def crear_tipos_discapacidad(self):
        tipos = [
            "Visual",
            "Auditiva",
            "Motora",
            "Cognitiva",
            "Dislexia",
            "Sensibilidad visual",
            "Sensibilidad auditiva",
            "Dificultad de lectura",
            "Necesidades de comunicación",
            "Accesibilidad múltiple",
        ]

        for nombre in tipos:
            if TipoDiscapacidad.objects.count() >= 10:
                break

            TipoDiscapacidad.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": (
                        f"Necesidades de accesibilidad relacionadas con "
                        f"{nombre.lower()}."
                    ),
                    "icono": "fa-universal-access",
                    "activo": True,
                },
            )

    
    # 3. INSIGNIA

    def crear_insignias(self):
        nombres = [
            "Primera colaboración",
            "Traductor principiante",
            "Experto en subtítulos",
            "Especialista en audio",
            "Revisor de accesibilidad",
            "Colaborador habitual",
            "Ayudante de la comunidad",
            "Experto en inclusión",
            "Maestro de accesibilidad",
            "Embajador AnimeAccess",
        ]

        while Insignia.objects.count() < 10:
            indice = Insignia.objects.count()
            nombre = nombres[indice] if indice < len(nombres) else (
                f"Insignia {self.sufijo_unico()}"
            )

            Insignia.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": fake.text(max_nb_chars=200),
                    "puntos_necesarios": random.choice(
                        [0, 10, 20, 50, 100, 200]
                    ),
                    "colaboraciones_necesarias": random.randint(0, 10),
                    "activa": True,
                },
            )

    # 4. PLATAFORMA

    def crear_plataformas(self):
        nombres = [
            "Crunchyroll",
            "Netflix",
            "Prime Video",
            "Disney+",
            "Hulu",
            "AnimeBox",
            "HIDIVE",
            "Plataforma Anime 8",
            "Plataforma Anime 9",
            "Plataforma Anime 10",
        ]

        dominios = [
            "https://www.crunchyroll.com",
            "https://www.netflix.com",
            "https://www.primevideo.com",
            "https://www.disneyplus.com",
            "https://www.hulu.com",
            "https://example.com/animebox",
            "https://www.hidive.com",
            "https://example.com/anime8",
            "https://example.com/anime9",
            "https://example.com/anime10",
        ]

        while Plataforma.objects.count() < 10:
            indice = Plataforma.objects.count()

            nombre = (
                nombres[indice]
                if indice < len(nombres)
                else f"Plataforma {self.sufijo_unico()}"
            )

            web = (
                dominios[indice]
                if indice < len(dominios)
                else f"https://example.com/{self.sufijo_unico()}"
            )

            Plataforma.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": fake.text(max_nb_chars=250),
                    "web": web,
                    "activa": True,
                },
            )

    # 5. USUARIO

    def crear_usuarios(self):
        while Usuario.objects.count() < 10:
            sufijo = self.sufijo_unico()

            Usuario.objects.create(
                nombre_usuario=f"user_{sufijo}",
                email=f"user_{sufijo}@example.com",
                fecha_nacimiento=self.fecha_aleatoria(
                    "1970-01-01",
                    timezone.localdate(),
                ),
                activo=random.choice([True, True, True, False]),
            )

    # 6. ANIME

    def crear_animes(self):
        generos = [
            "Acción",
            "Aventura",
            "Fantasía",
            "Ciencia ficción",
            "Comedia",
            "Drama",
            "Deportes",
            "Romance",
            "Misterio",
            "Fantasía oscura",
        ]

        while Anime.objects.count() < 10:
            sufijo = self.sufijo_unico()

            Anime.objects.create(
                titulo=f"{fake.catch_phrase()} {sufijo}",
                titulo_original=f"Anime original {sufijo}",
                sinopsis=fake.text(max_nb_chars=700),
                anio_estreno=random.randint(1990, 2026),
                num_episodios=random.randint(1, 100),
                tipo=random.choice(
                    ["Serie", "Película", "OVA", "Especial"]
                ),
                estado=random.choice(
                    ["En emisión", "Finalizado", "En pausa"]
                ),
            )

    # 7. DISPONIBILIDAD

    def crear_disponibilidades(self):
        animes = list(Anime.objects.all())
        plataformas = list(Plataforma.objects.all())
        idiomas = list(Idioma.objects.all())

        if not animes or not plataformas or not idiomas:
            self.stdout.write(
                self.style.WARNING(
                    "No se pueden crear disponibilidades sin "
                    "animes, plataformas e idiomas."
                )
            )
            return

        intentos = 0
        max_intentos = 1000

        while (
            Disponibilidad.objects.count() < 10
            and intentos < max_intentos
        ):
            intentos += 1

            anime = random.choice(animes)
            plataforma = random.choice(plataformas)
            idioma = random.choice(idiomas)

            Disponibilidad.objects.get_or_create(
                anime=anime,
                plataforma=plataforma,
                idioma=idioma,
                defaults={
                    "subtitulos": random.choice([True, False]),
                    "doblaje": random.choice([True, False]),
                    "fecha_inicio": self.fecha_aleatoria(
                        "2020-01-01"
                    ),
                    "fecha_fin": None,
                    "activo": True,
                },
            )

        if Disponibilidad.objects.count() < 10:
            self.stdout.write(
                self.style.WARNING(
                    "No se han podido alcanzar 10 disponibilidades."
                )
            )

    # 8. ACCESIBILIDAD

    def crear_accesibilidades(self):
        for anime in Anime.objects.all():
            if Accesibilidad.objects.count() >= 10:
                break

            Accesibilidad.objects.get_or_create(
                anime=anime,
                defaults={
                    "subtitulos_accesibles": random.choice([True, False]),
                    "audiodescripcion": random.choice([True, False]),
                    "descripcion_sonidos": random.choice([True, False]),
                    "lengua_signos": random.choice([True, False]),
                    "doblaje": random.choice([True, False]),
                    "contraste_visual": random.choice([True, False]),
                    "observaciones": fake.text(max_nb_chars=300),
                },
            )

    # 9. PERFILACCESIBILIDAD

    def crear_perfiles(self):
        usuarios = Usuario.objects.all()

        for usuario in usuarios:
            if PerfilAccesibilidad.objects.count() >= 10:
                break

            PerfilAccesibilidad.objects.get_or_create(
                usuario=usuario,
                defaults={
                    "descripcion": fake.text(max_nb_chars=250),
                    "preferencia_subtitulos": random.choice([True, False]),
                    "preferencia_audiodescripcion": random.choice(
                        [True, False]
                    ),
                    "preferencia_lengua_signos": random.choice(
                        [True, False]
                    ),
                    "preferencia_doblaje": random.choice([True, False]),
                    "preferencia_descripcion_sonidos": random.choice(
                        [True, False]
                    ),
                },
            )

    # 10. VALORACION

    def crear_valoraciones(self):
        usuarios = list(Usuario.objects.all())
        animes = list(Anime.objects.all())

        if not usuarios or not animes:
            return

        while Valoracion.objects.count() < 10:
            Valoracion.objects.create(
                usuario=random.choice(usuarios),
                anime=random.choice(animes),
                puntuacion=random.randint(1, 5),
                comentario=fake.text(max_nb_chars=400),
                subtitulos_valoracion=random.randint(1, 5),
                audio_valoracion=random.randint(1, 5),
                accesibilidad_general=random.randint(1, 5),
                precision_accesibilidad=Decimal(
                    str(round(random.uniform(1, 5), 2))
                ),
                visible=True,
            )

    # 11. VOLUNTARIO

    def crear_voluntarios(self):
        usuarios = Usuario.objects.all()

        especialidades = [
            "Subtítulos accesibles",
            "Audiodescripción",
            "Lengua de signos",
            "Traducción",
            "Revisión de accesibilidad",
        ]

        for usuario in usuarios:
            if Voluntario.objects.count() >= 10:
                break

            Voluntario.objects.get_or_create(
                usuario=usuario,
                defaults={
                    "nombre_publico": f"Voluntario {usuario.nombre_usuario}",
                    "descripcion": fake.text(max_nb_chars=250),
                    "especialidad": random.choice(especialidades),
                    "disponible": random.choice([True, False]),
                    "puntos": random.randint(0, 500),
                    "colaboraciones_completadas": random.randint(0, 20),
                },
            )

    # 12. COLABORACION

    def crear_colaboraciones(self):
        voluntarios = list(Voluntario.objects.all())

        if not voluntarios:
            return

        tipos = [
            "Audiodescripción",
            "Subtítulos",
            "Lengua de signos",
            "Revisión",
        ]

        estados = [
            "Pendiente",
            "En proceso",
            "En revisión",
            "Aprobada",
            "Rechazada",
        ]

        while Colaboracion.objects.count() < 10:
            estado = random.choice(estados)
            fecha_creacion = self.fecha_hora_aleatoria()
            fecha_inicio = None
            fecha_finalizacion = None
            fecha_revision = None

            if estado != "Pendiente":
                fecha_inicio = fecha_creacion + timedelta(
                    hours=random.randint(1, 48)
                )

            if estado in ["Aprobada", "Rechazada"]:
                fecha_finalizacion = fecha_inicio + timedelta(
                    days=random.randint(1, 15)
                )
                fecha_revision = fecha_finalizacion

            Colaboracion.objects.create(
                voluntario=random.choice(voluntarios),
                titulo=fake.sentence(nb_words=5),
                descripcion=fake.text(max_nb_chars=700),
                tipo=random.choice(tipos),
                estado=estado,
                fecha_inicio=fecha_inicio,
                fecha_finalizacion=fecha_finalizacion,
                comentarios_revision=(
                    fake.text(max_nb_chars=300)
                    if estado in ["Aprobada", "Rechazada"]
                    else ""
                ),
                puntos_obtenidos=(
                    random.randint(10, 100)
                    if estado == "Aprobada"
                    else 0
                ),
                fecha_revision=fecha_revision,
            )

    # RELACIONES MUCHOS A MUCHOS

    def asociar_relaciones(self):
        tipos = list(TipoDiscapacidad.objects.all())
        insignias = list(Insignia.objects.all())

        # Cada ficha de accesibilidad puede cubrir varios tipos.
        for accesibilidad in Accesibilidad.objects.all():
            if tipos:
                cantidad = random.randint(1, min(3, len(tipos)))

                accesibilidad.tipos_discapacidad.add(
                    *random.sample(tipos, cantidad)
                )

        # Cada perfil puede tener diferentes necesidades.
        for perfil in PerfilAccesibilidad.objects.all():
            if tipos:
                cantidad = random.randint(1, min(3, len(tipos)))

                perfil.tipos_discapacidad.add(
                    *random.sample(tipos, cantidad)
                )

        # Cada voluntario puede conseguir varias insignias.
        for voluntario in Voluntario.objects.all():
            if insignias:
                cantidad = random.randint(1, min(3, len(insignias)))

                voluntario.insignias.add(
                    *random.sample(insignias, cantidad)
                )

        # Los usuarios pueden marcar animes como favoritos.
        usuarios = list(Usuario.objects.all())
        animes = list(Anime.objects.all())

        for usuario in usuarios:
            if animes:
                cantidad = random.randint(1, min(3, len(animes)))

                usuario.animes_favoritos.add(
                    *random.sample(animes, cantidad)
                )