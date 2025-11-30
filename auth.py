from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash a password using Werkzeug"""
    return generate_password_hash(password)

def check_password(password, hash):
    """Check if a password matches its hash"""
    return check_password_hash(hash, password)
