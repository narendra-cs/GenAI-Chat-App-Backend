from starlette import status
from fastapi import FastAPI, Path, Query, HTTPException

from app.ChatApp.request_models import Session, Message, Role


app = FastAPI()


# Session metadata store
session_store = []

# Chat history store (session_id -> list of messages)
chat_store = {}


# API endpoints for session handle
def is_session_valid(session_id: int):
    session = [session for session in session_store if session.session_id == session_id]
    return len(session) > 0


@app.get("/sessions/{session_id}", status_code=status.HTTP_200_OK)
def get_session(session_id: int = Path(min_value=1000, title="Session ID")):
    if not is_session_valid(session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    session = [session for session in session_store if session.session_id == session_id]
    return session[0]


@app.post("/sessions", status_code=status.HTTP_201_CREATED)
def create_session(session: Session):
    session.session_id = len(session_store) + 1
    session.session_user = session.session_user.strip().lower()
    session_store.append(session)
    chat_store[session.session_id] = []
    return session


# API endpoints for chat handle
@app.get("/sessions/{session_id}/messages", status_code=status.HTTP_200_OK)
def get_chat(
    session_id: int = Path(min_value=1000, title="Session ID"),
    role: Role = Query(default=None),
):
    if not is_session_valid(session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    if session_id not in chat_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    if role:
        chat_history = [
            message for message in chat_store[session_id] if message.role == role
        ]
    else:
        chat_history = chat_store[session_id]
    return chat_history


@app.post("/sessions/{session_id}/messages", status_code=status.HTTP_201_CREATED)
def add_message(
    message: Message, session_id: int = Path(min_value=1000, title="Session ID")
):
    if not is_session_valid(session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    if message.role not in (Role.USER, Role.ASSISTANT):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid message role"
        )

    if session_id not in chat_store:
        chat_store[session_id] = []
    chat_store[session_id].append(message)
