# Rama 11 - Páginas de error personalizadas

## Información general

- **Nombre de la rama:** URL_Paginas-Errores
- **Archivo de configuración:** `mysite/urls.py`
- **Vistas:** `error_400`, `error_403`, `error_404`, `error_500`
- **Plantillas:** `400.html`, `403.html`, `404.html`, `500.html`

## Objetivo

Proporcionar páginas de error personalizadas coherentes con la estética de AniAccess
para mejorar la experiencia de usuario ante fallos de navegación, permisos o del servidor.

## Manejadores configurados

En el archivo principal `mysite/urls.py` se registran las variables globales de Django:

- `handler400 = 'AniAccess.views.error_400'` (Solicitud incorrecta)
- `handler403 = 'AniAccess.views.error_403'` (Acceso denegado)
- `handler404 = 'AniAccess.views.error_404'` (Página no encontrada)
- `handler500 = 'AniAccess.views.error_500'` (Error interno del servidor)

## Vistas implementadas

Cada vista renderiza su plantilla correspondiente devolviendo el código de estado HTTP adecuado mediante `status`:

- `error_400(request, exception)`: devuelve `400.html` con `status=400`.
- `error_403(request, exception)`: devuelve `403.html` con `status=403`.
- `error_404(request, exception)`: devuelve `404.html` con `status=404`.
- `error_500(request)`: devuelve `500.html` con `status=500` (no recibe `exception`).

## Plantillas HTML

Todas las plantillas heredan de `base.html` y utilizan los estilos de `estilos.css` (`.empty-state`, `.eyebrow`, `.btn btn-primary`).

Muestran:

- Código de error HTTP (`ERROR 400`, `ERROR 403`, `ERROR 404`, `ERROR 500`).
- Título descriptivo y mensaje claro explicando el motivo del fallo.
- Botón de regreso directo a la página de inicio (`{% url 'index' %}`).

## Guía completa de prueba en local

Para visualizar las plantillas personalizadas (ya que con `DEBUG = True` Django muestra sus pantallas técnicas amarillas):

### 1. Desactivar el modo debug temporalmente
En `mysite/settings.py`, modificar:
```python
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

### 2. Añadir rutas temporales para forzar los errores 400, 403 y 500
En `AniAccess/urls.py`, añadir temporalmente las excepciones de prueba:
```python
from django.core.exceptions import PermissionDenied, SuspiciousOperation

def forzar_400(request):
    raise SuspiciousOperation("Prueba de error 400")

def forzar_403(request):
    raise PermissionDenied("Prueba de error 403")

def forzar_500(request):
    return 1 / 0
```
Y registrarlas dentro de `urlpatterns`:
```python
path('test-400/', forzar_400),
path('test-403/', forzar_403),
path('test-500/', forzar_500),
```

### 3. Arrancar el servidor cargando archivos estáticos
Ejecutar el servidor con la bandera `--insecure` para que sirva el CSS en modo `DEBUG = False`:
```bash
python3 manage.py runserver --insecure
```

### 4. Comprobar cada error en el navegador
- **Error 400:** `http://127.0.0.1:8000//test-400/`
- **Error 403:** `http://127.0.0.1:8000//test-403/`
- **Error 404:** `http://127.0.0.1:8000//test-404/`
- **Error 500:** `http://127.0.0.1:8000//test-500/`

### 5. Limpieza obligatoria antes de hacer commit
1. Eliminar las funciones `forzar_400`, `forzar_403`, `forzar_500` y las rutas `test-400/`, `test-403/`, `test-500/` de `AniAccess/urls.py`.
2. Volver a poner `DEBUG = True` en `mysite/settings.py`.

## Fusión

```bash
git add .
git commit -m "Añadir páginas de error personalizadas (400, 403, 404, 500)"
git push -u origin URL_Paginas-Errores

git switch URLs
git merge URL_Paginas-Errores
git push origin URLs
```
