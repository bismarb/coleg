"""
Models - Database Schema for School Management System
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)
    level = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    student_code = db.Column(db.String(50), unique=True, nullable=False)
    grade_id = db.Column(db.String(36), db.ForeignKey('grades.id'), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=True)
    apellido_materno = db.Column(db.String(100), nullable=True)
    enrollment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='student_profile')
    grade = db.relationship('Grade', backref='students')


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True)
    teacher_code = db.Column(db.String(50), unique=True, nullable=False)
    specialization = db.Column(db.Text)
    apellido_paterno = db.Column(db.String(100), nullable=True)
    apellido_materno = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='teacher_profile')


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = db.Column(db.String(36), db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable=False)
    grade_id = db.Column(db.String(36), db.ForeignKey('grades.id'), nullable=False)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    max_students = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subject = db.relationship('Subject', backref='courses')
    teacher = db.relationship('Teacher', backref='courses')
    grade_rel = db.relationship('Grade', backref='courses')


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled')
    final_grade = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')


class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    enrollment_id = db.Column(db.String(36), db.ForeignKey('enrollments.id'), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Numeric(5, 2), nullable=False)
    assessment_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollment = db.relationship('Enrollment', backref='assessments')


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    enrollment_id = db.Column(db.String(36), db.ForeignKey('enrollments.id'), nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    enrollment = db.relationship('Enrollment', backref='attendance_records')


class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    classroom = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course = db.relationship('Course', backref='schedule')
