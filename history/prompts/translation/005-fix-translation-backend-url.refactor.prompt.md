---
id: "005"
title: "Fix Translation Backend URL"
stage: refactor
date: 2025-12-08
surface: agent
model: gemini-2.0-flash-exp
feature: translation
branch: null
user: null
command: null
labels: ["bugfix", "translation", "config", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - e:\book-hackathon\my-ai-book\docusaurus.config.js
  - e:\book-hackathon\my-ai-book\src\components\TextSelection\TextSelection.js
  - e:\book-hackathon\my-ai-book\src\components\UrduTranslationToggle\UrduTranslationToggle.js
  - e:\book-hackathon\my-ai-book\src\pages\translate.js
tests_yaml: |
  - manual verification of config update
---

# User Request

@[backend] @[my-ai-book]  adter backend deployment my selected text tranlsation feature is not working 

localhost:3000 says Translation failed: Failed to fetch

# Response

Fixed the translation feature by updating the frontend to point to the deployed backend URL instead of localhost.
- Identified that `TextSelection.js` and `UrduTranslationToggle.js` were hardcoded to `http://localhost:8000`.
- Found the correct deployed URL `https://yusra-saleem123-hackathon-book-backend.hf.space` in `src/pages/translate.js`.
- Centralized the API URL configuration in `docusaurus.config.js` under `customFields.apiBaseUrl`.
- Updated all translation-related components to use the centralized configuration.
