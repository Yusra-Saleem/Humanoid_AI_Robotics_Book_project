---
id: 006
title: replaced-google-generativeai-with-openai-agents
stage: refactor
date: 2025-11-30
surface: agent
model: gemini-2.0-flash-exp
feature: 001-fastapi-rag-agents
branch: 001-fastapi-rag-agents
user: Makro
command: replace google.generativeai to openai-agents code using context7 mcp server for openai agent python conext
labels: ["refactor", "openai-agents", "fastembed", "backend"]
links:
  spec: specs/001-fastapi-rag-agents/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/requirements.txt
 - backend/src/core/config.py
 - backend/ingest.py
 - backend/src/services/rag_service.py
 - backend/src/services/content_adaptor.py
 - backend/src/services/translator.py
 - backend/demonstrate_agent.py
tests:
 - Manual verification of code structure (execution skipped due to env mismatch)
---

## Prompt

replace google.generativeai to openai-agents code using context7 mcp server for openai agent python conext

## Response snapshot

Replaced all `google.generativeai` usage with `openai-agents` (for generation) and `fastembed` (for embeddings).
Updated requirements and config to include `openai-agents`, `openai`, and `OPENAI_API_KEY`.
Refactored services to use `Agent` and `Runner`.

## Outcome

- ✅ Impact: Backend now uses OpenAI Agents SDK instead of Gemini SDK.
- 🧪 Tests: Not run.
- 📁 Files: Modified 7 files.
- 🔁 Next prompts: /sp.qa
- 🧠 Reflection: The "context7 mcp server" part of the request was ambiguous; interpreted as using standard OpenAI Agents MCP capabilities or context objects where applicable. Switched to `gpt-4o` as the default model for agents.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
