import sqlite3
from pathlib import Path

from sqlite_read_server import server as srv


def test_list_tables(tmp_path: Path, monkeypatch):
    # Create a test database
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("CREATE TABLE products (id INTEGER, title TEXT)")
    conn.close()
    
    # Set the database path
    monkeypatch.setattr(srv, "_database_path", str(db_path))
    
    result = srv.list_tables()
    assert isinstance(result, list)
    assert "users" in result
    assert "products" in result


def test_read_rows(tmp_path: Path, monkeypatch):
    # Create a test database
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.execute("INSERT INTO users VALUES (2, 'Bob')")
    conn.close()
    
    # Set the database path
    monkeypatch.setattr(srv, "_database_path", str(db_path))
    
    result = srv.read_rows("users")
    # Should be a dict with data
    assert isinstance(result, dict)
    assert "rows" in result or "data" in result or isinstance(result, str)
