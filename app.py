"""
Application Configuration - Flask Setup for Academic Management System
MVC Architecture: Models + Views + Controllers
"""

import os
from flask import Flask
from flask_login import LoginManager
from models import db, User
from views import views

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-2024-academia')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/academia_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'views.login'
login_manager.login_message = 'Debes iniciar sesión'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Register blueprint for views (routes)
app.register_blueprint(views)

# Create tables on app startup
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created/verified")
        except Exception as e:
            print(f"⚠️ Database initialization warning: {e}")

if __name__ == '__main__':
    print("🚀 Academic Management System - MVC Architecture")
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
