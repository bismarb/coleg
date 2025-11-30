#!/usr/bin/env python
"""
Run script for the Academic Management System
Execute this file to start the Flask application in development mode
"""

import os
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print(f"🚀 Starting Academic Management System...")
    print(f"📍 Running on http://0.0.0.0:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        use_reloader=True
    )
