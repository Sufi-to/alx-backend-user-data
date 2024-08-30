#!/usr/bin/env python3
"""Module for filtering data and logging"""

import logging
import mysql.connector
import os
import re
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
    logger = logging.getLogger('user_data')
    handle = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handle.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handle)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    """
    return mysql.connector.connection.MYSQLConnection(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    """Obtains the db connection and display the rows in a filtered format"""
    logger = get_logger()
    db_con = get_db()
    rows = db_con.cursor().execute("Select * from user").fetchall()
    for line in rows:
        msg = (
            "name={}; email={}; phone={}; ssn={}; "
            "password={}; ip={}; last_login={}; user_agent={};"
        ).format(
            line[0], line[1], line[2], line[3], line[4],
            line[5], line[6], line[7])
        logger.info(msg)
    db_con.cursor().close()
    db_con.close()


if __name__ == '__main__':
    main()
