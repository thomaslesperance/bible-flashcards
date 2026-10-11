import sqlite3
import os
from contextlib import contextmanager
from typing import List, Dict, Any, Optional

# Compute the path to data/bible.db relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'bible.db')

@contextmanager
def get_db_connection():
    """Provides a context manager for a SQLite database connection."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # Enable accessing columns by name
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def execute(query: str, params: tuple = ()) -> int:
    """Executes a query (INSERT, UPDATE, DELETE) and returns the row count."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount

# CREATE ----------------------

def insert(table: str, data: Dict[str, Any]) -> int:
    """Inserts a new record into the specified table and returns the last inserted ID."""
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return cursor.lastrowid

# READ ----------------------

def fetch_one(query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
    """Executes a SELECT query and returns the first result."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

# UPDATE ----------------------

def update(table: str, data: Dict[str, Any], where_clause: str, where_params: tuple = ()) -> int:
    """Updates records in the specified table and returns the number of affected rows."""
    set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    
    params = tuple(data.values()) + where_params
    return execute(query, params)

# DELETE ----------------------

def delete(table: str, where_clause: str, where_params: tuple = ()) -> int:
    """Deletes records from the specified table and returns the number of affected rows."""
    query = f"DELETE FROM {table} WHERE {where_clause}"
    return execute(query, where_params)

# LIST ----------------------

def fetch_all(query: str, params: tuple = ()) -> List[sqlite3.Row]:
    """Executes a SELECT query and returns all results."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
