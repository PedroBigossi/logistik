"""
Database initialization script.
Creates the database tables and adds default admin and user accounts.
Run this script once to set up the database.
"""

from app import app, db
from models import User

def init_database():
    """Initialize the database with tables and default users."""
    with app.app_context():
        # Create all database tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nCreating default admin user...")
            admin = User(
                username='admin',
                email='admin@logistik.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Admin user created!")
            print("  Username: admin")
            print("  Password: admin123")
        else:
            print("\nAdmin user already exists.")
        
        # Check if regular user already exists
        user = User.query.filter_by(username='user').first()
        if not user:
            print("\nCreating default regular user...")
            user = User(
                username='user',
                email='user@logistik.com',
                role='user'
            )
            user.set_password('user123')
            db.session.add(user)
            print("✓ Regular user created!")
            print("  Username: user")
            print("  Password: user123")
        else:
            print("\nRegular user already exists.")
        
        # Commit all changes
        db.session.commit()
        print("\n✓ Database initialization completed successfully!")
        print("\nYou can now start the application with: python app.py")

if __name__ == '__main__':
    init_database()

