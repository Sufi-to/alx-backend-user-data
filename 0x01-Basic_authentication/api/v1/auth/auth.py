#!/usr/bin/env python3
"""Module for templating authentication system for the api"""

from flask import request
from typing import List, TypeVar


class Auth:
    """template the authentication mechanism for the api"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns whether path is included in the excluded paths"""
        if path is None or (excluded_paths is None or excluded_paths == []):
            return True
        if path in excluded_paths:
            return False
        if path[-1] != '/' and path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks the validity of a request"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Checks if the user is valid"""
        return None
