"""
Database models for the logistics management system.
Defines User and Delivery models with their relationships.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize database object (will be initialized in app.py)
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model for authentication and authorization.
    Supports two roles: 'admin' and 'user'
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if the user has admin role."""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Delivery(db.Model):
    """
    Delivery model representing a logistics process/delivery.
    Contains tracking information and status updates.
    """
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_address = db.Column(db.Text, nullable=False)
    recipient_phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='ongoing')
    # Status options: 'late', 'ongoing', 'in_route', 'delivered'
    
    # Delivery details
    description = db.Column(db.Text)
    weight = db.Column(db.Float)  # in kg
    estimated_delivery_date = db.Column(db.Date)
    actual_delivery_date = db.Column(db.Date)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to track who created/updated
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='deliveries_created')
    updated_by = db.relationship('User', foreign_keys=[updated_by_id], backref='deliveries_updated')
    
    def __repr__(self):
        return f'<Delivery {self.tracking_number}>'

