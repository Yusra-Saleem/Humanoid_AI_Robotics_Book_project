---
id: "010"
title: "Hide Mobile Sidebar on Desktop"
stage: refactor
date: 2025-12-08
surface: agent
model: gemini-2.0-flash-exp
feature: ui-design
branch: null
user: null
command: null
labels: ["ui", "css", "bugfix", "sidebar"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - e:\book-hackathon\my-ai-book\src\css\custom.css
tests_yaml: |
  - manual verification of sidebar invisibility on desktop
---

# User Request

why this is showing below in footer in desktop screen please hide it

# Response

Fixed the issue where the mobile "Textbook" sidebar was appearing at the bottom of the page on desktop screens.

- **CSS Updates**: Modified `e:\book-hackathon\my-ai-book\src\css\custom.css`.
- **Change**:
  - Sets `.book-mobile-sidebar { display: none; }` by default (hiding it on desktop).
  - Maintains `display: block` and `position: fixed` inside the `@media (max-width: 996px)` query to ensure it still works correctly on mobile devices.
- **Reason**: The sidebar HTML is physically present in the DOM on all pages (injected by `Root.js`), so it must be explicitly hidden via CSS when not on mobile viewports.
