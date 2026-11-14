# Rama 9 - Detalle de colaboración

## Información general

- **Nombre de la rama:** URL_Detalle-Colaboracion
- **URL:** `/voluntariado/colaboraciones/<int:id>/<str:estado>/`
- **Vista:** `detalle_colaboracion`
- **Plantilla:** `detalle_colaboracion.html`

## Objetivo

Mostrar la información completa de una colaboración concreta,
incluyendo sus datos de gestión, fechas, puntos y la ficha del voluntario responsable.

## QuerySet utilizado

Se utiliza `Colaboracion.objects.select_related()` junto con `get_object_or_404()` filtrando por identificador y estado.

### Operaciones utilizadas

- `get_object_or_404()`: busca la colaboración que coincida con ambos parámetros o devuelve un error `404`.
- `select_related('voluntario__usuario')`: carga en la misma consulta el voluntario responsable y su cuenta de usuario mediante `INNER JOIN`.

## Parámetros de la URL

La ruta utiliza `path()` con convertidores de tipo y recibe dos parámetros dinámicos:

- `<int:id>`: identificador numérico entero de la colaboración.
- `<str:estado>`: cadena de texto con el estado de la colaboración (por ejemplo, `Aprobada` o `En proceso`).

## SQL RAW

Se incluye una consulta SQL equivalente con `INNER JOIN` a `AniAccess_voluntario` y `AniAccess_usuario`, y dos condiciones en el `WHERE` (`c.id = %s AND c.estado = %s`).
Está comentada y no se ejecuta.

## Relaciones utilizadas

- `Colaboracion` y `Voluntario`: `ManyToOne` mediante `ForeignKey`.
- `Voluntario` y `Usuario`: `OneToOne` mediante `OneToOneField`.

## Plantilla HTML

Muestra:

- Cabecera con título y descripción del trabajo.
- Tarjeta de información de la colaboración (`info-card`): tipo, estado actual, `puntos_obtenidos`, `fecha_creacion`, `fecha_inicio`, `fecha_finalizacion` y `fecha_revision`.
- Bloque condicional con `comentarios_revision` y enlace de descarga para `archivo_entrega` (si existen).
- Tarjeta del voluntario responsable: nombre público, usuario asociado (`@nombre_usuario`), especialidad, disponibilidad, puntos totales y colaboraciones completadas.
- Acceso directo desde la portada (`index.html`) hacia la colaboración de ejemplo `#1`.

## Prueba

1. Asegurarse de tener cargados los datos de prueba (`python3 manage.py loaddata datos_iniciales.json`).
2. Acceder desde el botón de la portada o directamente en el navegador a:

`http://127.0.0.1:8000/voluntariado/colaboraciones/1/Aprobada/`

*(También se puede probar con la segunda colaboración del fixture: `http://127.0.0`).*

## Fusión

```bash
git add .
git commit -m "Añadir detalle de colaboración"
git push -u origin URL_Detalle-Colaboracion

git switch URLs
git merge URL_Detalle-Colaboracion
git push origin URLs
```
