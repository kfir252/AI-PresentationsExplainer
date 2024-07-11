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
    uploads = relationship('Upload', back_populates='user')

    def __init__(self, email):
        self.email = email
        
    def __repr__(self):
        return f"({self.id},{self.email})"
    
    # @staticmethod
    # def getUser(email):
    #     ans = session.query(User).filter(User.email == email)
    #     a = None
    #     for a in ans:
    #         return a
        
class Upload(Base):
    __tablename__ = 'uploads'
    
    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False, primary_key=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime)
    finish_time = Column(DateTime, nullable=True)
    status = Column(String)
    json = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    path = Column(String)
    user = relationship('User', back_populates='uploads')

    def __init__(self, filename, user, path):
        self.uid = str(uuid.uuid4())
        self.filename = filename
        self.upload_time = datetime.datetime.utcnow()
        self.finish_time = None
        self.path = path
        self.status = 'pending'
        self.user = user
        
        self.user_id = None
        if user != None:
            self.user_id = user.id
        
    def __repr__(self):
        return f"({self.id},{self.uid},{self.filename},{self.upload_time},{self.finish_time},{self.status},{self.user_id},{self.user})"

    # @staticmethod
    # def getJsonPath(uid):
    #     ans = session.query(Upload).filter(Upload.uid == uid)
    #     a = None
    #     for a in ans:
    #         return a.path
            
engine = create_engine("sqlite:///db/app.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()



if __name__ == "__main__":
    us = User("test@gmail.com")
    up = Upload('file.pptx',us, 'abc/file.pptx')
         
    session.add(us)
    session.add(up)
    
    session.commit()