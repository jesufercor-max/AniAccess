# Rama 8 - Ranking de voluntarios

## Información general

- **Nombre de la rama:** URL_Ranking-Voluntarios
- **URL:** `/voluntariado/` (nombre de ruta: `ranking_voluntarios`)
- **Vista:** `ranking_voluntarios`
- **Plantilla:** `ranking_voluntarios.html`

## Objetivo

Mostrar un ranking de voluntarios disponibles,
ordenados según sus puntos acumulados y actividad colaborativa aprobada.

## QuerySet utilizado

Se utiliza `Voluntario.objects.filter()` combinado con `select_related()`, `prefetch_related()` y `annotate()`.

### Operaciones utilizadas

- `filter(disponible=True)`: obtiene únicamente los voluntarios disponibles.
- `select_related('usuario')`: carga en la misma consulta el usuario asociado (`OneToOne`).
- `prefetch_related('insignias', 'colaboraciones')`: optimiza la carga de insignias y colaboraciones relacionadas.
- `Q(colaboraciones__estado='Aprobada')`: filtra dentro del agregado exclusivamente las colaboraciones aprobadas.
- `Count('colaboraciones', filter=..., distinct=True)`: cuenta las colaboraciones aprobadas de cada voluntario.
- `annotate()`: añade el campo calculado `total_colaboraciones` al resultado.
- `order_by('-puntos', '-total_colaboraciones')`: ordena por puntos descendentes y, en caso de empate, por colaboraciones aprobadas.
- Slicing `[:10]`: limita el ranking a los diez primeros voluntarios.

## SQL RAW

Se incluye una consulta SQL equivalente con `INNER JOIN`, `LEFT JOIN`,
`COUNT(DISTINCT CASE WHEN ...)`, `GROUP BY` y `ORDER BY`.
Está comentada y no se ejecuta.

## Relaciones utilizadas

- `Voluntario` y `Usuario`: `OneToOneField`.
- `Voluntario` y `Colaboracion`: relación inversa `ManyToOne` mediante `related_name="colaboraciones"`.
- `Voluntario` e `Insignia`: `ManyToManyField` mediante `insignias`.

## Plantilla HTML

Muestra:

- Cabecera de sección y tarjetas de voluntarios (`data-grid` y `volunteer-card`).
- Posición en el ranking (`#1`, `#2`, etc.) mediante `forloop.counter`.
- Nombre público, descripción, usuario asociado (`@nombre_usuario`) y especialidad.
- Fecha de alta y estado de disponibilidad.
- Puntos acumulados, colaboraciones completadas y colaboraciones aprobadas.
- Insignias conseguidas con sus requisitos de puntos y colaboraciones.
- Colaboraciones registradas con tipo, estado, `puntos_obtenidos`, `fecha_inicio` y `fecha_finalizacion`.
- Enlace al detalle de la colaboración (comentado con `{% comment %}` para evitar `NoReverseMatch` hasta integrar la vista de detalle).

## Prueba

1. Asegurarse de tener cargados los datos de prueba (`python3 manage.py loaddata datos_iniciales.json`), que incluyen voluntarios disponibles con insignias y colaboraciones.
2. Acceder desde el menú o el botón de inicio, o directamente en el navegador a:

`http://127.0.0.1:8000/voluntariado/`

## Fusión

```bash
git add .
git commit -m "Añadir ranking de voluntarios"
git push -u origin URL_Ranking-Voluntarios

git switch URLs
git merge URL_Ranking-Voluntarios
git push origin URLs
```