#!/usr/bin/env python3
"""Module for hashing the database"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed passoword"""
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Returns a boolean that validates the password"""
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
