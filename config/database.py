from psycopg2 import connect

from config.conf import settings
from services.exceptions.database import UnableToConnectError


def create_query(sql: str = None) -> None:
    """Execute SQL query for creating, updating or deleting data"""
    if sql:
        connection = connect(
            database=settings.PG_NAME,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(sql)
        connection.commit()
        connection.close()
    else:
        raise UnableToConnectError(
            "Couldn't connect to database. Are you sure credentials are correct?"
        )


def read_query(sql: str = None) -> list:
    """Execute SQL query for reading data"""
    results = list()
    if sql:
        connection = connect(
            database=settings.PG_NAME,
            user=settings.PG_USER,
            password=settings.PG_PASSWORD,
            host=settings.PG_HOST,
            port=settings.PG_PORT,
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(sql)

        results = cursor.fetchall()
        connection.close()
    else:
        raise UnableToConnectError(
            "Couldn't connect to database. Are you sure credentials are correct?"
        )
    return results
