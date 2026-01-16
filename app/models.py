from app import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True, index=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)

    posts = relationship("Post", back_populates="user")

    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return str(self.uid)
class Post(db.Model):
    __tablename__ = 'posts'

    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    puid = db.Column(db.Integer, db.ForeignKey('users.uid'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    study_minutes = db.Column(db.Integer, default=0)

    user = relationship("User", back_populates="posts")
    tags = relationship("Tag", back_populates="posts", secondary='post_tags')

    def __init__(self, title, description, puid, study_minutes=0):
        self.title = title
        self.description = description
        self.puid = puid
        self.study_minutes = study_minutes

class Tag(db.Model):
    __tablename__ = 'tags'

    tid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    posts = relationship("Post", back_populates="tags", secondary='post_tags')

class PostTags(db.Model):
    __tablename__ = 'post_tags'

    pid = db.Column(db.Integer, db.ForeignKey('posts.pid'), primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey('tags.tid'), primary_key=True)
