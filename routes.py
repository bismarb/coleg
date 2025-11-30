"""
Routes - Flask Views for Teacher Management System
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from models import db, User, Teacher, Course, Grade, Department, Enrollment, Subject, AcademicPeriod, Attendance
from auth import verify_password, hash_password
from app import app
from datetime import datetime, date


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
        flash('Credenciales inválidas', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    if not teacher:
        flash('Perfil de profesor no encontrado', 'error')
        return redirect(url_for('login'))
    
    my_courses = Course.query.filter_by(teacher_id=teacher.id).all()
    total_students = sum(len(course.enrollments) for course in my_courses)
    
    stats = {
        'my_courses': len(my_courses),
        'total_students': total_students,
        'pending_grades': 0
    }
    
    return render_template('dashboard.html', stats=stats, teacher=teacher)


@app.route('/my-courses')
@login_required
def my_courses():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    
    if not teacher:
        flash('Perfil de profesor no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    return render_template('my_courses.html', courses=courses)


@app.route('/course/<course_id>/students')
@login_required
def course_students(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('my_courses'))
    
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if course.teacher_id != teacher.id:
        flash('No tienes acceso a este curso', 'error')
        return redirect(url_for('my_courses'))
    
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    return render_template('course_students.html', course=course, enrollments=enrollments)


@app.route('/course/<course_id>/attendance')
@login_required
def course_attendance(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('my_courses'))
    
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if course.teacher_id != teacher.id:
        flash('No tienes acceso a este curso', 'error')
        return redirect(url_for('my_courses'))
    
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    return render_template('course_attendance.html', course=course, enrollments=enrollments)


@app.route('/course/<course_id>/grades')
@login_required
def course_grades(course_id):
    course = Course.query.get(course_id)
    
    if not course:
        flash('Curso no encontrado', 'error')
        return redirect(url_for('my_courses'))
    
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if course.teacher_id != teacher.id:
        flash('No tienes acceso a este curso', 'error')
        return redirect(url_for('my_courses'))
    
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    return render_template('course_grades.html', course=course, enrollments=enrollments)


@app.route('/grade/add', methods=['POST'])
@login_required
def add_grade():
    try:
        enrollment_id = request.form.get('enrollment_id')
        assessment_type = request.form.get('assessment_type')
        grade = request.form.get('grade')
        assessment_date = request.form.get('assessment_date')
        
        enrollment = Enrollment.query.get(enrollment_id)
        if not enrollment:
            flash('Inscripción no encontrada', 'error')
            return jsonify({'error': 'Not found'}), 404
        
        course = enrollment.course
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        if course.teacher_id != teacher.id:
            flash('No tienes acceso', 'error')
            return jsonify({'error': 'Denied'}), 403
        
        new_grade = Grade(
            enrollment_id=enrollment_id,
            assessment_type=assessment_type,
            grade=float(grade),
            assessment_date=assessment_date
        )
        db.session.add(new_grade)
        db.session.commit()
        
        flash('Calificación registrada', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('course_grades', course_id=request.form.get('course_id')))


@app.route('/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    try:
        enrollment_id = request.form.get('enrollment_id')
        date_att = request.form.get('date')
        status = request.form.get('status')
        
        enrollment = Enrollment.query.get(enrollment_id)
        if not enrollment:
            flash('Inscripción no encontrada', 'error')
            return jsonify({'error': 'Not found'}), 404
        
        course = enrollment.course
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        if course.teacher_id != teacher.id:
            flash('No tienes acceso', 'error')
            return jsonify({'error': 'Denied'}), 403
        
        existing = Attendance.query.filter_by(enrollment_id=enrollment_id, date=date_att).first()
        if existing:
            existing.status = status
        else:
            attendance = Attendance(enrollment_id=enrollment_id, date=date_att, status=status)
            db.session.add(attendance)
        
        db.session.commit()
        flash('Asistencia registrada', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('course_attendance', course_id=request.form.get('course_id')))
