import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText

from fastapi import HTTPException
load_dotenv()
# dotenv =  It's a python package that help us to hide sensitive data  like api key database url 

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_reset_link(user_email : str,reset_link : str) :
    """
    This function helps to send the reset link to the user email but how let's understand
    1. it take reciver email and link(reset_password_api+token)
    2. MIMEText => it converts over email to email body headers (From, To, Subject) and body so that we can send this .
    3. we open the smtp sever with SMTP_SERVER , SMRP_PORT=1545 now with the help of STARTLIS it make over connection secure anad incrypted
    4. finally we send it
    """ 
    msg = MIMEText(f"click here to reset your password {reset_link}")
    msg["subject"] = "Password reset link"
    msg["From"] = SMTP_USER
    msg["To"] = user_email
    try :
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            return f"reset link sent on email"
    except Exception as e : 
      raise HTTPException(
        status_code=500,
        detail=f"Failed to send reset link: {str(e)}"
    )
