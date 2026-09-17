# PyGraphile Documentation

PyGraphile automatically generates GraphQL APIs from your database schema — no boilerplate, no manual resolvers.

## Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
  - [ASGI (FastAPI / Uvicorn)](#asgi--fastapi--uvicorn)
  - [WSGI (Gunicorn)](#wsgi--gunicorn)
- [API Reference](#api-reference)
- [Database Support](#database-support)
- [Identifier Sanitization](#identifier-sanitization)
- [Roadmap](#roadmap)

---

## Installation

```bash
# SQLite (no extra dependencies)
pip install pygraphile

# MariaDB / MySQL
pip install "pygraphile[mariadb]"

# Using uv
uv add pygraphile
uv add "pygraphile[mariadb]"
```

---

## Quick Start

### ASGI — FastAPI / Uvicorn

Use `get_asgi_app()` to get an ASGI-compatible app and mount it into FastAPI or any ASGI server.

**SQLite**

```python
from pygraphile import PyGraphile
from fastapi import FastAPI
import uvicorn

app = FastAPI()

pg = PyGraphile('mydb.sqlite', db_type='sqlite', debug=True)
app.mount('/graphql', pg.get_asgi_app())

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
```

**MariaDB / MySQL**

```python
from pygraphile import PyGraphile
from fastapi import FastAPI
import uvicorn

app = FastAPI()

md = PyGraphile(
    'mariadb://user:password@127.0.0.1:3306/mydb',
    db_type='mariadb',  # or 'mysql'
    debug=True,
)
app.mount('/graphql', md.get_asgi_app())

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
```

---

### WSGI — Gunicorn

Use `get_wsgi_app()` to get a WSGI-compatible app and serve it with Gunicorn or any WSGI server.

**MariaDB / MySQL**

```python
# app.py
# pip install "pygraphile[mariadb]" gunicorn
from pygraphile import PyGraphile

pg = PyGraphile(
    'mariadb://user:password@127.0.0.1:3306/mydb',
    db_type='mariadb',
    debug=True,
)
application = pg.get_wsgi_app()
```

```bash
gunicorn app:application
```

**SQLite**

```python
# app.py
# pip install pygraphile gunicorn
from pygraphile import PyGraphile

pg = PyGraphile('mydb.sqlite', db_type='sqlite', debug=True)
application = pg.get_wsgi_app()
```

```bash
gunicorn app:application
```

---

## API Reference

### `PyGraphile(db_name, db_type, migration_folder, debug)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `db_name` | `str` | `'pygraphile.sqlite'` | SQLite file path, or MariaDB/MySQL connection URI |
| `db_type` | `str` | `'sqlite'` | `'sqlite'`, `'sqlite3'`, `'mariadb'`, or `'mysql'` |
| `migration_folder` | `str` | `'nomigration'` | Reserved for future migration support |
| `debug` | `bool` | `False` | Enables Apollo Explorer and verbose logging |

### `pg.get_asgi_app()`

Returns an ASGI-compatible [Ariadne](https://ariadne.readthedocs.io/) `GraphQL` app. Mount into FastAPI, Starlette, or serve with Uvicorn/Hypercorn.

```python
app.mount('/graphql', pg.get_asgi_app())
```

### `pg.get_wsgi_app()`

Returns a WSGI-compatible [Ariadne](https://ariadne.readthedocs.io/) `GraphQL` app. Serve with Gunicorn or any WSGI-compatible server.

```python
# app.py
application = pg.get_wsgi_app()
# gunicorn app:application
```

### `pg.get_query_app(app_type='asgi')`

Convenience method that delegates to `get_asgi_app()` or `get_wsgi_app()`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `app_type` | `str` | `'asgi'` | `'asgi'` returns an ASGI app; `'wsgi'` returns a WSGI app |

```python
pg.get_query_app()           # ASGI (default)
pg.get_query_app('wsgi')     # WSGI
```

---

## Database Support

| Database | Status | Install |
|---|---|---|
| SQLite | ✅ Supported | `pip install pygraphile` |
| MariaDB | ✅ Supported | `pip install "pygraphile[mariadb]"` |
| MySQL | ✅ Supported | `pip install "pygraphile[mysql]"` |
| PostgreSQL | 🔜 Roadmap | — |

Connection URI format for MariaDB/MySQL:

```
mariadb://user:password@host:port/database
mysql://user:password@host:port/database
```

---

## Identifier Sanitization

Table and column names with spaces or special characters are automatically converted to valid GraphQL identifiers.

```python
from pygraphile import sanitize_field_name, sanitize_type_name

sanitize_field_name("full name")          # → "full_name"
sanitize_field_name("tabapi request log") # → "tabapi_request_log"
sanitize_type_name("tabapi request log")  # → "TabapiRequestLog"
sanitize_type_name("order-items")         # → "OrderItems"
```

- Field names (query fields, object fields): spaces and special characters → underscores
- Type names (GraphQL object types): converted to PascalCase

---

## Roadmap

- [x] SQLite schema introspection and query resolvers
- [x] GraphQL schema generation
- [x] MariaDB & MySQL support
- [x] Identifier sanitization (spaces & special characters)
- [x] WSGI support (`get_wsgi_app()`)
- [ ] Mutation support (INSERT / UPDATE / DELETE)
- [ ] PostgreSQL support
- [ ] Filtering & pagination
- [ ] Authentication & authorization
- [ ] Plugin system
