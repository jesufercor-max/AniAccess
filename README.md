# Rama 6 - Animes favoritos

## Información general

- **Nombre de la rama:** URL_Animes-Favoritos
- **URL:** `/usuarios/<str:nombre>/favoritos/`
- **Vista:** `animes_favoritos`
- **Plantilla:** `animes_favoritos.html`

## Objetivo

Mostrar los animes que un usuario ha añadido a su lista de favoritos y permitir filtrar la colección mediante un buscador por título o título original.

## QuerySet utilizado

Se utiliza la relación ManyToMany entre `Anime` y `Usuario`, combinando condiciones con objetos `Q` para la búsqueda dinámica.

### Operaciones utilizadas

- `get_object_or_404()`: obtiene el usuario a partir de su `nombre_usuario`.
- `filter()` y objetos `Q`: filtra los animes relacionados con el usuario y aplica búsqueda insensible a mayúsculas (`icontains`) por `titulo` o `titulo_original`.
- `prefetch_related()`: optimiza la carga de `plataformas` y `disponibilidades__idioma`.
- `order_by()`: ordena los títulos alfabéticamente.

## SQL RAW

Se incluye una consulta equivalente mediante `Anime.objects.raw()` con unión (`INNER JOIN`) a la tabla intermedia `AniAccess_anime_usuarios_favoritos` y filtrado por `LIKE`.
Está comentada y no se ejecuta.

## Relaciones utilizadas

- `Anime` y `Usuario`: ManyToMany mediante `usuarios_favoritos`.
- `Anime` y `Plataforma`: ManyToMany mediante `Disponibilidad`.
- `Disponibilidad` e `Idioma`: ManyToOne.

## Plantilla HTML

Muestra:

- Cabecera con el nombre del usuario y formulario de búsqueda (`GET`).
- Título e imagen del anime (con marcador visual si no tiene imagen).
- Sinopsis y título original.
- Año de estreno, número de episodios, tipo y estado.
- Plataformas disponibles.
- Disponibilidades por idioma (indicando subtítulos, doblaje y estado activo).
- Enlace al detalle del anime (comentado con `{% comment %}` para evitar `NoReverseMatch` hasta integrar la vista de detalle).

## Prueba

1. Asegurarse de tener datos cargados en la base de datos (`python3 manage.py loaddata datos_iniciales.json`) y favoritos asignados al usuario.
2. Acceder en el navegador a:

`http://127.0.0.1:8000/usuarios/elena_sub/favoritos/`

*(Se puede sustituir `elena_sub` por cualquier otro `nombre_usuario` existente en la base de datos).*

## Fusión

```bash
git add .
git commit -m "Añadir listado y buscador de animes favoritos"
git push -u origin URL_Animes-Favoritos

git switch URLs
git merge URL_Animes-Favoritos
git push origin URLs
```