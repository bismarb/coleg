"""
Application Configuration - Flask Setup for Academic Management System
MVC Architecture: Models + Views + Controllers
"""

import os
from datetime import datetime, date, timedelta
from flask import Flask
from flask_login import LoginManager
from models import db, User, Department, AcademicPeriod, Subject, Student, Teacher, Course, Enrollment, Grade
from views import views
from auth import hash_password

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


def create_sample_data():
    """Create sample data for testing"""
    try:
        # Check if admin user already exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print("✅ Sample data already exists")
            return
        
        print("📝 Creating sample data...")
        
        # Create users
        admin_user = User(
            email='admin@example.com',
            password=hash_password('123456'),
            name='Admin User',
            role='admin'
        )
        teacher_user = User(
            email='teacher@example.com',
            password=hash_password('123456'),
            name='Juan Profesor',
            role='teacher'
        )
        student_user = User(
            email='student@example.com',
            password=hash_password('123456'),
            name='María Estudiante',
            role='student'
        )
        
        db.session.add_all([admin_user, teacher_user, student_user])
        db.session.commit()
        print("✅ Users created")
        
        # Create departments
        dept1 = Department(name='Ingeniería', description='Departamento de Ingeniería')
        dept2 = Department(name='Ciencias', description='Departamento de Ciencias')
        db.session.add_all([dept1, dept2])
        db.session.commit()
        print("✅ Departments created")
        
        # Create subjects
        subj1 = Subject(
            name='Programación Python',
            code='PROG101',
            description='Introducción a Python',
            credits=3,
            department_id=dept1.id
        )
        subj2 = Subject(
            name='Cálculo I',
            code='CALC101',
            description='Fundamentos de Cálculo',
            credits=4,
            department_id=dept2.id
        )
        db.session.add_all([subj1, subj2])
        db.session.commit()
        print("✅ Subjects created")
        
        # Create academic period
        period = AcademicPeriod(
            name='2024-2025 Semestre 1',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            is_active=True
        )
        db.session.add(period)
        db.session.commit()
        print("✅ Academic period created")
        
        # Create teacher
        teacher = Teacher(
            user_id=teacher_user.id,
            teacher_code='PROF001',
            department_id=dept1.id,
            specialization='Python y Web',
            hire_date=date.today() - timedelta(days=365),
            status='active'
        )
        db.session.add(teacher)
        db.session.commit()
        print("✅ Teacher created")
        
        # Create course
        course = Course(
            subject_id=subj1.id,
            teacher_id=teacher.id,
            academic_period_id=period.id,
            course_code='PROG101-01',
            max_students=30,
            status='active'
        )
        db.session.add(course)
        db.session.commit()
        print("✅ Course created")
        
        # Create student
        student = Student(
            user_id=student_user.id,
            student_code='EST001',
            grade='10',
            enrollment_date=date.today(),
            status='active'
        )
        db.session.add(student)
        db.session.commit()
        print("✅ Student created")
        
        # Create enrollment
        enrollment = Enrollment(
            student_id=student.id,
            course_id=course.id,
            status='enrolled'
        )
        db.session.add(enrollment)
        db.session.commit()
        print("✅ Enrollment created")
        
        # Create grade
        grade = Grade(
            enrollment_id=enrollment.id,
            assessment_type='Examen Parcial',
            assessment_name='Examen 1',
            grade=8.5,
            assessment_date=date.today(),
            max_grade=10
        )
        db.session.add(grade)
        db.session.commit()
        print("✅ Grade created")
        
        print("✅ All sample data created successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Sample data creation error: {e}")


def init_db():
    """Initialize database with tables and sample data"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Create sample data
            create_sample_data()
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")


if __name__ == '__main__':
    print("🎓 Academia - Sistema de Gestión Académica")
    print("🌐 MVC Architecture: Models + Views + Controllers")
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
