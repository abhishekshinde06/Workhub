from fastapi import  Depends
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session



def get_user(user_id, db):
    """
    when we want to check the user weather user is exist or not
    """

    # we are cheking user from db

    get_user_data = db.query(User).filter(User.user_id == user_id).first()

    if get_user_data:
        return get_user_data

    # if user not exist then we will have a error

    raise HTTPException(detail="Username not found", status_code=404)



def service_get_all_normal_users(
    db: Session , current_superadmin: dict 
):
    """
    Superadmin-only endpoint to list all normal users.

    Steps:
    1. Ensure the caller is a superadmin (via dependency).
    2. Query the DB for all users where role != 'admin' and role != 'superadmin'.
    3. Return the list of normal users.

    """
    print(current_superadmin)
    if current_superadmin["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized as superadmin")

    # 1. Query DB for non-admin users
    users = db.query(User).filter(User.role.notin_(["admin","superadmin"])).all()

    if not users:
        raise HTTPException(status_code=404, detail="No normal users found")

    # 2. Return user list (you can shape the response as needed)
    return {"normal_users": [{"id": u.user_id, "username": u.username} for u in users]}



def service_make_admin(
    id: int,
    db: Session = Depends(get_db),current_superadmin :dict = Depends(verify_token),
):

   
    if current_superadmin["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized as superadmin")
    user = db.query(User).filter(User.user_id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(
            status_code=403, detail="user is not activate ,first activate the user"
        )
    if user.role in ["admin", "superadmin"]:
        raise HTTPException(status_code=400, detail="User is already admin")

    try:
        user.role = "admin"
        db.commit()

        # # Audit log entry
        # role_logger.info(
        #     f"Superadmin '{current_user.username}' changed role of user_id={id} "
        #     f"from '{old_role}' to 'admin'"
        # )

        return {"message": "User promoted to admin successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def service_delete_normal_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_superadmin: dict = Depends(verify_token),
):
    """
    Superadmin-only endpoint to delete a normal user.

    Steps:
    1. Ensure the caller is a superadmin (via dependency).
    2. Query the DB for the user by ID.
    3. Ensure the user exists and is NOT an admin/superadmin.
    4. Delete the user from DB.
    """

    # 1. Check role of current user
    if current_superadmin["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized as superadmin")

    # 2. Query DB for target user
    user = get_user(user_id, db)
    # 3. Prevent deleting admins or superadmins
    if user.role in ["admin", "superadmin"]:
        raise HTTPException(status_code=400, detail="Cannot delete admin or superadmin")

    # 4. Delete user
    db.delete(user)
    db.commit()
    return {"msg": f"User {user.username} deleted successfully"}
