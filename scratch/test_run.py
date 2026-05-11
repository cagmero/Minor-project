
import os
import sys

# Add root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)

# Add scratch to path if needed
sys.path.append(os.path.join(root_dir, 'scratch'))

# Import mock BEFORE the app imports anything
import mock_db

# Mock dotenv to avoid needing .env for this test
from unittest.mock import patch
with patch('dotenv.load_dotenv'):
    try:
        import app as app_module
        app = app_module.app
        print("Successfully imported app.py")
    except Exception as e:
        print(f"Failed to import app.py: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Check if we can start the test client
client = app.test_client()
try:
    # Need to set a secret key if it's missing in mocked env
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'test-secret'
        
    response = client.get('/')
    print(f"GET / response code: {response.status_code}")
    if response.status_code in [200, 302]:
        print("Basic routing test passed.")
    else:
        print(f"Basic routing test failed with status {response.status_code}")
except Exception as e:
    print(f"Failed to run basic routing test: {e}")
    import traceback
    traceback.print_exc()

print("Test run complete.")
