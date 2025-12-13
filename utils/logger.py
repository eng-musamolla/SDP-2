import logging
import os
from datetime import datetime
from config.settings import LOGGING_CONFIG

class Logger:
    """Enhanced logging system for the application"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(LOGGING_CONFIG['file'])
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, LOGGING_CONFIG['level']),
            format=LOGGING_CONFIG['format'],
            handlers=[
                logging.FileHandler(LOGGING_CONFIG['file']),
                logging.StreamHandler()  # Console output
            ]
        )
    
    def log_user_action(self, user_id, action, details=None):
        """Log user actions for audit trail"""
        logger = logging.getLogger('audit')
        message = f"User {user_id}: {action}"
        if details:
            message += f" - {details}"
        logger.info(message)
    
    def log_database_operation(self, operation, table, record_id=None):
        """Log database operations"""
        logger = logging.getLogger('database')
        message = f"Database {operation} on {table}"
        if record_id:
            message += f" (ID: {record_id})"
        logger.info(message)

# Global logger instance
app_logger = Logger()