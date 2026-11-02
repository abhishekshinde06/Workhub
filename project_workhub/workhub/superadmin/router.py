from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from workhub.auth.setting.auth_setting import verify_token
from workhub.db_connection import get_db
from workhub.superadmin import service

router = APIRouter(tags=["superadmin"])


@router.get("/superadmin/users")
def get_all_normal_users(
    db: Session = Depends(get_db), current_superadmin: str = Depends(verify_token)
):
    return service.service_get_all_normal_users(db,current_superadmin)

@router.put("/users/{id}/role")
def make_admin(
    id: int,
    db: Session = Depends(get_db) ,
    current_superadmin: str = Depends(verify_token)
):
    return service.service_make_admin(id, db, current_superadmin)

@router.delete("/superadmin/users/{user_id}")
def delete_normal_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_superadmin: dict = Depends(verify_token),
):
    return service.service_delete_normal_user(user_id,db,current_superadmin)