
import sys
from unittest.mock import MagicMock

# Mock flask_mysqldb
class MockMySQL:
    def __init__(self, app=None):
        self.app = app
        self.connection = MagicMock()
        if app:
            self.init_app(app)
            
    def init_app(self, app):
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['mysql'] = self

# Mock the module
mock_flask_mysqldb = MagicMock()
mock_flask_mysqldb.MySQL = MockMySQL
sys.modules['flask_mysqldb'] = mock_flask_mysqldb

# Mock MySQLdb
mock_mysqldb = MagicMock()
sys.modules['MySQLdb'] = mock_mysqldb
sys.modules['MySQLdb.cursors'] = mock_mysqldb.cursors
