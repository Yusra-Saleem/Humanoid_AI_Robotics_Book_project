---
id: "005"
title: "Fix AI Agent RAG Service Logic"
stage: "fix"
date: "2025-12-04"
surface: "agent"
model: "OPENAI_GPT_OSS_120B_MEDIUM"
feature: "ai-agent"
branch: "main"
user: "Makro"
command: "chatbot directly respond with open ai key not fixed answer"
labels:
  - "backend"
  - "rag"
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
chatbot directly respond with open ai key not fixed answer
hi -> Sorry, something went wrong. Please try again!

# Response
I fixed multiple issues in the `rag_service.py` to ensure the AI Agent works correctly and uses the LLM directly as requested.

1.  **Removed Fixed Answers**:
    *   Disabled canned responses for greetings.
    *   Disabled early returns for "no search results" or "low confidence scores".
    *   The flow now always proceeds to the LLM generation step.

2.  **Fixed `Runner` Usage**:
    *   Corrected the usage of `Runner.run` to match `translator.py`.
    *   Changed from synchronous instance method `runner.run(prompt)` to awaited static/class method `await Runner.run(agent, input=prompt)`.
    *   This fixes the "Something went wrong" crash which was likely due to incorrect async handling or API usage.

3.  **Improved Fallback**:
    *   Added logic to handle cases where `answer_parts` (RAG chunks) are empty, preventing `IndexError`.
    *   Added a generic fallback message if both LLM and RAG fail.
    *   Added verbose error reporting in the response for easier debugging.

The chatbot should now function as a "normal conversation agent" that uses OpenAI directly when needed, while still having access to the book content.
