import os
import sys
import pytest
from fastapi.testclient import TestClient
from fastapi import status

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ChatApp.main import app, session_store
from ChatApp.models.request_models import Session



client = TestClient(app)

def test_is_session_valid_with_existing_session():
    """Test that is_session_valid returns True for an existing session."""
    # Setup - create a test session
    session = Session(session_id=1001, session_user="test_user")
    session_store.session_store = [session]
    
    # Test
    assert session_store.is_session_valid(1001) is True

def test_is_session_valid_with_nonexistent_session():
    """Test that is_session_valid returns False for a non-existent session."""
    # Setup - ensure the session store is empty
    session_store.session_store = []
    
    # Test
    assert session_store.is_session_valid(9999) is False

def test_create_session_success():
    """Test successful creation of a new session."""
    # Setup - clear any existing sessions
    session_store.session_store = []
    
    # Test data
    session_data = {"session_user": "test_user"}
    
    # Make request
    response = client.post("/sessions", json=session_data)
    
    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "session_id" in response_data
    assert response_data["session_user"] == "test_user"
    assert "created_at" in response_data
    
    # Verify session was stored
    assert len(session_store.session_store) == 1
    assert session_store.session_store[0].session_user == "test_user"

def test_create_session_missing_required_field():
    """Test that creating a session without required fields fails."""
    # Test data - missing session_user
    invalid_data = {}
    
    # Make request
    response = client.post("/sessions", json=invalid_data)
    
    # Assertions
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "session_user" in response.text.lower()

def test_get_session_success():
    """Test successfully retrieving an existing session."""
    # Setup - create a test session
    session = Session(session_id=1001, session_user="test_user")
    session_store.session_store = [session]
    
    # Make request
    response = client.get("/sessions/1001")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["session_id"] == 1001
    assert response_data["session_user"] == "test_user"

def test_get_nonexistent_session():
    """Test retrieving a non-existent session returns 404."""
    # Setup - ensure the session store is empty
    session_store.session_store = []
    
    # Make request with non-existent session ID
    response = client.get("/sessions/9999")
    
    # Assertions
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.text.lower()

def test_get_session_with_invalid_id():
    """Test that getting a session with an invalid ID returns 422."""
    # Make request with invalid session ID (less than 1000)
    response = client.get("/sessions/999")
    
    # Assertions
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "greater than or equal to 1000" in response.text

# Cleanup after tests
@pytest.fixture(autouse=True)
def cleanup():
    """Fixture to clean up the session store before and after each test."""
    # Setup - clear any existing sessions
    session_store.session_store = []
    yield  # This is where the test runs
    # Teardown - clean up after test
    session_store.session_store = []
