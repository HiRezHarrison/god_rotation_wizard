# Project Checklist: God Rotation Manager

## Phase 1: Setup, Planning & Refactoring
- [x] Initialize `.cursor` directory and subdirectories.
- [x] Populate `.cursor/tools` and `.cursor/notes` from repo.
- [x] Initialize note files (`project_checklist.md`, `notebook.md`, `agentnotes.md`).
- [x] Initial project review (old requirements).
- [x] Update `agentnotes.md` with initial findings.
- [x] Create initial `project_checklist.md`.
- [x] Receive new requirements (God Rotation Management).
- [x] Identify relevant API endpoints (`GET /vendor/:vendor_id`, `PUT /loot/:loot_id`).
- [x] Identify God List Vendor ID (`00000000-0000-0000-0000-00000000004e`).
- [x] Update `agentnotes.md` for new project direction.
- [x] Update `project_checklist.md` for new project direction.
- [ ] **Codebase Search:** Confirm `PUT /loot/:loot_id` usage in existing code.
- [ ] **Refactor:** Rename `chest_creation_wizard.py` to `god_rotation_manager.py` (and update `.code-workspace`).
- [ ] **Refactor:** Remove obsolete file parsing logic.
- [ ] **Refactor:** Remove obsolete chest creation logic/variables.
- [ ] Analyze `Requirements.txt` and set up/update virtual environment.
- [ ] Define updated project architecture (confirm UI framework, module structure).
- [ ] Create detailed technical specification for God Rotation Manager in `.cursor/docs`.

## Phase 2: Core Logic Implementation
- [ ] Implement/Adapt API interaction module for `GET /vendor/:vendor_id` and `PUT /loot/:loot_id` (setting `active` flag).
- [ ] Implement core God rotation logic (fetch list, prepare updates based on selection).
- [ ] Adapt logging functionality for new API calls.

## Phase 3: UI Implementation
- [ ] Implement Screen 1 (Intro Text).
- [ ] Implement Screen 2 (Input: Auth Token, Sandbox ID).
- [ ] Implement Screen 3 (Fetch & Display God List with checkboxes).
- [ ] Implement Screen 4 (Adapt Progress Display for LTI updates, Log Button, Exit Button).

## Phase 4: Testing
- [ ] Set up/Adapt test framework (`tests/` directory).
- [ ] Write unit tests for API interaction (mocking API calls).
- [ ] Write unit tests for core God rotation logic.
- [ ] Write integration tests for component interactions.
- [ ] Write feature tests for UI and end-to-end workflow.

## Phase 5: Finalization
- [ ] Code review and refactoring.
- [ ] Final testing and bug fixing.
- [ ] Documentation updates. 