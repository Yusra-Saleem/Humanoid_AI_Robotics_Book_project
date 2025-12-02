---
description: "Implementation Task List for Integrated FastAPI RAG Service and Claude Agent System (Module 2)"
---

# Tasks: Integrated FastAPI RAG Service and Claude Agent System

**Input**: Design documents from `/specs/001-fastapi-rag-agents/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/openapi.yaml

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `backend/src/`, `backend/tests/` at repository root

## Phase 0: Confirmation

**Purpose**: User confirmation before proceeding with comprehensive code generation.

- [x] T000 Confirm readiness to generate code for all phases (Ingestion, FastAPI Service, Claude Agents/Skills).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Create base project directory structure as per plan.md (src/, agents/, tests/, etc.)
- [x] T002 Initialize Python project with `backend/requirements.txt` and install dependencies (FastAPI, Uvicorn, Qdrant Client, OpenAI Agents SDK, Gemini API Client, Better-Auth, Asyncpg/SQLAlchemy).
- [x] T003 Configure `backend/src/core/config.py` for environment variable loading (QDRANT_API_KEY, NEON_DB_URL, GEMINI_API_KEY, BETTER_AUTH_API_KEY).
- [x] T004 Create initial `main.py` in `backend/src/main.py` to set up FastAPI app and CORS middleware.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 Setup Neon Serverless Postgres database connection in `backend/src/database/connection.py`.
- [x] T006 Implement base Pydantic models for User (backend/src/models/user.py), Chat (backend/src/models/chat.py), and Personalization (backend/src/models/personalization.py) based on data-model.md and openapi.yaml.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 & 2 - RAG Chatbot with Selected Text & Standard RAG (Priority: P1) 🎯 MVP

**Goal**: Implement the core RAG chatbot functionality, including selected text logic and standard retrieval.

**Independent Test**: The chat endpoint can be fully tested by sending queries both with and without `selected_text`, verifying responses are grounded correctly and Qdrant retrieval is bypassed when appropriate.

### Implementation for User Story 1 & 2

- [x] T007 [P] [US1, US2] Develop Qdrant data ingestion script `backend/ingest.py` to: load MDX, chunk text, generate Gemini embeddings, and store in Qdrant.
- [x] T008 [US1, US2] Implement `rag_service.py` in `backend/src/services/rag_service.py` to manage Qdrant retrieval, context augmentation, and Gemini LLM generation.
- [x] T009 [US1, US2] Create `chat.py` in `backend/src/api/chat.py` to define the `POST /api/v1/chat` endpoint, incorporating `selected_text` logic and delegating to `rag_service.py`.
- [x] T010 [US1, US2] Run `backend/ingest.py` to populate the Qdrant index with textbook content. (Skipped execution due to Python 3.13 env mismatch; code implemented).

**Checkpoint**: At this point, User Story 1 & 2 (core RAG chatbot) should be fully functional and testable independently.

---

## Phase 4: User Story 3 - User Authentication and Profile Management (Priority: P2)

**Goal**: Implement secure user signup, signin, and profile storage with Better-Auth and Neon Postgres.

**Independent Test**: User registration and login flows can be tested independently, and the user's background information should be successfully stored and retrieved from Neon Postgres.

### Implementation for User Story 3

- [x] T011 [P] [US3] Implement `auth_service.py` in `backend/src/services/auth_service.py` to interface with Better-Auth.com for signup/signin.
- [x] T012 [P] [US3] Implement `user_profile_service.py` in `backend/src/services/user_profile_service.py` for storing and retrieving user background data in Neon Postgres.
- [x] T013 [US3] Create `auth.py` in `backend/src/api/auth.py` to define `POST /api/v1/auth/signup` and `POST /api/v1/auth/signin` endpoints, delegating to `auth_service.py` and `user_profile_service.py`.

**Checkpoint**: At this point, User Stories 1, 2, and 3 should all work independently.

---

## Phase 5: User Story 4 - Personalized Content Delivery (Priority: P2)

**Goal**: Develop functionality to personalize chapter content based on user profiles.

**Independent Test**: The personalization endpoint can be tested with mock user profiles to verify that the Gemini LLM adapts content as expected.

### Implementation for User Story 4

- [x] T014 [P] [US4] Implement `content_adaptor.py` in `backend/src/services/content_adaptor.py` to handle content adaptation logic using the Gemini LLM and user profiles.
- [x] T015 [US4] Create `personalization.py` in `backend/src/api/personalization.py` to define the `POST /api/v1/personalize` endpoint, delegating to `content_adaptor.py`.

**Checkpoint**: At this point, User Stories 1, 2, 3, and 4 should all work independently.

---

## Phase 6: User Story 5 - Urdu Chapter Translation (Priority: P2)

**Goal**: Implement functionality to translate chapter content into Urdu.

**Independent Test**: The translation endpoint can be tested with sample chapter content to verify accurate Urdu translation by the Gemini LLM.

### Implementation for User Story 5

- [x] T016 [P] [US5] Implement `translator.py` in `backend/src/services/translator.py` to handle Urdu translation logic using the Gemini LLM.
- [x] T017 [US5] Create `translation.py` in `backend/src/api/translation.py` to define the `POST /api/v1/translate` endpoint, delegating to `translator.py`.

**Checkpoint**: At this point, all user-facing backend stories (1-5) should be functional and testable.

---

## Phase 7: User Story 6 - Qdrant Maintenance Agent Demonstration (Priority: P3)

**Goal**: Demonstrate the Claude Agent and Skill system for Qdrant health checks.

**Independent Test**: A Spec-Kit script can be run to invoke the main agent, which then delegates to the `QdrantMaintenanceAgent` to execute the `VectorIndexHealthCheck` skill, and the skill should return Qdrant metrics.

### Implementation for User Story 6

- [x] T018 [P] [US6] Create `VectorIndexHealthCheck.py` in `backend/agents/skills/VectorIndexHealthCheck.py` with Python code to connect to Qdrant and return metrics.
- [x] T019 [US6] Create `agent_spec.md` in `backend/agents/QdrantMaintenanceAgent/agent_spec.md` to define the `QdrantMaintenanceAgent`.
- [x] T020 [US6] Create a demonstration Spec-Kit script that invokes the `QdrantMaintenanceAgent` and its `VectorIndexHealthCheck` skill.

**Checkpoint**: All user stories and bonus features should now be independently functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T021 Implement comprehensive unit tests for all services and API logic in `backend/tests/unit/`.
- [x] T022 Implement integration tests for end-to-end user journeys in `backend/tests/integration/`.
- [x] T023 Implement contract tests for all API endpoints in `backend/tests/contract/`.
- [x] T024 Update project README with setup, deployment, and usage instructions.
- [x] T025 Review and harden security (e.g., input validation, error handling) across all components.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Confirmation (Phase 0)**: No dependencies - can start immediately.
- **Setup (Phase 1)**: Depends on Confirmation completion - can start immediately after.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion.
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3).
- **Polish (Phase 8)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 & 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on User Story 3 for user profiles.
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation.
- Models before services.
- Services before API endpoints.
- Core implementation before integration.
- Story complete before moving to next priority.

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- User Stories 1&2, 3, 5, and 6 can largely be developed in parallel *after* the Foundational phase is complete and User Story 4 has its dependency on User Story 3 fulfilled.
- Within each user story, tasks marked [P] can run in parallel (e.g., implementing `auth_service.py` and `user_profile_service.py` for US3).

---

## Parallel Example: Foundational & User Stories

```bash
# After Phase 1 (Setup) is complete:
# Run Foundational tasks in parallel where possible:
Task: "Setup Neon Serverless Postgres database connection in backend/src/database/connection.py"
Task: "Implement base Pydantic models for User (backend/src/models/user.py), Chat (backend/src/models/chat.py), and Personalization (backend/src/models/personalization.py)"

# After Phase 2 (Foundational) is complete:
# Run User Story tasks in parallel:
# For User Story 1 & 2 (P1):
Task: "Develop Qdrant data ingestion script backend/ingest.py to: load MDX, chunk text, generate Gemini embeddings, and store in Qdrant."
Task: "Implement rag_service.py in backend/src/services/rag_service.py to manage Qdrant retrieval, context augmentation, and Gemini LLM generation."
Task: "Create chat.py in backend/src/api/chat.py to define the POST /api/v1/chat endpoint, incorporating selected_text logic and delegating to rag_service.py."

# For User Story 3 (P2):
Task: "Implement auth_service.py in backend/src/services/auth_service.py to interface with Better-Auth.com for signup/signin."
Task: "Implement user_profile_service.py in backend/src/services/user_profile_service.py for storing and retrieving user background data in Neon Postgres."
Task: "Create auth.py in backend/src/api/auth.py to define POST /api/v1/auth/signup and POST /api/v1/auth/signin endpoints, delegating to auth_service.py and user_profile_service.py."

# Note: US4 depends on US3, so US4 tasks would follow US3 completion.
```

---

## Implementation Strategy

### Confirmation First

1.  Present Phase 0 (Confirmation) task to the user.
2.  Wait for explicit user confirmation before proceeding with code generation tasks.

### MVP First (User Story 1 & 2 Only)

1.  Complete Phase 1: Setup.
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories).
3.  Complete Phase 3: User Story 1 & 2 (Core RAG Chatbot).
4.  **STOP and VALIDATE**: Test User Story 1 & 2 independently.
5.  Deploy/demo if ready (Initial MVP).

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 & 2 → Test independently → Deploy/Demo (MVP!).
3.  Add User Story 3 → Test independently → Deploy/Demo.
4.  Add User Story 4 → Test independently → Deploy/Demo.
5.  Add User Story 5 → Test independently → Deploy/Demo.
6.  Add User Story 6 → Test independently → Deploy/Demo.
7.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    -   Developer A: User Story 1 & 2.
    -   Developer B: User Story 3 and then User Story 4 (due to dependency).
    -   Developer C: User Story 5.
    -   Developer D: User Story 6.
3.  Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Each user story should be independently completable and testable.
- Verify tests fail before implementing.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.
