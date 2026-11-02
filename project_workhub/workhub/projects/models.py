
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from workhub.db_connection import Base


class Project(Base) :
    __tablename__ = 'projects'
    project_id = Column(Integer,primary_key = True, index = True,autoincrement=True)
    project_name = Column(String,nullable = False)
    description = Column(Text, nullable = False)
    status = Column(String, default="active",nullable = False)
    manager_id  = Column(Integer, ForeignKey('users.user_id'))
    manager = relationship("User", back_populates="project")
