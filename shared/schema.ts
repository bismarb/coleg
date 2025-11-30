import { sql } from "drizzle-orm";
import { pgTable, text, integer, timestamp, boolean, decimal, date, varchar } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// 1. Users Table (Authentication & Roles)
export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  email: varchar("email", { length: 255 }).notNull().unique(),
  password: text("password").notNull(),
  name: text("name").notNull(),
  role: varchar("role", { length: 20 }).notNull(), // 'admin', 'teacher', 'student'
  avatar: text("avatar"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertUserSchema = createInsertSchema(users).omit({ id: true, createdAt: true });
export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

// 2. Departments Table
export const departments = pgTable("departments", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: text("name").notNull(),
  description: text("description"),
  head: text("head"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertDepartmentSchema = createInsertSchema(departments).omit({ id: true, createdAt: true });
export type InsertDepartment = z.infer<typeof insertDepartmentSchema>;
export type Department = typeof departments.$inferSelect;

// 3. Academic Periods Table (Semesters/Years)
export const academicPeriods = pgTable("academic_periods", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: text("name").notNull(),
  startDate: date("start_date").notNull(),
  endDate: date("end_date").notNull(),
  isActive: boolean("is_active").default(false).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertAcademicPeriodSchema = createInsertSchema(academicPeriods).omit({ id: true, createdAt: true });
export type InsertAcademicPeriod = z.infer<typeof insertAcademicPeriodSchema>;
export type AcademicPeriod = typeof academicPeriods.$inferSelect;

// 4. Students Table
export const students = pgTable("students", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").references(() => users.id).notNull(),
  studentCode: varchar("student_code", { length: 50 }).notNull().unique(),
  grade: varchar("grade", { length: 20 }).notNull(),
  dateOfBirth: date("date_of_birth"),
  address: text("address"),
  phone: varchar("phone", { length: 20 }),
  enrollmentDate: date("enrollment_date").notNull(),
  status: varchar("status", { length: 20 }).default("active").notNull(), // 'active', 'inactive', 'at_risk'
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertStudentSchema = createInsertSchema(students).omit({ id: true, createdAt: true });
export type InsertStudent = z.infer<typeof insertStudentSchema>;
export type Student = typeof students.$inferSelect;

// 5. Teachers Table
export const teachers = pgTable("teachers", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  userId: varchar("user_id").references(() => users.id).notNull(),
  teacherCode: varchar("teacher_code", { length: 50 }).notNull().unique(),
  departmentId: varchar("department_id").references(() => departments.id),
  specialization: text("specialization"),
  hireDate: date("hire_date").notNull(),
  status: varchar("status", { length: 20 }).default("active").notNull(), // 'active', 'on_leave', 'inactive'
  phone: varchar("phone", { length: 20 }),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertTeacherSchema = createInsertSchema(teachers).omit({ id: true, createdAt: true });
export type InsertTeacher = z.infer<typeof insertTeacherSchema>;
export type Teacher = typeof teachers.$inferSelect;

// 6. Subjects Table
export const subjects = pgTable("subjects", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  name: text("name").notNull(),
  code: varchar("code", { length: 20 }).notNull().unique(),
  description: text("description"),
  credits: integer("credits").default(3).notNull(),
  departmentId: varchar("department_id").references(() => departments.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertSubjectSchema = createInsertSchema(subjects).omit({ id: true, createdAt: true });
export type InsertSubject = z.infer<typeof insertSubjectSchema>;
export type Subject = typeof subjects.$inferSelect;

// 7. Courses Table (Subject instances in a period)
export const courses = pgTable("courses", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  subjectId: varchar("subject_id").references(() => subjects.id).notNull(),
  teacherId: varchar("teacher_id").references(() => teachers.id).notNull(),
  academicPeriodId: varchar("academic_period_id").references(() => academicPeriods.id).notNull(),
  courseCode: varchar("course_code", { length: 50 }).notNull().unique(),
  schedule: text("schedule"),
  maxStudents: integer("max_students").default(30),
  status: varchar("status", { length: 20 }).default("active").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertCourseSchema = createInsertSchema(courses).omit({ id: true, createdAt: true });
export type InsertCourse = z.infer<typeof insertCourseSchema>;
export type Course = typeof courses.$inferSelect;

// 8. Enrollments Table (Student-Course relationship)
export const enrollments = pgTable("enrollments", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  studentId: varchar("student_id").references(() => students.id).notNull(),
  courseId: varchar("course_id").references(() => courses.id).notNull(),
  enrollmentDate: timestamp("enrollment_date").defaultNow().notNull(),
  status: varchar("status", { length: 20 }).default("enrolled").notNull(), // 'enrolled', 'dropped', 'completed'
  finalGrade: decimal("final_grade", { precision: 5, scale: 2 }),
});

export const insertEnrollmentSchema = createInsertSchema(enrollments).omit({ id: true, enrollmentDate: true });
export type InsertEnrollment = z.infer<typeof insertEnrollmentSchema>;
export type Enrollment = typeof enrollments.$inferSelect;

// 9. Grades Table (Individual assessments)
export const grades = pgTable("grades", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  enrollmentId: varchar("enrollment_id").references(() => enrollments.id).notNull(),
  assessmentType: varchar("assessment_type", { length: 50 }).notNull(), // 'exam', 'homework', 'project', etc.
  assessmentName: text("assessment_name").notNull(),
  grade: decimal("grade", { precision: 5, scale: 2 }).notNull(),
  maxGrade: decimal("max_grade", { precision: 5, scale: 2 }).default("100").notNull(),
  weight: decimal("weight", { precision: 5, scale: 2 }), // Percentage weight towards final grade
  assessmentDate: date("assessment_date").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertGradeSchema = createInsertSchema(grades).omit({ id: true, createdAt: true });
export type InsertGrade = z.infer<typeof insertGradeSchema>;
export type Grade = typeof grades.$inferSelect;

// 10. Attendance Table
export const attendance = pgTable("attendance", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  enrollmentId: varchar("enrollment_id").references(() => enrollments.id).notNull(),
  date: date("date").notNull(),
  status: varchar("status", { length: 20 }).notNull(), // 'present', 'absent', 'late', 'excused'
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertAttendanceSchema = createInsertSchema(attendance).omit({ id: true, createdAt: true });
export type InsertAttendance = z.infer<typeof insertAttendanceSchema>;
export type Attendance = typeof attendance.$inferSelect;

// 11. Schedules Table
export const schedules = pgTable("schedules", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  courseId: varchar("course_id").references(() => courses.id).notNull(),
  dayOfWeek: varchar("day_of_week", { length: 20 }).notNull(), // 'Monday', 'Tuesday', etc.
  startTime: varchar("start_time", { length: 10 }).notNull(), // '08:00'
  endTime: varchar("end_time", { length: 10 }).notNull(), // '09:30'
  classroom: varchar("classroom", { length: 50 }),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertScheduleSchema = createInsertSchema(schedules).omit({ id: true, createdAt: true });
export type InsertSchedule = z.infer<typeof insertScheduleSchema>;
export type Schedule = typeof schedules.$inferSelect;

// 12. Assignments Table
export const assignments = pgTable("assignments", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  courseId: varchar("course_id").references(() => courses.id).notNull(),
  title: text("title").notNull(),
  description: text("description"),
  dueDate: timestamp("due_date").notNull(),
  maxPoints: decimal("max_points", { precision: 5, scale: 2 }).default("100").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertAssignmentSchema = createInsertSchema(assignments).omit({ id: true, createdAt: true });
export type InsertAssignment = z.infer<typeof insertAssignmentSchema>;
export type Assignment = typeof assignments.$inferSelect;
