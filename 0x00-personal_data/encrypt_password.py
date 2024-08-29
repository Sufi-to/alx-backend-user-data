#!/usr/bin/env python3
"""Module for hashing the database"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed passoword"""
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())
