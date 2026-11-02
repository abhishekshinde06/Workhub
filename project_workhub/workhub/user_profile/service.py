
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.user_profile.schema import UpdateUserDetail


def service_update_detail(request : UpdateUserDetail, current_user : dict , db : Session ) : 
    user_data = db.query(User).filter(User.username == current_user["username"] ).first()
    update_data = request.model_dump(exclude_unset = True)
    for field,value in update_data.items() : 
        setattr(user_data,field,value)
    db.commit()
    db.refresh(user_data)
    return {"message": "Profile updated successfully"}
      
        
def service_get_detail(current_user:dict,db :Session) : 
    user_data = db.query(User).filter(User.username == current_user["username"] ).first()
    return user_data

    

