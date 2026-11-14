# Rama 10 - Catálogo de insignias

## Información general

- **Nombre de la rama:** URL_Catalogos-Insignias
- **URL:** `/voluntariado/insignias/` (nombre de ruta: `catalogo_insignias`)
- **Vista:** `catalogo_insignias`
- **Plantilla:** `catalogo_insignias.html`

## Objetivo

Mostrar el catálogo de insignias activas en la plataforma,
indicando sus requisitos y los voluntarios que las han conseguido.

## QuerySet utilizado

Se utiliza `Insignia.objects.filter()` combinado con `annotate()` y `prefetch_related()`.

### Operaciones utilizadas

- `filter(activa=True)`: obtiene únicamente las insignias que se encuentran activas.
- `Count('voluntarios', distinct=True)`: cuenta el número de voluntarios distintos que han obtenido cada insignia.
- `annotate()`: añade el campo calculado `total_voluntarios` al resultado.
- `prefetch_related('voluntarios__usuario')`: optimiza la carga de los voluntarios asociados y sus cuentas de usuario en la misma consulta.
- `order_by('puntos_necesarios')`: ordena las insignias de menor a mayor dificultad según los puntos requeridos.

## SQL RAW

Se incluye una consulta SQL equivalente con `LEFT JOIN` a la tabla intermedia `AniAccess_voluntario_insignias`,
`COUNT(DISTINCT ...)`, `GROUP BY` y `ORDER BY`.
Está comentada y no se ejecuta.

## Relaciones utilizadas

- `Insignia` y `Voluntario`: relación inversa `ManyToMany` mediante `related_name="voluntarios"`.
- `Voluntario` y `Usuario`: `OneToOne` mediante `OneToOneField`.

## Plantilla HTML

Muestra:

- Cabecera de sección y cuadrícula de tarjetas (`data-grid` y `badge-card`).
- Icono de la insignia (o marcador visual `.badge-icon` si no tiene imagen subida).
- Nombre y descripción del reconocimiento.
- Requisitos de puntos (`puntos_necesarios`), colaboraciones (`colaboraciones_necesarias`) y total de voluntarios que la poseen (`total_voluntarios`).
- Listado detallado de los voluntarios que han conseguido la insignia (`nombre_publico`, `@nombre_usuario`, `especialidad`, `puntos` y `colaboraciones_completadas`).

## Prueba

1. Asegurarse de tener cargados los datos de prueba (`python3 manage.py loaddata datos_iniciales.json`), que incluyen insignias activas y voluntarios asociados.
2. Acceder desde el menú o el botón de inicio, o directamente en el navegador a:

`http://127.0.0`

## Fusión

```bash
git add .
git commit -m "Añadir catálogo de insignias"
git push -u origin URL_Catalogos-Insignias

git switch URLs
git merge URL_Catalogos-Insignias
git push origin URLs
```
