# Agent Notes: God Rotation Manager

## Project Status

The God Rotation Manager is a Streamlit-based application for managing the active status of gods in SMITE 2 via the RallyHere API.

### Current State (as of Chunk 1 completion)
- Core workflow implemented: Welcome -> Config -> Selection -> **Confirmation** -> Processing -> Summary/Logs.
- APIs for fetching and updating god statuses are working.
- UI improvements implemented: Sorting, Check/Uncheck All, Top Nav Buttons, Save Template.
- Safety feature added: Confirmation screen detailing changes (activating, deactivating, unchanged).
- Basic UX feature added: Dark mode toggle (visual theme not yet applied).
- Bug fixed: Update loop no longer re-runs on Screen 4 after completion.
- Legacy files cleaned up.
- Helper script (`run_app.py`) handles dependencies and launch.

### Key Files
- `god_rotation_manager.py`: Main application file (Refactored slightly, needs further modularization).
- `src/rallyhere_api.py`: API client for RallyHere.
- `run_app.py`: Helper script with dependency handling.
- `config/app_config.json`: Application configuration.
- `config/api_template.json`: API templates (Likely largely unused currently).
- `templates/`: Directory for saved selection templates (JSON format).

### Configuration
- **APIs**: RallyHere developer API for fetching/updating gods (using individual `PUT /loot/{loot_id}` calls).
- **Sandbox ID**: User-provided (defaults to `412abbcb-5f50-4072-b05f-a3c371087dba` from config).
- **God Vendor ID**: `00000000-0000-0000-0000-00000000004e` (hardcoded).

## Technical Details

### Data Structure
- Gods fetched via `GET /vendor/{vendor_id}`. Full loot data stored in `st.session_state.god_list`.
- Selection stored in `st.session_state.god_selection` as `{loot_id: bool}`.
- Templates saved in `templates/` as JSON `{loot_id: bool}`.
- Updates require the full loot object with modified `active` field sent via `PUT /loot/{loot_id}`.
- Helper `get_god_name` resolves display names.
- Helper `calculate_update_summary` determines gods to update and unchanged gods.

### Update Process Speed
- Currently sequential, one API call per god update.
- Includes a `time.sleep(0.1)` between calls.
- Potential optimization: Remove sleep, investigate batch update endpoint.

### Known Issues/Areas for Improvement
- Dark mode toggle exists but doesn't visually change the theme yet.
- `god_rotation_manager.py` is long (>600 lines) and could be modularized.
- API calls are sequential; could be slow for very large updates.
- No unit/integration tests yet.
- Potential legacy code in `src/` (`chest_*.py`).

## User Information
- Expected users: Team members managing god rotations for SMITE 2.
- Users need RallyHere developer auth token with appropriate permissions.

## Next Steps (Post-Chunk 1)

1.  **Chunk 2: Enhanced Batch Ops & Data Preview**
    *   Implement loading selection templates from files in `templates/`.
    *   Implement Preview Mode on the confirmation screen to show example API payloads.
2.  **(Potential Optimization)** Remove `time.sleep(0.1)` in the update loop (Screen 4) to improve speed.
3.  **Chunk 3: Advanced UI & Interaction**
    *   Search/filter capabilities for the god list.
    *   Category/tag-based grouping (requires data source).

See `.cursor/notes/project_checklist.md` for the detailed task list and priorities. 