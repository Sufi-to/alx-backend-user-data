#!/usr/bin/env python3
"""Module for templating authentication system for the api"""

from flask import request
from typing import List, TypeVar


class Auth:
    """template the authentication mechanism for the api"""
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns whether path is included in the excluded paths"""
        return False

    def authorization_header(self, request=None) -> str:
        """Checks the validity of a request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Checks if the user is valid"""
        return None