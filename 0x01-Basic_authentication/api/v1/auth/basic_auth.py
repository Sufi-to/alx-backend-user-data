#!/usr/bin/env python3
"""Module for basicauth authentication system for the api"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Implements are basicauth system for authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the base64 string that is needed to be decoded"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        auth_head = authorization_header.strip()
        if auth_head[0:6] != 'Basic ':
            return None
        return auth_head[6:]