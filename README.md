# Rama 1 - Catálogo de animes

## Información general

- **Nombre de la rama:** URL_Animes
- **URL:** `/animes/`
- **Vista:** `catalogo_animes`
- **Plantilla:** `catalogo_animes.html`

## Objetivo

Mostrar un catálogo de animes en emisión y permitir al usuario
buscar títulos mediante su nombre o título original.

## QuerySet utilizado

Se utiliza `Anime.objects.filter()` para obtener los animes
que cumplen las condiciones de búsqueda.

### Operaciones utilizadas

- `Q`: permite construir condiciones complejas.
- AND (`&`): combina el estado del anime con la búsqueda.
- OR (`|`): busca coincidencias en el título o título original.
- `icontains`: búsqueda sin distinguir mayúsculas y minúsculas.
- `order_by`: ordena los animes por año de estreno descendente.
- Slicing `[:20]`: limita los resultados a 20 registros.

## SQL RAW

La vista incluye una consulta SQL equivalente mediante
`Anime.objects.raw()`.

La consulta RAW está comentada y se incluye como alternativa
didáctica. La consulta ORM es la que se ejecuta.

## Plantilla HTML

La plantilla muestra:

- Título del anime.
- Título original.
- Sinopsis.
- Imagen (Aún no, se mostrara en la rama principal URLs).
- Año de estreno.
- Número de episodios.
- Tipo.
- Estado.
- Enlace al detalle del anime (Aún no, se mostrara en la rama principal URLs).

## Prueba

Acceder a:

`http://127.0.0.1:8000/animes/`

También se puede realizar una búsqueda:

`http://127.0.0.1:8000/animes/?buscar=jujutsu kaisen`

## Fusión

Una vez comprobada la funcionalidad:

```bash
git add .
git commit -m "Añadir catálogo de animes"
git push -u origin URL_Animes

git switch URLs
git merge URL_Animes
git push origin URLs