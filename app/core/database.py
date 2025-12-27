import sqlite3
from contextlib import contextmanager
from typing import Generator, Optional

from app.core.config import settings
from app.core.logger import logger, log_error, log_database_operation


class DatabaseManager:
    """Manages SQLite database connections"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.db_path_str
        self._validate_database()
    
    def _validate_database(self):
        if not settings.validate_database():
            error_msg = f"Database not found at: {self.db_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        logger.info(f"Database validated at: {self.db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.db_path)
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            # Return rows as dictionaries
            conn.row_factory = sqlite3.Row
            log_database_operation("Connection created")
            return conn
        except Exception as e:
            log_error(e, "Failed to create database connection")
            raise
    
    @contextmanager
    def get_session(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
            log_database_operation("Session committed")
        except Exception as e:
            conn.rollback()
            log_error(e, "Session rollback")
            raise
        finally:
            conn.close()
            log_database_operation("Connection closed")
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        with self.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            log_database_operation(f"Query executed", f"Returned {len(results)} rows")
            return results
    
    def execute_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        with self.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            log_database_operation(f"Query executed", f"Returned single row")
            return result
    
    def test_connection(self) -> bool:
        try:
            with self.get_session() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            log_error(e, "Database connection test failed")
            return False


db_manager = DatabaseManager()


def get_db() -> DatabaseManager:
    return db_manager


def get_db_connection() -> sqlite3.Connection:
    return db_manager.get_connection()
