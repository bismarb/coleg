"""
Application Configuration - Flask Setup for Academic Management System
MVC Architecture: Models + Views + Controllers
"""

from flask import Flask
from flask_login import LoginManager
from models import db, User
from views import views

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'tu-clave-secreta-super-segura-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/academia_db'
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
with app.app_context():
    db.create_all()
    print("✅ Database tables created/verified")

if __name__ == '__main__':
    print("🚀 Academic Management System - MVC Architecture")
    app.run(host='0.0.0.0', port=5000, debug=True)
