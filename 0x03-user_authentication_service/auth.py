#!/usr/bin/env python3
"""Auth module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password) -> str:
    """Returns a hashed and salted password in bytes"""
    byte_password = password.encode('utf-8')
    return bcrypt.hashpw(byte_password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return a generated uuid string"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user to the database"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            hashed_pass = _hash_password(password)
            return self._db.add_user(email, hashed_pass)
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Validate the user login"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False

        user_pass = user.hashed_password
        enc_pass = password.encode('utf-8')
        if bcrypt.checkpw(enc_pass, user_pass):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Return a session of a given user"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Uses the session_id to get a User or None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session_id of a given user"""
        try:
            user = self._db.find_user_by(id=user_id)
        except Exception:
            return None
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email):
        """Update the users reset_token if available"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        new_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=new_token)
        return new_token

    def update_password(self, reset_token, password):
        """Update the user password"""
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hash_pass = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hash_pass,
                             reset_token=None)
