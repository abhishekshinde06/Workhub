from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from workhub.auth.schemas import CreateUser
from sqlalchemy import select
from workhub.auth.setting import auth_setting
from fastapi.security import OAuth2PasswordRequestForm
from workhub.auth.models import RefreshToken, User
from workhub.auth.setting.notify_setting import send_reset_link
from workhub.auth.setting.auth_setting import SECRET_KEY
from workhub.audit.service import record_audit_log
import jwt


async def get_user(username, db):
    """
    when we want to check the user weather user is exist or not
    """

    # we are cheking user from db

    result = await db.execute(select(User).where(User.username == username))
    get_user_data = result.scalar_one_or_none()
    if get_user_data:
        if get_user_data.is_active:
            return get_user_data
        else:
            raise HTTPException(detail="User is deactivated", status_code=403)

    # if user not exist then we will have a error

    raise HTTPException(detail="Username not found", status_code=404)


async def register_user(request: CreateUser, db: Session):
    result = await db.execute(select(User).where(User.username == request.username))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(detail="Username already taken", status_code=400)

    hashed_password = auth_setting.password_hash(request.password)
    user_data = User(
        name=request.name,
        gender=request.gender,
        role=request.role,
        username=request.username,
        password=hashed_password,
        email_id=request.email_id,
        mobile_no=request.mobile_no,
    )
    try:
        db.add(user_data)
        await  db.commit()
        await db.refresh(user_data)
        await record_audit_log(db, "user_registered", user_id=user_data.user_id, username=user_data.username)
        return {"message": "user registration successful"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(detail=f"Error: {str(e)}", status_code=400)


async def user_login(form_data: OAuth2PasswordRequestForm, db: Session):
    """
    Login endpoint.

    - Get user from DB using username
    - Verify password with stored hash
    - If valid, create JWT token (OAuth2)
    - Return token for authentication

    Args:
        form_data: username and password from request
        db: database session

    Returns:
        JWT token string
    """
    print(form_data,"everything is ok or not")
    get_user_data = await get_user(
        form_data.username, db
    )  # get user => that helps us to check we the user exits
    print("is everything ok",get_user_data)
    try :
        auth_setting.verify_password(
            get_user_data.password, form_data.password
        )  # decoding userpassword by the verify password funtion

        user_data = {"sub": get_user_data.username,"role" : get_user_data.role,"user_id" : get_user_data.user_id}

        access_token = auth_setting.create_token(user_data)
        refresh_token = auth_setting.create_token(user_data, 10080)
        r_token_db = RefreshToken(user_id=get_user_data.user_id, token=refresh_token)

        db.add(r_token_db)
        await db.commit()
        await db.refresh(r_token_db)
        record_audit_log(db, "user_login", user_id=get_user_data.user_id, username=get_user_data.username)
        # create token() It take userdata in string so that it can make sub for token sub always be string value
    except Exception as e:
       print("Login error:", repr(e))
       raise
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def serivce_forgot_password(username: str, db: Session):
    """
    Forgot password endpoint.

    - Check if user exists in DB using username
    - Create a short-lived token (15 min)
    - Build reset link with that token
    - Send reset link to user's email

    Args:
        username: user account name
        db: database session

    Returns:
        None (sends email with reset link)
    """

    get_user_data = await get_user(username, db)
    user_data = {"sub": get_user_data.username}
    token = auth_setting.create_token(user_data, 15)
    return await send_reset_link(
        get_user_data.email_id, f"http://127.0.0.1:8000/reset_password?{token}"
    )


async def service_reset_password(token: str, new_password: str, db: Session):
    """
    Reset password endpoint.

    - Verify token and get username
    - Find user in DB
    - Hash the new password
    - Update user record and commit changes

    Args:
        token: JWT token from reset link
        new_password: new password string
        db: database session

    Returns:
        dict with success message
    """
    user_info = auth_setting.verify_token(token)
    user_data = await db.execute(select(User.username == user_info["username"]))
    hashed_password = auth_setting.password_hash(new_password)
    user_data.password = hashed_password
    await db.commit()
    db.refresh(user_data)
    return {"msg": "Password reset successful"}


async def service_refresh_token(refresh_token: str, db: Session):
    db_token = (
        db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    )
    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found")
    db_token.revoked = True  # mark as revoked
    await db.commit()
    record_audit_log(db, "user_logout", user_id=db_token.user_id)
    return {"msg": "Logged out successfully"}


def get_new_access_token(refresh_token: str, db: Session):
    db_token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token, RefreshToken.revoked == False)
        .first()
    )
    if not db_token:
        raise HTTPException(detail="token not found", status_code=404)
    payload = jwt.decode(db_token.token, SECRET_KEY, algorithms=["HS256"])
    payload.pop("exp")
    print(payload)
    access_token = auth_setting.create_token(payload)
    return {"access_token": access_token, "token_type": "bearer"}
