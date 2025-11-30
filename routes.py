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


@app.route('/teachers/add', methods=['POST'])
@login_required
def create_teacher():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denied'}), 403
    
    try:
        name = request.form.get('name')
        email = f"{name.lower().replace(' ', '')}@teacher.edu"
        
        user = User(email=email, name=name, password=hash_password('123456'), role='teacher')
        db.session.add(user)
        db.session.flush()
        
        teacher = Teacher(user_id=user.id, hire_date=date.today())
        db.session.add(teacher)
        db.session.commit()
        
        flash('Teacher added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('teachers'))


@app.route('/courses/add', methods=['POST'])
@login_required
def create_course():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denied'}), 403
    
    try:
        name = request.form.get('name')
        code = request.form.get('code')
        status = request.form.get('status', 'active')
        
        course = Course(name=name, code=code, status=status)
        db.session.add(course)
        db.session.commit()
        
        flash('Course added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('courses'))


@app.route('/departments/add', methods=['POST'])
@login_required
def create_department():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denied'}), 403
    
    try:
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        dept = Department(name=name, description=description)
        db.session.add(dept)
        db.session.commit()
        
        flash('Department added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('departments'))


@app.route('/grades/add', methods=['POST'])
@login_required
def create_grade():
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'Denied'}), 403
    
    try:
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        grade_value = request.form.get('grade_value')
        
        grade = Grade(student_id=student_id, course_id=course_id, grade_value=grade_value)
        db.session.add(grade)
        db.session.commit()
        
        flash('Grade added', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('grades'))


@app.route('/courses/<course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    if current_user.role != 'student':
        flash('Only students can enroll', 'error')
        return redirect(url_for('courses'))
    
    try:
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            flash('Student profile not found', 'error')
            return redirect(url_for('courses'))
        
        course = Course.query.get(course_id)
        if not course:
            flash('Course not found', 'error')
            return redirect(url_for('courses'))
        
        existing = Enrollment.query.filter_by(student_id=student.id, course_id=course_id).first()
        if existing:
            flash('Already enrolled in this course', 'error')
            return redirect(url_for('courses'))
        
        enrollment = Enrollment(student_id=student.id, course_id=course_id, status='enrolled')
        db.session.add(enrollment)
        db.session.commit()
        
        flash(f'Successfully enrolled in {course.subject.name}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('courses'))


@app.route('/my-children')
@login_required
def my_children():
    if current_user.role != 'parent':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    children = []
    if parent:
        student = parent.student
        enrollments = Enrollment.query.filter_by(student_id=student.id).all()
        grades = Grade.query.join(Enrollment).filter(Enrollment.student_id == student.id).all()
        attendance = Attendance.query.join(Enrollment).filter(Enrollment.student_id == student.id).all()
        
        attendance_count = len([a for a in attendance if a.status == 'present'])
        total_attendance = len(attendance)
        
        children.append({
            'student': student,
            'enrollments': enrollments,
            'grades': grades,
            'attendance_rate': f"{(attendance_count/total_attendance*100) if total_attendance > 0 else 0:.1f}%"
        })
    
    return render_template('my_children.html', children=children)


@app.route('/attendance')
@login_required
def attendance_record():
    if current_user.role not in ['admin', 'teacher']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    attendance = Attendance.query.all()
    return render_template('attendance.html', attendance=attendance)


@app.route('/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'error': 'Denied'}), 403
    
    try:
        enrollment_id = request.form.get('enrollment_id')
        date = request.form.get('date')
        status = request.form.get('status')
        notes = request.form.get('notes', '')
        
        att = Attendance(enrollment_id=enrollment_id, date=date, status=status, notes=notes)
        db.session.add(att)
        db.session.commit()
        
        flash('Attendance marked', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('attendance_record'))


@app.route('/schedules')
@login_required
def schedules():
    schedules = Schedule.query.all()
    return render_template('schedules.html', schedules=schedules)


@app.route('/reports')
@login_required
def reports():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_courses = Course.query.filter_by(status='active').count()
    avg_attendance = 85
    
    return render_template('reports.html', 
                         total_students=total_students,
                         total_teachers=total_teachers,
                         total_courses=total_courses,
                         avg_attendance=avg_attendance)
