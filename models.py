"""
models.py - Database models for Flask application with Flask-SQLAlchemy and Flask-Login.
Defines User and UserAppData models for PostgreSQL database.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model with Flask-Login integration."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True, unique=True)
    supabase_id = db.Column(db.String(255), nullable=True, unique=True)
    profile_name = db.Column(db.String(100), nullable=True)
    profile_image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to UserAppData
    app_data = db.relationship('UserAppData', backref='user', lazy=True, cascade='all, delete-orphan')
    
    @property
    def is_active(self):
        """Flask-Login required property - always True."""
        return True
    
    def set_password(self, password):
        """Hash and set password using bcrypt."""
        if password:
            self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Verify password against hash using bcrypt."""
        if not self.password_hash or not password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Return user data as dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'profile_name': self.profile_name,
            'profile_image_url': self.profile_image_url,
            'has_google': self.google_id is not None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserAppData(db.Model):
    """Model for storing per-user application data as JSON."""
    __tablename__ = 'user_app_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_key = db.Column(db.String(100), nullable=False)
    data_value = db.Column(db.Text, default='{}', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint on (user_id, data_key)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'data_key', name='uq_user_data_key'),
    )


def init_db(app):
    """Initialize database with Flask app and create all tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
