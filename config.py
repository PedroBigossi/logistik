"""
Configuration file for the Flask application.
Contains database settings and secret key configuration.
"""

import os

class Config:
    """Base configuration class."""
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///logistik.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

