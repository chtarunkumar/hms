# app/logger.py

import logging
import os
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler # Import RotatingFileHandler

def setup_logging(app):
    """
    Sets up structured logging for the Flask application.
    Logs to a file and optionally to console.
    """
    log_file_path = os.path.join(app.root_path, '..', 'hms.log') # Log file in the root hms/ directory
    
    # --- IMPORTANT CHANGE HERE ---
    # Get log_level from app.config which was loaded from config.py
    log_level = app.config.get('LOG_LEVEL', 'INFO').upper()
    # --- END IMPORTANT CHANGE ---

    # Ensure the log directory exists if it's not the root
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Remove default Flask handlers
    for handler in list(app.logger.handlers): # Iterate over a copy to avoid modification issues
        app.logger.removeHandler(handler)
    for handler in list(logging.root.handlers): # Iterate over a copy
        logging.root.removeHandler(handler)

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # JSON Formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d %(message)s'
    )

    # File Handler
    file_handler = RotatingFileHandler( # Use the imported RotatingFileHandler
        log_file_path, maxBytes=10485760, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler (optional, for development)
    if os.getenv('FLASK_ENV', 'development') == 'development':
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Set Flask's default logger to use our configured logger
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    app.logger.propagate = False # Prevent messages from being passed to the root logger

    # Also configure the root logger to use our setup
    # This ensures other modules that get their own loggers also respect the level
    logging.basicConfig(handlers=[file_handler], level=log_level)
    if os.getenv('FLASK_ENV', 'development') == 'development':
        logging.getLogger().addHandler(console_handler)

    app.logger.info(f"Logging configured to {log_file_path} with level {log_level}")

    return logger