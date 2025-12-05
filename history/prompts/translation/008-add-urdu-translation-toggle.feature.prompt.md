---
id: "008"
title: "Add Urdu Translation Toggle"
stage: "feature"
date: "2025-12-04"
surface: "agent"
model: "claude-sonnet-4"
feature: "translation"
branch: "main"
user: "Makro"
command: "i want a translation page toggle button translate whole page in urdu"
labels:
  - "translation"
  - "urdu"
  - "ui"
  - "react"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "e:\\book-hackathon\\my-ai-book\\src\\components\\UrduTranslationToggle\\UrduTranslationToggle.js"
  - "e:\\book-hackathon\\my-ai-book\\src\\components\\UrduTranslationToggle\\UrduTranslationToggle.css"
  - "e:\\book-hackathon\\my-ai-book\\src\\theme\\DocItem\\index.js"
tests: []
---

# Prompt
thank you now move another feature i want a translation page toggle button translate whole page in urdu

# Response
I have implemented a new Urdu translation toggle feature that allows users to translate the entire page to Urdu with a single click.

## Implementation

1.  **Created `UrduTranslationToggle` Component**:
    *   Fixed toggle button positioned in the top-right corner
    *   Shows "اردو" when in English mode, "English" when in Urdu mode
    *   Uses green gradient for inactive state, amber gradient for active state
    *   Includes loading spinner during translation

2.  **Translation Overlay**:
    *   When activated, displays translated content in a full-page overlay
    *   Content is displayed right-to-left (RTL) for proper Urdu rendering
    *   Uses Urdu-specific fonts (Noto Nastaliq Urdu, Jameel Noori Nastaleeq)
    *   Overlay covers the main content area while keeping the navbar visible

3.  **User Experience**:
    *   Click the toggle button to translate the page to Urdu
    *   Click again to return to the original English content
    *   Error messages appear as toast notifications
    *   Responsive design for mobile devices

4.  **Integration**:
    *   Added to `DocItem` layout alongside other features
    *   Uses the existing `/api/v1/translate` backend endpoint
    *   Automatically finds and translates the main page content

The toggle button is now available on all documentation pages, providing quick access to Urdu translations.
