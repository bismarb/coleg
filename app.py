"""
Main Application - Flask Setup
"""

import os
from flask import Flask
from flask_login import LoginManager
from models import db, User
from auth import hash_password
from datetime import date
from sqlalchemy.pool import QueuePool

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'academia-secret-key-2024'
database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/academia_db')
# Add SSL and pool settings for reliable connections
if 'sslmode' not in database_url:
    database_url = database_url + '?sslmode=require'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
    'connect_args': {'connect_timeout': 10}
}

db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except Exception as e:
        print(f"Error loading user: {e}")
        return None


def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        
        # Create grades if they don't exist
        from models import Grade
        if Grade.query.count() == 0:
            grades_data = [
                Grade(name='1° Primaria', level=1),
                Grade(name='2° Primaria', level=2),
                Grade(name='3° Primaria', level=3),
                Grade(name='4° Primaria', level=4),
                Grade(name='5° Primaria', level=5),
                Grade(name='6° Primaria', level=6),
            ]
            db.session.add_all(grades_data)
            db.session.commit()


# Import routes AFTER app definition
import routes
