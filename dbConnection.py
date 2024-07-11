from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

import uuid
import datetime
import os

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)

    def __init__(self, id, email):
        self.id = id
        self.email = email
        
    def __repr__(self):
        return f"({self.id},{self.email})"
        
class Upload(Base):
    __tablename__ = 'uploads'
    
    id = Column(Integer, primary_key=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.datetime.utcnow)
    finish_time = Column(DateTime, nullable=True)
    status = Column(String, default='pending')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = Session(bind=engine)
    
    # Optional: Add initial data
    if session.query(User).count() == 0:
        # Adding a sample user
        user = User(email="test@example.com")
        session.add(user)
        session.commit()
    
    session.close()

if __name__ == "__main__":
    engine = create_engine("sqlite:///app.db", echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(User(10, "test@gmail.com"))
    session.commit()
    # Automatically create the database upon import
    if not os.path.exists("app.db"):
        pass
    
