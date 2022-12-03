from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#from app import login

db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def set_password(self, password): #convertir a codigo hash la contraseña que el usuario a escrito por el login
        self.password_hash = generate_password_hash(password)  

    def check_password(self, password): #REVISAR SI LAS 2 CONTRASEÑAS, SON IGUALES
        return check_password_hash(self.password_hash, password) 


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
            
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    def reset_permissions(self):
        self.permissions = 0
    def has_permission(self, perm):
        return self.permissions & perm == perm

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


""" 
@login.user_loader
def load_user(id): #recibe el id del usuario logueado
    return User.query.get(int(id)) #SELECT *FROM user WHERE id = id; """
      