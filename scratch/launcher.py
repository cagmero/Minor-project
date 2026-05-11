
import os
import sys

# Add root directory to sys.path so we can import sqlite_shim and app
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)

# 1. Load the SQLite Shim immediately to set up sys.modules mocks
import sqlite_shim

# 2. Import and run the Flask app
from app import app

if __name__ == "__main__":
    # app.py runs on port 5001 by default based on its code
    app.run(threaded=True, port=5001)
