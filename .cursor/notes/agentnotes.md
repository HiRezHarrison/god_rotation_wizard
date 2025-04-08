# Agent Notes: God Rotation Manager

## Project Status

The God Rotation Manager is a Streamlit-based application for managing the active status of gods in SMITE 2 via the RallyHere API.

### Current State (End of Session, V1.2 Target)
- Core workflow implemented: Welcome -> Config -> Selection -> Confirmation -> Processing -> Summary/Logs.
- APIs for fetching (`GET /vendor/{vid}`) and updating (`PUT /loot/{lid}`) god statuses are working.
- **Batch Operations (Partial):**
    - [x] Save current god selections to JSON templates (`templates/` dir).
    - [x] Load god selections from saved JSON templates.
- **UI Improvements:**
    - [x] God list sorting (Name, Active Status).
    - [x] Check All / Uncheck All buttons.
    - [x] Navigation buttons at top of Screen 3.
    - [x] Dark mode toggle control added (visual theme not implemented).
- **Safety Features:**
    - [x] Confirmation screen detailing changes (activating, deactivating, unchanged).
- **Bug Fixes:**
    - [x] Update loop no longer re-runs erroneously on Screen 4.
- **Performance:**
    - [x] Removed `time.sleep(0.1)` delay between individual god updates.
    - **Failed Attempt:** Batch update via `POST /loot` failed (409 Conflict, endpoint is for *creation*). Reverted to individual `PUT /loot/{lid}` calls. See Notebook for details.
- **Code Structure:**
    - Helper script (`run_app.py`) handles dependencies and launch.
    - Some refactoring (`get_god_name`, `calculate_update_summary`).
    - `god_rotation_manager.py` remains large (>700 lines).

### Key Files
- `god_rotation_manager.py`: Main application file.
- `src/rallyhere_api.py`: API client (Uses individual PUT for updates).
- `run_app.py`: Launcher script.
- `config/app_config.json`: Application configuration.
- `templates/`: Directory for saved selection templates.

### Configuration
- **APIs**: RallyHere developer API. Uses `GET /vendor/{vid}` and `PUT /loot/{lid}`.
- **Sandbox ID**: User-provided.
- **God Vendor ID**: `00000000-0000-0000-0000-00000000004e` (hardcoded).

## Technical Details

### Update Process
- Fetches all gods from vendor `0000...4e`.
- User selects desired `active` state via checkboxes or loading a template.
- Confirmation screen summarizes changes.
- On confirmation, iterates through gods whose desired state differs from current state.
- For each change, prepares the full loot data object, sets the `active` flag, removes read-only fields (`_prepare_loot_payload`), and sends a `PUT` request to `/v1/sandbox/{sandbox_id}/loot/{loot_id}`.
- Logs each individual API call.
- Displays summary upon completion.

### Batch Update Investigation (Failed)
- **Hypothesis:** `POST /v1/sandbox/{sid}/loot` with `{"data": [...]}` could perform batch updates.
- **Test 1 (PUT):** Attempted `PUT` to `/loot` endpoint with batch payload -> resulted in `405 Method Not Allowed`.
- **Test 2 (POST):** Changed to `POST` method for `/loot` endpoint -> resulted in `409 Conflict` with `"error_code": "loot_legacy_id_already_exists"`. 
- **Conclusion:** This endpoint appears strictly for *creating* new loot items, not batch *updating* existing ones based on `loot_id` in the payload. Reverted to sequential individual `PUT` calls.

### Known Issues/Areas for Improvement
- Dark mode toggle doesn't apply theme.
- `god_rotation_manager.py` needs modularization.
- Sequential updates can be slow for large changes (batch update not feasible with known endpoints).
- No automated tests.
- Potential legacy code (`src/chest_*.py`).

## User Information
- Expected users: Team members managing god rotations.
- Requires: RallyHere developer auth token with permissions.

## Next Steps (Post-V1.2)

1.  **Chunk 3: Advanced UI & Interaction**
    *   Search/filter capabilities for the god list.
    *   Category/tag-based grouping (requires data source).
2.  **Refactoring & Testing:**
    *   Modularize `god_rotation_manager.py`.
    *   Implement basic unit tests.
    *   Remove legacy code.
3.  **(Optional)** Apply Dark Mode visual theme.

See `.cursor/notes/project_checklist.md` for detailed task list. 