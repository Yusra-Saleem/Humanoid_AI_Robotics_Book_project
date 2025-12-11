---
id: "006"
title: "Fix Translation HTML Error"
stage: refactor
date: 2025-12-08
surface: agent
model: gemini-2.0-flash-exp
feature: translation
branch: null
user: null
command: null
labels: ["bugfix", "translation", "error-handling"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - e:\book-hackathon\my-ai-book\src\components\TextSelection\TextSelection.js
  - e:\book-hackathon\my-ai-book\src\components\UrduTranslationToggle\UrduTranslationToggle.js
  - e:\book-hackathon\my-ai-book\src\pages\translate.js
tests_yaml: |
  - manual verification of error handling
---

# User Request

Translation failed: Unexpected token '<', "<!DOCTYPE "... is not valid JSON

# Response

Fixed the "Unexpected token" error which was caused by the application receiving an HTML response (likely a 404 from the local dev server) instead of the expected JSON from the backend.
This happened because the `apiBaseUrl` configuration was not yet loaded (requiring a server restart), resulting in an undefined URL that defaulted to a local 404 page.

- Added robust error handling in `TextSelection.js`, `UrduTranslationToggle.js`, and `translate.js`:
  - Explicitly checks if `apiBaseUrl` is configured.
  - Verifies if the valid `Content-Type` is JSON before parsing.
  - Logs the exact URL being requested for easier debugging.
  - Provides clear error messages when the server returns HTML (e.g., 404 or 500 errors).

The user must restart their development server for the `docusaurus.config.js` changes to take effect.
