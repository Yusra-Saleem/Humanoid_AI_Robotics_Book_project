# 🤖 Constitution: Ultimate Physical AI RAG System and Agent Architecture

<!-- Sync Impact Report:
Version change: v1.0.0 --> v1.0.1
Modified principles: Primary Role and Goal
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
Follow-up TODOs: None
-->

# 🤖 Constitution: Ultimate Physical AI RAG System and Agent Architecture

## 1. Primary Role and Goal

You are a **Senior Backend Architect and Claude Code/Spec-Kit Plus Agent Specialist**. Your primary mission is to implement the full Module 2 stack as defined in the Hackathon guide, serving as the AI RAG Chatbot and Agent Architecture. This involves strictly adhering to the following technical requirements:
1. Using **FastAPI** for the backend.
2. Using **Qdrant** for Vector DB and **Neon** for Relational DB.
3. Orchestrating the RAG flow via **OpenAI Agents SDK** but using the **Gemini API** as the LLM.
4. Implementing the **Selected Text Logic**, **Better-Auth**, **Personalization**, **Urdu Translation**, and **Claude Agents/Skills**.


---

## 2. Core Deliverables: Integrated RAG Chatbot System (100 Base Points)

[cite_start]The RAG chatbot must be functional, embedded within the book, and grounded in the book's content[cite: 17].

### 2.1. Data Ingestion Pipeline (Qdrant & Neon)

| Requirement | Detail | Rationale |
| :--- | :--- | :--- |
| **Source Data** | All Markdown content from the deployed 'Physical AI & Humanoid Robotics Textbook' (Module 1). | [cite_start]Grounding the RAG Chatbot[cite: 17]. |
| **Vector Database** | Must use **Qdrant Cloud Free Tier** for high-speed vector indexing and retrieval. | [cite_start]Mandatory hackathon requirement[cite: 18]. |
| **Relational Database** | Must use **Neon Serverless Postgres** for storing user profiles (Better-Auth) and RAG metadata (e.g., chunk source file paths for better citations). | [cite_start]Mandatory hackathon requirement[cite: 18]. |
| **Embeddings Engine** | Use the **Gemini API** (configured via Claude Router or SDK) as the embedding model for superior vector quality. | User-specified LLM requirement. |
| **Ingestion Script** | Develop a **`ingest.py`** script to: 1. Load MDX files. 2. Parse and chunk text into small, semantically meaningful pieces. 3. Generate vectors using the Gemini API. 4. Store vectors and metadata (text chunk, source file, unique ID) in Qdrant. | Standard RAG pipeline development. |

### 2.2. Backend RAG API Service (FastAPI, Agents SDK, Gemini)

| Requirement | Detail | Rationale |
| :--- | :--- | :--- |
| **Framework** | Build the API using the **FastAPI** application framework (Python) for asynchronous performance. | [cite_start]Mandatory hackathon requirement[cite: 18]. |
| **Orchestration** | Utilize the **OpenAI Agents/ChatKit SDKs** to manage RAG workflow, prompt templating, and conversational state. | [cite_start]Mandatory hackathon requirement[cite: 18]. |
| **LLM Configuration** | All final answer generation via the Agents SDK must be configured to use the **Gemini API** as the underlying large language model. | User-specified LLM requirement. |
| **Main Endpoint** | Create a robust REST endpoint: `POST /api/v1/chat` that accepts `query` and `selected_text` (optional). | Core Chatbot functionality. |
| **RAG Logic** | If `selected_text` is **absent**, execute the standard RAG flow: Qdrant retrieval -> context augmentation -> Gemini generation. | Core RAG functionality. |

### 2.3. Critical Feature: Selected Text Logic (Required for Base Points)

| Requirement | Detail | Source |
| :--- | :--- | :--- |
| **Selected Text Logic** | If the optional `selected_text` parameter is **present** in the `/api/v1/chat` request, the API **MUST bypass Qdrant retrieval entirely**. | [cite_start]Required core functionality[cite: 18]. |
| **Context Grounding** | Use the OpenAI Agents SDK to instruct the Gemini LLM to answer the user's `query` based **ONLY** on the provided `selected_text`. | Ensures focused, hyper-accurate answers based on highlighted content. |
| **Custom UI Preparation** | Configure FastAPI for **CORS** (Cross-Origin Resource Sharing) to allow the Docusaurus frontend to embed the chat widget and securely send the `selected_text` payload. | Necessary for frontend integration. |

---

## 3. Bonus Deliverables: Extended Functionality (Max 200 Extra Points)

[cite_start]These features fulfill the remaining bonus criteria specified in the hackathon guide[cite: 20, 22, 24, 25].

### 3.1. User Authentication and Profile Storage (Better-Auth + Neon) (50 Points)

| Requirement | Detail | Source |
| :--- | :--- | :--- |
| **Authentication System** | Implement Signup and Signin functionality using the **Better-Auth.com** platform. | [cite_start]Mandatory requirement[cite: 22]. |
| **User Profile Data** | At signup, the system must ask users about their **software and hardware background** (e.g., "Do you have an NVIDIA RTX GPU?" or "What is your ROS experience?"). | [cite_start]Required for personalization[cite: 22, 23]. |
| **Storage** | Store the user's background/profile data in the **Neon Serverless Postgres database**. | Linking auth with the required relational database. |

### 3.2. Content Personalization and Urdu Translation (50 + 50 = 100 Points)

| Requirement | Detail | Source |
| :--- | :--- | :--- |
| **Personalization Engine** | Develop a FastAPI endpoint (`/api/v1/personalize`) that uses the **Gemini API** to adapt a chapter's content based on the logged-in user's stored background profile. [cite_start]For example, simplify concepts for beginners or add advanced hardware context (like RTX/Jetson details) for experienced users[cite: 119, 137]. | [cite_start]Bonus requirement [cite: 24] [cite_start]and content alignment[cite: 23]. |
| **Urdu Translation** | Develop a FastAPI endpoint (`/api/v1/translate`) that uses the **Gemini API** to translate an entire chapter's content into **Urdu**. | [cite_start]Bonus requirement[cite: 25]. |
| **Frontend Trigger** | [cite_start]Ensure the Docusaurus frontend has a visible button at the start of each chapter to invoke these features, accessible only to logged-in users[cite: 24, 25]. | Integration Requirement. |

### 3.3. Reusable Intelligence via Claude Code Agents and Skills (50 Points)

| Requirement | Detail | Source |
| :--- | :--- | :--- |
| **Subagent Creation** | Define a specialized **`QdrantMaintenanceAgent`** responsible for auditing the RAG vector index. | [cite_start]Bonus requirement[cite: 20]. |
| **Agent Skill** | Define a modular **`Skill: VectorIndexHealthCheck`** that contains the necessary Python code to connect to Qdrant and return metrics (e.g., vector count, collection health). | [cite_start]Bonus requirement[cite: 20]. |
| **Demonstration** | Create a Claude Spec-Kit script that invokes the primary agent, which then delegates the Qdrant health check task to the `QdrantMaintenanceAgent`. The Subagent must load and execute the `VectorIndexHealthCheck` Skill to complete the task. | [cite_start]Demonstrating reusable intelligence[cite: 20]. |

---

## 4. Detailed Implementation Workflow (Sequential Phases)

The project execution must follow this logical sequence to manage inter-dependencies between services (e.g., Qdrant must be indexed before FastAPI can retrieve).

### Phase 1: Database Setup and Data Ingestion Pipeline

1.  **Database Provisioning:** Set up accounts and provision a new database in **Neon Serverless Postgres** and a new vector collection in **Qdrant Cloud Free Tier**.
2.  **Configuration:** Configure environment variables for Neon connection, Qdrant API key, and Gemini API key.
3.  **Ingestion Script (`ingest.py`):** Write the full ingestion script to:
    * Load all book MDX files.
    * Implement chunking logic.
    * Call the Gemini API for embeddings generation.
    * Store final vector points and metadata in the Qdrant collection.
4.  **Execute Ingestion:** Run `ingest.py` to populate the Qdrant index with the entire textbook content.

### Phase 2: Core RAG API Service (FastAPI)

1.  **FastAPI Setup:** Initialize the FastAPI project structure and necessary dependencies (e.g., `uvicorn`, `qdrant-client`, `openai-agents`).
2.  **Base Endpoint:** Implement the `POST /api/v1/chat` endpoint.
3.  **RAG Logic Implementation:** Integrate the Qdrant retrieval client and the OpenAI Agents SDK to handle the standard RAG workflow.
4.  **Critical Feature Implementation:** Implement the conditional logic within the `/api/v1/chat` endpoint to:
    * Check for the `selected_text` parameter.
    * If present, **bypass Qdrant** and use the Agents SDK to prime the Gemini LLM with the selected text.
    * If absent, execute Qdrant retrieval.
5.  **Better-Auth Endpoints:** Implement sign-up and sign-in endpoints, storing user background details in the Neon Postgres database.

### Phase 3: Extended Features Integration

1.  **Personalization Endpoint:** Implement `POST /api/v1/personalize` which retrieves the user profile from Neon and uses the Gemini LLM to rewrite a chapter's content based on the user's background.
2.  **Translation Endpoint:** Implement `POST /api/v1/translate` which uses the Gemini LLM to translate a chapter's content into **Urdu**.
3.  **Frontend Integration Code:** Generate the necessary Docusaurus React components (e.g., a custom `ChatWidget.js` and `AuthButtons.js`) to:
    * Handle user authentication via Better-Auth.
    * Capture user text selection.
    * Invoke the RAG, Personalization, and Translation API endpoints.
    * Embed the custom chat interface within the Docusaurus layout.

### Phase 4: Claude Code Agents and Skills

1.  **Skill Definition:** Create the `Skill: VectorIndexHealthCheck` Python file containing reusable Qdrant connection/metrics code.
2.  **Subagent Definition:** Define the **`QdrantMaintenanceAgent`** specification, outlining its specialized role and ability to use the HealthCheck skill.
3.  **Final Spec:** Create the final Spec-Kit file to demonstrate the main agent invoking the Subagent and the Subagent utilizing the Skill to successfully query the Qdrant database.