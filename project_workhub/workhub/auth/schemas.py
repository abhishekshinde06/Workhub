from pydantic import BaseModel, Field
from enum import Enum

class Role(str,Enum) : 
    admin = "admin"
    manager = "manager"
    developer = "developer"
class Gender(str,Enum) : 
    male = "Male"
    Female = "Female"
class CreateUser(BaseModel) :
    name : str
    email_id : str
    mobile_no :str
    username :str
    password :str = Field(min_length=8)
    gender : Gender
    role : Role = Role.developer
class LoginUser(BaseModel):
    username : str
    password : str