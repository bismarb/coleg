import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import { eq, and, desc } from "drizzle-orm";
import * as schema from "@shared/schema";

const sql = neon(process.env.DATABASE_URL!);
const db = drizzle(sql, { schema });

// Storage Interface
export interface IStorage {
  // Users
  getUserById(id: string): Promise<schema.User | undefined>;
  getUserByEmail(email: string): Promise<schema.User | undefined>;
  createUser(user: schema.InsertUser): Promise<schema.User>;
  updateUser(id: string, user: Partial<schema.InsertUser>): Promise<schema.User | undefined>;
  
  // Students
  getAllStudents(): Promise<Array<schema.Student & { user: schema.User }>>;
  getStudentById(id: string): Promise<schema.Student | undefined>;
  getStudentByUserId(userId: string): Promise<schema.Student | undefined>;
  createStudent(student: schema.InsertStudent): Promise<schema.Student>;
  updateStudent(id: string, student: Partial<schema.InsertStudent>): Promise<schema.Student | undefined>;
  deleteStudent(id: string): Promise<void>;
  
  // Teachers
  getAllTeachers(): Promise<Array<schema.Teacher & { user: schema.User; department?: schema.Department }>>;
  getTeacherById(id: string): Promise<schema.Teacher | undefined>;
  getTeacherByUserId(userId: string): Promise<schema.Teacher | undefined>;
  createTeacher(teacher: schema.InsertTeacher): Promise<schema.Teacher>;
  updateTeacher(id: string, teacher: Partial<schema.InsertTeacher>): Promise<schema.Teacher | undefined>;
  deleteTeacher(id: string): Promise<void>;
  
  // Departments
  getAllDepartments(): Promise<schema.Department[]>;
  getDepartmentById(id: string): Promise<schema.Department | undefined>;
  createDepartment(department: schema.InsertDepartment): Promise<schema.Department>;
  updateDepartment(id: string, department: Partial<schema.InsertDepartment>): Promise<schema.Department | undefined>;
  deleteDepartment(id: string): Promise<void>;
  
  // Subjects
  getAllSubjects(): Promise<schema.Subject[]>;
  getSubjectById(id: string): Promise<schema.Subject | undefined>;
  createSubject(subject: schema.InsertSubject): Promise<schema.Subject>;
  updateSubject(id: string, subject: Partial<schema.InsertSubject>): Promise<schema.Subject | undefined>;
  deleteSubject(id: string): Promise<void>;
  
  // Academic Periods
  getAllAcademicPeriods(): Promise<schema.AcademicPeriod[]>;
  getActivePeriod(): Promise<schema.AcademicPeriod | undefined>;
  createAcademicPeriod(period: schema.InsertAcademicPeriod): Promise<schema.AcademicPeriod>;
  updateAcademicPeriod(id: string, period: Partial<schema.InsertAcademicPeriod>): Promise<schema.AcademicPeriod | undefined>;
  
  // Courses
  getAllCourses(): Promise<Array<schema.Course & { subject: schema.Subject; teacher: schema.Teacher & { user: schema.User } }>>;
  getCourseById(id: string): Promise<schema.Course | undefined>;
  createCourse(course: schema.InsertCourse): Promise<schema.Course>;
  updateCourse(id: string, course: Partial<schema.InsertCourse>): Promise<schema.Course | undefined>;
  deleteCourse(id: string): Promise<void>;
  
  // Enrollments
  getEnrollmentsByCourse(courseId: string): Promise<schema.Enrollment[]>;
  getEnrollmentsByStudent(studentId: string): Promise<schema.Enrollment[]>;
  createEnrollment(enrollment: schema.InsertEnrollment): Promise<schema.Enrollment>;
  updateEnrollment(id: string, enrollment: Partial<schema.InsertEnrollment>): Promise<schema.Enrollment | undefined>;
  
  // Grades
  getAllGrades(): Promise<Array<schema.Grade & { enrollment: schema.Enrollment & { student: schema.Student & { user: schema.User }; course: schema.Course & { subject: schema.Subject } } }>>;
  getGradesByEnrollment(enrollmentId: string): Promise<schema.Grade[]>;
  createGrade(grade: schema.InsertGrade): Promise<schema.Grade>;
  updateGrade(id: string, grade: Partial<schema.InsertGrade>): Promise<schema.Grade | undefined>;
  deleteGrade(id: string): Promise<void>;
  
  // Dashboard Statistics
  getStatistics(): Promise<{
    totalStudents: number;
    totalTeachers: number;
    activeCourses: number;
    totalDepartments: number;
  }>;
}

// PostgreSQL Storage Implementation
export class PostgresStorage implements IStorage {
  // Users
  async getUserById(id: string) {
    const [user] = await db.select().from(schema.users).where(eq(schema.users.id, id));
    return user;
  }

  async getUserByEmail(email: string) {
    const [user] = await db.select().from(schema.users).where(eq(schema.users.email, email));
    return user;
  }

  async createUser(insertUser: schema.InsertUser) {
    const [user] = await db.insert(schema.users).values(insertUser).returning();
    return user;
  }

  async updateUser(id: string, updateData: Partial<schema.InsertUser>) {
    const [user] = await db.update(schema.users).set(updateData).where(eq(schema.users.id, id)).returning();
    return user;
  }

  // Students
  async getAllStudents() {
    return await db
      .select()
      .from(schema.students)
      .leftJoin(schema.users, eq(schema.students.userId, schema.users.id))
      .then(results => results.map(r => ({ ...r.students, user: r.users! })));
  }

  async getStudentById(id: string) {
    const [student] = await db.select().from(schema.students).where(eq(schema.students.id, id));
    return student;
  }

  async getStudentByUserId(userId: string) {
    const [student] = await db.select().from(schema.students).where(eq(schema.students.userId, userId));
    return student;
  }

  async createStudent(student: schema.InsertStudent) {
    const [newStudent] = await db.insert(schema.students).values(student).returning();
    return newStudent;
  }

  async updateStudent(id: string, student: Partial<schema.InsertStudent>) {
    const [updated] = await db.update(schema.students).set(student).where(eq(schema.students.id, id)).returning();
    return updated;
  }

  async deleteStudent(id: string) {
    await db.delete(schema.students).where(eq(schema.students.id, id));
  }

  // Teachers
  async getAllTeachers() {
    return await db
      .select()
      .from(schema.teachers)
      .leftJoin(schema.users, eq(schema.teachers.userId, schema.users.id))
      .leftJoin(schema.departments, eq(schema.teachers.departmentId, schema.departments.id))
      .then(results => results.map(r => ({
        ...r.teachers,
        user: r.users!,
        department: r.departments || undefined
      })));
  }

  async getTeacherById(id: string) {
    const [teacher] = await db.select().from(schema.teachers).where(eq(schema.teachers.id, id));
    return teacher;
  }

  async getTeacherByUserId(userId: string) {
    const [teacher] = await db.select().from(schema.teachers).where(eq(schema.teachers.userId, userId));
    return teacher;
  }

  async createTeacher(teacher: schema.InsertTeacher) {
    const [newTeacher] = await db.insert(schema.teachers).values(teacher).returning();
    return newTeacher;
  }

  async updateTeacher(id: string, teacher: Partial<schema.InsertTeacher>) {
    const [updated] = await db.update(schema.teachers).set(teacher).where(eq(schema.teachers.id, id)).returning();
    return updated;
  }

  async deleteTeacher(id: string) {
    await db.delete(schema.teachers).where(eq(schema.teachers.id, id));
  }

  // Departments
  async getAllDepartments() {
    return await db.select().from(schema.departments);
  }

  async getDepartmentById(id: string) {
    const [dept] = await db.select().from(schema.departments).where(eq(schema.departments.id, id));
    return dept;
  }

  async createDepartment(department: schema.InsertDepartment) {
    const [newDept] = await db.insert(schema.departments).values(department).returning();
    return newDept;
  }

  async updateDepartment(id: string, department: Partial<schema.InsertDepartment>) {
    const [updated] = await db.update(schema.departments).set(department).where(eq(schema.departments.id, id)).returning();
    return updated;
  }

  async deleteDepartment(id: string) {
    await db.delete(schema.departments).where(eq(schema.departments.id, id));
  }

  // Subjects
  async getAllSubjects() {
    return await db.select().from(schema.subjects);
  }

  async getSubjectById(id: string) {
    const [subject] = await db.select().from(schema.subjects).where(eq(schema.subjects.id, id));
    return subject;
  }

  async createSubject(subject: schema.InsertSubject) {
    const [newSubject] = await db.insert(schema.subjects).values(subject).returning();
    return newSubject;
  }

  async updateSubject(id: string, subject: Partial<schema.InsertSubject>) {
    const [updated] = await db.update(schema.subjects).set(subject).where(eq(schema.subjects.id, id)).returning();
    return updated;
  }

  async deleteSubject(id: string) {
    await db.delete(schema.subjects).where(eq(schema.subjects.id, id));
  }

  // Academic Periods
  async getAllAcademicPeriods() {
    return await db.select().from(schema.academicPeriods).orderBy(desc(schema.academicPeriods.startDate));
  }

  async getActivePeriod() {
    const [period] = await db.select().from(schema.academicPeriods).where(eq(schema.academicPeriods.isActive, true));
    return period;
  }

  async createAcademicPeriod(period: schema.InsertAcademicPeriod) {
    const [newPeriod] = await db.insert(schema.academicPeriods).values(period).returning();
    return newPeriod;
  }

  async updateAcademicPeriod(id: string, period: Partial<schema.InsertAcademicPeriod>) {
    const [updated] = await db.update(schema.academicPeriods).set(period).where(eq(schema.academicPeriods.id, id)).returning();
    return updated;
  }

  // Courses
  async getAllCourses() {
    return await db
      .select()
      .from(schema.courses)
      .leftJoin(schema.subjects, eq(schema.courses.subjectId, schema.subjects.id))
      .leftJoin(schema.teachers, eq(schema.courses.teacherId, schema.teachers.id))
      .leftJoin(schema.users, eq(schema.teachers.userId, schema.users.id))
      .then(results => results.map(r => ({
        ...r.courses,
        subject: r.subjects!,
        teacher: { ...r.teachers!, user: r.users! }
      })));
  }

  async getCourseById(id: string) {
    const [course] = await db.select().from(schema.courses).where(eq(schema.courses.id, id));
    return course;
  }

  async createCourse(course: schema.InsertCourse) {
    const [newCourse] = await db.insert(schema.courses).values(course).returning();
    return newCourse;
  }

  async updateCourse(id: string, course: Partial<schema.InsertCourse>) {
    const [updated] = await db.update(schema.courses).set(course).where(eq(schema.courses.id, id)).returning();
    return updated;
  }

  async deleteCourse(id: string) {
    await db.delete(schema.courses).where(eq(schema.courses.id, id));
  }

  // Enrollments
  async getEnrollmentsByCourse(courseId: string) {
    return await db.select().from(schema.enrollments).where(eq(schema.enrollments.courseId, courseId));
  }

  async getEnrollmentsByStudent(studentId: string) {
    return await db.select().from(schema.enrollments).where(eq(schema.enrollments.studentId, studentId));
  }

  async createEnrollment(enrollment: schema.InsertEnrollment) {
    const [newEnrollment] = await db.insert(schema.enrollments).values(enrollment).returning();
    return newEnrollment;
  }

  async updateEnrollment(id: string, enrollment: Partial<schema.InsertEnrollment>) {
    const [updated] = await db.update(schema.enrollments).set(enrollment).where(eq(schema.enrollments.id, id)).returning();
    return updated;
  }

  // Grades
  async getAllGrades() {
    return await db
      .select()
      .from(schema.grades)
      .leftJoin(schema.enrollments, eq(schema.grades.enrollmentId, schema.enrollments.id))
      .leftJoin(schema.students, eq(schema.enrollments.studentId, schema.students.id))
      .leftJoin(schema.users, eq(schema.students.userId, schema.users.id))
      .leftJoin(schema.courses, eq(schema.enrollments.courseId, schema.courses.id))
      .leftJoin(schema.subjects, eq(schema.courses.subjectId, schema.subjects.id))
      .then(results => results.map(r => ({
        ...r.grades,
        enrollment: {
          ...r.enrollments!,
          student: { ...r.students!, user: r.users! },
          course: { ...r.courses!, subject: r.subjects! }
        }
      })));
  }

  async getGradesByEnrollment(enrollmentId: string) {
    return await db.select().from(schema.grades).where(eq(schema.grades.enrollmentId, enrollmentId));
  }

  async createGrade(grade: schema.InsertGrade) {
    const [newGrade] = await db.insert(schema.grades).values(grade).returning();
    return newGrade;
  }

  async updateGrade(id: string, grade: Partial<schema.InsertGrade>) {
    const [updated] = await db.update(schema.grades).set(grade).where(eq(schema.grades.id, id)).returning();
    return updated;
  }

  async deleteGrade(id: string) {
    await db.delete(schema.grades).where(eq(schema.grades.id, id));
  }

  // Dashboard Statistics
  async getStatistics() {
    const [studentsCount] = await db.select({ count: schema.students.id }).from(schema.students);
    const [teachersCount] = await db.select({ count: schema.teachers.id }).from(schema.teachers);
    const [coursesCount] = await db.select({ count: schema.courses.id }).from(schema.courses).where(eq(schema.courses.status, 'active'));
    const [deptsCount] = await db.select({ count: schema.departments.id }).from(schema.departments);

    return {
      totalStudents: studentsCount?.count || 0,
      totalTeachers: teachersCount?.count || 0,
      activeCourses: coursesCount?.count || 0,
      totalDepartments: deptsCount?.count || 0,
    };
  }
}

export const storage = new PostgresStorage();
