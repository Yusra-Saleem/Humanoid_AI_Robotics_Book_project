# Feature Specification: Integrated FastAPI RAG Service and Claude Agent System

**Feature Branch**: `001-fastapi-rag-agents`
**Created**: 2025-11-29
**Status**: Draft
**Input**: User description: "Integrated FastAPI RAG Service and Claude Agent System\n\nBased on the Constitution, the specification is to develop a complete, integrated backend service encompassing the RAG pipeline, the FastAPI API with all required endpoints, the Better-Auth integration logic (Neon DB), and the architecture for the Claude Agents and Skills system. The project must be structured for immediate deployment and use of the specified cloud services (Qdrant, Neon)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAG Chatbot with Selected Text (Priority: P1)

As a user reading the textbook, I want to highlight a section of text and ask questions based *only* on that selection, receiving accurate and contextually relevant answers, so I can deeply understand specific parts of the content.

**Why this priority**: This is a core, critical feature explicitly required by the hackathon guide and the constitution. It demonstrates a key differentiator.

**Independent Test**: The chat endpoint can be fully tested by sending a query and a `selected_text` payload, verifying that the response is grounded *only* in the `selected_text` and does not perform Qdrant retrieval.

**Acceptance Scenarios**:

1.  **Given** I am on a textbook page, **When** I highlight a paragraph and ask "What is this about?", **Then** the chatbot provides a concise summary based *only* on the highlighted text.
2.  **Given** I highlight a section and ask a question whose answer is *not* in the highlighted text, **When** the chatbot should state it cannot answer based on the provided context, **Then** it accurately reflects the limitation.

---

### User Story 2 - Standard RAG Chatbot (Priority: P1)

As a user, I want to ask general questions about the textbook content, and have the system retrieve relevant information from the entire book to provide comprehensive answers, so I can explore concepts beyond the current page.

**Why this priority**: This is the other half of the core RAG functionality, essential for a complete chatbot experience as per the hackathon requirements.

**Independent Test**: The chat endpoint can be fully tested by sending a query *without* `selected_text`, verifying that the response leverages Qdrant retrieval and context augmentation from the entire textbook.

**Acceptance Scenarios**:

1.  **Given** I am on any page and ask "What is a humanoid robot?", **When** the chatbot retrieves information from the book's content, **Then** it provides an accurate and comprehensive answer.
2.  **Given** I ask a question not covered by the book's content, **When** the chatbot should state it cannot answer based on the provided context, **Then** it accurately reflects the limitation.

---

### User Story 3 - User Authentication and Profile Management (Priority: P2)

As a user, I want to securely sign up and log in to the application using Better-Auth, and provide details about my software/hardware background, so the system can personalize content for me.

**Why this priority**: This enables personalization and other user-specific bonus features, making it a critical prerequisite for those functionalities.

**Independent Test**: User registration and login flows can be tested independently, and the user's background information should be successfully stored and retrieved from Neon Postgres.

**Acceptance Scenarios**:

1.  **Given** I am a new user, **When** I sign up and provide my background details, **Then** my account is created, and my profile is stored in Neon DB.
2.  **Given** I am a registered user, **When** I log in, **Then** I am successfully authenticated, and my personalized features are enabled.

---

### User Story 4 - Personalized Content Delivery (Priority: P2)

As a logged-in user with a profile, I want to view textbook chapters adapted to my specific software/hardware background, so I can learn at a pace and depth that suits my experience level.

**Why this priority**: This is a key bonus feature enhancing user engagement, dependent on authentication and profile data.

**Independent Test**: A chapter can be personalized based on a mock user profile, verifying that the Gemini LLM adapts the content as expected (e.g., simplifying for beginners, adding advanced details for experts).

**Acceptance Scenarios**:

1.  **Given** I am a logged-in user with a "beginner" ROS background, **When** I request a personalized chapter, **Then** the chapter content is simplified with basic ROS explanations.
2.  **Given** I am a logged-in user with an "advanced RTX GPU" background, **When** I request a personalized chapter, **Then** the chapter content includes advanced details relevant to RTX GPUs.

---

### User Story 5 - Urdu Chapter Translation (Priority: P2)

As a logged-in user, I want to translate entire textbook chapters into Urdu, so I can access the content in my preferred language.

**Why this priority**: This is another important bonus feature for accessibility, also dependent on authentication.

**Independent Test**: A chapter can be sent for translation, verifying that the Gemini LLM accurately translates the content into Urdu.

**Acceptance Scenarios**:

1.  **Given** I am a logged-in user, **When** I request a chapter to be translated to Urdu, **Then** the entire chapter content is returned in Urdu.

---

### User Story 6 - Qdrant Maintenance Agent Demonstration (Priority: P3)

As a developer, I want to observe a Claude Agent performing a health check on the Qdrant vector index, so I can verify the functionality of the custom agent and skill system.

**Why this priority**: This is a bonus feature demonstrating agent capabilities, less critical for initial user functionality but important for hackathon completeness.

**Independent Test**: A Spec-Kit script can be run to invoke the main agent, which then delegates to the `QdrantMaintenanceAgent` to execute the `VectorIndexHealthCheck` skill, and the skill should return Qdrant metrics.

**Acceptance Scenarios**:

1.  **Given** the Claude Agent system is running, **When** the demonstration script is executed, **Then** the `QdrantMaintenanceAgent` is invoked, successfully executes `VectorIndexHealthCheck`, and returns Qdrant metrics (e.g., vector count, collection health).

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: System MUST provide a REST API endpoint `POST /api/v1/chat` that accepts `query` and an optional `selected_text`.
-   **FR-002**: If `selected_text` is present, the system MUST use the Gemini LLM to answer the `query` based *only* on `selected_text`, bypassing Qdrant retrieval.
-   **FR-003**: If `selected_text` is absent, the system MUST perform Qdrant retrieval, augment context, and use the Gemini LLM to answer the `query`.
-   **FR-004**: System MUST store and retrieve user profiles (software/hardware background) in Neon Serverless Postgres.
-   **FR-005**: System MUST implement user signup and signin functionality via Better-Auth.com.
-   **FR-006**: System MUST provide a REST API endpoint `POST /api/v1/personalize` that adapts chapter content based on a logged-in user's profile using the Gemini LLM.
-   **FR-007**: System MUST provide a REST API endpoint `POST /api/v1/translate` that translates chapter content into Urdu using the Gemini LLM.
-   **FR-008**: System MUST define and utilize a `QdrantMaintenanceAgent` with a `VectorIndexHealthCheck` skill.
-   **FR-009**: System MUST support CORS for frontend integration, allowing Docusaurus to embed the chat widget and send `selected_text`.
-   **FR-010**: System MUST use the Gemini API for all LLM interactions (embeddings, RAG generation, personalization, translation).
-   **FR-011**: System MUST use Qdrant Cloud Free Tier as the vector database for RAG.
-   **FR-012**: System MUST use Neon Serverless Postgres for relational data storage (user profiles, RAG metadata).
-   **FR-013**: System MUST provide an `ingest.py` script to process MDX files, generate Gemini embeddings, and store them in Qdrant.

### Key Entities *(include if feature involves data)*

-   **User**: Represents a user of the system with attributes like `id`, `email`, `password_hash`, `software_background`, `hardware_background`. Stored in Neon Postgres.
-   **Text Chunk**: A semantically meaningful piece of text from the textbook, with attributes like `content`, `source_file`, `unique_id`, `vector_embedding`. Stored in Qdrant.
-   **Chapter**: A logical unit of the textbook, which can be personalized or translated.


## Clarifications

### Session 2025-11-29

- Q: Detailed outline of necessary Python files and Claude Agent files, Neon Postgres database schema, and FastAPI endpoints. → A: Provided a detailed file structure, database schema, and endpoint definitions.

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

## Success Criteria *(mandatory)*


### Measurable Outcomes

-   **SC-001**: Users receive contextually relevant RAG responses within 3 seconds for both standard and selected text queries.
-   **SC-002**: User signup and login via Better-Auth complete successfully within 5 seconds, and profile data is persistently stored.
-   **SC-003**: Personalized chapter content is delivered to users within 7 seconds, accurately reflecting their stored preferences.
-   **SC-004**: Urdu translations of chapters are generated within 10 seconds, maintaining grammatical accuracy and context.
-   **SC-005**: The `QdrantMaintenanceAgent` successfully executes its health check skill and returns valid metrics, demonstrating proper agent orchestration.
-   **SC-006**: The system correctly bypasses Qdrant retrieval when `selected_text` is provided, achieving 100% accuracy in grounding responses to the provided text.
-   **SC-007**: The `ingest.py` script successfully processes all MDX textbook files and populates the Qdrant index without errors.
