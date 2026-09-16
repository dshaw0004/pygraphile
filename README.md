# PyGraphile

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/pygraphile.svg)](https://pypi.org/project/pygraphile/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library inspired by [PostGraphile](https://www.graphile.org/postgraphile/) — automatically generates GraphQL APIs from your database schema.

Point PyGraphile at a SQLite file or a MariaDB/MySQL database, and get a fully working, ASGI-compatible GraphQL API. No schema writing, no manual resolvers.

## 🚧 Project Status

**v0.6.2** — Early access. Core query API is working for SQLite, MariaDB, and MySQL. Mutations, filtering, and PostgreSQL are on the roadmap.

## ✨ Features

- 🔍 **Schema introspection** — Automatically reads tables, columns, and types from your database
- ⚡ **Instant GraphQL** — Generates a complete, executable GraphQL schema with resolvers on the fly
- 🗄️ **Multi-database support** — SQLite, MariaDB, and MySQL supported today
- 🔤 **Identifier sanitization** — Table and column names with spaces or special characters are automatically converted to valid GraphQL names (e.g. `"full name"` → `full_name`, `"tabapi request log"` → `TabapiRequestLog`)
- 🔌 **ASGI native** — Returns a standard ASGI app you can mount into FastAPI, Starlette, or any ASGI framework
- 🐍 **Pure Python** — Supports Python 3.9 through 3.13+

## 🚀 Installation

### SQLite (no extra dependencies)

```bash
pip install pygraphile
```

### MariaDB / MySQL

```bash
pip install "pygraphile[mariadb]"
# or for mysql alias:
pip install "pygraphile[mysql]"
```

### Using uv

```bash
uv add pygraphile              # SQLite only
uv add "pygraphile[mariadb]"   # with MariaDB/MySQL support
```

### From source

```bash
git clone https://github.com/dshaw0004/pygraphile.git
cd pygraphile
uv pip install -e .
```

## 📖 Quick Start

### SQLite

```python
from pygraphile import PyGraphile
from fastapi import FastAPI
import uvicorn

app = FastAPI()

pg = PyGraphile('mydb.sqlite', db_type='sqlite', debug=True)
app.mount('/graphql', pg.get_query_app())

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
```

### MariaDB / MySQL

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
app.mount('/graphql', md.get_query_app())

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
```

### What gets generated

Given a table named `"tabapi request log"` with columns `id INT` and `full name VARCHAR`:

```graphql
# Table and column names with spaces are sanitized automatically
type TabapiRequestLog {
  id: Int
  full_name: String
}

type Query {
  tabapi_request_log: [TabapiRequestLog]
}
```

Query it:

```bash
curl -X POST http://localhost:8000/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query":"{ tabapi_request_log { id full_name } }"}'
```

With `debug=True`, an Apollo GraphQL Explorer is also available at `/graphql`.

## ⚙️ API Reference

### `PyGraphile(db_name, db_type, migration_folder, debug)`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `db_name` | `str` | `'pygraphile.sqlite'` | SQLite file path, or MariaDB/MySQL connection URI |
| `db_type` | `str` | `'sqlite'` | `'sqlite'`, `'sqlite3'`, `'mariadb'`, or `'mysql'` |
| `migration_folder` | `str` | `'nomigration'` | Reserved for future migration support |
| `debug` | `bool` | `False` | Enables Apollo Explorer and verbose logging |

### `pg.get_query_app()`

Returns an ASGI-compatible [Ariadne](https://ariadne.readthedocs.io/) `GraphQL` app ready to be mounted.

### Utility functions

```python
from pygraphile import sanitize_field_name, sanitize_type_name

sanitize_field_name("full name")        # → "full_name"
sanitize_field_name("tabapi request log") # → "tabapi_request_log"
sanitize_type_name("tabapi request log")  # → "TabapiRequestLog"
sanitize_type_name("order-items")         # → "OrderItems"
```

## 🗺️ Roadmap

- [x] Project setup and structure
- [x] SQLite schema introspection and query resolvers
- [x] GraphQL schema generation
- [x] MariaDB & MySQL support
- [x] Identifier sanitization (spaces & special characters in table/column names)
- [ ] Mutation support (INSERT / UPDATE / DELETE)
- [ ] PostgreSQL support
- [ ] Filtering & pagination
- [ ] Authentication & authorization
- [ ] Plugin system

## 🤝 Contributing

Contributions are welcome! This project is in early stages, so there's plenty of opportunity to shape its direction.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [PostGraphile](https://www.graphile.org/postgraphile/) — An amazing tool for PostgreSQL
- Built with [Ariadne](https://ariadne.readthedocs.io/) for GraphQL execution
- Tooling powered by [uv](https://github.com/astral-sh/uv)

## 📬 Contact

- GitHub: [@dshaw0004](https://github.com/dshaw0004)
- Project: [https://github.com/dshaw0004/pygraphile](https://github.com/dshaw0004/pygraphile)

---

**Note**: This project is under active development. APIs and features are subject to change.
