# Project Checklist: God Rotation Manager

## Completed Tasks
- [x] Rename `chest_creation_wizard.py` to `god_rotation_manager.py` (and update `.code-workspace`)
- [x] Refactor the codebase to focus on God rotation management
- [x] Implement 4-screen workflow (Welcome, Configuration, God Selection, Processing)
- [x] Create the God Selection interface with sorting options
- [x] Implement Check All/Uncheck All functionality
- [x] Add detailed logging for API operations
- [x] Add download capability for logs
- [x] Fix UI navigation by adding buttons at the top of Screen 3
- [x] Ensure application works on first run with dependency checking
- [x] Clean up legacy files (chest_item_lists, assets)
- [x] Ability to save current selections as templates for future use (Batch Ops - Chunk 1)
- [x] Dark mode toggle for UI (UX - Chunk 1)
- [x] Confirmation screen before processing updates (Safety - Chunk 1)

## Prioritized Features for Tomorrow / Next Steps

### Chunk 2: Enhanced Batch Ops & Data Preview
- [ ] Support for loading predefined god lists from JSON/CSV files (Batch Ops)
- [ ] Preview mode for API payloads without submitting (Safety)

### Chunk 3: Advanced UI & Interaction
- [ ] Search/filter capabilities for the god list (UX)
- [ ] Categories/tags for gods to enable group selection (by pantheon, role) (UX)

### Chunk 4: Integration & Automation
- [ ] Simple REST API wrapper for programmatic access (Integration)
- [ ] Slack/Discord notifications for rotation changes (Integration)
- [ ] Scheduled rotation changes (future date/time) (Operational)

### Chunk 5: Deployment & Ops
- [ ] Dockerize the application (Operational)
- [ ] Health check endpoint (Operational)

### Deferred / High Risk
- [ ] Rollback capability to revert to previous state

## Technical Debt / Refactoring
- [ ] Add comprehensive inline code documentation
- [ ] Create unit tests for critical components
- [ ] Modularize the code further for maintainability
- [ ] Refactor `god_rotation_manager.py` (currently > 500 lines) into smaller modules
- [ ] Review and potentially remove unused code in `src/` (e.g., `chest_*.py`)

## Phase 1: Setup, Planning & Refactoring (Mostly Complete)
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
- [ ] **Codebase Search:** Confirm `PUT /loot/:loot_id` usage in existing code (Likely done, verify).
- [ ] **Refactor:** Remove obsolete file parsing logic (Likely done, verify).
- [ ] **Refactor:** Remove obsolete chest creation logic/variables (`chest_*.py`).
- [x] Analyze `Requirements.txt` and set up/update virtual environment (Handled by `run_app.py`).
- [ ] Define updated project architecture (confirm UI framework, module structure).
- [ ] Create detailed technical specification for God Rotation Manager in `.cursor/docs` (Needs creation).

## Phase 2: Core Logic Implementation (Complete)
- [x] Implement/Adapt API interaction module for `GET /vendor/:vendor_id` and `PUT /loot/:loot_id` (setting `active` flag).
- [x] Implement core God rotation logic (fetch list, prepare updates based on selection).
- [x] Adapt logging functionality for new API calls.

## Phase 3: UI Implementation (Complete for Core + Chunk 1)
- [x] Implement Screen 1 (Intro Text).
- [x] Implement Screen 2 (Input: Auth Token, Sandbox ID).
- [x] Implement Screen 3 (Fetch & Display God List with checkboxes, sorting, bulk ops, Save Template).
- [x] Implement Screen 3b (Confirmation Screen).
- [x] Implement Screen 4 (Progress Display, Log Buttons, Start Over Button).
- [x] Implement Sidebar (Dark Mode Toggle).

## Phase 4: Testing
- [ ] Set up/Adapt test framework (`tests/` directory).
- [ ] Write unit tests for API interaction (mocking API calls).
- [ ] Write unit tests for core God rotation logic.
- [ ] Write unit tests for Save/Load Template functionality.
- [ ] Write integration tests for component interactions.
- [ ] Write feature tests for UI and end-to-end workflow.

## Phase 5: Finalization
- [ ] Code review and refactoring.
- [ ] Final testing and bug fixing.
- [ ] Documentation updates. 