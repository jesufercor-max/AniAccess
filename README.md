# Rama 2 - Detalle de anime

## Información general

- **Nombre de la rama:** URL_Detalle-Anime
- **URL:** `/anime/<int:id>/`
- **Vista:** `detalle_anime`
- **Plantilla:** `detalle_anime.html`

## Objetivo

Mostrar la ficha completa de un anime, incluyendo su información
general, plataformas, disponibilidades por idioma, accesibilidad
y valoraciones realizadas por los usuarios.

## QuerySet utilizado

Se utiliza `get_object_or_404()` junto con un QuerySet de Anime. (Este error se implementa el la rama URLs)

### Operaciones utilizadas

- `select_related()`: carga la relación OneToOne de accesibilidad.
- `prefetch_related()`: carga plataformas, disponibilidades,
  idiomas, valoraciones y tipos de discapacidad.
- `annotate()`: añade cálculos a cada anime.
- `Count()`: cuenta las valoraciones.
- `Avg()`: calcula la media de accesibilidad.
- `distinct=True`: evita contar valoraciones duplicadas
  cuando se realizan uniones con otras relaciones.

## SQL RAW

La vista incluye una consulta SQL equivalente mediante
`Anime.objects.raw()`.

La consulta RAW está comentada. La consulta ORM es la que se ejecuta.
Las relaciones múltiples se cargan mediante consultas adicionales
en el ORM.

## Relaciones utilizadas

- Anime y Accesibilidad: OneToOne.
- Anime y Plataforma: ManyToMany mediante Disponibilidad.
- Disponibilidad e Idioma: ManyToOne.
- Anime y Valoracion: ManyToOne.
- Valoracion y Usuario: ManyToOne.
- Accesibilidad y TipoDiscapacidad: ManyToMany.

## Plantilla HTML

La plantilla muestra:

- Información general del anime.
- Imagen, título y sinopsis.
- Año, episodios, tipo y estado.
- Estadísticas de valoraciones.
- Plataformas relacionadas.
- Disponibilidades e idiomas.
- Opciones de accesibilidad.
- Tipos de discapacidad.
- Valoraciones y usuarios que las realizan.

## Prueba

Acceder a:

`http://127.0.0.1:8000/anime/3/`

El identificador debe corresponder a un anime existente.

## Fusión

```bash
git add .
git commit -m "Añadir detalle completo de anime"
git push -u origin URL_Detalle-Anime

git switch URLs
git merge URL_Detalle-Anime
git push origin URLs