from sqlalchemy import Column,Integer,String,DateTime,LargeBinary,ForeignKey
from backend.Database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(LargeBinary,nullable=False)
    created_at = Column(DateTime , default=datetime.utcnow)


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer , ForeignKey('users.id'))
    title = Column(String,nullable=False)
    description = Column(String)
    
class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    request_id = Column(Integer,ForeignKey('requests.id'))
    payment_screenshot = Column(LargeBinary , unique=True,nullable=False)

