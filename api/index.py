"""
Vercel serverless function entry point for Flask application.
This file is required for Vercel to properly deploy the Flask app.
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    from flask import Flask
    import traceback
    app = Flask(__name__)
    
    @app.route('/')
    @app.route('/<path:path>')
    def error(path='/'):
        error_msg = str(e)
        error_trace = traceback.format_exc()
        return {
            'error': 'Failed to import Flask app',
            'message': error_msg,
            'traceback': error_trace
        }, 500