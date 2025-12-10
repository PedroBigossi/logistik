"""
Vercel serverless function entry point for Flask application.
This file is required for Vercel to properly deploy the Flask app.
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the app to be exposed as a global variable
# The Flask app will be automatically detected by Vercel's Python runtime

