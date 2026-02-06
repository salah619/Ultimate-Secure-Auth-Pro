# Secure Auth System - Production Ready

Developed by **Engineer Salah Al-Wafi**

## Project Overview
**Ultimate-Secure-Auth-Pro** is a highly secure, production-ready Authentication and Authorization system built with **FastAPI**, **PostgreSQL**, and **Docker**. It implements industry-standard security practices to ensure robust protection against common vulnerabilities.

## Core Features
- **Robust Authentication**: Secure registration and login using **Argon2** password hashing.
- **Token Management**: JWT implementation with Access and Refresh tokens.
- **RBAC (Role-Based Access Control)**: Granular permissions for Guest, User, and Admin roles.
- **Security Hardening**:
  - Rate Limiting (SlowAPI) to prevent brute-force attacks.
  - Security Headers (X-Frame-Options, CSP, HSTS, etc.).
  - CORS configuration.
- **Audit Logs**: Every login attempt and critical action is logged in the database.
- **Containerization**: Fully dockerized environment with `docker-compose`.

## Tech Stack
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Security**: PyJWT, Passlib (Argon2), SlowAPI
- **DevOps**: Docker, Docker Compose

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Ultimate-Secure-Auth-Pro
   ```
2. Create a `.env` file based on `.env.example`.
3. Start the system:
   ```bash
   docker-compose up --build
   ```

## API Documentation
Once the system is running, you can access the interactive API documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Security Checklist Implemented
- [x] Argon2 Password Hashing
- [x] JWT with Expiration & Refresh Strategy
- [x] Role-Based Access Control
- [x] Rate Limiting per IP
- [x] Secure HTTP Headers
- [x] SQL Injection Prevention (via SQLAlchemy)
- [x] Audit Logging for Critical Actions

## Clean Architecture Structure
```text
app/
├── api/          # API Routes & Dependencies
├── core/         # Security, Config & Settings
├── crud/         # Database Operations
├── db/           # Session & Engine
├── models/       # SQLAlchemy Models
└── schemas/      # Pydantic Schemas
```

## License
MIT
