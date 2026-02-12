import asyncio
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
    
    result = asyncio.run(srv.list_tables())
    assert "users" in result
    assert "products" in result


def test_query_database(tmp_path: Path, monkeypatch):
    # Create a test database
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Alice')")
    conn.execute("INSERT INTO users VALUES (2, 'Bob')")
    conn.close()
    
    # Set the database path
    monkeypatch.setattr(srv, "_database_path", str(db_path))
    
    result = asyncio.run(srv.query_database("SELECT * FROM users"))
    assert "Alice" in result
    assert "Bob" in result
