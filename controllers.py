"""
Controllers Layer - Business Logic for Academic Management System
Handles all CRUD operations and business logic
"""

from models import db, User, Student, Teacher, Department, Subject, Course, Enrollment, Grade, Attendance, AcademicPeriod
from datetime import datetime
import uuid


class StudentController:
    """Controller for Student CRUD operations"""
    
    @staticmethod
    def get_all():
        return Student.query.all()
    
    @staticmethod
    def get_by_id(student_id):
        return Student.query.get(student_id)
    
    @staticmethod
    def create(user_id, student_code, grade, **kwargs):
        student = Student(
            id=str(uuid.uuid4()),
            user_id=user_id,
            student_code=student_code,
            grade=grade,
            enrollment_date=kwargs.get('enrollment_date', datetime.utcnow().date()),
            status=kwargs.get('status', 'active'),
            **{k: v for k, v in kwargs.items() if k not in ['enrollment_date', 'status']}
        )
        db.session.add(student)
        db.session.commit()
        return student
    
    @staticmethod
    def update(student_id, **kwargs):
        student = Student.query.get(student_id)
        if student:
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            db.session.commit()
        return student
    
    @staticmethod
    def delete(student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
        return True


class TeacherController:
    """Controller for Teacher CRUD operations"""
    
    @staticmethod
    def get_all():
        return Teacher.query.all()
    
    @staticmethod
    def get_by_id(teacher_id):
        return Teacher.query.get(teacher_id)
    
    @staticmethod
    def create(user_id, teacher_code, **kwargs):
        teacher = Teacher(
            id=str(uuid.uuid4()),
            user_id=user_id,
            teacher_code=teacher_code,
            hire_date=kwargs.get('hire_date', datetime.utcnow().date()),
            status=kwargs.get('status', 'active'),
            **{k: v for k, v in kwargs.items() if k not in ['hire_date', 'status']}
        )
        db.session.add(teacher)
        db.session.commit()
        return teacher
    
    @staticmethod
    def update(teacher_id, **kwargs):
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            for key, value in kwargs.items():
                if hasattr(teacher, key):
                    setattr(teacher, key, value)
            db.session.commit()
        return teacher
    
    @staticmethod
    def delete(teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
        return True


class CourseController:
    """Controller for Course CRUD operations"""
    
    @staticmethod
    def get_all():
        return Course.query.all()
    
    @staticmethod
    def get_by_id(course_id):
        return Course.query.get(course_id)
    
    @staticmethod
    def create(subject_id, teacher_id, academic_period_id, course_code, **kwargs):
        course = Course(
            id=str(uuid.uuid4()),
            subject_id=subject_id,
            teacher_id=teacher_id,
            academic_period_id=academic_period_id,
            course_code=course_code,
            max_students=kwargs.get('max_students', 30),
            status=kwargs.get('status', 'active'),
            **{k: v for k, v in kwargs.items() if k not in ['max_students', 'status']}
        )
        db.session.add(course)
        db.session.commit()
        return course
    
    @staticmethod
    def update(course_id, **kwargs):
        course = Course.query.get(course_id)
        if course:
            for key, value in kwargs.items():
                if hasattr(course, key):
                    setattr(course, key, value)
            db.session.commit()
        return course
    
    @staticmethod
    def delete(course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
        return True


class DepartmentController:
    """Controller for Department CRUD operations"""
    
    @staticmethod
    def get_all():
        return Department.query.all()
    
    @staticmethod
    def get_by_id(dept_id):
        return Department.query.get(dept_id)
    
    @staticmethod
    def create(name, **kwargs):
        dept = Department(
            id=str(uuid.uuid4()),
            name=name,
            **kwargs
        )
        db.session.add(dept)
        db.session.commit()
        return dept
    
    @staticmethod
    def update(dept_id, **kwargs):
        dept = Department.query.get(dept_id)
        if dept:
            for key, value in kwargs.items():
                if hasattr(dept, key):
                    setattr(dept, key, value)
            db.session.commit()
        return dept
    
    @staticmethod
    def delete(dept_id):
        dept = Department.query.get(dept_id)
        if dept:
            db.session.delete(dept)
            db.session.commit()
        return True


class SubjectController:
    """Controller for Subject CRUD operations"""
    
    @staticmethod
    def get_all():
        return Subject.query.all()
    
    @staticmethod
    def get_by_id(subject_id):
        return Subject.query.get(subject_id)
    
    @staticmethod
    def create(name, code, **kwargs):
        subject = Subject(
            id=str(uuid.uuid4()),
            name=name,
            code=code,
            **kwargs
        )
        db.session.add(subject)
        db.session.commit()
        return subject


class GradeController:
    """Controller for Grade CRUD operations"""
    
    @staticmethod
    def get_all():
        return Grade.query.all()
    
    @staticmethod
    def get_by_enrollment(enrollment_id):
        return Grade.query.filter_by(enrollment_id=enrollment_id).all()
    
    @staticmethod
    def create(enrollment_id, assessment_type, grade, **kwargs):
        grade_obj = Grade(
            id=str(uuid.uuid4()),
            enrollment_id=enrollment_id,
            assessment_type=assessment_type,
            assessment_name=kwargs.get('assessment_name', assessment_type),
            grade=grade,
            assessment_date=kwargs.get('assessment_date', datetime.utcnow().date()),
            **{k: v for k, v in kwargs.items() if k not in ['assessment_name', 'assessment_date']}
        )
        db.session.add(grade_obj)
        db.session.commit()
        return grade_obj
    
    @staticmethod
    def update(grade_id, **kwargs):
        grade_obj = Grade.query.get(grade_id)
        if grade_obj:
            for key, value in kwargs.items():
                if hasattr(grade_obj, key):
                    setattr(grade_obj, key, value)
            db.session.commit()
        return grade_obj
    
    @staticmethod
    def delete(grade_id):
        grade_obj = Grade.query.get(grade_id)
        if grade_obj:
            db.session.delete(grade_obj)
            db.session.commit()
        return True


class EnrollmentController:
    """Controller for Enrollment CRUD operations"""
    
    @staticmethod
    def get_by_student(student_id):
        return Enrollment.query.filter_by(student_id=student_id).all()
    
    @staticmethod
    def get_by_course(course_id):
        return Enrollment.query.filter_by(course_id=course_id).all()
    
    @staticmethod
    def create(student_id, course_id, **kwargs):
        enrollment = Enrollment(
            id=str(uuid.uuid4()),
            student_id=student_id,
            course_id=course_id,
            status=kwargs.get('status', 'enrolled')
        )
        db.session.add(enrollment)
        db.session.commit()
        return enrollment


class AttendanceController:
    """Controller for Attendance CRUD operations"""
    
    @staticmethod
    def get_by_enrollment(enrollment_id):
        return Attendance.query.filter_by(enrollment_id=enrollment_id).all()
    
    @staticmethod
    def create(enrollment_id, date, status, **kwargs):
        attendance = Attendance(
            id=str(uuid.uuid4()),
            enrollment_id=enrollment_id,
            date=date,
            status=status,
            **kwargs
        )
        db.session.add(attendance)
        db.session.commit()
        return attendance


class UserController:
    """Controller for User operations"""
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create(email, password, name, role, **kwargs):
        from auth import hash_password
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password=hash_password(password),
            name=name,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user


class DashboardController:
    """Controller for Dashboard statistics"""
    
    @staticmethod
    def get_statistics():
        return {
            'totalStudents': Student.query.count(),
            'totalTeachers': Teacher.query.count(),
            'activeCourses': Course.query.filter_by(status='active').count(),
            'totalDepartments': Department.query.count()
        }
