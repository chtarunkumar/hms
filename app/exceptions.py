# app/exceptions.py

from flask import jsonify, request # <--- ADD 'request' here
import logging

logger = logging.getLogger(__name__)

class PatientNotFound(Exception):
    """Custom exception for when a patient is not found."""
    def __init__(self, message="Patient not found", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InvalidInput(Exception):
    """Custom exception for invalid input data."""
    def __init__(self, message="Invalid input data", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class EmailSendError(Exception):
    """Custom exception for email sending failures."""
    def __init__(self, message="Failed to send email", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def register_error_handlers(app):
    """Registers custom error handlers with the Flask application."""

    @app.errorhandler(PatientNotFound)
    def handle_patient_not_found(error):
        logger.warning(f"PatientNotFound: {error.message}", exc_info=True)
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    @app.errorhandler(InvalidInput)
    def handle_invalid_input(error):
        logger.warning(f"InvalidInput: {error.message}", exc_info=True)
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    @app.errorhandler(EmailSendError)
    def handle_email_send_error(error):
        logger.error(f"EmailSendError: {error.message}", exc_info=True)
        response = jsonify({"error": error.message})
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found_error(error):
        # 'request' is now imported and available
        logger.warning(f"404 Not Found: {request.path}", exc_info=True)
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {error}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

    # Catch all other unhandled exceptions
    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        logger.error(f"An unexpected error occurred: {error}", exc_info=True)
        response = jsonify({"error": "An unexpected error occurred"})
        response.status_code = 500
        return response