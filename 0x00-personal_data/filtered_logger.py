#!/usr/bin/env python3
"""Module for filtering data and logging"""

import os
import re
import mysql.connector as connector
import logging
from typing import List, Tuple


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated:"""
    pattern = r"|".join([f"(?<={field}=)[^{separator}]+" for field in fields])
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log records"""
        log = super(RedactingFormatter, self).format(record=record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a configured logger object"""
    logger = get_logger('user_data')
    handle = logging.StreamHandler()
    handle.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handle)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    """
    return connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        host=os.getenv("PERSONAL_DATA_DB_HOST"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
