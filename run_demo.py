
import os
import sys
import subprocess

def run_demo():
    print("Setting up Presentation Mode (SQLite)...")
    
    # 1. Check if virtual environment exists
    venv_path = 'venv_test_mock'
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
    
    # 2. Install dependencies
    print("Installing dependencies...")
    pip_path = os.path.join(venv_path, 'bin', 'pip')
    subprocess.run([pip_path, 'install', 'Flask', 'python-dotenv', 'pytz', 'pyjwt', 'flask-mail', 'requests', 'xlrd', 'xlwt', 'openpyxl', 'xlsxwriter'], check=True)
    
    # 3. Run migration if DB doesn't exist
    if not os.path.exists('test_wise.db'):
        print("Migrating MySQL data to SQLite...")
        subprocess.run([os.path.join(venv_path, 'bin', 'python3'), 'migrate_to_sqlite.py'], check=True)
    else:
        print("SQLite database already exists.")

    # 4. Start the app
    print("\n" + "="*50)
    print("DEMO MODE READY")
    print("Database: SQLite (local file: test_wise.db)")
    print("App: http://127.0.0.1:5000")
    print("="*50 + "\n")
    
    # Set Flask env and run
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = 'development'
    
    try:
        subprocess.run([os.path.join(venv_path, 'bin', 'python3'), 'scratch/launcher.py'], env=env)
    except KeyboardInterrupt:
        print("\nShutting down demo...")

if __name__ == '__main__':
    run_demo()
