# Implementation Plan: Finalize Textbook Generation Plan

**Branch**: `001-number` | **Date**: 2025-11-29 | **Spec**: `specs/001-number/spec.md`
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the finalization of the textbook generation for the Docusaurus project 'my-ai-book', including a nested folder structure, mapping of MDX files to the Constitution's module/weekly breakdown, and confirmation of `sidebars.js` functionality. The goal is to create a well-structured and navigable textbook.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: JavaScript (Node.js for Docusaurus), Markdown/MDX
**Primary Dependencies**: Docusaurus, React (implicit with Docusaurus)
**Storage**: Filesystem (Markdown/MDX files)
**Testing**: Manual verification of Docusaurus build and navigation
**Target Platform**: Web (Docusaurus static site)
**Project Type**: Web (documentation site)
**Performance Goals**: Fast page loads, efficient sidebar rendering
**Constraints**: Adherence to Docusaurus folder structure and sidebar configuration
**Scale/Scope**: Single book with nested chapters and sections

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Compliance with Constitution `1.0.0`:**
- **Output Format**: All output will be Docusaurus-compatible Markdown (.mdx) with necessary frontmatter. **(Compliant)**
- **Structure**: The structure will include 5 main documents as outlined: Introduction (Weeks 1-2 & Hardware), and then Module 1 to Module 4 chapters. **(Compliant)**
- **Content Alignment**: Each MDX file will cover the corresponding Module/Weekly Breakdown as specified in "The Course Details" and "Weekly Breakdown" sections of the Constitution. Specifically:
    - `book/_index.md`: Introduction (Weeks 1-2: Introduction to Physical AI & Hardware Requirements)
    - `book/chapter1/_index.md`: Module 1: The Robotic Nervous System (ROS 2) / Weeks 3-5: ROS 2 Fundamentals
    - `book/chapter2/_index.md`: Module 2: The Digital Twin (Gazebo & Unity) / Weeks 6-7: Robot Simulation with Gazebo
    - `book/chapter3/_index.md`: Module 3: The AI-Robot Brain (NVIDIA Isaac™) / Weeks 8-10: NVIDIA Isaac Platform
    - `book/chapter4/_index.md`: Module 4: Vision-Language-Action (VLA) / Weeks 11-12: Humanoid Robot Development & Week 13: Conversational Robotics **(Compliant)**
- **Developer-Ready Educational Content Principle (3)**: The generated textbook content will be structured for clarity and ease of learning, adhering to Docusaurus standards, and practical for developers and students. **(Compliant)**

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

This project will primarily consist of Docusaurus documentation files within a `book/` directory at the repository root.

```text
E:/book-hackathon/
├── sidebars.js
└── book/
    ├── _category_.json
    ├── _index.md
    ├── chapter1/
    │   ├── _category_.json
    │   └── _index.md
    ├── chapter2/
    │   ├── _category_.json
    │   └── _index.md
    ├── chapter3/
    │   ├── _category_.json
    │   └── _index.md
    └── chapter4/
        ├── _category_.json
        └── _index.md
```

**Final List of 7 Key Files with Full Paths:**
1. `E:\book-hackathon\book\_index.md` (Introduction: Weeks 1-2 & Hardware)
2. `E:\book-hackathon\book\chapter1\_index.md` (Module 1: The Robotic Nervous System (ROS 2))
3. `E:\book-hackathon\book\chapter2\_index.md` (Module 2: The Digital Twin (Gazebo & Unity))
4. `E:\book-hackathon\book\chapter3\_index.md` (Module 3: The AI-Robot Brain (NVIDIA Isaac™))
5. `E:\book-hackathon\book\chapter4\_index.md` (Module 4: Vision-Language-Action (VLA))
6. `E:\book-hackathon\sidebars.js` (Docusaurus Sidebar Configuration)
7. `E:\book-hackathon\book\_category_.json` (Top-level Book Category Metadata)

**sidebars.js Confirmation:**
The `sidebars.js` file, as previously generated and included in the plan, is configured to correctly display this nested folder structure in the Docusaurus sidebar using `type: 'category'` and `link: { type: 'doc', id: '...' }` to create navigable sections corresponding to the book's chapters and their introductory `_index.md` files.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
