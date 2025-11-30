from models import db, User, Student, Teacher, Department, Subject, Course, Enrollment, Grade, Attendance, AcademicPeriod

class Storage:
    """Storage layer for database operations"""
    
    def __init__(self):
        pass
    
    # Users
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def create_user(self, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    
    # Students
    def get_all_students(self):
        return Student.query.all()
    
    def get_student(self, student_id):
        return Student.query.get(student_id)
    
    def create_student(self, **kwargs):
        student = Student(**kwargs)
        db.session.add(student)
        db.session.commit()
        return student
    
    def update_student(self, student_id, **kwargs):
        student = Student.query.get(student_id)
        if student:
            for key, value in kwargs.items():
                setattr(student, key, value)
            db.session.commit()
        return student
    
    def delete_student(self, student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
    
    # Teachers
    def get_all_teachers(self):
        return Teacher.query.all()
    
    def get_teacher(self, teacher_id):
        return Teacher.query.get(teacher_id)
    
    def create_teacher(self, **kwargs):
        teacher = Teacher(**kwargs)
        db.session.add(teacher)
        db.session.commit()
        return teacher
    
    def update_teacher(self, teacher_id, **kwargs):
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            for key, value in kwargs.items():
                setattr(teacher, key, value)
            db.session.commit()
        return teacher
    
    def delete_teacher(self, teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            db.session.delete(teacher)
            db.session.commit()
    
    # Departments
    def get_all_departments(self):
        return Department.query.all()
    
    def get_department(self, dept_id):
        return Department.query.get(dept_id)
    
    def create_department(self, **kwargs):
        dept = Department(**kwargs)
        db.session.add(dept)
        db.session.commit()
        return dept
    
    # Subjects
    def get_all_subjects(self):
        return Subject.query.all()
    
    def get_subject(self, subject_id):
        return Subject.query.get(subject_id)
    
    def create_subject(self, **kwargs):
        subject = Subject(**kwargs)
        db.session.add(subject)
        db.session.commit()
        return subject
    
    # Courses
    def get_all_courses(self):
        return Course.query.all()
    
    def get_course(self, course_id):
        return Course.query.get(course_id)
    
    def create_course(self, **kwargs):
        course = Course(**kwargs)
        db.session.add(course)
        db.session.commit()
        return course
    
    def update_course(self, course_id, **kwargs):
        course = Course.query.get(course_id)
        if course:
            for key, value in kwargs.items():
                setattr(course, key, value)
            db.session.commit()
        return course
    
    def delete_course(self, course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
    
    # Enrollments
    def get_enrollments_by_course(self, course_id):
        return Enrollment.query.filter_by(course_id=course_id).all()
    
    def get_enrollments_by_student(self, student_id):
        return Enrollment.query.filter_by(student_id=student_id).all()
    
    def create_enrollment(self, **kwargs):
        enrollment = Enrollment(**kwargs)
        db.session.add(enrollment)
        db.session.commit()
        return enrollment
    
    # Grades
    def get_all_grades(self):
        return Grade.query.all()
    
    def get_grades_by_enrollment(self, enrollment_id):
        return Grade.query.filter_by(enrollment_id=enrollment_id).all()
    
    def create_grade(self, **kwargs):
        grade = Grade(**kwargs)
        db.session.add(grade)
        db.session.commit()
        return grade
    
    def update_grade(self, grade_id, **kwargs):
        grade = Grade.query.get(grade_id)
        if grade:
            for key, value in kwargs.items():
                setattr(grade, key, value)
            db.session.commit()
        return grade
    
    def delete_grade(self, grade_id):
        grade = Grade.query.get(grade_id)
        if grade:
            db.session.delete(grade)
            db.session.commit()
    
    # Attendance
    def get_attendance(self, attendance_id):
        return Attendance.query.get(attendance_id)
    
    def get_attendance_by_enrollment(self, enrollment_id):
        return Attendance.query.filter_by(enrollment_id=enrollment_id).all()
    
    def create_attendance(self, **kwargs):
        attendance = Attendance(**kwargs)
        db.session.add(attendance)
        db.session.commit()
        return attendance
    
    # Statistics
    def get_statistics(self):
        return {
            'totalStudents': Student.query.count(),
            'totalTeachers': Teacher.query.count(),
            'activeCourses': Course.query.filter_by(status='active').count(),
            'totalDepartments': Department.query.count()
        }
