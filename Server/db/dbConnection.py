from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

import uuid
import datetime
import os

Base = declarative_base()



'''
    Database SqlAlchemy Classes:
    ** User
    ** Upload
'''
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    uploads = relationship('Upload', back_populates='user')

    def __init__(self, email):
        self.email = email
        
    def __repr__(self):
        return f"({self.id},{self.email})"
    
    @staticmethod
    def getUser(email):
        ans = session.query(User).filter(User.email == email)
        a = None
        for a in ans:
            return a

class Upload(Base):
    __tablename__ = 'uploads'
    
    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime)
    finish_time = Column(DateTime, nullable=True)
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='uploads')

    def __init__(self, filename, email):
        self.uid = str(uuid.uuid4())
        self.filename = filename
        self.upload_time = datetime.datetime.utcnow()
        self.finish_time = None
        self.status = "panding"
        self.user = User.getUser(email)
        self.user_id = self.user.id
        
    def __repr__(self):
        return f"({self.id},{self.uid},{self.filename},{self.upload_time},{self.finish_time},{self.status},{self.user_id})"

    @staticmethod
    def getUpload(uid):
        ans = session.query(Upload).filter(Upload.uid == uid)
        a = None
        for a in ans:
            return a


#things you can do with just the users email
def addUser(email):
    session.add(User(email))
    session.commit()

def getUser(email):
    return User.getUser(email)

def getUserUploads(email):
    return User.getUser(email).uploads



def addUpload(filename, email):
    session.add(Upload(filename, email))
    session.commit()

def getUpload(uid):
    return Upload.getUpload(uid)


# setup the connection
engine = create_engine("sqlite:///Server/db/app.db", echo=True)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
session = Session()


# tests
if __name__ == "__main__":
    #Make User
    session.add(User("test@gmail.com"))
    
    #Make Uploads
    session.add(Upload('first', "test@gmail.com"))
    session.add(Upload('sec', "test@gmail.com"))
    session.add(Upload('שלישי', "test@gmail.com"))
    session.add(Upload('רביעי', "test@gmail.com"))
    
    #Check On Users Uploads
    print(User.getUser("test@gmail.com").uploads)
    
    #commit changes
    session.commit()
    