"""
Database connection and session management
"""
import sqlite3
from contextlib import contextmanager
from typing import Generator, Optional

from app.core.config import settings
from app.core.logger import logger, log_error, log_database_operation


class DatabaseManager:
    """Manages SQLite database connections"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or settings.db_path_str
        self._validate_database()
    
    def _validate_database(self):
        """Validate that database exists and is accessible"""
        if not settings.validate_database():
            error_msg = f"Database not found at: {self.db_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        logger.info(f"Database validated at: {self.db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a database connection
        
        Returns:
            SQLite connection object
        """
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
        """
        Context manager for database sessions
        
        Yields:
            SQLite connection object
        
        Example:
            with db_manager.get_session() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM banks")
        """
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
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
        
        Returns:
            List of Row objects
        """
        with self.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            log_database_operation(f"Query executed", f"Returned {len(results)} rows")
            return results
    
    def execute_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """
        Execute a SELECT query and return single result
        
        Args:
            query: SQL query string
            params: Query parameters
        
        Returns:
            Single Row object or None
        """
        with self.get_session() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            log_database_operation(f"Query executed", f"Returned single row")
            return result
    
    def test_connection(self) -> bool:
        """
        Test database connection
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with self.get_session() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            log_error(e, "Database connection test failed")
            return False


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> DatabaseManager:
    """Get database manager instance"""
    return db_manager


def get_db_connection() -> sqlite3.Connection:
    """Get a database connection (for dependency injection)"""
    return db_manager.get_connection()
