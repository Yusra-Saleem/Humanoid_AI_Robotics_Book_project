---
id: 001
title: Update Constitution for AI RAG Chatbot Architecture
stage: constitution
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: N/A
command: /sp.constitution
labels: ["constitution", "update", "ai-rag-chatbot"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:
- None
---

## Prompt

```text
AI RAG Chatbot and Agent Architecture

Define the AI's role as a Senior Backend Architect and Agent Specialist. The core objective is to implement the full Module 2 stack as defined in the Hackathon guide. The AI must strictly adhere to the technical requirements, including:
1. Using **FastAPI** for the backend.
2. Using **Qdrant** for Vector DB and **Neon** for Relational DB.
3. Orchestrating the RAG flow via **OpenAI Agents SDK** but using the **Gemini API** as the LLM.
4. Implementing the **Selected Text Logic**, **Better-Auth**, **Personalization**, **Urdu Translation**, and **Claude Agents/Skills**.
Don't remove my constitution file conent jus maintain the constitution.md without removing my constitution update little perfectly
--- END DETAILED CONSTITUTION ---
```

## Response snapshot

The project constitution has been updated to version v1.0.1, with a patch bump to reflect the update of the "Primary Role and Goal" principle.

The following templates may require manual follow-up to align with the updated principles:
- `.specify/templates/plan-template.md`
- `.specify/templates/spec-template.md`
- `.specify/templates/tasks-template.md`

Suggested commit message: `docs: amend constitution to v1.0.1 (principle additions + governance update)`

## Outcome

- ✅ Impact: Constitution updated to reflect AI RAG Chatbot and Agent Architecture requirements.
- 🧪 Tests: No tests run.
- 📁 Files: .specify/memory/constitution.md updated.
- 🔁 Next prompts: Committing the changes.
- 🧠 Reflection: User explicitly asked to maintain existing content while updating, which was handled by using `Edit` instead of `Write` for the entire file.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` script not found, requiring manual PHR creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Ensure `create-phr.sh` is accessible or add a check for its existence before attempting to run.
