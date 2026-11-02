📌 WorkHub – Team Collaboration Platform

WorkHub is a scalable backend application that enables organizations to manage users, projects, tasks, documents, and collaboration workflows through REST APIs.
It is designed to simulate a real-world software development environment, covering requirement analysis, architecture design, database schema creation, API implementation, and documentation.

Features

User Management → Admin, Manager, Employee roles with role-based access control

Project Management → Create, update, delete, view, list and search projects

Task Management → Assign tasks, track status/priority/due date, search tasks

Comments → Comment on projects and tasks

Document Management → Upload/download/delete PDF, DOCX, TXT and CSV files

Search → Search projects, tasks, users and documents (one at a time, or all together)

Dashboard → Totals for users, projects, tasks, completed/pending tasks and documents

Audit Logs → Tracks key events (login, logout, registration, project creation, task status changes, document uploads/deletes)

Scalable APIs → RESTful endpoints for seamless integration

Tech Stack
FastAPI – backend framework
## ⚡ Quick Start
```bash
git clone https://github.com/abhishekshinde-hub/work_hub.git
cd work_hub
uv pip install -r requirements.txt
uvicorn main:app --reload
```

PostgreSQL – relational database

Pydantic – schema validation

JWT Authentication – secure access control

Microservices Architecture – modular and scalable design

Project Strucuture
WorkHub/
│
│   ├── auth/          # authentication & role checks
│   ├── admin/          # admin user management
│   ├── superadmin/     # superadmin-only user/role management
│   ├── user_profile/  # logged-in user's own profile
│   ├── projects/       # project CRUD, list, search
│   ├── task/           # task CRUD, status, list, search
│   ├── comments/       # comments on projects/tasks
│   ├── documents/      # document upload/download/list/search
│   ├── search/         # search across all entities
│   ├── dashboard/       # dashboard statistics
│   ├── audit/           # audit log records
│
│── alembic/            # DB migrations
│── requirements.txt   # dependencies
│── main.py            # entry point
│── README.md          # documentation

Not implemented yet
- AI Assistant (SRS Module 11, Phase 2) — left out on purpose for now.
- Automated tests (SRS section 12).

