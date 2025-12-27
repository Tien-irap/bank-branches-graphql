import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from app.core.config import settings


def setup_logger(
    name: str = "bank_branches_api",
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up and configure logger with both file and console handlers
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
    
    Returns:
        Configured logger instance
    """
    log_level = log_level or settings.LOG_LEVEL
    log_file = log_file or settings.LOG_FILE
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if logger.handlers:
        return logger
    
    detailed_formatter = logging.Formatter(
        settings.LOG_FORMAT,
        datefmt=settings.LOG_DATE_FORMAT
    )
    
    console_formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(message)s"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File Handler (rotating)
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Failed to create file handler: {e}")
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name:
        return logging.getLogger(name)
    return logging.getLogger("bank_branches_api")


logger = setup_logger()


def log_request(method: str, path: str, status_code: int, duration: float):
    logger.info(f"{method} {path} - {status_code} - {duration:.3f}s")


def log_error(error: Exception, context: str = ""):
    logger.error(f"{context}: {str(error)}", exc_info=True)


def log_database_operation(operation: str, details: str = ""):
    logger.debug(f"DB Operation: {operation} - {details}")


def log_graphql_query(query_name: str, variables: dict = None):
    logger.info(f"GraphQL Query: {query_name} - Variables: {variables}")
