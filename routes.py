"""
Routes - Flask Views for School Management System
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from models import db, User, Student, Teacher, Grade, Subject, Enrollment, Assessment, Attendance, Schedule, TeacherSubject, Calificacion
from auth import verify_password, hash_password
from app import app
from datetime import date, datetime


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
    stats = {}
    
    if current_user.role == 'admin':
        stats = {
            'students': Student.query.count(),
            'teachers': Teacher.query.count(),
            'enrollments': Enrollment.query.count(),
            'grades': Grade.query.count()
        }
    elif current_user.role == 'teacher':
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        my_enrollments = Enrollment.query.filter_by(teacher_id=teacher.id).all() if teacher else []
        total_students = len(set(e.student_id for e in my_enrollments))
        stats = {
            'my_enrollments': len(my_enrollments),
            'total_students': total_students
        }
    elif current_user.role == 'student':
        student = Student.query.filter_by(user_id=current_user.id).first()
        enrollments = Enrollment.query.filter_by(student_id=student.id).all() if student else []
        stats = {
            'courses': len(enrollments),
            'attendance': 0
        }
    
    return render_template('dashboard.html', stats=stats)


@app.route('/students')
@login_required
def students():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    students = Student.query.all()
    grades = Grade.query.all()
    return render_template('students.html', students=students, grades=grades)


@app.route('/student/add', methods=['POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        student_code = request.form.get('student_code')
        grade_id = request.form.get('grade_id')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        
        # Validar que el grado tiene cupos disponibles
        grade = Grade.query.get(grade_id)
        if not grade:
            flash('Grado no encontrado', 'error')
            return redirect(url_for('students'))
        
        enrolled_count = Student.query.filter_by(grade_id=grade_id).count()
        if enrolled_count >= grade.max_students:
            flash(f'El grado {grade.name} está lleno ({enrolled_count}/{grade.max_students}). No se pueden agregar más estudiantes.', 'error')
            return redirect(url_for('students'))
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('El email ya está registrado', 'error')
            return redirect(url_for('students'))
        
        user = User(email=email, name=name, password=hash_password('123456'), role='student')
        db.session.add(user)
        db.session.flush()
        
        student = Student(user_id=user.id, student_code=student_code, grade_id=grade_id, enrollment_date=date.today(), apellido_paterno=apellido_paterno, apellido_materno=apellido_materno)
        db.session.add(student)
        db.session.commit()
        
        flash(f'Estudiante {name} agregado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('students'))


@app.route('/student/<student_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    student = Student.query.get(student_id)
    if not student:
        flash('Estudiante no encontrado', 'error')
        return redirect(url_for('students'))
    
    if request.method == 'POST':
        try:
            student.user.name = request.form.get('name')
            student.user.email = request.form.get('email')
            student.student_code = request.form.get('student_code')
            student.grade_id = request.form.get('grade_id')
            student.status = request.form.get('status')
            student.apellido_paterno = request.form.get('apellido_paterno')
            student.apellido_materno = request.form.get('apellido_materno')
            
            db.session.commit()
            flash('Estudiante actualizado', 'success')
            return redirect(url_for('students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    grades = Grade.query.all()
    return render_template('edit_student.html', student=student, grades=grades)


@app.route('/student/<student_id>/delete', methods=['POST'])
@login_required
def delete_student(student_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        student = Student.query.get(student_id)
        if not student:
            flash('Estudiante no encontrado', 'error')
            return redirect(url_for('students'))
        
        user = student.user
        Enrollment.query.filter_by(student_id=student_id).delete()
        db.session.delete(student)
        db.session.delete(user)
        db.session.commit()
        
        flash('Estudiante eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('students'))


@app.route('/teachers')
@login_required
def teachers():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)


@app.route('/teacher/add', methods=['POST'])
@login_required
def add_teacher():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        teacher_code = request.form.get('teacher_code')
        specialization = request.form.get('specialization')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        end_contract_date = request.form.get('end_contract_date')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('El email ya está registrado', 'error')
            return redirect(url_for('teachers'))
        
        user = User(email=email, name=name, password=hash_password('123456'), role='teacher')
        db.session.add(user)
        db.session.flush()
        
        end_date = None
        if end_contract_date:
            end_date = datetime.strptime(end_contract_date, '%Y-%m-%d').date()
        
        teacher = Teacher(user_id=user.id, teacher_code=teacher_code, specialization=specialization, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, hire_date=date.today(), end_contract_date=end_date)
        db.session.add(teacher)
        db.session.commit()
        
        flash(f'Profesor {name} agregado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('teachers'))


@app.route('/teacher/<teacher_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        flash('Profesor no encontrado', 'error')
        return redirect(url_for('teachers'))
    
    if request.method == 'POST':
        try:
            teacher.user.name = request.form.get('name')
            teacher.user.email = request.form.get('email')
            teacher.teacher_code = request.form.get('teacher_code')
            teacher.specialization = request.form.get('specialization')
            teacher.apellido_paterno = request.form.get('apellido_paterno')
            teacher.apellido_materno = request.form.get('apellido_materno')
            teacher.status = request.form.get('status')
            
            end_contract_date = request.form.get('end_contract_date')
            if end_contract_date:
                teacher.end_contract_date = datetime.strptime(end_contract_date, '%Y-%m-%d').date()
            else:
                teacher.end_contract_date = None
            
            db.session.commit()
            flash('Profesor actualizado', 'success')
            return redirect(url_for('teachers'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('edit_teacher.html', teacher=teacher)


@app.route('/teacher/<teacher_id>/delete', methods=['POST'])
@login_required
def delete_teacher(teacher_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            flash('Profesor no encontrado', 'error')
            return redirect(url_for('teachers'))
        
        user = teacher.user
        Enrollment.query.filter_by(teacher_id=teacher_id).delete()
        Schedule.query.filter_by(teacher_id=teacher_id).delete()
        db.session.delete(teacher)
        db.session.delete(user)
        db.session.commit()
        
        flash('Profesor eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('teachers'))




@app.route('/grades')
@login_required
def grades():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)


@app.route('/grade/add', methods=['POST'])
@login_required
def add_grade():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        name = request.form.get('name')
        level = request.form.get('level')
        max_students = request.form.get('max_students', 40)
        
        grade = Grade(name=name, level=level, max_students=max_students)
        db.session.add(grade)
        db.session.commit()
        
        flash('Grado agregado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('grades'))


@app.route('/grade/<grade_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_grade(grade_id):
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('grades'))
    
    grade = Grade.query.get(grade_id)
    if not grade:
        flash('Grado no encontrado', 'error')
        return redirect(url_for('grades'))
    
    if request.method == 'POST':
        try:
            grade.name = request.form.get('name')
            grade.level = request.form.get('level')
            grade.max_students = request.form.get('max_students')
            
            db.session.commit()
            flash('Grado actualizado', 'success')
            return redirect(url_for('grades'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('edit_grade.html', grade=grade)


@app.route('/grade/<grade_id>/delete', methods=['POST'])
@login_required
def delete_grade(grade_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        grade = Grade.query.get(grade_id)
        if not grade:
            flash('Grado no encontrado', 'error')
            return redirect(url_for('grades'))
        
        Student.query.filter_by(grade_id=grade_id).delete()
        Enrollment.query.filter_by(grade_id=grade_id).delete()
        Schedule.query.filter_by(grade_id=grade_id).delete()
        db.session.delete(grade)
        db.session.commit()
        
        flash('Grado eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('grades'))


@app.route('/student/<student_id>/assessments')
@login_required
def student_assessments(student_id):
    student = Student.query.get(student_id)
    if not student:
        flash('Estudiante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    assessments = Assessment.query.join(Enrollment).filter(Enrollment.student_id == student_id).all()
    return render_template('student_assessments.html', student=student, assessments=assessments)


@app.route('/assessment/add', methods=['POST'])
@login_required
def add_assessment():
    if current_user.role != 'teacher':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        enrollment_id = request.form.get('enrollment_id')
        assessment_type = request.form.get('assessment_type')
        score = request.form.get('score')
        assessment_date = request.form.get('assessment_date')
        
        assessment = Assessment(
            enrollment_id=enrollment_id,
            assessment_type=assessment_type,
            score=float(score),
            assessment_date=assessment_date
        )
        db.session.add(assessment)
        db.session.commit()
        flash('Evaluación registrada', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('courses'))


@app.route('/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role != 'teacher':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        enrollment_id = request.form.get('enrollment_id')
        attendance_date = request.form.get('attendance_date')
        status = request.form.get('status')
        
        existing = Attendance.query.filter_by(enrollment_id=enrollment_id, attendance_date=attendance_date).first()
        if existing:
            existing.status = status
        else:
            attendance = Attendance(enrollment_id=enrollment_id, attendance_date=attendance_date, status=status)
            db.session.add(attendance)
        
        db.session.commit()
        flash('Asistencia registrada', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('courses'))


@app.route('/schedule')
@login_required
def view_schedule():
    schedules = Schedule.query.all()
    grades = Grade.query.order_by(Grade.level).all()
    
    # Get only teachers with active contracts (end_contract_date is NULL or in the future)
    today = date.today()
    teachers = Teacher.query.filter(
        (Teacher.end_contract_date == None) | (Teacher.end_contract_date >= today)
    ).all()
    
    # Organize schedules by grade
    schedules_by_grade = {}
    for grade in grades:
        grade_schedules = []
        for schedule in schedules:
            if schedule.grade_id == grade.id:
                grade_schedules.append(schedule)
        schedules_by_grade[grade.id] = {
            'grade': grade,
            'schedules': grade_schedules
        }
    
    return render_template('schedules.html', schedules_by_grade=schedules_by_grade, teachers=teachers)


@app.route('/schedule/add', methods=['POST'])
@login_required
def add_schedule():
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        day_of_week = request.form.get('day_of_week')
        teacher_id = request.form.get('teacher_id')
        grade_id = request.form.get('grade_id')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        classroom = request.form.get('classroom')
        
        schedule = Schedule(teacher_id=teacher_id, grade_id=grade_id, day_of_week=day_of_week, start_time=start_time, end_time=end_time, classroom=classroom)
        db.session.add(schedule)
        db.session.commit()
        
        flash('Horario agregado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('view_schedule'))


@app.route('/schedule/<schedule_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('view_schedule'))
    
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        flash('Horario no encontrado', 'error')
        return redirect(url_for('view_schedule'))
    
    if request.method == 'POST':
        try:
            teacher_id = request.form.get('teacher_id')
            grade_id = request.form.get('grade_id')
            day_of_week = request.form.get('day_of_week')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            classroom = request.form.get('classroom')
            
            schedule.teacher_id = teacher_id
            schedule.grade_id = grade_id
            schedule.day_of_week = day_of_week
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.classroom = classroom
            
            db.session.commit()
            flash('Horario actualizado', 'success')
            return redirect(url_for('view_schedule'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    today = date.today()
    teachers = Teacher.query.filter(
        (Teacher.end_contract_date == None) | (Teacher.end_contract_date >= today)
    ).all()
    grades = Grade.query.all()
    return render_template('edit_schedule.html', schedule=schedule, teachers=teachers, grades=grades)


@app.route('/schedule/<schedule_id>/delete', methods=['POST'])
@login_required
def delete_schedule(schedule_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Denegado'}), 403
    
    try:
        schedule = Schedule.query.get(schedule_id)
        if not schedule:
            flash('Horario no encontrado', 'error')
            return redirect(url_for('view_schedule'))
        
        db.session.delete(schedule)
        db.session.commit()
        
        flash('Horario eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('view_schedule'))


@app.route('/api/teacher/<teacher_id>/specialization', methods=['GET'])
@login_required
def get_teacher_specialization(teacher_id):
    """API endpoint para obtener especialización de un profesor"""
    try:
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return jsonify({'error': 'Profesor no encontrado'}), 404
        
        # Get first subject from teacher's subjects
        subject_id = None
        if teacher.teacher_subjects and len(teacher.teacher_subjects) > 0:
            subject_id = teacher.teacher_subjects[0].subject.id
        else:
            # Fallback to first subject in database
            first_subject = Subject.query.first()
            subject_id = first_subject.id if first_subject else None
        
        return jsonify({
            'specialization': teacher.specialization or '',
            'subject_id': subject_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/admin/all-grades', methods=['GET', 'POST'])
@login_required
def admin_all_grades():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all enrollments with all data
    enrollments = Enrollment.query.all()
    
    # Group by grade
    grades_data = {}
    for enrollment in enrollments:
        grade = enrollment.grade
        if grade.id not in grades_data:
            grades_data[grade.id] = {
                'grade': grade,
                'enrollments': []
            }
        
        # Calculate average
        sem1 = float(enrollment.semester_1) if enrollment.semester_1 else 0
        sem2 = float(enrollment.semester_2) if enrollment.semester_2 else 0
        sem3 = float(enrollment.semester_3) if enrollment.semester_3 else 0
        total_score = round((sem1 + sem2 + sem3) / 3, 2)
        
        grades_data[grade.id]['enrollments'].append({
            'enrollment': enrollment,
            'total_score': total_score
        })
    
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            
            if action == 'update_grades':
                enrollment_id = request.form.get('enrollment_id')
                semester_1 = request.form.get('semester_1')
                semester_2 = request.form.get('semester_2')
                semester_3 = request.form.get('semester_3')
                
                enrollment = Enrollment.query.get(enrollment_id)
                if enrollment:
                    if semester_1:
                        enrollment.semester_1 = float(semester_1)
                    if semester_2:
                        enrollment.semester_2 = float(semester_2)
                    if semester_3:
                        enrollment.semester_3 = float(semester_3)
                    
                    db.session.commit()
                    flash('Calificaciones actualizadas exitosamente', 'success')
                else:
                    flash('Inscripción no encontrada', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('admin_all_grades'))
    
    return render_template('admin_all_grades.html', grades_data=grades_data)


@app.route('/teacher/grades', methods=['GET', 'POST'])
@login_required
def teacher_grades():
    if current_user.role != 'teacher':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        flash('Profesor no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all grades
    all_grades = Grade.query.order_by(Grade.level).all()
    
    # Get all students grouped by grade
    grades_data = {}
    for grade in all_grades:
        # Get all students in this grade
        students_in_grade = Student.query.filter_by(grade_id=grade.id).all()
        
        # Calculate total scores for each student
        students_with_scores = []
        for student in students_in_grade:
            # Get enrollment with this teacher (if exists)
            enrollment = Enrollment.query.filter_by(student_id=student.id, teacher_id=teacher.id).first()
            
            if enrollment:
                # Calculate average from three semesters divided by 3
                sem1 = float(enrollment.semester_1) if enrollment.semester_1 else 0
                sem2 = float(enrollment.semester_2) if enrollment.semester_2 else 0
                sem3 = float(enrollment.semester_3) if enrollment.semester_3 else 0
                total_score = round((sem1 + sem2 + sem3) / 3, 2)
                # Check if any semester has a value
                has_grades = enrollment.semester_1 or enrollment.semester_2 or enrollment.semester_3
                students_with_scores.append({
                    'student': student,
                    'enrollment': enrollment,
                    'total_score': total_score,
                    'has_enrollment': True,
                    'has_grades': has_grades
                })
        
        # Always add grade to grades_data, even if no students are enrolled yet
        grades_data[grade.id] = {
            'grade': grade,
            'students_with_scores': students_with_scores
        }
    
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            
            if action == 'update_grades':
                enrollment_id = request.form.get('enrollment_id')
                semester_1 = request.form.get('semester_1')
                semester_2 = request.form.get('semester_2')
                semester_3 = request.form.get('semester_3')
                
                enrollment = Enrollment.query.get(enrollment_id)
                if enrollment:
                    if semester_1:
                        enrollment.semester_1 = float(semester_1)
                        # Also save to Calificacion table for students to see
                        existing_cal = Calificacion.query.filter_by(
                            enrollment_id=enrollment_id,
                            student_id=enrollment.student_id,
                            subject_id=enrollment.subject_id,
                            teacher_id=teacher.id,
                            semester=1
                        ).first()
                        if existing_cal:
                            existing_cal.calificacion = float(semester_1)
                        else:
                            cal = Calificacion(
                                enrollment_id=enrollment_id,
                                student_id=enrollment.student_id,
                                subject_id=enrollment.subject_id,
                                teacher_id=teacher.id,
                                semester=1,
                                calificacion=float(semester_1)
                            )
                            db.session.add(cal)
                    
                    if semester_2:
                        enrollment.semester_2 = float(semester_2)
                        existing_cal = Calificacion.query.filter_by(
                            enrollment_id=enrollment_id,
                            student_id=enrollment.student_id,
                            subject_id=enrollment.subject_id,
                            teacher_id=teacher.id,
                            semester=2
                        ).first()
                        if existing_cal:
                            existing_cal.calificacion = float(semester_2)
                        else:
                            cal = Calificacion(
                                enrollment_id=enrollment_id,
                                student_id=enrollment.student_id,
                                subject_id=enrollment.subject_id,
                                teacher_id=teacher.id,
                                semester=2,
                                calificacion=float(semester_2)
                            )
                            db.session.add(cal)
                    
                    if semester_3:
                        enrollment.semester_3 = float(semester_3)
                        existing_cal = Calificacion.query.filter_by(
                            enrollment_id=enrollment_id,
                            student_id=enrollment.student_id,
                            subject_id=enrollment.subject_id,
                            teacher_id=teacher.id,
                            semester=3
                        ).first()
                        if existing_cal:
                            existing_cal.calificacion = float(semester_3)
                        else:
                            cal = Calificacion(
                                enrollment_id=enrollment_id,
                                student_id=enrollment.student_id,
                                subject_id=enrollment.subject_id,
                                teacher_id=teacher.id,
                                semester=3,
                                calificacion=float(semester_3)
                            )
                            db.session.add(cal)
                    
                    db.session.commit()
                    flash('Calificaciones registradas exitosamente', 'success')
                else:
                    flash('Error: Inscripción no encontrada', 'error')
            
            elif action == 'add_student':
                student_id = request.form.get('student_id')
                grade_id = request.form.get('grade_id')
                subject_id = request.form.get('subject_id')
                
                student = Student.query.get(student_id)
                if student:
                    # Check if enrollment already exists
                    existing = Enrollment.query.filter_by(student_id=student_id, teacher_id=teacher.id).first()
                    if not existing:
                        enrollment = Enrollment(
                            student_id=student_id,
                            teacher_id=teacher.id,
                            subject_id=subject_id,
                            grade_id=grade_id,
                            status='enrolled'
                        )
                        db.session.add(enrollment)
                        db.session.commit()
                        flash(f'Estudiante {student.user.name} agregado exitosamente', 'success')
                    else:
                        flash('El estudiante ya está inscrito contigo', 'warning')
                else:
                    flash('Estudiante no encontrado', 'error')
            
            elif action == 'delete_enrollment':
                enrollment_id = request.form.get('enrollment_id')
                enrollment = Enrollment.query.get(enrollment_id)
                if enrollment:
                    db.session.delete(enrollment)
                    db.session.commit()
                    flash('Estudiante removido exitosamente', 'success')
                else:
                    flash('Inscripción no encontrada', 'error')
            
            elif action == 'create_student_with_grades':
                name = request.form.get('name')
                apellido_paterno = request.form.get('apellido_paterno')
                apellido_materno = request.form.get('apellido_materno')
                grade_id = request.form.get('grade_id')
                subject_id = request.form.get('subject_id')
                semester_1 = request.form.get('semester_1')
                semester_2 = request.form.get('semester_2')
                semester_3 = request.form.get('semester_3')
                
                # Create new user
                email = request.form.get('email', f'{name.lower().replace(" ", ".")}.{apellido_paterno.lower()}@student.com')
                existing_email = User.query.filter_by(email=email).first()
                if existing_email:
                    flash('El email ya existe', 'error')
                else:
                    user = User(email=email, name=name, password=hash_password('123456'), role='student')
                    db.session.add(user)
                    db.session.flush()
                    
                    # Create student
                    student_code = f'STU-{name.upper()[:3]}-{date.today().strftime("%Y%m%d")}'
                    student = Student(user_id=user.id, student_code=student_code, grade_id=grade_id, 
                                    enrollment_date=date.today(), apellido_paterno=apellido_paterno, 
                                    apellido_materno=apellido_materno)
                    db.session.add(student)
                    db.session.flush()
                    
                    # Create enrollment with grades
                    enrollment = Enrollment(
                        student_id=student.id,
                        teacher_id=teacher.id,
                        subject_id=subject_id,
                        grade_id=grade_id,
                        status='enrolled',
                        semester_1=float(semester_1) if semester_1 else None,
                        semester_2=float(semester_2) if semester_2 else None,
                        semester_3=float(semester_3) if semester_3 else None
                    )
                    db.session.add(enrollment)
                    db.session.flush()
                    
                    # Also create calificaciones for each semester
                    if semester_1:
                        cal = Calificacion(
                            enrollment_id=enrollment.id,
                            student_id=student.id,
                            subject_id=subject_id,
                            teacher_id=teacher.id,
                            semester=1,
                            calificacion=float(semester_1)
                        )
                        db.session.add(cal)
                    
                    if semester_2:
                        cal = Calificacion(
                            enrollment_id=enrollment.id,
                            student_id=student.id,
                            subject_id=subject_id,
                            teacher_id=teacher.id,
                            semester=2,
                            calificacion=float(semester_2)
                        )
                        db.session.add(cal)
                    
                    if semester_3:
                        cal = Calificacion(
                            enrollment_id=enrollment.id,
                            student_id=student.id,
                            subject_id=subject_id,
                            teacher_id=teacher.id,
                            semester=3,
                            calificacion=float(semester_3)
                        )
                        db.session.add(cal)
                    
                    db.session.commit()
                    flash(f'Estudiante {name} creado y calificaciones guardadas exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('teacher_grades'))
    
    return render_template('teacher_grades.html', grades_data=grades_data, all_grades=all_grades, all_subjects=Subject.query.all())


@app.route('/teacher/attendance', methods=['GET', 'POST'])
@login_required
def teacher_attendance():
    if current_user.role != 'teacher':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        flash('Profesor no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all enrollments for this teacher
    all_enrollments = Enrollment.query.filter_by(teacher_id=teacher.id).all()
    
    # Get only enrollments from this teacher's courses, grouped by grade
    grades_data = {}
    for enrollment in all_enrollments:
        grade = enrollment.grade
        if grade.id not in grades_data:
            # Get only enrollments from THIS TEACHER in this grade
            enrollments = Enrollment.query.filter_by(teacher_id=teacher.id, grade_id=grade.id).all()
            
            # Calculate attendance statistics for each enrollment
            enrollments_with_stats = []
            for enr in enrollments:
                attendance_records = Attendance.query.filter_by(enrollment_id=enr.id).order_by(Attendance.attendance_date.desc()).all()
                total_records = len(attendance_records)
                present_count = len([a for a in attendance_records if a.status == 'present'])
                absent_count = len([a for a in attendance_records if a.status == 'absent'])
                late_count = len([a for a in attendance_records if a.status == 'late'])
                excused_count = len([a for a in attendance_records if a.status == 'excused'])
                
                attendance_percentage = round((present_count / total_records * 100), 1) if total_records > 0 else 0
                # Get all attendance records sorted by date (most recent first)
                all_attendance = sorted(attendance_records, key=lambda x: x.attendance_date, reverse=True)
                recent_attendance = all_attendance[:10]  # Show last 10
                
                enrollments_with_stats.append({
                    'enrollment': enr,
                    'total_records': total_records,
                    'present_count': present_count,
                    'absent_count': absent_count,
                    'late_count': late_count,
                    'excused_count': excused_count,
                    'attendance_percentage': attendance_percentage,
                    'recent_attendance': recent_attendance,
                    'all_attendance': all_attendance  # Add all records for expanded view
                })
            
            grades_data[grade.id] = {
                'grade': grade,
                'enrollments': enrollments_with_stats
            }
    
    if request.method == 'POST':
        try:
            enrollment_id = request.form.get('enrollment_id')
            attendance_date = request.form.get('attendance_date')
            status = request.form.get('status')
            
            # Validate that status is provided
            if not status:
                flash('Error: Por favor selecciona un estado de asistencia', 'error')
                return redirect(url_for('teacher_attendance'))
            
            # If no date provided, use today's date
            if not attendance_date:
                attendance_date = date.today()
            
            existing = Attendance.query.filter_by(enrollment_id=enrollment_id, attendance_date=attendance_date).first()
            if existing:
                existing.status = status
            else:
                attendance = Attendance(enrollment_id=enrollment_id, attendance_date=attendance_date, status=status)
                db.session.add(attendance)
            
            db.session.commit()
            flash('Asistencia registrada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('teacher_attendance'))
    
    return render_template('teacher_attendance.html', grades_data=grades_data, today=date.today())


@app.route('/student/my-courses')
@login_required
def student_my_courses():
    if current_user.role != 'student':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Estudiante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all enrollments for this student
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()
    
    # Get schedules for the student's grade
    schedules = Schedule.query.filter_by(grade_id=student.grade_id).all()
    
    # Organize enrollments with their schedules
    courses_data = []
    for enrollment in enrollments:
        teacher = enrollment.teacher
        subject = enrollment.subject
        # Get schedules for this teacher in this grade
        teacher_schedules = [s for s in schedules if s.teacher_id == teacher.id]
        courses_data.append({
            'teacher': teacher,
            'subject': subject,
            'grade': enrollment.grade,
            'schedules': teacher_schedules
        })
    
    return render_template('student_my_courses.html', courses_data=courses_data, student=student)


@app.route('/student/my-grades')
@login_required
def student_my_grades():
    if current_user.role != 'student':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash('Estudiante no encontrado', 'error')
        return redirect(url_for('dashboard'))
    
    # Get all grades from calificaciones table for this student
    calificaciones = Calificacion.query.filter_by(student_id=student.id).order_by(Calificacion.fecha_calificacion.desc()).all()
    
    # Group by subject
    subjects_grades = {}
    total_promedio = 0
    total_calificaciones = 0
    
    for cal in calificaciones:
        subject_id = cal.subject_id
        if subject_id not in subjects_grades:
            subjects_grades[subject_id] = {
                'subject': cal.subject.name,
                'teacher': cal.teacher,
                'grades': []
            }
        subjects_grades[subject_id]['grades'].append({
            'calificacion': float(cal.calificacion) if cal.calificacion else 0,
            'semester': cal.semester,
            'fecha': cal.fecha_calificacion,
            'nota_texto': cal.nota_texto
        })
        
        if cal.calificacion:
            total_promedio += float(cal.calificacion)
            total_calificaciones += 1
    
    # Convert to list
    grades_data = list(subjects_grades.values())
    
    # Calculate general average
    general_average = round(total_promedio / total_calificaciones, 2) if total_calificaciones > 0 else 0
    
    return render_template('student_my_grades.html', grades_data=grades_data, student=student, general_average=general_average)


@app.route('/admin/credentials', methods=['GET', 'POST'])
@login_required
def admin_credentials():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.get(user_id)
            if not user:
                flash('Usuario no encontrado', 'error')
                return redirect(url_for('admin_credentials'))
            
            # Check if email already exists
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user_id:
                flash('El email ya está en uso', 'error')
                return redirect(url_for('admin_credentials'))
            
            user.email = email
            if password:
                user.password = hash_password(password)
            
            db.session.commit()
            flash(f'Credenciales de {user.name} actualizadas correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('admin_credentials'))
    
    # Get all students with their users
    students = Student.query.all()
    return render_template('admin_credentials.html', students=students)


@app.route('/admin/teacher-credentials', methods=['GET', 'POST'])
@login_required
def admin_teacher_credentials():
    if current_user.role != 'admin':
        flash('Acceso denegado', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.get(user_id)
            if not user:
                flash('Usuario no encontrado', 'error')
                return redirect(url_for('admin_teacher_credentials'))
            
            # Check if email already exists
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != user_id:
                flash('El email ya está en uso', 'error')
                return redirect(url_for('admin_teacher_credentials'))
            
            user.email = email
            if password:
                user.password = hash_password(password)
            
            db.session.commit()
            flash(f'Credenciales de {user.name} actualizadas correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
        
        return redirect(url_for('admin_teacher_credentials'))
    
    # Get all teachers with their users
    teachers = Teacher.query.all()
    return render_template('admin_teacher_credentials.html', teachers=teachers)
