import os
import sys
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from typing import List, Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ChatApp.main import app, session_store, chat_store
from ChatApp.models.request_models import Session, Role, Message

client = TestClient(app)


# Fixtures
@pytest.fixture(autouse=True)
def cleanup():
    """Fixture to clean up the session and chat stores before and after each test."""
    # Setup: clear all data before test
    session_store.clean()
    chat_store.clear()

    # Create a test session
    session = Session(session_id=1001, session_user="test_user")
    session_store.add_session(session)

    yield session.session_id  # this is where the testing happens

    # Teardown: clear all data after test
    session_store.clean()
    chat_store.clear()


@pytest.fixture
def test_session(cleanup) -> int:
    """Fixture to get the test session ID."""
    return cleanup


# Helper functions
def create_test_message(role: Role, content: str = "Test message") -> Dict[str, Any]:
    """Helper to create a test message dictionary."""
    return {"role": role.value, "content": content}


def add_test_messages(test_session: int, messages: List[Dict[str, Any]]) -> None:
    """Helper to add multiple test messages to a session."""
    for msg in messages:
        response = client.post(f"/sessions/{test_session}/messages", json=msg)
        assert response.status_code == status.HTTP_201_CREATED, response.json()


def create_large_message(role: Role, size_kb: int = 4) -> Dict[str, Any]:
    """Create a large message of approximately size_kb KB."""
    content = "x" * (size_kb * 1024)  # Roughly size_kb KB of content
    return create_test_message(role, content)


# Test cases for GET /sessions/{session_id}/messages
def test_get_messages_success(test_session):
    """Test successfully retrieving all messages for a session."""
    # Setup: Add test messages
    test_messages = [
        create_test_message(Role.USER, "Hello"),
        create_test_message(Role.ASSISTANT, "Hi there!"),
        create_test_message(Role.USER, "How are you?"),
    ]
    add_test_messages(test_session, test_messages)

    # Test
    response = client.get(f"/sessions/{test_session}/messages")

    # Assertions
    assert response.status_code == status.HTTP_200_OK
    messages = response.json()
    assert len(messages) == 3
    for i, msg in enumerate(test_messages):
        assert messages[i]["role"] == msg["role"]
        assert messages[i]["content"] == msg["content"]


def test_get_messages_filtered_by_role(test_session: int):
    """Test retrieving messages filtered by role."""
    # Setup: Add test messages
    test_messages = [
        create_test_message(Role.USER, "User message 1"),
        create_test_message(Role.ASSISTANT, "Assistant message 1"),
        create_test_message(Role.USER, "User message 2"),
    ]
    add_test_messages(test_session, test_messages)

    # Test: Filter by user role
    response = client.get(f"/sessions/{test_session}/messages?role=user")
    assert response.status_code == status.HTTP_200_OK
    user_messages = response.json()
    assert len(user_messages) == 2
    assert all(msg["role"] == "user" for msg in user_messages)

    # Test: Filter by assistant role
    response = client.get(f"/sessions/{test_session}/messages?role=assistant")
    assert response.status_code == status.HTTP_200_OK
    assistant_messages = response.json()
    assert len(assistant_messages) == 1
    assert all(msg["role"] == "assistant" for msg in assistant_messages)


# Test cases for POST /sessions/{session_id}/messages
def test_add_message_success(test_session: int):
    """Test successfully adding a new message to a session."""
    # Test data
    message_data = create_test_message(Role.USER, "Hello, world!")

    # Test
    response = client.post(f"/sessions/{test_session}/messages", json=message_data)

    # Assertions
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the message was added to the chat store
    response = client.get(f"/sessions/{test_session}/messages")
    messages = response.json()
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello, world!"


def test_add_multiple_messages_in_sequence(test_session: int):
    """Test adding multiple messages in sequence preserves order."""
    messages = [
        create_test_message(Role.USER, "First message"),
        create_test_message(Role.ASSISTANT, "Second message"),
        create_test_message(Role.USER, "Third message"),
    ]

    # Add messages in sequence
    for msg in messages:
        response = client.post(f"/sessions/{test_session}/messages", json=msg)
        assert response.status_code == status.HTTP_201_CREATED

    # Verify order is preserved
    response = client.get(f"/sessions/{test_session}/messages")
    stored_messages = response.json()
    assert len(stored_messages) == 3
    for i, msg in enumerate(messages):
        assert stored_messages[i]["content"] == msg["content"]
        assert stored_messages[i]["role"] == msg["role"]


def test_add_message_with_special_characters(test_session: int):
    """Test adding messages with special characters and emojis."""
    test_cases = [
        ("Hello, world! 😊", "Emoji test"),
        ("Special chars: !@#$%^&*()", "Special characters"),
        ("Multiline\nstring\ntest", "Multiline string"),
        ("   Trim test   ", "Whitespace test"),
    ]

    for content, description in test_cases:
        message_data = create_test_message(Role.USER, content)
        response = client.post(f"/sessions/{test_session}/messages", json=message_data)
        assert (
            response.status_code == status.HTTP_201_CREATED
        ), f"Failed on: {description}"

        # Verify the message was stored correctly
        response = client.get(f"/sessions/{test_session}/messages")
        messages = response.json()
        assert any(
            msg["content"] == content.strip() for msg in messages
        ), f"Failed to verify: {description}"


def test_add_large_message(test_session: int):
    """Test adding a large message (4KB)."""
    large_message = create_large_message(Role.USER, size_kb=4)
    response = client.post(f"/sessions/{test_session}/messages", json=large_message)
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the message was stored correctly
    response = client.get(f"/sessions/{test_session}/messages")
    messages = response.json()
    assert len(messages) == 1
    assert len(messages[0]["content"]) == len(large_message["content"])


# Error test cases
def test_add_message_nonexistent_session():
    """Test adding a message to a non-existent session."""
    message_data = create_test_message(Role.USER, "This should fail")
    response = client.post("/sessions/9999/messages", json=message_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Session not found"


def test_add_message_invalid_role(test_session: int):
    """Test adding a message with an invalid role."""
    # Test with invalid role
    message_data = {"role": "invalid_role", "content": "This should fail"}
    response = client.post(f"/sessions/{test_session}/messages", json=message_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_message_missing_required_fields(test_session: int):
    """Test adding a message with missing required fields."""
    # Missing role
    response = client.post(
        f"/sessions/{test_session}/messages", json={"content": "No role"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Missing content
    response = client.post(f"/sessions/{test_session}/messages", json={"role": "user"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_message_empty_content(test_session: int):
    """Test adding a message with empty content."""
    message_data = create_test_message(Role.USER, "")
    response = client.post(f"/sessions/{test_session}/messages", json=message_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_message_invalid_session_id():
    """Test adding a message with an invalid session ID."""
    message_data = create_test_message(Role.USER, "Test message")

    # Test with string instead of number
    response = client.post("/sessions/invalid/messages", json=message_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test with ID less than 1000
    response = client.post("/sessions/999/messages", json=message_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
