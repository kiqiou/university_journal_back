# University Journal Backend

Backend system for managing an electronic university journal, including disciplines, academic sessions, groups, students, and attestation logic.

The system is built with Django REST Framework and JWT authentication and follows a modular domain-driven architecture.

---

# Tech Stack

* Python 3
* Django
* Django REST Framework
* PostgreSQL
* JWT (SimpleJWT)
* Docker / Docker Compose
* Cloudinary (media storage)
* Locust (load testing)

---

# Project Overview

The project is a backend system for an academic journal that manages:

* students and groups
* disciplines and courses
* academic sessions
* attestation and grading system
* authentication and role-based access

The system is designed as a modular Django project with clear separation of business domains.

---

# Architecture

## Core project

```text id="uj-core"
universityjournalback/
- settings.py
- urls.py
- wsgi.py
- asgi.py
```

Responsible for:

* global configuration
* database setup
* JWT configuration
* routing between applications
* media and static configuration

---

# Applications

---

## 1. Authentication app

Responsible for:

* user management
* roles and groups
* authentication (JWT)
* student-related logic

### Key modules:

* models/

  * User (custom user model)
  * Group

* serializers/

  * user serializer
  * group serializer

* views/

  * auth views
  * user views
  * group views

* services/

  * student_service (business logic layer)

* urls/

  * auth routes
  * user routes
  * group routes

---

### Features:

* custom user model (AUTH_USER_MODEL)
* JWT authentication (access + refresh tokens)
* role/group-based access control
* separated domain logic (auth/user/group)
* service layer for business logic

---

## 2. Journal app

Responsible for academic structure:

* disciplines (courses)
* academic sessions

### Structure:

* models/

  * discipline.py
  * session.py

* serializers/

  * discipline serializer
  * session serializer

* views/

  * discipline views
  * session views

* urls/

  * discipline API
  * session API

---

### Features:

* full CRUD for disciplines
* session management
* structured separation by domain
* scalable API design

---

## 3. Attestation app

Responsible for:

* student attestation
* grading system
* evaluation logic

### Structure:

* models.py
* serializers.py
* views.py
* urls.py

---

### Features:

* attestation tracking
* grade management
* integration with journal data
* REST API for evaluation workflows

---

# API Structure

## Authentication

```text id="auth-api"
POST   /api/register/
POST   /api/token/
POST   /api/token/refresh/
GET    /api/user/
POST   /logout/
```

---

## Journal

```text id="journal-api"
GET    /api/get_disciplines_list/
POST   /api/add_course/
PUT    /api/update_course/
DELETE /api/delete_course/
```

---

## Groups / Users

```text id="group-user-api"
GET/POST /api/groups/
GET/POST /api/users/
```

---

## Attestation

```text id="attest-api"
GET/POST /api/attest/
```

---

# Database Design

Main entities:

* User (custom model)
* Group
* Discipline
* Session
* Attestation

### Key relationships:

* User → Group (many-to-one)
* Discipline → Session (academic structure)
* Session → Attestation (grading results)

---

# Authentication System

* JWT-based authentication (SimpleJWT)
* Access + Refresh token flow
* Custom user model
* Role/group-based permissions

---

# Infrastructure

## Docker

The project is fully containerized:

* Django backend container
* PostgreSQL database
* environment-based configuration (.env)
* entrypoint script for initialization

Run project:

```bash id="docker-run-uj"
docker-compose up --build
```

---

# Media Storage

* Cloudinary used for media storage
* teacher images stored in cloud storage
* media folder for local fallback

---

# Load Testing

Project includes Locust configuration:

* locustfile.py
* used for API stress testing
* validates scalability of authentication and journal endpoints

---

# Key Architectural Decisions

## 1. Modular Django design

Each domain is separated into apps:

* authentication
* journal
* attestation

This improves:

* scalability
* maintainability
* testability

---

## 2. Service layer usage

Business logic is partially moved into:

* services/student_service.py

This separates:

* API logic (views)
* business logic (services)

---

## 3. JWT authentication

Used for:

* stateless authentication
* frontend SPA integration
* secure API access

---

## 4. Domain-based URL structure

Each module has isolated routing:

* auth/*
* user/*
* group/*
* journal/*
* attestation/*

---

# Security

* environment variables (.env)
* JWT authentication
* CORS configuration
* separated user roles
* controlled API access

---

# Performance & Testing

* Locust used for load testing
* optimized database queries
* modular API design reduces coupling

---

# Deployment

```bash id="deploy-uj"
docker-compose up --build
```

---

# Author

Ekaterina Kuksar
GitHub: https://github.com/kiqiou
