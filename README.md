# Rama 5 - Perfil de usuario

## Información general

- **Nombre de la rama:** URL_Perfil-Usuario
- **URL:** `/usuarios/<str:nombre>/`
- **Vista:** `perfil_usuario`
- **Plantilla:** `perfil_usuario.html`

## Objetivo

Mostrar la información de un usuario, sus preferencias de accesibilidad,
valoraciones y actividad como voluntario.

## QuerySet utilizado

Se utiliza `Usuario.objects.select_related()` y `prefetch_related()`.

### Operaciones utilizadas

- `get_object_or_404()`: obtiene el usuario o devuelve un error 404.
- `select_related()`: carga las relaciones OneToOne.
- `prefetch_related()`: carga las relaciones inversas y ManyToMany.

## SQL RAW

Se incluye una consulta SQL mediante `Usuario.objects.raw()`.
Está comentada como alternativa didáctica. La consulta ORM es la ejecutada.

## Relaciones utilizadas

- Usuario y PerfilAccesibilidad: OneToOne.
- Usuario y Voluntario: OneToOne.
- Usuario y Valoracion: relación inversa ManyToOne.
- PerfilAccesibilidad y TipoDiscapacidad: ManyToMany.
- Voluntario e Insignia: ManyToMany.
- Voluntario y Colaboracion: relación inversa ManyToOne.

## Plantilla HTML

Muestra:

- Datos del usuario.
- Preferencias de accesibilidad.
- Tipos de discapacidad.
- Valoraciones realizadas.
- Información del voluntario.
- Insignias y colaboraciones.

## Prueba

`http://127.0.0.1:8000/usuarios/elena_sub/`

Sustituir `nombre_usuario` por un usuario existente (elena_sub).

## Fusión

```bash
git add .
git commit -m "Añadir perfil de usuario"
git push -u originURL_Perfil-Usuario

git switch URLs
git mergeURL_Perfil-Usuario
git push origin URLs