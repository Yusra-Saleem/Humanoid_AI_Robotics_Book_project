---
id: 3
title: Ensure chatbot visibility in Docusaurus by explicit wrapPageElement configuration
stage: red
date: 2025-11-30
surface: agent
model: gemini-1.5-flash-latest
feature: ai-book-chat-interface
branch: 001-fastapi-rag-agents
user: rayyan726.m@gmail.com
command: "chatbot is not showing in textbook"
labels: ["frontend", "docusaurus", "chatbot", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - my-ai-book/docusaurus.config.js
tests:
 - null
---

## Prompt

chatbot is not showing in textbook

## Response snapshot

Modified `docusaurus.config.js` to explicitly use `src/theme/Root.js` for `wrapPageElement`, ensuring the chatbot is rendered on all Docusaurus pages, including the textbook/docs.

## Outcome

- ✅ Impact: The chatbot placeholder should now be visible on all Docusaurus pages.
- 🧪 Tests: User needs to rebuild and restart Docusaurus project to verify the fix.
- 📁 Files: `my-ai-book/docusaurus.config.js` was modified.
- 🔁 Next prompts: User verification of the fix, further UI refinements.
- 🧠 Reflection: The issue was likely due to implicit theme component overriding not functioning as expected, requiring explicit configuration.

## Evaluation notes (flywheel)

- Failure modes observed: Chatbot not appearing on pages despite `Root.js` placement.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
