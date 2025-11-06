import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False