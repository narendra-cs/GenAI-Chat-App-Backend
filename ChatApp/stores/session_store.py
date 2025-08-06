from ..models.request_models import Session


class SessionStore:
    def __init__(self):
        self.session_store: list[Session] = []

    def is_session_valid(self, session_id: int):
        session = [
            session
            for session in self.session_store
            if session.session_id == session_id
        ]
        return len(session) > 0

    def get_session(self, session_id: int):
        session = [
            session
            for session in self.session_store
            if session.session_id == session_id
        ]
        return session[0]

    def get_all_sessions(self):
        return self.session_store

    def get_first_session(self):
        return self.session_store[0]

    def delete_session(self, session_id: int):
        self.session_store = [
            session
            for session in self.session_store
            if session.session_id != session_id
        ]
        return True

    def add_session(self, session: Session):
        self.session_store.append(session)
        return True

    def clean(self):
        self.session_store = []
        return True

    def get_session_count(self):
        return len(self.session_store)
