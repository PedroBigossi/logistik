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
    try:
        return User.query.get(int(user_id))
    except Exception:
        # If database is not available, return None
        return None


# Register blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')


@app.route('/health')
def health():
    """Health check endpoint that doesn't require database."""
    return {'status': 'ok', 'message': 'Flask app is running'}, 200


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


# Lazy database initialization - will happen on first request
# This prevents crashes during serverless cold starts
_db_initialized = False
_users_initialized = False

@app.before_request
def ensure_db_initialized():
    """Ensure database is initialized before handling requests."""
    global _db_initialized, _users_initialized
    if not _db_initialized:
        try:
            with app.app_context():
                # Create all database tables
                db.create_all()
                _db_initialized = True
        except Exception as e:
            print(f"Database initialization failed: {e}")
            _db_initialized = True
    
    # Create demo users only if database is empty (first time setup)
    # SECURITY: Use environment variables for production credentials
    if not _users_initialized and _db_initialized:
        try:
            with app.app_context():
                # Only create demo users if no users exist in the database
                user_count = User.query.count()
                if user_count == 0:
                    import os
                    
                    # Get admin credentials from environment variables or use defaults
                    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
                    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
                    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@logistik.com')
                    
                    # Get regular user credentials from environment variables or use defaults
                    user_username = os.environ.get('USER_USERNAME', 'user')
                    user_password = os.environ.get('USER_PASSWORD', 'user123')
                    user_email = os.environ.get('USER_EMAIL', 'user@logistik.com')
                    
                    # Create admin user
                    admin = User(
                        username=admin_username,
                        email=admin_email,
                        role='admin'
                    )
                    admin.set_password(admin_password)
                    db.session.add(admin)
                    
                    # Create regular user
                    user = User(
                        username=user_username,
                        email=user_email,
                        role='user'
                    )
                    user.set_password(user_password)
                    db.session.add(user)
                    
                    db.session.commit()
                    
                    # Security warning if using default credentials
                    if admin_password == 'admin123' or user_password == 'user123':
                        print("⚠️  SECURITY WARNING: Using default demo credentials!")
                        print("⚠️  Set ADMIN_PASSWORD and USER_PASSWORD environment variables in production!")
                    else:
                        print(f"Users created: {admin_username} and {user_username}")
                _users_initialized = True
        except Exception as e:
            print(f"User initialization failed: {e}")
            _users_initialized = True


if __name__ == '__main__':
    app.run(debug=True)

