#!/usr/bin/env python3
"""Module for templating a session authentication system for the api"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Class the implements authenticating with sessions"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Returns session id based on the user_id"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user_id based on session id"""
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns current user based on the session id"""
        if request is None:
            return None
        session_name = self.session_cookie(request)
        if session_name:
            user_id = self.user_id_for_session_id(session_name)
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """Logs out the user by destroying the session"""
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if user_id:
            del self.user_id_by_session_id[sess_id]
            return True
        return False
