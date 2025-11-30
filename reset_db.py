#!/usr/bin/env python3
"""Reset database and initialize with proper data"""
import os
from app import app, db
from models import Grade, User, Student, Teacher
from auth import hash_password
from datetime import date

with app.app_context():
    # Drop all tables
    db.drop_all()
    print("✅ Dropped all tables")
    
    # Create all tables
    db.create_all()
    print("✅ Created all tables")
    
    # Add grades
    grades = [
        Grade(name='1° Primaria', level=1),
        Grade(name='2° Primaria', level=2),
        Grade(name='3° Primaria', level=3),
        Grade(name='4° Primaria', level=4),
        Grade(name='5° Primaria', level=5),
        Grade(name='6° Primaria', level=6),
    ]
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
    
    # Add teacher record
    teacher_record = Teacher(
        user_id=teacher.id,
        teacher_code='TCH001',
        specialization='Matemáticas',
        hire_date=date.today()
    )
    db.session.add(teacher_record)
    db.session.flush()
    print("✅ Added teacher record")
    
    # Add student record
    student_grade = Grade.query.first()
    student_record = Student(
        user_id=student_user.id,
        student_code='STU001',
        grade_id=student_grade.id,
        enrollment_date=date.today()
    )
    db.session.add(student_record)
    
    db.session.commit()
    print("✅ Database initialized successfully!")
    
    # Verify
    total_grades = Grade.query.count()
    total_users = User.query.count()
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    print(f"\n✅ Final count:")
    print(f"   Grades: {total_grades}")
    print(f"   Users: {total_users}")
    print(f"   Students: {total_students}")
    print(f"   Teachers: {total_teachers}")
