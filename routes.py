"""
Routes - Flask Views
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from models import db, User, Student, Teacher, Course, Grade, Department, Enrollment, Subject, AcademicPeriod
from auth import verify_password, hash_password
from app import app
from datetime import datetime, date, timedelta


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and verify_password(password, user.password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role', 'student')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(email=email, name=name, password=hash_password(password), role=role)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Login now', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'students': Student.query.count(),
        'teachers': Teacher.query.count(),
        'courses': Course.query.filter_by(status='active').count(),
        'departments': Department.query.count()
    }
    return render_template('dashboard.html', stats=stats)


@app.route('/students')
@login_required
def students():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    students = Student.query.all()
    return render_template('students.html', students=students)


@app.route('/students/add', methods=['POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denied'}), 403
    
    try:
        code = request.form.get('code')
        grade = request.form.get('grade')
        email = f"{code}@student.edu"
        
        user = User(email=email, name=f"Student {code}", password=hash_password('123456'), role='student')
        db.session.add(user)
        db.session.flush()
        
        student = Student(user_id=user.id, student_code=code, grade=grade, enrollment_date=date.today())
        db.session.add(student)
        db.session.commit()
        
        flash('Student added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('students'))


@app.route('/teachers')
@login_required
def teachers():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)


@app.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


@app.route('/grades')
@login_required
def grades():
    if current_user.role not in ['admin', 'teacher']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)


@app.route('/departments')
@login_required
def departments():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    depts = Department.query.all()
    return render_template('departments.html', departments=depts)
