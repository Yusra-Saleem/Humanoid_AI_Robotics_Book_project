---
id: 002
title: Clarify File Structure, DB Schema, and API Endpoints for FastAPI RAG
stage: spec
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: fastapi-rag-agents
branch: 001-fastapi-rag-agents
user: N/A
command: /sp.clarify
labels: ["clarification", "file-structure", "db-schema", "api-endpoints"]
links:
  spec: specs/001-fastapi-rag-agents/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/001-fastapi-rag-agents/spec.md
tests:
- N/A
---

## Prompt

```text
File Structure, Database Schema, and API Endpoints

Provide a detailed outline of:
1. The necessary Python files (e.g., ingest.py, main.py, rag_service.py) and Claude Agent files (agent_spec.md, skill.py).
2. The essential **Neon Postgres database schema** required to store Better-Auth user profiles (including background data).
3. The full list of **FastAPI endpoints** to be created: /api/v1/chat, /api/v1/auth/signup, /api/v1/auth/signin, /api/v1/personalize, and /api/v1/translate.
```

## Response snapshot

I have provided a detailed outline of the file structure, database schema, and API endpoints as requested, and then updated the specification document with this information.

### File Structure Outline

```
.
├── src/
│   ├── main.py                     # FastAPI application entry point, registers routes
│   ├── api/                        # API routes definition
│   │   ├── __init__.py
│   │   ├── chat.py                 # Handles /api/v1/chat endpoint logic
│   │   ├── auth.py                 # Handles /api/v1/auth/signup, /api/v1/auth/signin
│   │   ├── personalization.py      # Handles /api/v1/personalize endpoint logic
│   │   └── translation.py          # Handles /api/v1/translate endpoint logic
│   ├── services/                   # Core business logic and external integrations
│   │   ├── __init__.py
│   │   ├── rag_service.py          # Manages Qdrant retrieval and Gemini RAG flow
│   │   ├── auth_service.py         # Interfaces with Better-Auth.com
│   │   ├── user_profile_service.py # Manages user profile data in Neon DB
│   │   ├── content_adaptor.py      # Logic for personalization
│   │   └── translator.py           # Logic for Urdu translation
│   ├── models/                     # Pydantic models for request/response bodies and DB schemas
│   │   ├── __init__.py
│   │   ├── user.py                 # User Pydantic model
│   │   ├── chat.py                 # Chat request/response Pydantic models
│   │   └── personalization.py      # Personalization request/response Pydantic models
│   ├── database/                   # Database connection and ORM setup
│   │   ├── __init__.py
│   │   └── connection.py           # Handles Neon Postgres connection
│   └── core/                       # Core utilities, config, LLM client setup
│       ├── __init__.py
│       └── config.py               # Environment variable loading
├── ingest.py                       # Script for data ingestion into Qdrant
├── agents/
│   ├── QdrantMaintenanceAgent/     # Claude Agent definition
│   │   └── agent_spec.md           # Agent specification
│   └── skills/
│       └── VectorIndexHealthCheck.py # Python code for the Qdrant health check skill
├── .env.example                    # Example environment variables
└── tests/                          # Project tests
    ├── unit/
    ├── integration/
    └── contract/
```

### Neon Postgres Database Schema for User Profiles

A `users` table will store user authentication and profile data.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    software_background TEXT, -- Free-form text for user's software experience
    hardware_background TEXT, -- Free-form text for user's hardware experience
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Full List of FastAPI Endpoints

-   `POST /api/v1/chat`
    -   **Description**: Main chatbot endpoint for RAG queries.
    -   **Request Body**:
        ```json
        {
            "query": "string",
            "selected_text": "string | null"
        }
        ```
    -   **Response Body**:
        ```json
        {
            "answer": "string",
            "sources": ["string"]
        }
        ```

-   `POST /api/v1/auth/signup`
    -   **Description**: Registers a new user with Better-Auth and stores profile.
    -   **Request Body**:
        ```json
        {
            "email": "string",
            "password": "string",
            "software_background": "string | null",
            "hardware_background": "string | null"
        }
        ```
    -   **Response Body**:
        ```json
        {
            "message": "User registered successfully",
            "user_id": "string"
        }
        ```

-   `POST /api/v1/auth/signin`
    -   **Description**: Authenticates an existing user via Better-Auth.
    -   **Request Body**:
        ```json
        {
            "email": "string",
            "password": "string"
        }
        ```
    -   **Response Body**:
        ```json
        {
            "message": "Login successful",
            "access_token": "string",
            "token_type": "bearer"
        }
        ```

-   `POST /api/v1/personalize`
    -   **Description**: Adapts chapter content based on user profile.
    -   **Request Body**:
        ```json
        {
            "chapter_content": "string",
            "user_id": "string"
        }
        ```
    -   **Response Body**:
        ```json
        {
            "personalized_content": "string"
        }
        ```

-   `POST /api/v1/translate`
    -   **Description**: Translates chapter content into Urdu.
    -   **Request Body**:
        ```json
        {
            "chapter_content": "string"
        }
        ```
    -   **Response Body**:
        ```json
        {
            "translated_content": "string"
        }
        ```

## Outcome

- ✅ Impact: Detailed outlines for file structure, DB schema, and API endpoints added to the feature spec.
- 🧪 Tests: No code tests run.
- 📁 Files: `specs/001-fastapi-rag-agents/spec.md` updated.
- 🔁 Next prompts: Commit changes to git, and then proceed with planning using `/sp.plan`.
- 🧠 Reflection: The user's request was a direct query for implementation details rather than ambiguities in the spec. Handled by providing the requested information and appending it to the spec under a new `Clarifications` section.

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
