from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

from werkzeug.security import generate_password_hash , check_password_hash
# from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def getJsonData(self):
        return {
            "username":self.username,
            "name":self.name,
            "email":self.email,
        }

class Workspace(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    admin_username = db.Column(db.String(80), index=True)

    def getJsonData(self):
        return {
            "id": self.id,
            "name": self.name,
            "admin_username": self.admin_username,
        }

class Channel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    admin_username = db.Column(db.String(80), index=True)
    wid = db.Column(db.Integer,index = True)


    def getJsonData(self):
        return {
            "id": self.id,
            "name": self.name,
            "admin_username": self.admin_username,
            "workspace_id": self.wid,
        }

class Chats(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80), index=True)
    username = db.Column(db.String(80), index=True)
    wid = db.Column(db.Integer,index = True)
    channel_id = db.Column(db.Integer,index = True)


    def getJsonData(self):
        return {
            "id": self.id,
            "message": self.message,
            "username": self.username,
            "wid": self.wid,
            "channel_id": self.channel_id,
        }

def create_app():
    current_direc = os.getcwd()
    databasePath = os.path.join(current_direc,"db.sqlite")
    print(databasePath)
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'xyzxyz xyzxyz xyzxyz'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    
    with app.app_context():
        # from .models import user
        db.init_app(app)
        db.create_all()
        print("heelo")

        from .views import views
        from .auth import auth

        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

    return app