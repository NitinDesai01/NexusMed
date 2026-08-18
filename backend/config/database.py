from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """Initialize database"""
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")

def get_db_session():
    """Get database session"""
    return db.session
