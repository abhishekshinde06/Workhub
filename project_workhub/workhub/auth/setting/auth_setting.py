from datetime import datetime, timedelta, timezone
import os
import jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from workhub.auth.models import User
from workhub.db_connection import get_db

# SECRET_KEY now comes from the environment (see .env -> JWT_SECRET_KEY) instead
# of being hardcoded, so it isn't sitting in plain text inside the source code.
# Falls back to the old hardcoded value only if the env var is missing, so the
# app still boots on a fresh checkout that forgot to set it (a warning is not
# raised here to keep this file's original behaviour unchanged otherwise).
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "i am abhishek shinde from indore")

Oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")


"""PasswordHasher it is a module that we get pwdlib-argon2 it help us to hash the password so that no one can hack password"""

hash_password = PasswordHasher()


def password_hash(password):
    """
    we call it at user register time
    This funtion help us to hash the password it means convert noraml password in encrypted form
    """
    return hash_password.hash(password)


def verify_password(hashed_password, plan_password):
    """
    This funtion check to user password weather is correct not decrypt user encrypted password
    """
    try:
        hash_password.verify(hashed_password, plan_password)
    except:
        raise HTTPException(detail="password not matched", status_code=401)

#==================================================================================================

def create_token(data: dict, expire_time: timedelta | None = None):
    """
    This funtion we call when login api run , it passes useinfo  in data args Like (username,user_id)
    when it check user data and security key and alogorithm , and help us to create token .

    """
    jwt_payload = data.copy()

    if expire_time:
        token_expire_time = datetime.now(timezone.utc) +  timedelta(minutes=expire_time)
    else:
        token_expire_time = datetime.now(timezone.utc) + timedelta(minutes=35)
    try:
        jwt_payload.update({"exp": token_expire_time})
        return jwt.encode(jwt_payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Token generation failed: {str(e)}"
        )


def verify_token(token: str = Depends(Oauth_scheme)):

    """
    It runs when user try to login at this time it decrypt user access token like expire time and other details
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("user_id")

        if not username:
            raise HTTPException(
                detail="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError as e:
        print("Toked decoded time error =>", e)
        raise HTTPException(status_code=401, detail="Could not validate token")
    return {"username" : username, "role" : role,"user_id" : user_id}


def require_role(*allowed_roles: str):
    """
    Reusable role-check dependency for RBAC (Module 3 of the SRS).

    Usage in a router:
        @router.get("/some-admin-thing")
        def handler(current_user: dict = Depends(require_role("admin", "superadmin"))):
            ...

    It builds on top of `verify_token` (so the caller must still be logged in
    with a valid JWT) and then additionally checks that the caller's role is
    one of `allowed_roles`. This avoids repeating
    `if current_user["role"] != "..."` checks inside every service function.

    Args:
        *allowed_roles: one or more role strings that are allowed through.

    Returns:
        A FastAPI dependency function that returns the decoded token dict
        (username, role, user_id) when the check passes, and raises a 403
        HTTPException otherwise.
    """

    def role_checker(current_user: dict = Depends(verify_token)) -> dict:
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return role_checker

