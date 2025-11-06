# app/__init__.py

from flask import Flask
from .models import db

import logging

logging.basicConfig(
    filename='app.log',      # Log file will be created here!
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register your routes here!
    from .routes import bp
    app.register_blueprint(bp)

    from app.exceptions import register_error_handlers 
    register_error_handlers(app)

    return app