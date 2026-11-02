from fastapi import APIRouter, Depends
from workhub.auth.models import User
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.user_profile.schema import UpdateUserDetail
from sqlalchemy.orm import Session
from workhub.user_profile import service



router = APIRouter(tags= ["user profile"])


@router.put("/user", status_code = 200)
def update_user_detail(request : UpdateUserDetail,current_user : User = Depends(verify_token),db : Session= Depends(get_db) ) :
    return service.service_update_detail(request,current_user,db)
                
@router.get("/user")
def get_user_detail(current_user:dict =  Depends(verify_token),db : Session = Depends(get_db)) :
    return service.service_get_detail(current_user,db)
    
    
    