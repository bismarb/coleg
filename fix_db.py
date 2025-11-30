#!/usr/bin/env python3
"""Reinitialize database correctly"""
from app import app, db
from models import Grade, User, Student, Teacher, Subject, Course
from auth import hash_password
from datetime import date

with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("✅ All tables created")
    
    # Add 6 grades (1° to 6° Primaria)
    grades = []
    for i in range(1, 7):
        g = Grade(name=f'{i}° Primaria', level=i)
        grades.append(g)
    db.session.add_all(grades)
    db.session.flush()
    print(f"✅ Added {len(grades)} grades")
    
    # Add users
    admin = User(email='admin@example.com', password=hash_password('123456'), name='Admin', role='admin')
    teacher = User(email='teacher@example.com', password=hash_password('123456'), name='Professor', role='teacher')
    student_user = User(email='student@example.com', password=hash_password('123456'), name='Student', role='student')
    
    db.session.add_all([admin, teacher, student_user])
    db.session.flush()
    print("✅ Added 3 users")
    
    # Add teacher
    teacher_record = Teacher(
        user_id=teacher.id,
        teacher_code='TCH001',
        specialization='Matemáticas',
        hire_date=date.today()
    )
    db.session.add(teacher_record)
    db.session.flush()
    print("✅ Added teacher")
    
    # Add student
    student_record = Student(
        user_id=student_user.id,
        student_code='STU001',
        grade_id=grades[0].id,
        enrollment_date=date.today()
    )
    db.session.add(student_record)
    db.session.flush()
    print("✅ Added student")
    
    # Add sample subject
    subject = Subject(name='Matemáticas', code='MAT101', credits=4)
    db.session.add(subject)
    db.session.flush()
    print("✅ Added subject")
    
    # Add sample course
    course = Course(
        subject_id=subject.id,
        teacher_id=teacher_record.id,
        grade_id=grades[0].id,
        course_code='MAT-1A',
        max_students=30
    )
    db.session.add(course)
    
    db.session.commit()
    print("\n✅ DATABASE INITIALIZED SUCCESSFULLY!")
    
    # Verify
    print(f"\n📊 Summary:")
    print(f"   Grades: {Grade.query.count()}")
    print(f"   Users: {User.query.count()}")
    print(f"   Students: {Student.query.count()}")
    print(f"   Teachers: {Teacher.query.count()}")
    print(f"   Subjects: {Subject.query.count()}")
    print(f"   Courses: {Course.query.count()}")
