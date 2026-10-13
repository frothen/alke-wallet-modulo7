# Informe técnico — Alke Wallet (Módulo 7)

## 1. Objetivo
Construir una aplicación web Django para administrar perfiles de clientes, cuentas y registros de transacciones, consultar saldos y generar reportes básicos.

## 2. Arquitectura
- `websolutions_platform/settings.py`: configuración de aplicaciones, seguridad, archivos estáticos y motor de base de datos.
- `gestion/models.py`: entidades y relaciones ORM.
- `gestion/forms.py`: formularios ModelForm y validaciones.
- `gestion/views.py`: vistas basadas en clases para CRUD.
- `gestion/urls.py`: rutas dinámicas.
- `gestion/admin.py`: administración personalizada.
- `gestion/templates/`: interfaz HTML con herencia de `base.html`.
- `gestion/static/gestion/css/styles.css`: estilos.
- `gestion/tests.py`: pruebas automatizadas.

## 3. Base de datos
SQLite se utiliza por defecto para desarrollo local. La configuración permite seleccionar PostgreSQL con `DJANGO_DB_ENGINE=postgresql` y las variables `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST` y `DJANGO_DB_PORT`. El paquete instala `psycopg` como adaptador.

## 4. Modelos y relaciones
`Cliente` está asociado uno a uno con el usuario autenticado. `Cuenta` tiene una relación muchos-a-uno con Cliente. Cuenta y Cliente se relacionan muchos-a-muchos para guardar beneficiarios. `Transaccion` referencia una cuenta de origen y una de destino.

## 5. Migraciones
Ejecutar `python manage.py makemigrations gestion` y `python manage.py migrate`. El historial generado debe conservarse en `gestion/migrations/` y versionarse en Git.

## 6. Consultas personalizadas
La aplicación utiliza `filter`, `exclude`, `annotate`, `aggregate`, `values` y `select_related`. `scripts/consultas_orm.py` incluye ejemplos con `raw()` y cursor parametrizado. Ejecutar desde `python manage.py shell` copiando sus bloques o con `exec(open('scripts/consultas_orm.py', encoding='utf-8').read())`.

## 7. CRUD y seguridad
Vistas basadas en clases permiten crear, listar, consultar, actualizar y eliminar cuentas; gestionar el perfil y registrar/consultar transacciones. Se usa `LoginRequiredMixin`, filtrado por el usuario autenticado, tokens CSRF en formularios POST y validación de entradas.

## 8. Aplicaciones preinstaladas
`django.contrib.admin`, `django.contrib.auth`, `django.contrib.sessions`, `django.contrib.messages` y `django.contrib.staticfiles` están habilitadas. Los modelos se registran en admin y el login/logout utiliza las rutas estándar de Django.

## 9. Pruebas
`gestion/tests.py` verifica relaciones 1:1, 1:N y N:M, registro de transacciones, acceso autenticado, aislamiento de cuentas y presencia de CSRF en formularios. Ejecutar `python manage.py test`.

## 10. Git y GitHub
Consultar `docs/Git_GitHub.md` para comandos de repositorio, commits y ramas `feature/modelos` y `feature/crud`.

## 11. Limitaciones
Este proyecto es un prototipo educativo. No realiza transferencias reales ni ajusta saldos cuando se registra una transacción. Para producción se requieren secretos fuera del código, `DEBUG=False`, HTTPS, controles de fraude, auditoría, pruebas de concurrencia y revisión de seguridad.
