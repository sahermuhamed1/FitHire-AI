import os
import tempfile
import pytest
from app import create_app
from app.utils.db_utils import init_db, get_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Create the database and load test data
    with app.app_context():
        init_db()
    
    yield app

    # Clean up the temporary file
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
