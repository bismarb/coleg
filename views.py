"""
Views Layer - Flask Routes for Academic Management System
Handles all HTTP requests and template rendering
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from datetime import datetime, date

from models import db, User, Student, Teacher, Course, Grade, Department, Enrollment, Subject, AcademicPeriod
from controllers import (
    StudentController, TeacherController, CourseController, 
    DepartmentController, GradeController, EnrollmentController,
    UserController, DashboardController, SubjectController, AttendanceController
)
from auth import hash_password, check_password

# Create blueprint
views = Blueprint('views', __name__)


# ==================== AUTHENTICATION ROUTES ====================

@views.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserController.get_by_email(email)
        
        if user and check_password(password, user.password):
            login_user(user)
            flash('¡Bienvenido!', 'success')
            return redirect(url_for('views.dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'error')
    
    return render_template('login.html')


@views.route('/register', methods=['GET', 'POST'])
def register_page():
    """Register route"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if UserController.get_by_email(email):
            flash('El email ya está registrado', 'error')
            return redirect(url_for('views.register_page'))
        
        try:
            user = UserController.create(email=email, password=password, name=name, role=role)
            flash('¡Cuenta creada! Inicia sesión', 'success')
            return redirect(url_for('views.login'))
        except Exception as e:
            flash(f'Error al registrar: {str(e)}', 'error')
    
    return render_template('register.html')


@views.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('views.login'))


# ==================== DASHBOARD ROUTE ====================

@views.route('/dashboard')
@login_required
def dashboard():
    """Dashboard route"""
    stats = DashboardController.get_statistics()
    return render_template('dashboard.html', stats=stats)


@views.route('/')
@login_required
def index():
    """Index redirect to dashboard"""
    return redirect(url_for('views.dashboard'))


# ==================== STUDENTS ROUTES ====================

@views.route('/students')
@login_required
def students_page():
    """Students page"""
    if current_user.role != 'admin':
        flash('No tienes permiso', 'error')
        return redirect(url_for('views.dashboard'))
    
    students = StudentController.get_all()
    return render_template('students.html', students=students)


@views.route('/students/create', methods=['POST'])
@login_required
def create_student():
    """Create student"""
    if current_user.role != 'admin':
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        student_code = request.form.get('student_code')
        grade = request.form.get('grade')
        
        # Create user first
        email = f"{student_code}@student.edu"
        user = UserController.create(
            email=email,
            password=hash_password('123456'),
            name=f"Estudiante {student_code}",
            role='student'
        )
        
        # Create student
        StudentController.create(
            user_id=user.id,
            student_code=student_code,
            grade=grade
        )
        
        flash('Estudiante creado', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('views.students_page'))


@views.route('/api/students/<student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    """Delete student API"""
    if current_user.role != 'admin':
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        student = StudentController.get_by_id(student_id)
        if student:
            StudentController.delete(student_id)
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'No encontrado'}), 404


# ==================== TEACHERS ROUTES ====================

@views.route('/teachers')
@login_required
def teachers_page():
    """Teachers page"""
    if current_user.role != 'admin':
        flash('No tienes permiso', 'error')
        return redirect(url_for('views.dashboard'))
    
    teachers = TeacherController.get_all()
    return render_template('teachers.html', teachers=teachers)


@views.route('/teachers/create', methods=['POST'])
@login_required
def create_teacher():
    """Create teacher"""
    if current_user.role != 'admin':
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        teacher_code = request.form.get('teacher_code')
        specialization = request.form.get('specialization')
        
        # Create user first
        email = f"{teacher_code}@teacher.edu"
        user = UserController.create(
            email=email,
            password=hash_password('123456'),
            name=f"Profesor {teacher_code}",
            role='teacher'
        )
        
        # Create teacher
        TeacherController.create(
            user_id=user.id,
            teacher_code=teacher_code,
            specialization=specialization
        )
        
        flash('Profesor creado', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('views.teachers_page'))


@views.route('/api/teachers/<teacher_id>', methods=['DELETE'])
@login_required
def delete_teacher(teacher_id):
    """Delete teacher API"""
    if current_user.role != 'admin':
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        teacher = TeacherController.get_by_id(teacher_id)
        if teacher:
            TeacherController.delete(teacher_id)
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'No encontrado'}), 404


# ==================== COURSES ROUTES ====================

@views.route('/courses')
@login_required
def courses_page():
    """Courses page"""
    courses = CourseController.get_all()
    return render_template('courses.html', courses=courses)


@views.route('/courses/create', methods=['POST'])
@login_required
def create_course():
    """Create course"""
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        course_code = request.form.get('course_code')
        max_students = request.form.get('max_students', 30)
        
        # Get first subject and academic period (for demo)
        subject = SubjectController.get_all()
        periods = AcademicPeriod.query.all()
        
        if not subject or not periods:
            flash('Asignatura o período académico no encontrado', 'error')
            return redirect(url_for('views.courses_page'))
        
        # Get teacher
        teacher = TeacherController.get_all()
        if not teacher:
            flash('Profesor no encontrado', 'error')
            return redirect(url_for('views.courses_page'))
        
        CourseController.create(
            subject_id=subject[0].id,
            teacher_id=teacher[0].id,
            academic_period_id=periods[0].id,
            course_code=course_code,
            max_students=max_students
        )
        
        flash('Curso creado', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('views.courses_page'))


# ==================== GRADES ROUTES ====================

@views.route('/grades')
@login_required
def grades_page():
    """Grades page"""
    if current_user.role not in ['admin', 'teacher']:
        flash('No tienes permiso', 'error')
        return redirect(url_for('views.dashboard'))
    
    grades = GradeController.get_all()
    return render_template('grades.html', grades=grades)


@views.route('/grades/create', methods=['POST'])
@login_required
def create_grade():
    """Create grade"""
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        assessment_type = request.form.get('assessment_type')
        grade = request.form.get('grade')
        
        # Get first enrollment (for demo)
        enrollment = Enrollment.query.first()
        if not enrollment:
            flash('Inscripción no encontrada', 'error')
            return redirect(url_for('views.grades_page'))
        
        GradeController.create(
            enrollment_id=enrollment.id,
            assessment_type=assessment_type,
            grade=grade
        )
        
        flash('Calificación registrada', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('views.grades_page'))


# ==================== DEPARTMENTS ROUTES ====================

@views.route('/departments')
@login_required
def departments_page():
    """Departments page"""
    if current_user.role != 'admin':
        flash('No tienes permiso', 'error')
        return redirect(url_for('views.dashboard'))
    
    departments = DepartmentController.get_all()
    return render_template('departments.html', departments=departments)


@views.route('/departments/create', methods=['POST'])
@login_required
def create_department():
    """Create department"""
    if current_user.role != 'admin':
        return jsonify({'error': 'No permitido'}), 403
    
    try:
        name = request.form.get('name')
        description = request.form.get('description')
        head = request.form.get('head')
        
        DepartmentController.create(
            name=name,
            description=description,
            head=head
        )
        
        flash('Departamento creado', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('views.departments_page'))
