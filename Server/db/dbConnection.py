from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, delete, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session

import uuid
import datetime

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
        for a in ans:
            return a
        return None

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

    def __init__(self, filename, email, uid):
        self.uid = uid
        self.filename = filename
        self.upload_time = datetime.datetime.utcnow()
        self.finish_time = None
        self.status = "panding"
        
        if email == None:
            self.user = getUser('Anonymous_user')
        else:
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
    user = getUser(email)
    if not user:
        session.add(User(email))
        session.commit()

def getUser(email):
    return User.getUser(email)

def getUserUploads(email):
    return User.getUser(email).uploads

def deleteUser(email):
    user = getUser(email)
    if not user:
        return
    session.query(Upload).filter(Upload.user_id == user.id).delete()
    session.query(User).filter(User.id == user.id).delete()
    session.commit()
        
    
    
    
def getUpload(uid):
    return Upload.getUpload(uid)

def addUpload(filename, uid, email=None):
    if email != None:
        addUser(email)
        
    session.add(Upload(filename, email, uid))
    session.commit()

def GetPendingUploads():
    ans = session.query(Upload).filter(Upload.status == 'panding').order_by(Upload.upload_time.asc()).all()
    return ans

def SetUploadToProcessing(uid):
    up = getUpload(uid)
    up.status = 'processing'
    session.commit()

def SetUploadToDone(uid):
    up = getUpload(uid)
    up.finish_time = datetime.datetime.utcnow()
    up.status = 'done'
    session.commit()


# setup the connection
engine = create_engine("sqlite:///Server/db/app.db", echo=True)#<------------------------------echo
Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
session = Session()


unknown_user = getUser('Anonymous_user')
if not unknown_user:
    unknown_user = User('Anonymous_user')
    unknown_user.id = -1
    session.add(unknown_user)
    session.commit()

# tests
if __name__ == "__main__":
    #Make User
    addUser("kfir@gmail.com")
    addUpload('first', '10', "tamir@gmail.com")
    # addUser("tamir@gmail.com")
    # addUser("amir@gmail.com")
    
    # #Make Uploads
    # addUpload('first', "tamir@gmail.com")
    # addUpload('sec', "kfir@gmail.com")
    # addUpload('שלישי', "tamir@gmail.com")
    # addUpload('רביעי', "kfir@gmail.com")
    # addUpload('רביעי', "kfir@gmail.com")
    # addUpload('אנונימי')
    
    
    for i in GetPendingUploads():
        print(i)
    # deleteUser("kfir@gmail.com")
    # deleteUser("tamir@gmail.com")
    # deleteUser("amir@gmail.com")
    #commit changes
    