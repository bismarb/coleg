# 📚 Sistema de Gestión Académica

Sistema completo de gestión académica desarrollado en **Python/Flask** con autenticación basada en roles, 10 tablas relacionales PostgreSQL y diseño responsivo.

## 🚀 Características

- ✅ **10 Tablas Relacionales**: users, departments, academic_periods, students, teachers, subjects, courses, enrollments, grades, attendance
- ✅ **Autenticación por Roles**: Admin, Teacher, Student
- ✅ **CRUD Completo**: Para todos los módulos académicos
- ✅ **Dashboard con Estadísticas**: Métricas en tiempo real
- ✅ **Interfaz Responsiva**: Diseño con Tailwind CSS
- ✅ **API REST**: Endpoints para integración futura

## 🛠️ Tecnologías

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Base de Datos**: PostgreSQL
- **Frontend**: Jinja2 Templates, Tailwind CSS, Bootstrap
- **Autenticación**: Werkzeug (Password Hashing)

## 📋 Requisitos

- Python 3.11+
- PostgreSQL 12+
- pip

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd academic-management
```

### 2. Crear archivo `.env`

```bash
cp .env.example .env
```

Edita `.env` con tu información:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost/academic_management
SESSION_SECRET=tu-clave-secreta-aqui
FLASK_ENV=development
PORT=5000
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la Aplicación

### Opción 1: Línea de Comando

```bash
python run.py
```

### Opción 2: Visual Studio Code (Recomendado)

1. Abre el proyecto en VS Code
2. Presiona `F5` o ve a Run → Start Debugging
3. Selecciona "Academic Management System"

La aplicación se abrirá en `http://0.0.0.0:5000`

### Opción 3: Con Flask directamente

```bash
flask run
```

## 🔐 Credenciales de Prueba

La aplicación incluye datos de prueba. Al iniciar por primera vez, usa:

- **Admin**: admin@example.com / 123456
- **Teacher**: teacher@example.com / 123456
- **Student**: student@example.com / 123456

## 📊 Base de Datos

### Tablas (10 Total)

1. **users** - Usuarios del sistema
2. **departments** - Departamentos académicos
3. **academic_periods** - Períodos/Semestres
4. **students** - Información de estudiantes
5. **teachers** - Información de profesores
6. **subjects** - Asignaturas/Cursos
7. **courses** - Instancias de cursos
8. **enrollments** - Inscripciones estudiante-curso
9. **grades** - Calificaciones
10. **attendance** - Asistencia

### Crear base de datos

```bash
createdb academic_management
```

## 📂 Estructura del Proyecto

```
.
├── app.py                 # Aplicación Flask principal
├── models.py              # Modelos SQLAlchemy
├── auth.py                # Funciones de autenticación
├── storage.py             # Capa de almacenamiento
├── run.py                 # Script para ejecutar
├── templates/             # Templates Jinja2
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── students.html
│   ├── teachers.html
│   ├── courses.html
│   ├── grades.html
│   └── departments.html
├── static/                # Archivos estáticos
├── .vscode/
│   └── launch.json        # Configuración de debugging
├── .env.example           # Variables de entorno de ejemplo
└── requirements.txt       # Dependencias Python
```

## 🎯 Módulos Principales

### Autenticación (`auth.py`)
- Hash seguro de contraseñas con Werkzeug
- Gestión de sesiones
- Validación de credenciales

### Modelos (`models.py`)
- 10 modelos SQLAlchemy
- Relaciones entre tablas
- Métodos `to_dict()` para serialización

### Almacenamiento (`storage.py`)
- Capa de abstracción de base de datos
- Operaciones CRUD para cada modelo
- Métodos de estadísticas

### Rutas (`app.py`)
- 30+ endpoints REST
- Páginas HTML para el dashboard
- Validación de roles

## 🔄 Flujo de Autenticación

1. Usuario se registra o inicia sesión
2. Contraseña se valida y encripta
3. Sesión se crea en PostgreSQL
4. Usuario recibe acceso basado en su rol
5. Rutas protegidas con `@login_required`

## 📱 Funcionalidades por Rol

### Admin
- ✅ Gestionar estudiantes
- ✅ Gestionar profesores
- ✅ Gestionar departamentos
- ✅ Ver estadísticas completas

### Teacher
- ✅ Ver cursos asignados
- ✅ Registrar calificaciones
- ✅ Ver estudiantes inscritos

### Student
- ✅ Ver cursos inscritos
- ✅ Ver calificaciones
- ✅ Consultar asistencia

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### Error: "Can't connect to PostgreSQL"

Verifica que:
- PostgreSQL esté corriendo
- La DATABASE_URL sea correcta
- La base de datos exista

```bash
psql -l  # Listar bases de datos
```

### Error en VS Code: "Python interpreter not found"

1. Abre la paleta de comandos (Ctrl+Shift+P)
2. Busca "Python: Select Interpreter"
3. Elige el intérprete correcto

## 📝 APIs Disponibles

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Estudiantes
- `GET /api/students` - Listar todos
- `POST /api/students` - Crear nuevo
- `PATCH /api/students/<id>` - Actualizar
- `DELETE /api/students/<id>` - Eliminar

### Profesores
- `GET /api/teachers` - Listar todos
- `POST /api/teachers` - Crear nuevo
- `DELETE /api/teachers/<id>` - Eliminar

### Cursos
- `GET /api/courses` - Listar todos
- `POST /api/courses` - Crear nuevo
- `PATCH /api/courses/<id>` - Actualizar
- `DELETE /api/courses/<id>` - Eliminar

### Calificaciones
- `GET /api/grades` - Listar todas
- `POST /api/grades` - Registrar nueva
- `PATCH /api/grades/<id>` - Actualizar
- `DELETE /api/grades/<id>` - Eliminar

### Dashboard
- `GET /api/dashboard/statistics` - Obtener estadísticas

## 🚀 Despliegue

Para producción:

1. Cambiar `FLASK_ENV` a `production`
2. Usar un servidor WSGI (Gunicorn, uWSGI)
3. Configurar certificados SSL
4. Habilitar CORS si es necesario

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📄 Licencia

MIT License

## 👨‍💻 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**Nota**: Este es un sistema de gestión académica educativo. Para uso en producción, se recomienda agregar medidas de seguridad adicionales como HTTPS, rate limiting y validación de entrada más robusta.
