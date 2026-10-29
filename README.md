# AniAccess - Rama de backups

Esta rama recoge el trabajo realizado para **rellenar la base de datos con datos de prueba** y **guardar una copia de seguridad** de esos datos.

## Qué se ha hecho

1. **Rellenar las tablas con seeders.**
2. **Crear un comando que genere 10 registros aleatorios de cada modelo con Faker** (`generar_datos.py`).
3. **Crear un backup de los datos con fixtures** (`datos.json`).

> **Importante:** los datos de `generar_datos.py` y de `datos.json` han sido **creados por IA** a partir de nuestros modelos.

## Estructura

```
AniAccess/
├── fixtures/
│   └── datos.json                  # Backup de datos (fixture)
└── management/
    └── commands/
        └── generar_datos.py        # Comando que genera datos con Faker
```

## Configuración necesaria: `USE_TZ`

Nuestros modelos usan campos de fecha y hora (`DateTimeField`, por ejemplo `fecha_registro`, `fecha_creacion` o `fecha_revision`). Por el manejo de zonas horarias, **es obligatorio tener `USE_TZ = True`** en `settings.py` para poder generar datos en la base de datos:

```python
USE_TZ = True
```

## 1. Seeders

Se intentó rellenar las tablas con `django-seed`:

```bash
python manage.py seed AniAccess --number=10
```

`django-seed` no soporta el `ManyToManyField` con tabla intermedia (`through`) de `Anime.plataformas` (que usa `Disponibilidad`) y lanza el error `Field AniAccess.Anime.plataformas cannot be null`. Por eso la relación `Anime` - `Plataforma` - `Idioma` se rellena con el comando de Faker descrito a continuación.

## 2. Generar datos con Faker

El comando `generar_datos` crea **10 registros aleatorios de cada modelo** y después asocia las relaciones muchos a muchos:

```bash
python manage.py generar_datos
```

Modelos que rellena: `Idioma`, `TipoDiscapacidad`, `Insignia`, `Plataforma`, `Usuario`, `Anime`, `Disponibilidad`, `Accesibilidad`, `PerfilAccesibilidad`, `Valoracion`, `Voluntario` y `Colaboracion`.

Notas:

- No acepta parámetros: siempre genera 10 registros por modelo.
- Solo crea los que faltan hasta llegar a 10, por lo que se puede ejecutar sobre una base de datos con datos previos.

## 3. Backup con fixtures

### Crear o actualizar el backup

```bash
python manage.py dumpdata AniAccess --indent 4 -o AniAccess/fixtures/datos.json
```

### Restaurar el backup

Con la base de datos vacía y migrada:

```bash
python manage.py migrate
python manage.py loaddata AniAccess/fixtures/datos.json
```

Para comprobar que se han cargado los datos:

```bash
python manage.py shell -c "from AniAccess.models import Anime, Usuario; print(Anime.objects.count(), Usuario.objects.count())"
```

## Contenido del fixture `datos.json`

91 objetos: 6 idiomas, 5 tipos de discapacidad, 5 insignias, 5 plataformas, 8 usuarios, 8 animes, 14 disponibilidades, 8 accesibilidades, 8 perfiles de accesibilidad, 12 valoraciones, 4 voluntarios y 8 colaboraciones.

## Problemas habituales

- **`Installed N object(s)` pero no hay datos:** el fixture se generó sin indicar la app. Usa `dumpdata AniAccess` y no `dumpdata` a secas.
- **`JSONDecodeError` al cargar el fixture:** el archivo quedó incompleto porque `dumpdata` falló al escribir. Usa `-o` en lugar de `>` y no borres la base de datos antes de exportar.
- **Error por `unique` al cargar:** la base de datos ya tiene esos registros. Bórrala y ejecuta `migrate`, o usa `python manage.py flush`.
- **Error de fechas o zona horaria:** comprueba que `USE_TZ = True`.