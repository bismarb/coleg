import type { Express } from "express";
import { type Server } from "http";
import session from "express-session";
import ConnectPgSimple from "connect-pg-simple";
import passport from "./auth";
import { storage } from "./storage";
import { hashPassword, isAuthenticated, hasRole } from "./auth";
import { insertUserSchema, insertStudentSchema, insertTeacherSchema, insertDepartmentSchema, insertSubjectSchema, insertCourseSchema, insertGradeSchema } from "@shared/schema";
import { neon } from "@neondatabase/serverless";

const PgSession = ConnectPgSimple(session);

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Session configuration
  const pgPool = neon(process.env.DATABASE_URL!);
  
  app.use(
    session({
      store: new PgSession({
        conObject: {
          connectionString: process.env.DATABASE_URL,
        },
        createTableIfMissing: true,
      }),
      secret: process.env.SESSION_SECRET || "academic-management-secret-key-change-in-production",
      resave: false,
      saveUninitialized: false,
      cookie: {
        maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
      },
    })
  );

  // Initialize Passport
  app.use(passport.initialize());
  app.use(passport.session());

  // ==================== AUTH ROUTES ====================
  
  // Register
  app.post("/api/auth/register", async (req, res) => {
    try {
      const { email, password, name, role } = req.body;
      
      // Validate input
      if (!email || !password || !name || !role) {
        return res.status(400).json({ message: "Todos los campos son requeridos" });
      }

      // Check if user exists
      const existingUser = await storage.getUserByEmail(email);
      if (existingUser) {
        return res.status(400).json({ message: "El correo ya está registrado" });
      }

      // Hash password and create user
      const hashedPassword = await hashPassword(password);
      const user = await storage.createUser({
        email,
        password: hashedPassword,
        name,
        role,
        avatar: null,
      });

      // Create role-specific record
      if (role === "student") {
        await storage.createStudent({
          userId: user.id,
          studentCode: `STU-${Date.now()}`,
          grade: "Por asignar",
          enrollmentDate: new Date().toISOString().split('T')[0],
          status: "active",
          dateOfBirth: null,
          address: null,
          phone: null,
        });
      } else if (role === "teacher") {
        await storage.createTeacher({
          userId: user.id,
          teacherCode: `TCH-${Date.now()}`,
          hireDate: new Date().toISOString().split('T')[0],
          status: "active",
          departmentId: null,
          specialization: null,
          phone: null,
        });
      }

      // Auto login after registration
      req.login(user, (err) => {
        if (err) {
          return res.status(500).json({ message: "Error al iniciar sesión" });
        }
        
        const { password: _, ...userWithoutPassword } = user;
        res.json({ user: userWithoutPassword });
      });
    } catch (error) {
      console.error("Registration error:", error);
      res.status(500).json({ message: "Error al crear la cuenta" });
    }
  });

  // Login
  app.post("/api/auth/login", (req, res, next) => {
    passport.authenticate("local", (err: any, user: any, info: any) => {
      if (err) {
        return res.status(500).json({ message: "Error en el servidor" });
      }
      
      if (!user) {
        return res.status(401).json({ message: info?.message || "Credenciales incorrectas" });
      }

      req.login(user, (loginErr) => {
        if (loginErr) {
          return res.status(500).json({ message: "Error al iniciar sesión" });
        }
        
        const { password: _, ...userWithoutPassword } = user;
        res.json({ user: userWithoutPassword });
      });
    })(req, res, next);
  });

  // Logout
  app.post("/api/auth/logout", (req, res) => {
    req.logout((err) => {
      if (err) {
        return res.status(500).json({ message: "Error al cerrar sesión" });
      }
      res.json({ message: "Sesión cerrada correctamente" });
    });
  });

  // Get current user
  app.get("/api/auth/me", isAuthenticated, async (req, res) => {
    const user = req.user;
    const { password: _, ...userWithoutPassword } = user as any;
    res.json({ user: userWithoutPassword });
  });

  // ==================== STUDENTS ROUTES ====================
  
  app.get("/api/students", isAuthenticated, async (req, res) => {
    try {
      const students = await storage.getAllStudents();
      res.json(students);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener estudiantes" });
    }
  });

  app.post("/api/students", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      const data = insertStudentSchema.parse(req.body);
      const student = await storage.createStudent(data);
      res.json(student);
    } catch (error) {
      res.status(400).json({ message: "Datos inválidos" });
    }
  });

  app.patch("/api/students/:id", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      const student = await storage.updateStudent(req.params.id, req.body);
      if (!student) {
        return res.status(404).json({ message: "Estudiante no encontrado" });
      }
      res.json(student);
    } catch (error) {
      res.status(500).json({ message: "Error al actualizar estudiante" });
    }
  });

  app.delete("/api/students/:id", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      await storage.deleteStudent(req.params.id);
      res.json({ message: "Estudiante eliminado" });
    } catch (error) {
      res.status(500).json({ message: "Error al eliminar estudiante" });
    }
  });

  // ==================== TEACHERS ROUTES ====================
  
  app.get("/api/teachers", isAuthenticated, async (req, res) => {
    try {
      const teachers = await storage.getAllTeachers();
      res.json(teachers);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener profesores" });
    }
  });

  app.post("/api/teachers", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      const data = insertTeacherSchema.parse(req.body);
      const teacher = await storage.createTeacher(data);
      res.json(teacher);
    } catch (error) {
      res.status(400).json({ message: "Datos inválidos" });
    }
  });

  app.patch("/api/teachers/:id", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      const teacher = await storage.updateTeacher(req.params.id, req.body);
      if (!teacher) {
        return res.status(404).json({ message: "Profesor no encontrado" });
      }
      res.json(teacher);
    } catch (error) {
      res.status(500).json({ message: "Error al actualizar profesor" });
    }
  });

  app.delete("/api/teachers/:id", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      await storage.deleteTeacher(req.params.id);
      res.json({ message: "Profesor eliminado" });
    } catch (error) {
      res.status(500).json({ message: "Error al eliminar profesor" });
    }
  });

  // ==================== DEPARTMENTS ROUTES ====================
  
  app.get("/api/departments", isAuthenticated, async (req, res) => {
    try {
      const departments = await storage.getAllDepartments();
      res.json(departments);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener departamentos" });
    }
  });

  app.post("/api/departments", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      const data = insertDepartmentSchema.parse(req.body);
      const department = await storage.createDepartment(data);
      res.json(department);
    } catch (error) {
      res.status(400).json({ message: "Datos inválidos" });
    }
  });

  // ==================== SUBJECTS ROUTES ====================
  
  app.get("/api/subjects", isAuthenticated, async (req, res) => {
    try {
      const subjects = await storage.getAllSubjects();
      res.json(subjects);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener asignaturas" });
    }
  });

  app.post("/api/subjects", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      const data = insertSubjectSchema.parse(req.body);
      const subject = await storage.createSubject(data);
      res.json(subject);
    } catch (error) {
      res.status(400).json({ message: "Datos inválidos" });
    }
  });

  // ==================== COURSES ROUTES ====================
  
  app.get("/api/courses", isAuthenticated, async (req, res) => {
    try {
      const courses = await storage.getAllCourses();
      res.json(courses);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener cursos" });
    }
  });

  app.post("/api/courses", isAuthenticated, hasRole("admin", "teacher"), async (req, res) => {
    try {
      const data = insertCourseSchema.parse(req.body);
      const course = await storage.createCourse(data);
      res.json(course);
    } catch (error) {
      res.status(400).json({ message: "Datos inválidos" });
    }
  });

  app.patch("/api/courses/:id", isAuthenticated, hasRole("admin", "teacher"), async (req, res) => {
    try {
      const course = await storage.updateCourse(req.params.id, req.body);
      if (!course) {
        return res.status(404).json({ message: "Curso no encontrado" });
      }
      res.json(course);
    } catch (error) {
      res.status(500).json({ message: "Error al actualizar curso" });
    }
  });

  app.delete("/api/courses/:id", isAuthenticated, hasRole("admin"), async (req, res) => {
    try {
      await storage.deleteCourse(req.params.id);
      res.json({ message: "Curso eliminado" });
    } catch (error) {
      res.status(500).json({ message: "Error al eliminar curso" });
    }
  });

  // ==================== GRADES ROUTES ====================
  
  app.get("/api/grades", isAuthenticated, async (req, res) => {
    try {
      const grades = await storage.getAllGrades();
      res.json(grades);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener calificaciones" });
    }
  });

  app.post("/api/grades", isAuthenticated, hasRole("admin", "teacher"), async (req, res) => {
    try {
      const data = insertGradeSchema.parse(req.body);
      const grade = await storage.createGrade(data);
      res.json(grade);
    } catch (error) {
      res.status(400).json({ message: "Datos inválidos" });
    }
  });

  app.patch("/api/grades/:id", isAuthenticated, hasRole("admin", "teacher"), async (req, res) => {
    try {
      const grade = await storage.updateGrade(req.params.id, req.body);
      if (!grade) {
        return res.status(404).json({ message: "Calificación no encontrada" });
      }
      res.json(grade);
    } catch (error) {
      res.status(500).json({ message: "Error al actualizar calificación" });
    }
  });

  app.delete("/api/grades/:id", isAuthenticated, hasRole("admin", "teacher"), async (req, res) => {
    try {
      await storage.deleteGrade(req.params.id);
      res.json({ message: "Calificación eliminada" });
    } catch (error) {
      res.status(500).json({ message: "Error al eliminar calificación" });
    }
  });

  // ==================== DASHBOARD STATISTICS ====================
  
  app.get("/api/dashboard/statistics", isAuthenticated, async (req, res) => {
    try {
      const stats = await storage.getStatistics();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Error al obtener estadísticas" });
    }
  });

  return httpServer;
}
