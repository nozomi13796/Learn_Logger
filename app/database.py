from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def init_db(app):
    from .models import User, Post
    engine = create_engine('sqlite:///blog.db')
    SessionLocal = scoped_session(sessionmaker(bind=engine))
    app.session = SessionLocal
    Base.metadata.create_all(bind=engine)
