"""Basic tests for the pygraphile package."""

import pygraphile


def test_version():
    """Test that version is defined."""
    assert hasattr(pygraphile, "__version__")
    assert isinstance(pygraphile.__version__, str)
    assert pygraphile.__version__ == "0.7.0"


def test_module_imports():
    """Test that the module can be imported."""
    assert pygraphile is not None
    assert pygraphile.__author__ == "dshaw0004"


def test_asgi_and_wsgi_apps(tmp_path):
    """Test that get_asgi_app and get_wsgi_app return valid Ariadne apps."""
    from ariadne.asgi.graphql import GraphQL as AsgiGraphQL
    from ariadne.wsgi import GraphQL as WsgiGraphQL

    db_path = str(tmp_path / "test.sqlite")
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);")
    conn.commit()
    conn.close()

    pg = pygraphile.PyGraphile(db_path, db_type="sqlite")
    asgi_app = pg.get_asgi_app()
    wsgi_app = pg.get_wsgi_app()

    assert isinstance(asgi_app, AsgiGraphQL)
    assert isinstance(wsgi_app, WsgiGraphQL)

