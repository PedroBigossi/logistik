"""
Main Flask application file.
Initializes the app, database, and registers blueprints.
"""

from flask import Flask, redirect
from flask_login import LoginManager
from config import Config
from models import db, User

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


# Register blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')


@app.route('/')
def index():
    """Redirect to dashboard based on user role."""
    from flask_login import current_user
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect('/admin/dashboard')
        else:
            return redirect('/user/dashboard')
    return redirect('/auth/login')


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

