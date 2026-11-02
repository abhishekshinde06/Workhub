from fastapi import FastAPI
from workhub.db_connection import Base,engine
from workhub.auth import router as auth_router
from workhub.admin import router as admin_router
from workhub .superadmin import router as superadmin_router
from workhub.user_profile import router as user_profile_router
from workhub.projects import router as project_router
from workhub.task import routes as task_router
# New modules added to cover the rest of the SRS (Modules 6-10): Comments,
# Documents, Search, Dashboard and Audit Logs. AI Assistant (Module 11,
# Phase 2) was intentionally left out for now, as requested.
from workhub.comments import router as comment_router
from workhub.documents import router as document_router
from workhub.search import router as search_router
from workhub.dashboard import router as dashboard_router
from workhub.audit import router as audit_router
from workhub.chatbot import router as chatbot_router
app = FastAPI()

"Include => When we make router then we have to run router files b'coz over main logic and code into the router thats why we include router in here so that when we run main over other file will be run"
app.include_router(superadmin_router.router)
app.include_router(auth_router.router)
app.include_router(user_profile_router.router)
app.include_router(admin_router.router)
app.include_router(project_router.router)
app.include_router(task_router.router)
app.include_router(comment_router.router)
app.include_router(document_router.router)
app.include_router(search_router.router)
app.include_router(dashboard_router.router)
app.include_router(audit_router.router)
app.include_router(chatbot_router.router)


