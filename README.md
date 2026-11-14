# AniAccess — Plataforma de Anime Accesible

**AniAccess** es una aplicación web desarrollada con **Django** cuyo objetivo es facilitar el acceso al anime a personas con distintas necesidades de accesibilidad (auditiva, visual o fotosensible), conectando información sobre catálogos, plataformas de streaming, valoraciones de la comunidad y un sistema de voluntariado colaborativo.

---

## Estructura del proyecto

```text
AniAccess/
├── AniAccess/
│   ├── fixtures/
│   │   └── datos_iniciales.json
│   ├── migrations/
│   ├── static/
│   │   └── AniAccess/
│   │       └── css/
│   │           └── estilos.css
│   ├── templates/
│   │   └── AniAccess/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── catalogo_animes.html
│   │       ├── detalle_anime.html
│   │       ├── comparador_plataformas.html
│   │       ├── buscador_accesibilidad.html
│   │       ├── perfil_usuario.html
│   │       ├── animes_favoritos.html
│   │       ├── ranking_accesibilidad.html
│   │       ├── ranking_voluntarios.html
│   │       ├── detalle_colaboracion.html
│   │       ├── catalogo_insignias.html
│   │       ├── 400.html
│   │       ├── 403.html
│   │       ├── 404.html
│   │       └── 500.html
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/
│   ├── animes/
│   ├── plataformas/
│   └── insignias/
├── mysite/
│   ├── settings.py
│   └── urls.py
├── db.sqlite3
├── manage.py
└── README.md
```

---

## Modelos de datos (`AniAccess/models.py`)

El sistema se apoya en **12 modelos relacionales** registrados en `AniAccess/admin.py`:

1. **`Anime`**: Información general de cada obra (`titulo`, `titulo_original`, `sinopsis`, `anio_estreno`, `num_episodios`, `tipo`, `estado`, `imagen`).
2. **`Plataforma`**: Servicios de streaming (`Crunchyroll`, `Netflix`, `Prime Video`, etc.) con logotipo (`logo`).
3. **`Disponibilidad`**: Tabla intermedia (`through`) entre `Anime`, `Plataforma` e `Idioma` con atributos propios (`subtitulos`, `doblaje`, `fecha_inicio`, `fecha_fin`, `activo`).
4. **`Accesibilidad`**: Ficha `OneToOne` asociada a cada anime con sus opciones (`subtitulos_accesibles`, `audiodescripcion`, `descripcion_sonidos`, `lengua_signos`, `doblaje`, `contraste_visual`).
5. **`TipoDiscapacidad`**: Clasificación de necesidades (`Discapacidad Auditiva`, `Discapacidad Visual`, `Sensibilidad Fotosensible`).
6. **`Idioma`**: Catálogo de idiomas y códigos ISO (`es-ES`, `ja-JP`, `en-US`).
7. **`Usuario`**: Cuentas de usuario de la plataforma.
8. **`PerfilAccesibilidad`**: Preferencias individuales `OneToOne` de cada usuario.
9. **`Valoracion`**: Puntuaciones y reseñas de accesibilidad realizadas por los usuarios sobre los animes.
10. **`Voluntario`**: Perfil colaborador asociado `OneToOne` a un usuario, con puntos y especialidad.
11. **`Colaboracion`**: Trabajos de subtitulado, audiodescripción o revisión realizados por voluntarios.
12. **`Insignia`**: Logros y reconocimientos desbloqueables por los voluntarios con icono personalizado (`icono`).

---

## Mapa de URLs y Vistas

| Nº | Sección | Ruta URL | Nombre de ruta (`name`) | Vista (`views.py`) |
| :- | :--- | :--- | :--- | :--- |
| 0 | **Inicio** | `/` | `index` | `index` |
| 1 | **Catálogo de animes** | `/animes/` | `catalogo_animes` | `catalogo_animes` |
| 2 | **Detalle del anime** | `/animes/<int:id>/` | `detalle_anime` | `detalle_anime` |
| 3 | **Comparador de plataformas** | `/plataformas/` | `comparador_plataformas` | `comparador_plataformas` |
| 4 | **Buscador de accesibilidad** | `/accesibilidad/` | `buscador_accesibilidad` | `buscador_accesibilidad` |
| 5 | **Perfil de usuario** | `/usuarios/<str:nombre>/` | `perfil_usuario` | `perfil_usuario` |
| 6 | **Animes favoritos** | `/usuarios/<str:nombre>/favoritos/` | `animes_favoritos` | `animes_favoritos` |
| 7 | **Ranking de accesibilidad** | `/ranking-accesibilidad/` | `ranking_accesibilidad` | `ranking_accesibilidad` |
| 8 | **Ranking de voluntarios** | `/voluntariado/` | `ranking_voluntarios` | `ranking_voluntarios` |
| 9 | **Detalle de colaboración** | `/voluntariado/colaboraciones/<int:id>/<str:estado>/` | `detalle_colaboracion` | `detalle_colaboracion` |
| 10 | **Catálogo de insignias** | `/voluntariado/insignias/` | `catalogo_insignias` | `catalogo_insignias` |

### Páginas de error personalizadas (`mysite/urls.py`)

- **`400.html`** (`handler400` → `error_400`): Solicitud incorrecta.
- **`403.html`** (`handler403` → `error_403`): Acceso denegado.
- **`404.html`** (`handler404` → `error_404`): Página no encontrada.
- **`500.html`** (`handler500` → `error_500`): Error interno del servidor.

---

## Diseño y Recursos Multimedia (`static/` y `media/`)

- **Interfaz oscura accesible (`estilos.css`):** Diseñada con variables CSS personalizadas, rejillas adaptables (`CSS Grid`), tarjetas de presentación y tipografías `Space Grotesk` y `DM Sans`.
- **Gestión de imágenes (`MEDIA_URL` y `MEDIA_ROOT`):** Configurada en `mysite/settings.py` y servida en desarrollo desde `mysite/urls.py`. Incluye portadas de animes encuadradas sin recortes (`object-fit: contain`), logotipos de plataformas e iconos de insignias procesados con fondo transparente en formato `PNG`.

---

## Instalación y puesta en marcha

1. **Activar el entorno virtual:**
   ```bash
   source myvenv/bin/activate
   ```

2. **Aplicar las migraciones a la base de datos:**
   ```bash
   python3 manage.py migrate
   ```

3. **Cargar los datos iniciales de prueba (fixture):**
   ```bash
   python3 manage.py loaddata datos_iniciales.json
   ```

4. **Arrancar el servidor de desarrollo:**
   ```bash
   python3 manage.py runserver
   ```

5. **Acceder a la aplicación:**
   - Web pública: `http://127.0.0`
   - Panel de administración: `http://127.0.0admin/`

---

## Consultas ORM y SQL RAW

Todas las vistas implementan consultas optimizadas mediante el **ORM de Django** (`select_related`, `prefetch_related`, `annotate`, `Count`, `Avg`, objetos `Q` y `distinct`), acompañadas de su consulta equivalente en **SQL RAW** (`Model.objects.raw()`) documentada y comentada dentro de `AniAccess/views.py`.
