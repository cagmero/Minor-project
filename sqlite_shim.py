
import sqlite3
import os

class SQLiteCursor:
    def __init__(self, sqlite_cursor):
        self.cursor = sqlite_cursor
        self._last_row_id = None
        self._row_count = -1

    def execute(self, query, params=None):
        # Convert MySQL placeholders (%) to SQLite placeholders (?)
        query = query.replace('%s', '?')
        
        # Handle some basic MySQL vs SQLite syntax differences if needed
        # (Most simple queries are compatible)
        
        if params:
            # Handle single params passed as non-tuple
            if not isinstance(params, (list, tuple, dict)):
                params = (params,)
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
            
        self._last_row_id = self.cursor.lastrowid
        self._row_count = self.cursor.rowcount
        return self.cursor

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    @property
    def lastrowid(self):
        return self._last_row_id

    @property
    def rowcount(self):
        return self._row_count

    def close(self):
        self.cursor.close()

class SQLiteConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        # Enable dictionary-like access
        self._conn.row_factory = self._dict_factory

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def cursor(self, cursor_type=None):
        # We ignore cursor_type because we always use dict_factory for SQLite
        return SQLiteCursor(self._conn.cursor())

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

class MySQL:
    def __init__(self, app=None):
        self.db_path = 'test_wise.db'
        self.connection = SQLiteConnection(self.db_path)
        if app:
            self.init_app(app)

    def init_app(self, app):
        # This is a dummy for Flask-MySQLdb compatibility
        pass

# Mocking MySQLdb constants for imports in the app
class MockMySQLdb:
    class cursors:
        DictCursor = "DictCursor"

import sys
sys.modules['MySQLdb'] = MockMySQLdb
sys.modules['MySQLdb.cursors'] = MockMySQLdb.cursors

# Mock dotenv to avoid errors if .env is missing
class MockDotenv:
    def load_dotenv(*args, **kwargs):
        pass
    def find_dotenv(*args, **kwargs):
        return None
sys.modules['dotenv'] = MockDotenv

# Provide default environment variables if they are missing
import os
if not os.environ.get("APP_SECRET_KEY"):
    os.environ["APP_SECRET_KEY"] = "presentation-secret-key"
if not os.environ.get("HOST"):
    os.environ["HOST"] = "localhost"
if not os.environ.get("MYSQL_USER"):
    os.environ["MYSQL_USER"] = "root"
if not os.environ.get("MYSQL_DB"):
    os.environ["MYSQL_DB"] = "test_wise"
