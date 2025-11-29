export const STUDENTS = [
  { id: "s1", name: "Ana García", grade: "10A", status: "Activo", attendance: "95%", gpa: 3.8 },
  { id: "s2", name: "Carlos López", grade: "10A", status: "Activo", attendance: "92%", gpa: 3.5 },
  { id: "s3", name: "María Rodríguez", grade: "11B", status: "Activo", attendance: "98%", gpa: 3.9 },
  { id: "s4", name: "Jorge Martínez", grade: "9C", status: "En Riesgo", attendance: "75%", gpa: 2.8 },
  { id: "s5", name: "Lucía Fernández", grade: "11B", status: "Activo", attendance: "96%", gpa: 4.0 },
  { id: "s6", name: "Miguel Ángel", grade: "10A", status: "Inactivo", attendance: "0%", gpa: 0.0 },
];

export const TEACHERS = [
  { id: "t1", name: "Prof. Juan Pérez", department: "Matemáticas", subjects: ["Cálculo", "Álgebra"], status: "Activo" },
  { id: "t2", name: "Dra. Elena Torres", department: "Ciencias", subjects: ["Física", "Química"], status: "Activo" },
  { id: "t3", name: "Lic. Roberto Gómez", department: "Historia", subjects: ["Historia Universal"], status: "Licencia" },
  { id: "t4", name: "Mtra. Sofia Ruiz", department: "Lenguaje", subjects: ["Literatura", "Redacción"], status: "Activo" },
];

export const COURSES = [
  { id: "c1", name: "Matemáticas Avanzadas", code: "MAT301", teacher: "Prof. Juan Pérez", students: 25, schedule: "Lun/Mie 10:00" },
  { id: "c2", name: "Física I", code: "FIS101", teacher: "Dra. Elena Torres", students: 22, schedule: "Mar/Jue 08:00" },
  { id: "c3", name: "Literatura Española", code: "LIT202", teacher: "Mtra. Sofia Ruiz", students: 18, schedule: "Vie 11:00" },
  { id: "c4", name: "Historia del Arte", code: "HIS405", teacher: "Lic. Roberto Gómez", students: 30, schedule: "Lun 14:00" },
];

export const GRADES = [
  { id: "g1", student: "Ana García", course: "Matemáticas Avanzadas", grade: 95, date: "2023-10-15", type: "Examen Parcial" },
  { id: "g2", student: "Carlos López", course: "Matemáticas Avanzadas", grade: 82, date: "2023-10-15", type: "Examen Parcial" },
  { id: "g3", student: "María Rodríguez", course: "Física I", grade: 98, date: "2023-10-12", type: "Laboratorio" },
  { id: "g4", student: "Jorge Martínez", course: "Literatura Española", grade: 65, date: "2023-10-10", type: "Ensayo" },
  { id: "g5", student: "Lucía Fernández", course: "Historia del Arte", grade: 100, date: "2023-10-05", type: "Proyecto Final" },
];

export const STATS = {
  totalStudents: 1250,
  totalTeachers: 84,
  activeCourses: 62,
  passRate: 92,
};

export const ENROLLMENT_DATA = [
  { name: 'Ene', students: 1150 },
  { name: 'Feb', students: 1180 },
  { name: 'Mar', students: 1200 },
  { name: 'Abr', students: 1210 },
  { name: 'May', students: 1230 },
  { name: 'Jun', students: 1250 },
];

export const PERFORMANCE_DATA = [
  { subject: 'Matemáticas', A: 120, B: 110, C: 30, D: 5 },
  { subject: 'Ciencias', A: 90, B: 130, C: 40, D: 10 },
  { subject: 'Lenguaje', A: 150, B: 80, C: 20, D: 2 },
  { subject: 'Historia', A: 110, B: 100, C: 50, D: 15 },
];
