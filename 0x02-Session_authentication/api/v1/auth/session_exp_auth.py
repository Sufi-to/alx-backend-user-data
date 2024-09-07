#!/usr/bin/env python3
"""Module for a session with expersion time"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class the implements session with expiration"""

    def __init__(self):
        """Initialize the instance."""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a session using the parent class"""
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Returns user_id from the session dictionary"""
        if not session_id:
            return None
        all_sess = super().user_id_by_session_id
        if session_id not in all_sess:
            return None
        sess_dict = all_sess[session_id]
        if sess_dict is None:
            return None
        if self.session_duration == 0 or self.session_duration < 0:
            return sess_dict.get("user_id")

        created_at = sess_dict.get('created_at')

        if created_at is None:
            return None

        lapsed_time = created_at + timedelta(seconds=self.session_duration)

        if lapsed_time < datetime.now():
            return None

        return sess_dict.get('user_id')
