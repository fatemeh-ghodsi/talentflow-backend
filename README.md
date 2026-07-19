> Enterprise-grade recruitment platform backend built with FastAPI, PostgreSQL, Async SQLAlchemy, Docker, and modern backend engineering practices.
---
## ⭐ Key Highlights

- Production-ready FastAPI backend
- JWT Authentication & RBAC
- Async SQLAlchemy + PostgreSQL
- Dockerized Development
- Clean Architecture
- Enterprise-ready Project Structure


# 🚀 Overview
TalentFlow Backend is a production-ready backend platform for recruitment workflows, designed with modern software engineering principles including clean architecture, asynchronous programming, layered application design, and secure REST API development.

---

# 🎯 Design Principles

TalentFlow was designed as a scalable recruitment platform backend following enterprise software engineering practices.

The project emphasizes:

- Clean Architecture
- Asynchronous Programming
- Layered Design
- RESTful API Development
- Secure Authentication & Authorization
- Maintainable and Scalable Codebase

These principles ensure that the project remains maintainable, extensible, and suitable for real-world backend applications.
# ✨ Features

TalentFlow Backend provides a complete backend foundation for a modern recruitment platform.

## 🔐 Authentication & Security

- JWT Authentication
- Secure Password Hashing (bcrypt)
- Access & Refresh Token Support
- OAuth2 Password Flow
- Protected API Endpoints
- Authentication Middleware

---
## 👥 User Management

- Secure User Registration
- JWT-based Authentication
- Role-Based Access Control (RBAC)
- User Profile Management
- Profile Updates
- Account Status Management

---

## 🛡 Role-Based Access Control (RBAC)

TalentFlow supports multiple user roles.

- Administrator
- Recruiter
- Candidate

Each role has isolated permissions to ensure secure access to system resources.

---

## 🏢 Company Management

- Company Profile
- Company Information
- Recruiter Assignment

---

## 📄 Resume Management

Candidates can upload and manage resumes.

Supported features include:

- Resume Upload
- File Validation
- File Storage
- Download Support

---

## 💼 Job Management

Recruiters can manage job postings through REST APIs.

Features include:

- Create Jobs
- Update Jobs
- Delete Jobs
- List Available Jobs
- Job Details

---

## ⚡ Backend Engineering

The project is designed using modern backend development practices.

- Async FastAPI
- Async SQLAlchemy
- Repository Pattern
- Service Layer
- Dependency Injection
- Pydantic Validation
- Clean Architecture

---

## 🗄 Database

- PostgreSQL
- AsyncPG
- Alembic Migration
- Relationship Mapping
- Transaction Management

---

## 🐳 DevOps

- Docker Support
- Docker Compose
- Environment Configuration
- Production-ready Structure

---

## 📚 API Documentation

Interactive API documentation is automatically generated using Swagger UI.

```
http://localhost:8000/docs
```

ReDoc documentation is also available.

```
http://localhost:8000/redoc
```

---

## 🚀 Future Enhancements

AI-powered Resume Screening
Candidate Recommendation
Semantic Search
Background Processing
Email Notifications


---

# 🏗 Architecture

TalentFlow Backend follows a layered architecture inspired by production-ready backend systems.

The application separates business logic, data access, API endpoints, and database models into independent layers to improve scalability, maintainability, and testability.

```
                Client
                   │
            HTTP Request
                   │
            FastAPI Router
                   │
              Service Layer
                   │
          Repository Layer
                   │
        SQLAlchemy Async ORM
                   │
             PostgreSQL
```

## Architecture Principles

The project follows several modern backend engineering principles:

- Separation of Concerns
- Dependency Injection
- Repository Pattern
- Service Layer Pattern
- Asynchronous Programming
- Data Validation using Pydantic
- Database Abstraction
- Clean Project Structure

---

# 📂 Project Structure

```
TalentFlow Backend
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   │
│   ├── api/
│   │   └── routers/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   └── base.py
│   │
│   ├── models/
│   │
│   ├── repositories/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── docs/
│   └── images/
│
├── uploads/
│
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

---

# 🔄 Request Flow

Every request follows the same lifecycle.

```
Client

↓

API Router

↓

Business Service

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

JSON Response
```

This approach keeps the application modular, testable, and easy to extend.

---

# 🧩 Why this Architecture?

Instead of placing all business logic directly inside API routes, TalentFlow separates responsibilities into dedicated layers.

This design provides several advantages:

- Easier maintenance
- Better code readability
- Reusable business logic
- Cleaner API endpoints
- Simplified testing
- Better scalability
- Easier collaboration in larger development teams

The same architecture is commonly used in enterprise backend applications built with FastAPI and other modern Python frameworks.
---

# 🗄 Database Design

TalentFlow uses PostgreSQL as the primary relational database.

The database schema has been designed to ensure data consistency, scalability, and maintainability while supporting future feature expansion.

The project uses **SQLAlchemy Async ORM** together with **Alembic** for schema migration and version control.

---

# Core Entities

The current database contains the following main entities.

| Entity | Description |
|---------|-------------|
| User | Stores authentication and account information |
| Role | Defines application permissions |
| Company | Company profile information |
| Candidate | Candidate profile |
| Resume | Candidate uploaded resumes |
| Job | Job postings |
| Application | Candidate job applications |

---

# Relationships

The project uses relational database modeling with SQLAlchemy ORM.

Examples include:

- One Company → Many Jobs
- One Candidate → Many Applications
- One User → One Role
- One Candidate → Multiple Resume Files

The database design follows normalization principles to reduce redundancy while maintaining performance.

---

# 🔐 Authentication Flow

TalentFlow implements secure JWT authentication.

Authentication process

```

User Login

↓

Verify Credentials

↓

Generate JWT Token

↓

Return Access Token

↓

Authenticated Requests

↓

Protected Endpoints

```

Security features

- Password hashing using bcrypt
- JWT Access Tokens
- OAuth2 Password Flow
- Protected Routes
- Role Validation

---

# 👥 Authorization (RBAC)

TalentFlow uses Role-Based Access Control (RBAC).

Each authenticated user is assigned a role.

Current roles

- Administrator
- Recruiter
- Candidate

Each role has its own permissions and API access.

This architecture makes it easy to introduce new roles without modifying existing business logic.

---

# 📁 Resume Upload

TalentFlow supports secure resume management.

Features

- Resume Upload
- File Validation
- Safe File Naming
- File Storage
- Resume Download

Uploaded files are managed separately from business logic to simplify future migration to cloud storage providers such as AWS S3 or Azure Blob Storage.

---

# 📡 REST API

The backend exposes RESTful APIs following common HTTP standards.

Example endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /auth/login | User Login |
| POST | /auth/register | Register User |
| GET | /users/me | Current User |
| GET | /jobs | List Jobs |
| POST | /jobs | Create Job |
| POST | /upload | Upload Resume |

Interactive API documentation is available through Swagger UI.

```

http://localhost:8000/docs

```

---

# ⚙ Environment Configuration

The application supports multiple environments using environment variables.

Configuration includes

- Database Connection
- JWT Secret Key
- Token Expiration
- Upload Directory
- Docker Configuration

Sensitive values are never stored inside the source code.

Environment variables are managed through

```

.env

```

and

```

.env.example

```

to simplify deployment.
---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure the following tools are installed.

- Python 3.12+
- PostgreSQL
- Docker & Docker Compose
- Git

---

# Installation

Clone the repository

```bash
git clone https://github.com/fatemeh-ghodsi/talentflow-backend.git
```

Navigate to the project

```bash
cd talentflow-backend
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/talentflow
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Database Migration

Run Alembic migrations

```bash
alembic upgrade head
```

Create a new migration

```bash
alembic revision --autogenerate -m "message"
```

---

# Running the Project

Development server

```bash
uvicorn app.main:app --reload
```

Application will be available at

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```



ReDoc

```
http://localhost:8000/redoc
```

---

# Docker

Start services

```bash
docker compose up --build
```

Stop services

```bash
docker compose down
```

---

# Development Practices

The project follows modern backend engineering practices.

- Clean Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Async Programming
- REST API Design
- Environment-based Configuration
- Database Migration with Alembic

---



# Roadmap

### Backend

- ✅ Authentication
- ✅ User Management
- ✅ Resume Upload
- ✅ Docker Deployment

### AI Integration

- Resume Parsing
- Resume Ranking
- Semantic Candidate Search
- Job Recommendation
- AI Interview Assistant
- Skill Matching using NLP

---

# Engineering Highlights

This backend includes practical implementation of:

- FastAPI
- Async SQLAlchemy
- PostgreSQL
- JWT Authentication
- Docker
- Alembic
- RESTful APIs
- Clean Architecture
- Layered Design

# Contact

**Fatemeh Ghodsi**

📧 **Email**  
mailto:fghodsi92@gmail.com

💼 **LinkedIn**  
https://www.linkedin.com/in/fatemehghodsi

💻 **GitHub**  
https://github.com/fatemeh-ghodsi
---

⭐ If you found this project interesting, consider giving it a star.