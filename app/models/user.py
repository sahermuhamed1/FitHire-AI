from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password_hash, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
    
    @staticmethod
    def create(username, email, password, is_admin=False):
        """Create a new user with hashed password"""
        password_hash = generate_password_hash(password)
        return User(None, username, email, password_hash, is_admin)
        
    def check_password(self, password):
        """Validate password against stored hash"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def get_by_id(user_id, db):
        """Retrieve user by ID"""
        user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        
        if user is None:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            password_hash=user['password_hash'],
            is_admin=bool(user['is_admin'])
        )
        
    @staticmethod
    def get_by_email(email, db):
        """Retrieve user by email"""
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        
        if user is None:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            password_hash=user['password_hash'],
            is_admin=bool(user['is_admin'])
        )
        
    @staticmethod
    def get_by_username(username, db):
        """Retrieve user by username"""
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        
        if user is None:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            email=user['email'],
            password_hash=user['password_hash'],
            is_admin=bool(user['is_admin'])
        )