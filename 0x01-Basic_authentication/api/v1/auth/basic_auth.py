#!/usr/bin/env python3
"""Module for basicauth authentication system for the api"""

import base64
import binascii
from api.v1.auth.auth import Auth
from typing import Tuple


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
