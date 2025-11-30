import os
from flask import Flask, jsonify, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_session import Session
from datetime import timedelta
from models import db, User, Student, Teacher, Department, Subject, Course, Enrollment, Grade, AcademicPeriod, Schedule, Assignment, Attendance
from auth import hash_password, check_password
from storage import Storage

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/academic_management')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET', 'academic-management-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SESSION_SQLALCHEMY'] = db
Session(app)

storage = Storage()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ==================== AUTH ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if not all([email, password, name, role]):
        return jsonify({'message': 'Todos los campos son requeridos'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'El correo ya está registrado'}), 400

    user = User(
        email=email,
        password=hash_password(password),
        name=name,
        role=role
    )
    db.session.add(user)
    db.session.commit()

    # Create role-specific record
    if role == 'student':
        student = Student(
            user_id=user.id,
            student_code=f'STU-{user.id}',
            grade='Por asignar',
            enrollment_date=db.func.current_date(),
            status='active'
        )
        db.session.add(student)
    elif role == 'teacher':
        teacher = Teacher(
            user_id=user.id,
            teacher_code=f'TCH-{user.id}',
            hire_date=db.func.current_date(),
            status='active'
        )
        db.session.add(teacher)

    db.session.commit()

    login_user(user)
    return jsonify({'user': user.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password(password, user.password):
        return jsonify({'message': 'Credenciales incorrectas'}), 401

    login_user(user)
    return jsonify({'user': user.to_dict()})

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Sesión cerrada correctamente'})

@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_me():
    return jsonify({'user': current_user.to_dict()})

# ==================== STUDENTS ROUTES ====================

@app.route('/api/students', methods=['GET'])
@login_required
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])

@app.route('/api/students', methods=['POST'])
@login_required
def create_student():
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    data = request.get_json()
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@app.route('/api/students/<student_id>', methods=['PATCH'])
@login_required
def update_student(student_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    student = Student.query.get_or_404(student_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify(student.to_dict())

@app.route('/api/students/<student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Estudiante eliminado'})

# ==================== TEACHERS ROUTES ====================

@app.route('/api/teachers', methods=['GET'])
@login_required
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify([t.to_dict() for t in teachers])

@app.route('/api/teachers', methods=['POST'])
@login_required
def create_teacher():
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    data = request.get_json()
    teacher = Teacher(**data)
    db.session.add(teacher)
    db.session.commit()
    return jsonify(teacher.to_dict()), 201

@app.route('/api/teachers/<teacher_id>', methods=['PATCH'])
@login_required
def update_teacher(teacher_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    teacher = Teacher.query.get_or_404(teacher_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(teacher, key, value)
    db.session.commit()
    return jsonify(teacher.to_dict())

@app.route('/api/teachers/<teacher_id>', methods=['DELETE'])
@login_required
def delete_teacher(teacher_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'Profesor eliminado'})

# ==================== DEPARTMENTS ROUTES ====================

@app.route('/api/departments', methods=['GET'])
@login_required
def get_departments():
    departments = Department.query.all()
    return jsonify([d.to_dict() for d in departments])

@app.route('/api/departments', methods=['POST'])
@login_required
def create_department():
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    data = request.get_json()
    department = Department(**data)
    db.session.add(department)
    db.session.commit()
    return jsonify(department.to_dict()), 201

# ==================== SUBJECTS ROUTES ====================

@app.route('/api/subjects', methods=['GET'])
@login_required
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([s.to_dict() for s in subjects])

@app.route('/api/subjects', methods=['POST'])
@login_required
def create_subject():
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    data = request.get_json()
    subject = Subject(**data)
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.to_dict()), 201

# ==================== COURSES ROUTES ====================

@app.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])

@app.route('/api/courses', methods=['POST'])
@login_required
def create_course():
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': 'Acceso denegado'}), 403
    
    data = request.get_json()
    course = Course(**data)
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@app.route('/api/courses/<course_id>', methods=['PATCH'])
@login_required
def update_course(course_id):
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': 'Acceso denegado'}), 403
    
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(course, key, value)
    db.session.commit()
    return jsonify(course.to_dict())

@app.route('/api/courses/<course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    if current_user.role != 'admin':
        return jsonify({'message': 'Acceso denegado'}), 403
    
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Curso eliminado'})

# ==================== GRADES ROUTES ====================

@app.route('/api/grades', methods=['GET'])
@login_required
def get_grades():
    grades = Grade.query.all()
    return jsonify([g.to_dict() for g in grades])

@app.route('/api/grades', methods=['POST'])
@login_required
def create_grade():
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': 'Acceso denegado'}), 403
    
    data = request.get_json()
    grade = Grade(**data)
    db.session.add(grade)
    db.session.commit()
    return jsonify(grade.to_dict()), 201

@app.route('/api/grades/<grade_id>', methods=['PATCH'])
@login_required
def update_grade(grade_id):
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': 'Acceso denegado'}), 403
    
    grade = Grade.query.get_or_404(grade_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(grade, key, value)
    db.session.commit()
    return jsonify(grade.to_dict())

@app.route('/api/grades/<grade_id>', methods=['DELETE'])
@login_required
def delete_grade(grade_id):
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'message': 'Acceso denegado'}), 403
    
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    return jsonify({'message': 'Calificación eliminada'})

# ==================== DASHBOARD STATISTICS ====================

@app.route('/api/dashboard/statistics', methods=['GET'])
@login_required
def get_statistics():
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    active_courses = Course.query.filter_by(status='active').count()
    total_departments = Department.query.count()
    
    return jsonify({
        'totalStudents': total_students,
        'totalTeachers': total_teachers,
        'activeCourses': active_courses,
        'totalDepartments': total_departments
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'No encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_ENV') == 'development')
