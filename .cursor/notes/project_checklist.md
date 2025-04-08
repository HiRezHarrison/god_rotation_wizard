# Project Checklist: God Rotation Manager

## Completed Tasks
- [x] Rename `chest_creation_wizard.py` to `god_rotation_manager.py` (and update `.code-workspace`)
- [x] Refactor the codebase to focus on God rotation management
- [x] Implement 4-screen workflow (Welcome, Config, Selection, Confirmation, Processing, Summary)
- [x] Create the God Selection interface with sorting options
- [x] Implement Check All/Uncheck All functionality
- [x] Add detailed logging for API operations (per-item updates)
- [x] Add download capability for logs
- [x] Fix UI navigation by adding buttons at the top of Screen 3
- [x] Ensure application works on first run with dependency checking
- [x] Clean up legacy files (chest_item_lists, assets)
- [x] Ability to save current selections as templates (Batch Ops - Chunk 1)
- [x] Dark mode toggle for UI control (UX - Chunk 1)
- [x] Confirmation screen with detailed change summary (Safety - Chunk 1)
- [x] Fix Screen 4 update re-run bug
- [x] Ability to load selections from templates (Batch Ops - Chunk 2)
- [x] Remove `time.sleep(0.1)` from update loop (Performance)
- [x] Investigate & Revert failed Batch Update attempt (API Limitation)
- [x] Ability to delete saved templates (Batch Ops - V1.2 Addon)
- [x] Implement template save/load functionality
- [x] Add template deletion capability (**Tested and confirmed working**)

## Prioritized Features for Next Session

### Testing
- [x] Test Delete Template functionality.

### Chunk 3: Advanced UI & Interaction
- [x] Enhance search/filter capabilities for the god list.
  - [x] Implement advanced search options (exact match, contains, starts with)
  - [x] Add filtering options for active/inactive status
  - [x] Improve visual feedback for search results
  - [x] Save search history or frequently used searches
- [ ] ~~Categories/tags for gods (pantheons, roles, etc.)~~ *POSTPONED* - Will be implemented in a future iteration when we have clearer requirements for the feature.

### Refactoring & Testing
- [ ] Modularize `god_rotation_manager.py` (currently > 800 lines) into smaller modules (e.g., `ui_screens.py`, `state_helpers.py`).
- [ ] Create unit tests for critical components (API client mocking, state logic, template functions).
- [ ] Remove legacy code (`src/chest_*.py`).

### Optional / Polish
- [ ] Apply visual Dark Mode theme based on toggle.
- [ ] Add comprehensive inline code documentation.

### Deferred / Longer Term
- [ ] Simple REST API wrapper for programmatic access (Integration - Chunk 4)
- [ ] Slack/Discord notifications for rotation changes (Integration - Chunk 4)
- [ ] Scheduled rotation changes (future date/time) (Operational - Chunk 4)
- [ ] Dockerize the application (Operational - Chunk 5)
- [ ] Health check endpoint (Operational - Chunk 5)
- [ ] Rollback capability to revert to previous state (High Risk / Effort)

## Phase 1: Setup, Planning & Refactoring (Complete)
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
- [x] Analyze `Requirements.txt` and set up/update virtual environment (Handled by `run_app.py`).

## Phase 2: Core Logic Implementation (Complete)
- [x] Implement/Adapt API interaction module for `GET /vendor/:vendor_id` and `PUT /loot/:loot_id` (setting `active` flag).
- [x] Implement core God rotation logic (fetch list, prepare updates based on selection).
- [x] Adapt logging functionality for new API calls.

## Phase 3: UI Implementation (Complete for V1.2)
- [x] Implement Screen 1 (Intro Text).
- [x] Implement Screen 2 (Input: Auth Token, Sandbox ID).
- [x] Implement Screen 3 (Fetch & Display God List, sorting, bulk ops, Save/Load/Delete Template).
- [x] Implement Screen 3b (Confirmation Screen).
- [x] Implement Screen 4 (Sequential Progress Display, Log Buttons, Start Over Button).
- [x] Implement Sidebar (Dark Mode Toggle).

## Phase 4: Testing
- [ ] Set up/Adapt test framework (`tests/` directory).
- [ ] Write unit tests for API interaction (mocking API calls).
- [ ] Write unit tests for core God rotation logic.
- [ ] Write unit tests for Save/Load/Delete Template functionality.
- [ ] Write integration tests for component interactions.
- [ ] Write feature tests for UI and end-to-end workflow.

## Phase 5: Finalization
- [ ] Code review and refactoring (Ongoing - See Technical Debt section).
- [ ] Final testing and bug fixing.
- [ ] Documentation updates (Ongoing - This checklist, agentnotes, notebook).

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

## Recent Updates & Changes

### Version 1.4.2 Updates (COMPLETED)
- [x] Fixed persistent search bug where two enter keypresses were required
- [x] Completely redesigned search implementation to use direct callbacks
- [x] Removed form-based search to eliminate input submission issues
- [x] Search now responds immediately to input changes without requiring button clicks

### Version 1.4.1 Updates (COMPLETED)
- [x] Fixed search bug that required two attempts to execute a search query
- [x] Implemented proper form handling for search functionality
- [x] Added "Clear Search" button for better user experience
- [x] Improved handling of Enter key in search field

### Version 1.4 Updates (COMPLETED)
- [x] Enhanced search and filter capabilities for the god list:
  - [x] Added advanced search options (contains, exact match, starts with)
  - [x] Implemented status filtering (all, active, inactive)
  - [x] Added case sensitivity option
  - [x] Implemented recent searches history (up to 5 saved searches)
  - [x] Improved visual feedback with search result counts and percentages
  - [x] Added metrics showing total gods, currently active, and selected to be active
  - [x] Search parameters now persist when navigating between screens

### Version 1.3 Updates (COMPLETED)
- [x] Implemented the version display feature in terminal output and UI
  - Added version to app_config.json
  - Created config_utils.py for loading configuration
  - Updated run_app.py to show version in terminal
  - Updated god_rotation_manager.py to display version in UI title
- [x] Fixed Screen 4 implementation to use full loot data for API updates
- [x] Enhanced the god selection screen (Screen 3) to store full loot dictionaries
- [x] Improved error handling throughout the application
- [x] Fixed dark mode toggle to work with a single click
- [x] Ensured dark mode settings persist between screen navigation

### Ready for Next Phase
- Version 1.3 has been successfully tested and all features are working correctly
- Core functionality is complete and stable
- User interface is intuitive and responsive 