# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/002-docusaurus-nested-modules/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All Docusaurus project files will be generated within the `my-ai-book/` directory.
- All textbook content files (`.mdx`) will be generated inside `my-ai-book/docs/` with deep nesting.

## Phase 1: Setup (Project Initialization)

**Purpose**: Create the base directory structure for the Docusaurus project.

- [ ] T001 Create `my-ai-book/` directory
- [ ] T002 Create `my-ai-book/docs/` directory

---

## Phase 2: Foundational (Configuration Files)

**Purpose**: Create and configure the essential Docusaurus configuration files.

**⚠️ CRITICAL**: No content generation can begin until this phase is complete.

- [ ] T003 Create and configure `my-ai-book/docusaurus.config.js` for the textbook title and project name
- [ ] T004 Create `my-ai-book/sidebars.js` with the correct nested structure for all modules and weekly chapters

**Checkpoint**: Docusaurus configuration files are ready.

---

## Phase 3: User Story 1 - Generate Textbook (Priority: P1) 🎯 MVP

**Goal**: Generate all deeply nested content files for the Physical AI & Humanoid Robotics Textbook.

**Independent Test**: The generated `my-ai-book` project can be built, and all modules and weekly chapters are correctly displayed and navigable in the Docusaurus sidebar.

### Implementation for User Story 1

**Create Module/Chapter Directories within `my-ai-book/docs/`**
- [ ] T005 [P] [US1] Create `my-ai-book/docs/Introduction/` directory
- [ ] T006 [P] [US1] Create `my-ai-book/docs/Module-1-ROS2/` directory
- [ ] T007 [P] [US1] Create `my-ai-book/docs/Module-2-DigitalTwin/` directory
- [ ] T008 [P] [US1] Create `my-ai-book/docs/Module-3-IsaacBrain/` directory
- [ ] T009 [P] [US1] Create `my-ai-book/docs/Module-4-VLA/` directory

**Create Content MDX Files with Detailed Educational Content within `my-ai-book/docs/`**
- [ ] T010 [P] [US1] Create and populate `my-ai-book/docs/Introduction/01-Foundations-Hardware.md` (Weeks 1-2)
- [ ] T011 [P] [US1] Create and populate `my-ai-book/docs/Module-1-ROS2/01-Week-3-Nodes-Topics.md` (Week 3)
- [ ] T012 [P] [US1] Create and populate `my-ai-book/docs/Module-1-ROS2/02-Week-4-Services-Actions.md` (Week 4)
- [ ] T013 [P] [US1] Create and populate `my-ai-book/docs/Module-1-ROS2/03-Week-5-URDF-rclpy.md` (Week 5)
- [ ] T014 [P] [US1] Create and populate `my-ai-book/docs/Module-2-DigitalTwin/01-Week-6-Gazebo-Setup.md` (Week 6)
- [ ] T015 [P] [US1] Create and populate `my-ai-book/docs/Module-2-DigitalTwin/02-Week-7-Sensors-Unity.md` (Week 7)
- [ ] T016 [P] [US1] Create and populate `my-ai-book/docs/Module-3-IsaacBrain/01-Week-8-Isaac-Sim-SDK.md` (Week 8)
- [ ] T017 [P] [US1] Create and populate `my-ai-book/docs/Module-3-IsaacBrain/02-Week-9-VSLAM-Nav2.mdx` (Week 9)
- [ ] T018 [P] [US1] Create and populate `my-ai-book/docs/Module-3-IsaacBrain/03-Week-10-Reinforcement-Learning.md` (Week 10)
- [ ] T019 [P] [US1] Create and populate `my-ai-book/docs/Module-4-VLA/01-Week-11-Kinematics-Dynamics.md` (Week 11)
- [ ] T020 [P] [US1] Create and populate `my-ai-book/docs/Module-4-VLA/02-Week-12-Manipulation-Interaction.md` (Week 12)
- [ ] T021 [P] [US1] Create and populate `my-ai-book/docs/Module-4-VLA/03-Week-13-Conversational-AI.md` (Week 13)

**Checkpoint**: All textbook content and configuration files for the Docusaurus project are generated.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all content generation tasks
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion

### Within Each User Story

- Module/Chapter directories creation can be parallelized.
- Content MDX file creation within modules can be parallelized.

### Parallel Opportunities

- All tasks marked [P] within Phase 1 and Phase 3 can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch all module/chapter directory creations together:
Task: "Create my-ai-book/docs/Introduction/ directory"
Task: "Create my-ai-book/docs/Module-1-ROS2/ directory"
# ... and so on for all module directories

# Once directories are created, launch all content file creations together:
Task: "Create and populate my-ai-book/docs/Introduction/01-Foundations-Hardware.md"
Task: "Create and populate my-ai-book/docs/Module-1-ROS2/01-Week-3-Nodes-Topics.md"
# ... and so on for all content files
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all content generation)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Build the Docusaurus project and verify all content and navigation.

### Incremental Delivery

- The current task list focuses on a single, large user story. This will be delivered as a complete unit.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    - Multiple developers can work in parallel on creating different module directories and their respective content MDX files within Phase 3.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
