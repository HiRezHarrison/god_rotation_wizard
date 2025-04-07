# Agent Notes: god_rotation_wizard / chest_creation_wizard

## Project Overview (Updated)
- **Goal**: **Manage the active status of Gods in SMITE 2 rotations via the RallyHere API.**
- **Core Functionality**: UI for input (Sandbox ID, Auth Token) and God selection/status display, sequential API calls (Get Vendor, Update Loot), logging.
- **Technology**: Python (likely Streamlit, TBC).
- **API Endpoint**: `https://developer.rallyhere.gg/api/` (Requires auth token).
- **Key Vendor ID**: `00000000-0000-0000-0000-00000000004e` (for God list).

## Key Files/Directories (To Be Updated)
- **Rename:** `chest_creation_wizard.py` -> `god_rotation_manager.py` (Recommended).
- `src/`: Source code directory (API interaction module likely reusable).
- `tests/`: Test directory (needs updates).
- `config/`: Configuration (API docs added).
- `assets/`: UI assets (status icons reusable).
- ~~`chest_item_lists/`~~ (No longer needed).
- ~~`writeup.txt`~~ (Superseded by new requirements).
- `ui_outline.txt`: Needs significant updates for new Screens 1, 3, 4.
- `Requirements.txt`: Dependencies (review needed).
- `.cursor/`: Agent support files (rules, tools, docs, notes).

## Initial Setup Notes
- `.cursor` directory created and populated with standard tools/notes from `mycursorrules` repo (rules folder was empty in repo).
- Key note files initialized: `project_checklist.md`, `notebook.md`, `agentnotes.md`.

## Approach Guidance (Updated)
- **UI:**
    - Screen 1: Simplify - Intro text only.
    - Screen 2: Modify - Add Sandbox ID input.
    - Screen 3 (New): Fetch God list (`GET /vendor/:vendor_id`), display with checkboxes (default unchecked=deactivate).
    - Screen 4 (Old Screen 3): Adapt - Display progress of God LTI updates.
- **API:**
    - Get God List: `GET /api/v1/sandbox/:sandbox_id/vendor/:vendor_id` (using provided Vendor ID).
    - Update God Status: `PUT /api/v1/sandbox/:sandbox_id/loot/:loot_id` (likely adapting existing loot creation function, setting `active` flag).
- **Logic:**
    - Remove file parsing.
    - Implement new application flow.
    - Adapt logging.
- **Code Reuse:** Leverage existing API call structure and UI framework.
- Ensure secure handling of the user-provided auth token. 