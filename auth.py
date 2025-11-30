"""
Authentication - Password hashing and verification
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """Hash password"""
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """Verify password"""
    return check_password_hash(password_hash, password)
