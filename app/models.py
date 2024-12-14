from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(60), unique = True,nullable=False, index=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(),nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, email,username ,password, is_admin=False, is_verified=False):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.is_verified = is_verified
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def update_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.updated_at = datetime.now()
        db.session.commit()

    def __repr__(self):
        return f"User {self.email}"