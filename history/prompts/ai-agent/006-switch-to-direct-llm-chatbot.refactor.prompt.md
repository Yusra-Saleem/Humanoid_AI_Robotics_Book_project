---
id: "006"
title: "Switch to Direct LLM Chatbot"
stage: "refactor"
date: "2025-12-04"
surface: "agent"
model: "OPENAI_GPT_OSS_120B_MEDIUM"
feature: "ai-agent"
branch: "main"
user: "Makro"
command: "i want normal chotbot without rag or qudrant data"
labels:
  - "backend"
  - "llm"
  - "refactor"
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
i want normal chotbot without rag or qudrant data
Debug Error: NameError: name 'search_text' is not defined

# Response
I have refactored the `rag_service.py` to completely bypass the RAG (Retrieval-Augmented Generation) pipeline and Qdrant database.

1.  **Direct LLM Integration**:
    *   The `generate_response` method now directly calls the OpenAI Agent with the user's query and conversation history.
    *   It no longer performs embeddings or vector searches.
    *   It no longer relies on `search_text` or other RAG-specific variables.

2.  **Context Handling**:
    *   If `selected_text` is provided (e.g., from the "AI Explain" panel), it is included in the prompt as context for the LLM to explain.
    *   Conversation history is formatted and passed to the LLM to maintain context.

This change effectively converts the system into a standard AI chatbot that relies solely on the LLM's training data (and provided text selection) rather than the textbook content in the vector database.
