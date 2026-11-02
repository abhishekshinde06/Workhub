from fastapi import Depends,status, APIRouter
from workhub.admin import service
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags= ["admin"])

@router.get('/users',status_code= 200)
def get_all_users(
    db : Session = Depends(get_db),
    offset : int = 3,limit : int = 3):
    return service.service_get_all_users(db,offset = offset,limit = limit)
    
@router.get("/users/{id}", status_code = 200)
def user(id : int,db : Session = Depends(get_db),current_admin: dict = Depends(verify_token)) : 
    return service.service_user(id,db)
    

@router.delete("/users/{id}")
def delete_user(id :int,db :Session = Depends(get_db),current_admin: dict = Depends(verify_token)) : 
    return service.service_delete_user(id,db)

@router.put("/users/{id}") 
def activate_user(id : int, db : Session = Depends(get_db),current_admin: str = Depends(verify_token)) :
    return service.service_activate_user(id,db,current_admin)
    
   