# PyGraphile

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library inspired by [PostGraphile](https://www.graphile.org/postgraphile/) - automatically generates GraphQL APIs from your database schema.

## 🚧 Project Status

This project is in early development. Currently supporting SQLite with plans to add support for PostgreSQL, MySQL, and other databases in the future.

## ✨ Features

- 🗄️ **Database Introspection**: Automatically analyzes your database schema
- 🔄 **GraphQL API Generation**: Creates a GraphQL API based on your database structure
- 🎯 **SQLite Support**: Initial support for SQLite databases (more databases coming soon)
- 🐍 **Python Native**: Built for Python with modern best practices
- 📦 **Easy to Use**: Simple setup and configuration

## 🚀 Installation

### Using pip

```bash
pip install pygraphile
```

### Using uv

```bash
uv pip install pygraphile
```

### From source

```bash
git clone https://github.com/dshaw0004/pygraphile.git
cd pygraphile
uv pip install -e .
```

## 📖 Quick Start

```python
from pygraphile import Pygraphile

# Coming soon! Basic usage example will be:
# api = Pygraphile('path/to/database.db')
# api.serve()
```

## 🗺️ Roadmap

- [x] Project setup and structure
- [x] SQLite schema introspection
- [x] GraphQL schema generation
- [x] Query resolver implementation
- [ ] Mutation support
- [ ] PostgreSQL support
- [ ] MySQL support
- [ ] Advanced filtering and pagination
- [ ] Authentication and authorization
- [ ] Plugin system

## 🤝 Contributing

Contributions are welcome! This project is in early stages, so there's plenty of opportunity to shape its direction.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [PostGraphile](https://www.graphile.org/postgraphile/) - An amazing tool for PostgreSQL
- Built with modern Python tooling including [uv](https://github.com/astral-sh/uv)

## 📬 Contact

- GitHub: [@dshaw0004](https://github.com/dshaw0004)
- Project Link: [https://github.com/dshaw0004/pygraphile](https://github.com/dshaw0004/pygraphile)

---

**Note**: This project is under active development. APIs and features are subject to change.
