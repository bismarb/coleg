#!/usr/bin/env python
"""
Run script for the Academic Management System
Python/Flask MVC Architecture
Execute this file to start the application in development mode
"""

import os
import sys
from app import app, init_db

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Get configuration
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"\n{'='*60}")
    print(f"🎓 Academia - Sistema de Gestión Académica")
    print(f"🌐 Running on http://0.0.0.0:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📚 MVC Architecture - Python + Flask")
    print(f"{'='*60}\n")
    
    print("📝 Credenciales de prueba:")
    print("  👨‍💼 Admin: admin@example.com / 123456")
    print("  👨‍🏫 Profesor: teacher@example.com / 123456")
    print("  👨‍🎓 Estudiante: student@example.com / 123456\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)
