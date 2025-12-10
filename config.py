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
    # For Vercel, you MUST set DATABASE_URL environment variable
    # SQLite will NOT work on Vercel (filesystem is read-only)
    # Use PostgreSQL: postgresql://user:password@host:port/database
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Vercel provides DATABASE_URL, but might need to convert postgres:// to postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback to SQLite for local development only
        SQLALCHEMY_DATABASE_URI = 'sqlite:///logistik.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

