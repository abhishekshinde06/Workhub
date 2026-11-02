from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from fastapi import HTTPException, Depends,status


def get_user(id, db) : 

    data = db.query(User).filter(User.user_id == id).first()
    if data : 
        return data
    else : 
        raise HTTPException(detail = "User not found", status_code = status.HTTP_404_NOT_FOUND)


def service_get_all_users(db : Session,offset:int,limit:int):
    user_data  = db.query(User).all()
    if user_data :
        
        return user_data[offset : offset +limit]
    raise HTTPException (detail =  "user not exist", status_code = 404)


def service_user(id : int,db : Session = Depends(get_db)) : 
    user_data = get_user(id, db)
    return user_data

def service_delete_user(id :int,db :Session = Depends(get_db)) : 
    user_data = get_user(id,db)
    if user_data.role in ['superadmin','admin'] :
        raise HTTPException(detail = 'Cannot delete admin or superadmin', status_code = 404)
    db.delete(user_data)
    db.commit()
    return {"message" : "account is deleted"}


def service_activate_user(id : int, db : Session = Depends(get_db),current_admin: str = Depends(verify_token)) :
    
    user_data = db.query(User).filter(User.user_id == id).first()
    if user_data.role in ["superadmin",'admin'] :
        return f"you can not deactivate superadmin or admin"
    try :
        if user_data.is_active == False: 
            user_data.is_active = True
            db.commit()
            db.refresh(user_data)
            return {"message" : "user activated"}
        else :
            user_data.is_active = False
            db.commit()
            db.refresh(user_data)
            return {"message" : "user deactivated"}
    except Exception as e :
        db.rollback()
        print("here is some errors",e)
