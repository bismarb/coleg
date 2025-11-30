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
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    avatar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship('Student', backref='user', uselist=False)
    teachers = db.relationship('Teacher', backref='user', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'avatar': self.avatar,
            'createdAt': self.created_at.isoformat()
        }

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    head = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teachers = db.relationship('Teacher', backref='department')
    subjects = db.relationship('Subject', backref='department')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'head': self.head,
            'createdAt': self.created_at.isoformat()
        }

class AcademicPeriod(db.Model):
    __tablename__ = 'academic_periods'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship('Course', backref='academic_period')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'startDate': self.start_date.isoformat(),
            'endDate': self.end_date.isoformat(),
            'isActive': self.is_active,
            'createdAt': self.created_at.isoformat()
        }

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    student_code = db.Column(db.String(50), unique=True, nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    enrollment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship('Enrollment', backref='student')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'studentCode': self.student_code,
            'grade': self.grade,
            'dateOfBirth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'phone': self.phone,
            'enrollmentDate': self.enrollment_date.isoformat(),
            'status': self.status,
            'createdAt': self.created_at.isoformat()
        }

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    teacher_code = db.Column(db.String(50), unique=True, nullable=False)
    department_id = db.Column(db.String(36), db.ForeignKey('departments.id'))
    specialization = db.Column(db.Text)
    hire_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship('Course', backref='teacher')

    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'teacherCode': self.teacher_code,
            'departmentId': self.department_id,
            'specialization': self.specialization,
            'hireDate': self.hire_date.isoformat(),
            'status': self.status,
            'phone': self.phone,
            'createdAt': self.created_at.isoformat()
        }

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=3)
    department_id = db.Column(db.String(36), db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship('Course', backref='subject')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'credits': self.credits,
            'departmentId': self.department_id,
            'createdAt': self.created_at.isoformat()
        }

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id = db.Column(db.String(36), db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.String(36), db.ForeignKey('teachers.id'), nullable=False)
    academic_period_id = db.Column(db.String(36), db.ForeignKey('academic_periods.id'), nullable=False)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    schedule = db.Column(db.Text)
    max_students = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship('Enrollment', backref='course')

    def to_dict(self):
        return {
            'id': self.id,
            'subjectId': self.subject_id,
            'teacherId': self.teacher_id,
            'academicPeriodId': self.academic_period_id,
            'courseCode': self.course_code,
            'schedule': self.schedule,
            'maxStudents': self.max_students,
            'status': self.status,
            'createdAt': self.created_at.isoformat()
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String(36), db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.String(36), db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled')
    final_grade = db.Column(db.Numeric(5, 2))

    grades = db.relationship('Grade', backref='enrollment')
    attendance = db.relationship('Attendance', backref='enrollment')

    def to_dict(self):
        return {
            'id': self.id,
            'studentId': self.student_id,
            'courseId': self.course_id,
            'enrollmentDate': self.enrollment_date.isoformat(),
            'status': self.status,
            'finalGrade': str(self.final_grade) if self.final_grade else None
        }

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    enrollment_id = db.Column(db.String(36), db.ForeignKey('enrollments.id'), nullable=False)
    assessment_type = db.Column(db.String(50), nullable=False)
    assessment_name = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.Numeric(5, 2), nullable=False)
    max_grade = db.Column(db.Numeric(5, 2), default=100)
    weight = db.Column(db.Numeric(5, 2))
    assessment_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'enrollmentId': self.enrollment_id,
            'assessmentType': self.assessment_type,
            'assessmentName': self.assessment_name,
            'grade': str(self.grade),
            'maxGrade': str(self.max_grade),
            'weight': str(self.weight) if self.weight else None,
            'assessmentDate': self.assessment_date.isoformat(),
            'createdAt': self.created_at.isoformat()
        }

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    enrollment_id = db.Column(db.String(36), db.ForeignKey('enrollments.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'enrollmentId': self.enrollment_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat()
        }
