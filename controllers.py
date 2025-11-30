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
        try:
            student = Student(
                id=str(uuid.uuid4()),
                user_id=user_id,
                student_code=student_code,
                grade=grade,
                enrollment_date=kwargs.get('enrollment_date', datetime.utcnow().date()),
                status=kwargs.get('status', 'active')
            )
            if 'date_of_birth' in kwargs:
                student.date_of_birth = kwargs['date_of_birth']
            if 'address' in kwargs:
                student.address = kwargs['address']
            if 'phone' in kwargs:
                student.phone = kwargs['phone']
            db.session.add(student)
            db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update(student_id, **kwargs):
        try:
            student = Student.query.get(student_id)
            if student:
                for key, value in kwargs.items():
                    if hasattr(student, key) and key not in ['id', 'created_at']:
                        setattr(student, key, value)
                db.session.commit()
            return student
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete(student_id):
        try:
            student = Student.query.get(student_id)
            if student:
                db.session.delete(student)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            teacher = Teacher(
                id=str(uuid.uuid4()),
                user_id=user_id,
                teacher_code=teacher_code,
                hire_date=kwargs.get('hire_date', datetime.utcnow().date()),
                status=kwargs.get('status', 'active')
            )
            if 'specialization' in kwargs:
                teacher.specialization = kwargs['specialization']
            if 'department_id' in kwargs:
                teacher.department_id = kwargs['department_id']
            if 'phone' in kwargs:
                teacher.phone = kwargs['phone']
            db.session.add(teacher)
            db.session.commit()
            return teacher
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update(teacher_id, **kwargs):
        try:
            teacher = Teacher.query.get(teacher_id)
            if teacher:
                for key, value in kwargs.items():
                    if hasattr(teacher, key) and key not in ['id', 'created_at']:
                        setattr(teacher, key, value)
                db.session.commit()
            return teacher
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete(teacher_id):
        try:
            teacher = Teacher.query.get(teacher_id)
            if teacher:
                db.session.delete(teacher)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            course = Course(
                id=str(uuid.uuid4()),
                subject_id=subject_id,
                teacher_id=teacher_id,
                academic_period_id=academic_period_id,
                course_code=course_code,
                max_students=kwargs.get('max_students', 30),
                status=kwargs.get('status', 'active')
            )
            if 'schedule' in kwargs:
                course.schedule = kwargs['schedule']
            db.session.add(course)
            db.session.commit()
            return course
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update(course_id, **kwargs):
        try:
            course = Course.query.get(course_id)
            if course:
                for key, value in kwargs.items():
                    if hasattr(course, key) and key not in ['id', 'created_at']:
                        setattr(course, key, value)
                db.session.commit()
            return course
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete(course_id):
        try:
            course = Course.query.get(course_id)
            if course:
                db.session.delete(course)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            dept = Department(
                id=str(uuid.uuid4()),
                name=name,
                description=kwargs.get('description'),
                head=kwargs.get('head')
            )
            db.session.add(dept)
            db.session.commit()
            return dept
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update(dept_id, **kwargs):
        try:
            dept = Department.query.get(dept_id)
            if dept:
                for key, value in kwargs.items():
                    if hasattr(dept, key) and key not in ['id', 'created_at']:
                        setattr(dept, key, value)
                db.session.commit()
            return dept
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete(dept_id):
        try:
            dept = Department.query.get(dept_id)
            if dept:
                db.session.delete(dept)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            subject = Subject(
                id=str(uuid.uuid4()),
                name=name,
                code=code,
                description=kwargs.get('description'),
                credits=kwargs.get('credits', 3),
                department_id=kwargs.get('department_id')
            )
            db.session.add(subject)
            db.session.commit()
            return subject
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            grade_obj = Grade(
                id=str(uuid.uuid4()),
                enrollment_id=enrollment_id,
                assessment_type=assessment_type,
                assessment_name=kwargs.get('assessment_name', assessment_type),
                grade=grade,
                assessment_date=kwargs.get('assessment_date', datetime.utcnow().date()),
                max_grade=kwargs.get('max_grade', 100),
                weight=kwargs.get('weight')
            )
            db.session.add(grade_obj)
            db.session.commit()
            return grade_obj
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update(grade_id, **kwargs):
        try:
            grade_obj = Grade.query.get(grade_id)
            if grade_obj:
                for key, value in kwargs.items():
                    if hasattr(grade_obj, key) and key not in ['id', 'created_at']:
                        setattr(grade_obj, key, value)
                db.session.commit()
            return grade_obj
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete(grade_id):
        try:
            grade_obj = Grade.query.get(grade_id)
            if grade_obj:
                db.session.delete(grade_obj)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            enrollment = Enrollment(
                id=str(uuid.uuid4()),
                student_id=student_id,
                course_id=course_id,
                status=kwargs.get('status', 'enrolled'),
                final_grade=kwargs.get('final_grade')
            )
            db.session.add(enrollment)
            db.session.commit()
            return enrollment
        except Exception as e:
            db.session.rollback()
            raise e


class AttendanceController:
    """Controller for Attendance CRUD operations"""
    
    @staticmethod
    def get_by_enrollment(enrollment_id):
        return Attendance.query.filter_by(enrollment_id=enrollment_id).all()
    
    @staticmethod
    def create(enrollment_id, date, status, **kwargs):
        try:
            attendance = Attendance(
                id=str(uuid.uuid4()),
                enrollment_id=enrollment_id,
                date=date,
                status=status,
                notes=kwargs.get('notes')
            )
            db.session.add(attendance)
            db.session.commit()
            return attendance
        except Exception as e:
            db.session.rollback()
            raise e


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
        try:
            from auth import hash_password
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                password=hash_password(password),
                name=name,
                role=role,
                avatar=kwargs.get('avatar')
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e


class DashboardController:
    """Controller for Dashboard statistics"""
    
    @staticmethod
    def get_statistics():
        try:
            return {
                'totalStudents': Student.query.count(),
                'totalTeachers': Teacher.query.count(),
                'activeCourses': Course.query.filter_by(status='active').count(),
                'totalDepartments': Department.query.count()
            }
        except Exception:
            return {
                'totalStudents': 0,
                'totalTeachers': 0,
                'activeCourses': 0,
                'totalDepartments': 0
            }
