"""
Simple database connection helper
"""
import mysql.connector
from Conf.config import DB_CONFIG


def get_connection(database=None):
    """Get MySQL connection"""
    config = {
        'host': DB_CONFIG['host'],
        'user': DB_CONFIG['user'],
        'password': DB_CONFIG['password'],
        'autocommit': True
    }
    if database:
        config['database'] = database

    return mysql.connector.connect(**config)


def close_connection(conn):
    """Close connection"""
    if conn:
        conn.close()
