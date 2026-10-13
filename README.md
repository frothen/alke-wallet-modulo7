# Alke Wallet — Módulo 7: Desarrollo Web con Django

Prototipo académico de billetera digital para practicar configuración de bases de datos, modelos ORM, relaciones, migraciones, consultas personalizadas, CRUD, aplicaciones integradas de Django y control de versiones.

## Requisitos
- Python 3.10+.
- pip.
- Django 5.2.
- SQLite (incluido con Python) para desarrollo.
- PostgreSQL opcional para producción, con el adaptador `psycopg`.

## Instalar en Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations gestion
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Visita `http://127.0.0.1:8000/` y `http://127.0.0.1:8000/admin/`.

## macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations gestion
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Pruebas
```bash
python manage.py test
```

## Consultas ORM, raw y cursor
Inicia `python manage.py shell` y ejecuta:
```python
exec(open("scripts/consultas_orm.py", encoding="utf-8").read())
```
Para obtener resultados representativos, crea primero perfiles, cuentas y transacciones de prueba.

## PostgreSQL
Instala las dependencias con `pip install -r requirements.txt`, crea la base de datos y define variables de entorno descritas en `.env.example`. Establece `DJANGO_DB_ENGINE=postgresql`. El archivo `settings.py` contiene los parámetros de conexión. No guardes contraseñas reales en GitHub.

## Estructura
- `websolutions_platform/`: configuración del proyecto.
- `gestion/`: modelos, formularios, vistas, rutas, admin, pruebas, templates y CSS.
- `scripts/consultas_orm.py`: consultas personalizadas.
- `docs/`: informe técnico, modelo de datos y guía GitHub.
- `evidencias/`: guía de capturas necesarias.

## Alcance y seguridad
Es un prototipo educativo. Registrar una transacción no mueve dinero automáticamente ni constituye una operación financiera real. Para producción se necesita revisión de seguridad, gestión de secretos, HTTPS, validación transaccional atómica y auditoría.
