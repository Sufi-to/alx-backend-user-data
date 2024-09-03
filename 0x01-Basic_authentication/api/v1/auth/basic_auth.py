#!/usr/bin/env python3
"""Module for basicauth authentication system for the api"""

import base64
import binascii
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implements are basicauth system for authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the base64 string that is needed to be decoded"""
        if authorization_header is None or type(authorization_header) != str:
            return None
        auth_head = authorization_header.strip()
        if auth_head[0:6] != 'Basic ':
            return None
        return auth_head[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode the base64 string to utf-8 strings"""
        if base64_authorization_header is None \
                or type(base64_authorization_header) != str:
            return None

        try:
            base64_as_bytes = str.encode(base64_authorization_header)
            return base64.b64decode(base64_as_bytes).decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """Extract username and password from the decoded base64 object"""
        if decoded_base64_authorization_header is None \
                or type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        username, password = decoded_base64_authorization_header.split(":")
        return username, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Get a user instance based on his email and password"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        try:
            all_users = User.search({'email': user_email})
        except Exception:
            return None

        for i in all_users:
            if i.is_valid_password(user_pwd):
                return i
        return None
