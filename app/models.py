from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import datetime

from .database import Base

class User(Base, UserMixin):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(50), unique=True, index=True)
    password = Column(String(200))
    email = Column(String(50), unique=True, index=True)
    dateofreg = Column(DateTime, default=datetime.datetime.now)

    posts = relationship("Post", back_populates="user")

    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return str(self.uid)
class Post(Base):
    __tablename__ = 'posts'

    pid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(1000))
    puid = Column(Integer, ForeignKey('users.uid'))

    user = relationship("User", back_populates="posts")

    def __init__(self, title, description, puid):
        self.title = title
        self.description = description
        self.puid = puid
