from app import create_app
from app.models import db
import logging

app = create_app()
logger = logging.getLogger(__name__) # Get the logger configured in app/__init__.py

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        logger.info("Database initialized.")
    logger.info("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000) # Added host and port for clarity