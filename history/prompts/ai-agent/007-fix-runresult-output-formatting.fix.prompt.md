---
id: "007"
title: "Fix RunResult Output Formatting"
stage: "fix"
date: "2025-12-04"
surface: "agent"
model: "OPENAI_GPT_OSS_120B_MEDIUM"
feature: "ai-agent"
branch: "main"
user: "Makro"
command: "good i want to set the response syntax"
labels:
  - "backend"
  - "bugfix"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "e:\\book-hackathon\\backend\\src\\services\\rag_service.py"
tests: []
---

# Prompt
good i want to set the response syntax
RunResult: - Last agent: ... - Final output (str): ...

# Response
I fixed the issue where the raw `RunResult` object from the `openai-agents` library was being returned as the chat response.

1.  **Output Extraction**:
    *   Updated `rag_service.py` to inspect the `RunResult` object.
    *   Added logic to extract text from `final_output`, `output`, or `content` attributes.
    *   Added a fallback string parser to extract the "Final output (str):" content if attribute access fails.

The chatbot should now return clean, human-readable text responses.
