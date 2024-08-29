#!/usr/bin/env python3
"""Module for hashing the database"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed passoword"""
    return bcrypt.hashpw(password, bcrypt.gensalt())
