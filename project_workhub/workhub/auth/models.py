from workhub.db_connection import Base
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean
# class Role(str, Enum) : 
#     admin = "admin"
#     manager = "manager"
#     developer = "developer"
class User(Base) :
    __tablename__ = 'users'   
    user_id = Column(Integer,primary_key=True,index=True, autoincrement= True)
    name = Column(String,nullable=False)
    email_id = Column(String,unique=True,index= True,nullable = False)
    username = Column(String,unique=True,index = True, nullable = False)
    password = Column(String, nullable = False)
    role = Column(String)
    mobile_no = Column(String,unique=True, nullable = False)
    gender = Column(String, nullable = False )
    is_active = Column(Boolean,default=True,nullable=False)
    refresh_token = relationship("RefreshToken", back_populates= "user")
    project = relationship("Project", back_populates = "manager")

class RefreshToken(Base) : 
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    token = Column(String)
    revoked = Column(Boolean, default=False)
    user = relationship("User", back_populates='refresh_token')
