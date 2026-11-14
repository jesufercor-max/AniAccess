# Rama 7 - Ranking de accesibilidad

## Información general

- **Nombre de la rama:** URL_Ranking-Accesibilidad
- **URL:** `/ranking-accesibilidad/`
- **Vista:** `ranking_accesibilidad`
- **Plantilla:** `ranking_accesibilidad.html`

## Objetivo

Mostrar los animes mejor valorados por su accesibilidad,
utilizando las puntuaciones de accesibilidad general realizadas por los usuarios.

## QuerySet utilizado

Se utiliza `Anime.objects.annotate()` sobre la relación inversa `valoraciones` para calcular estadísticas agregadas de cada título.

### Operaciones utilizadas

- `annotate()`: añade los campos calculados `total_valoraciones` y `media_puntuacion` al QuerySet.
- `Count('valoraciones', distinct=True)`: cuenta el total de valoraciones distintas recibidas por cada anime.
- `Avg('valoraciones__accesibilidad_general')`: calcula la puntuación media de accesibilidad general.
- `filter()`: filtra los resultados agregados (`total_valoraciones__gte=1` y `media_puntuacion__gte=3`).
- `order_by()`: ordena de forma descendente por puntuación media (`-media_puntuacion`) y, en caso de empate, por número de valoraciones (`-total_valoraciones`).
- Slicing `[:10]`: limita el ranking a los diez mejores resultados.

## Filtro de agregado

El filtro se aplica después de `annotate()`:

`total_valoraciones__gte=1, media_puntuacion__gte=3`

En SQL equivale a utilizar `HAVING`, porque filtra los resultados
de una función de agregación tras agrupar por anime.

## SQL RAW

La vista incluye una consulta SQL equivalente con `INNER JOIN` a `AniAccess_valoracion`, `GROUP BY` y `HAVING`.
Está comentada y no se ejecuta.

## Relaciones utilizadas

- `Anime` y `Valoracion`: relación inversa ManyToOne mediante `related_name="valoraciones"`.
- `Valoracion` contiene el campo `accesibilidad_general` utilizado para el cálculo de la media.

## Plantilla HTML

Muestra:

- Cabecera de sección y listado estructurado con tarjetas de ranking (`ranking-list` y `ranking-card`).
- Posición en el ranking (`#1`, `#2`, etc.) mediante `forloop.counter`.
- Título e imagen del anime (con marcador visual `ANIACCESS` si no tiene imagen asignada).
- Sinopsis resumida.
- Media de accesibilidad formateada a dos decimales (`floatformat:2`) y total de valoraciones.
- Año de estreno y estado del anime.
- Enlace a la ficha del anime (comentado con `{% comment %}` para evitar `NoReverseMatch` hasta integrar la vista de detalle).

## Prueba

1. Asegurarse de tener cargados los datos de prueba (`python3 manage.py loaddata datos_iniciales.json`), que incluyen valoraciones con puntuación de accesibilidad igual o superior a 3.
2. Acceder en el navegador desde el botón de inicio o directamente a:

`http://127.0.0.1:8000/ranking-accesibilidad/`

## Fusión

```bash
git add .
git commit -m "Añadir ranking de accesibilidad"
git push -u origin URL_Ranking-Accesibilidad

git switch URLs
git merge URL_Ranking-Accesibilidad
git push origin URLs
```