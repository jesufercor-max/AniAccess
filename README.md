# Rama 3 - Comparador de plataformas

## Información general

- **Nombre de la rama:** URL_Plataformas
- **URL:** `/plataformas/`
- **Vista:** `comparador_plataformas`
- **Plantilla:** `comparador_plataformas.html`

## Objetivo

Mostrar las plataformas activas y sus animes disponibles,
incluyendo información sobre idiomas, subtítulos y doblaje.

## QuerySet utilizado

Se utiliza `Plataforma.objects.filter()` para obtener las
plataformas que tienen disponibilidades activas y vigentes.

### Operaciones utilizadas

- `filter()`: filtra plataformas y disponibilidades activas.
- `fecha_fin__isnull=True`: selecciona disponibilidades
  sin fecha de finalización.
- `annotate()`: añade el número de animes disponibles.
- `Count()`: cuenta los animes asociados.
- `distinct=True`: evita contar un mismo anime varias veces.
- `prefetch_related()`: carga animes e idiomas relacionados.
- `order_by()`: ordena las plataformas alfabéticamente.

## SQL RAW

La vista incluye una consulta SQL equivalente mediante
`Plataforma.objects.raw()`.

La consulta RAW está comentada y no se ejecuta.
La consulta ORM es la utilizada por la página.

## Relaciones utilizadas

- Plataforma y Disponibilidad: relación inversa ManyToOne.
- Disponibilidad y Anime: ManyToOne.
- Disponibilidad e Idioma: ManyToOne.

## Plantilla HTML

Se muestra:

- Nombre y logo de la plataforma.
- Descripción y página web.
- Estado de actividad.
- Número de animes disponibles.
- Títulos y títulos originales.
- Idiomas.
- Subtítulos y doblaje.
- Fechas de disponibilidad.

## Prueba

Acceder a:

`http://127.0.0.1:8000/plataformas/`

Para mostrar resultados deben existir plataformas activas
con disponibilidades activas y fecha_fin nula.

## Fusión

```bash
git add .
git commit -m "Añadir comparador de plataformas"
git push -u origin URL_Plataformas

git switch URLs
git merge URL_Plataformas
git push origin URLs