# 🚀 Workhub – AI-Powered Project & Task Management System

Workhub is an AI-powered project and task management platform built to simplify team collaboration, project tracking, task assignments, and workflow automation.

It combines traditional project management functionality with modern AI capabilities, allowing users to interact with an intelligent assistant to perform project-related operations using natural language.

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- Secure user authentication using JWT.
- Role-based access control.
- User and session management.

### 📁 Project Management
- Create, update, and retrieve projects.
- Manage project details.
- Assign developers to projects.
- Track project progress.

### 📋 Task Management
- Create and manage tasks.
- Assign tasks to developers.
- Update task status and details.
- Track task progress.

### 🤖 AI-Powered Assistant
- Natural language interaction with an AI assistant.
- AI-based project and task operations.
- LLM tool calling for executing application functions.
- Context-aware conversations.
- Conversation history management.

### 🧠 RAG Integration
- Retrieval-Augmented Generation (RAG).
- Context-based information retrieval.
- ChromaDB vector database integration.

### ⚡ Asynchronous Processing
- Async API endpoints using FastAPI.
- Asynchronous database operations where supported.
- Improved handling of concurrent requests.

### 🐳 Docker & Microservices
- Containerized application using Docker.
- Docker Compose for service orchestration.
- Service-based application architecture.
- API Gateway integration.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Authentication | JWT |
| AI Framework | LangChain |
| Agent Orchestration | LangGraph |
| LLM Provider | Groq |
| Vector Database | ChromaDB |
| Containerization | Docker |
| Orchestration | Docker Compose |
| API Documentation | Swagger / OpenAPI |

---

## 🏗️ System Architecture

Workhub uses a modular, service-oriented architecture to separate different business functionalities.

```text
                    Client
                      |
                      v
                 API Gateway
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
  Auth Service   Project Service  Document Service
       |              |              |
       v              v              v
   Auth DB        Project DB      Document DB

       +--------------+--------------+
                      |
                      v
                AI Assistant
                      |
              LangGraph Workflow
                      |
              LangChain Tool Calling
                      |
                Groq LLM
                      |
                RAG Pipeline
                      |
                  ChromaDB
```

### Main Services

- **Auth Service:** Handles authentication and authorization.
- **Project Service:** Manages projects and project assignments.
- **Document Service:** Handles document-related functionality.
- **Audit Service:** Maintains application activity records.
- **Chatbot Service:** Provides AI-powered interactions.
- **Search Service:** Supports search functionality.
- **Dashboard Service:** Provides dashboard-related functionality.
- **API Gateway:** Acts as the entry point for client requests.

---

## 📂 Project Structure

```text
Workhub/
│
├── project_workhub/
│   ├── auth/
│   ├── projects/
│   ├── tasks/
│   ├── admin/
│   ├── chatbot/
│   ├── documents/
│   ├── audit/
│   ├── search/
│   ├── dashboard/
│   │
│   ├── main.py
│   └── db_connection.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

*Note: Update the folder structure to match your final repository before publishing.*

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Workhub.git

cd Workhub
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Linux / macOS**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/workhub_db

SECRET_KEY=your_secret_key

GROQ_API_KEY=your_groq_api_key
```

Add any other environment variables required by your services.

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start the Application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 📖 API Documentation

Workhub uses FastAPI's automatic API documentation.

Once the application is running, access:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 🐳 Running with Docker

Build and start the application using Docker Compose:

```bash
docker compose up --build
```

Run containers in the background:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

Stop all services:

```bash
docker compose down
```

---

## 🎯 Project Goals

The primary goal of Workhub is to make project management more intelligent and efficient by combining backend engineering with AI-driven automation.

The project focuses on:

- Scalable backend development.
- Clean and modular architecture.
- Efficient database management.
- Asynchronous programming.
- AI agent workflows.
- LLM-powered tool execution.
- Context-aware AI interactions.
- Containerized deployment.

---

## 🔮 Future Enhancements

- Advanced multi-agent architecture.
- Automated task assignment using AI.
- Intelligent project recommendations.
- Real-time notifications.
- Advanced analytics and reporting.
- Improved RAG pipeline.
- Production deployment and monitoring.

---

## 👨‍💻 Developer

**Developed by:** Abhishek Shinde

**Role:** Python Backend Developer

**Technologies:** Python | FastAPI | PostgreSQL | LangChain | LangGraph | Docker

---

⭐ If you find this project interesting, feel free to explore the repository and contribute.

**Workhub – Manage Projects Smarter. Collaborate Better. Work Efficiently.**
