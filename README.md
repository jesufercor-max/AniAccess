# Rama 4 - Buscador de accesibilidad

## Información general

- **Nombre de la rama:** URL_Accesibilidad
- **URL:** `/accesibilidad/`
- **Vista:** `buscador_accesibilidad`
- **Plantilla:** `buscador_accesibilidad.html`

## Objetivo

Mostrar los animes que disponen de características de accesibilidad,
como subtítulos descriptivos, audiodescripción y lengua de signos.

## QuerySet utilizado

Se utiliza `Anime.objects.filter()` con expresiones Q.

### Operaciones utilizadas

- `Q()`: permite construir filtros complejos.
- OR (`|`): obtiene animes que cumplan al menos una condición.
- `select_related()`: carga la relación OneToOne de accesibilidad.
- `prefetch_related()`: carga los tipos de discapacidad relacionados.
- `distinct()`: evita duplicados.
- `order_by()`: ordena los animes por título.

## SQL RAW

Se incluye una consulta SQL equivalente mediante
`Anime.objects.raw()`.

Está comentada y no se ejecuta. La consulta ORM es la utilizada.

## Relaciones utilizadas

- Anime y Accesibilidad: OneToOne.
- Accesibilidad y TipoDiscapacidad: ManyToMany.

## Plantilla HTML

Muestra:

- Título e imagen del anime.
- Título original y sinopsis.
- Disponibilidad de subtítulos CC.
- Disponibilidad de audiodescripción.
- Disponibilidad de lengua de signos.
- Tipos de discapacidad asociados.
- Enlace a la ficha completa.

## Prueba

Acceder a:

`http://127.0.0.1:8000/accesibilidad/`

Deben existir animes con registros asociados en Accesibilidad.

## Fusión

```bash
git add .
git commit -m "Añadir buscador de accesibilidad"
git push -u origin URL_Accesibilidad

git switch URLs
git merge URL_Accesibilidad
git push origin URLs