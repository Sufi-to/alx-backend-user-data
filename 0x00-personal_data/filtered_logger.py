#!/usr/bin/env python3
"""Module for filtering data and logging"""

import re


def filter_datum(fields: list[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated:"""
    pattern = r"|".join([f"(?<={field}=)[^{separator}]+" for field in fields])
    return re.sub(pattern, redaction, message)
