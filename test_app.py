#!/usr/bin/env python
"""Quick test of app startup"""
import sys
from app import app, init_db

try:
    print("🧪 Testing app startup...")
    init_db()
    print("✅ Database initialized")
    
    with app.app_context():
        from models import User, Student, Teacher
        users = User.query.count()
        print(f"✅ Users in DB: {users}")
        print("✅ APP READY TO RUN")
        sys.exit(0)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
