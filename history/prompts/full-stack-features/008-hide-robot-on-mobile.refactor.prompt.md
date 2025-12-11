---
id: "008"
title: "Hide Robot on Mobile"
stage: refactor
date: 2025-12-08
surface: agent
model: gemini-2.0-flash-exp
feature: ui-design
branch: null
user: null
command: null
labels: ["ui", "css", "mobile", "hero-section"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - e:\book-hackathon\my-ai-book\src\pages\index.module.css
tests_yaml: |
  - manual verification of robot visibility on mobile
---

# User Request

in mobile device only hide robot part

# Response

Hid the robot animation on mobile devices as requested.

- **CSS Update**: Modified `e:\book-hackathon\my-ai-book\src\pages\index.module.css`.
- **Change**: In the `@media screen and (max-width: 640px)` block, replaced all robot sizing rules with a single `.robotContainer { display: none; }` rule.
- **Effect**: The robot animation will now completely disappear on screens narrower than 640px (mobile phones), while remaining visible on larger screens (tablets and desktops).
