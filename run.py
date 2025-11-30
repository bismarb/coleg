#!/usr/bin/env python
"""
Run the Flask application
"""

import os
from app import app, init_db

if __name__ == '__main__':
    init_db()
    
    port = int(os.getenv('PORT', 5000))
    print(f"\n🎓 Academia - Sistema de Gestión Académica")
    print(f"🌐 Running on http://0.0.0.0:{port}")
    print(f"📝 Test: admin@example.com / 123456\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
