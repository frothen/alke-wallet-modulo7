# Git y GitHub: flujo de trabajo sugerido

Desde la carpeta raíz del proyecto:

```bash
git init
git add .
git commit -m "chore: crear estructura inicial de Alke Wallet"
git branch -M main
```

Crea un repositorio vacío en GitHub y conecta la URL real:

```bash
git remote add origin URL_REAL_DE_TU_REPOSITORIO
git push -u origin main
```

Desarrollo de modelos en rama propia:

```bash
git switch -c feature/modelos
git add gestion/models.py gestion/admin.py
git commit -m "feat: agregar modelos y relaciones ORM"
git push -u origin feature/modelos
```

Desarrollo de CRUD y vistas:

```bash
git switch main
git switch -c feature/crud
git add gestion/forms.py gestion/views.py gestion/urls.py gestion/templates
git commit -m "feat: implementar operaciones CRUD"
git push -u origin feature/crud
```

Cuando corresponda, abre Pull Requests en GitHub y fusiona las ramas tras revisar los cambios. No subas `.env`, `db.sqlite3`, contraseñas ni claves privadas. Si `origin` ya existe, usa `git remote -v` y no vuelvas a ejecutar `git remote add origin`.
