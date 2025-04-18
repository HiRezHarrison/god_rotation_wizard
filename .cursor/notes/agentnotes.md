# Agent Notes: God Rotation Manager

## Project Status

The God Rotation Manager is a Streamlit-based application for managing the active status of gods in SMITE 2 via the RallyHere API.

### Current State
- Basic workflow is implemented with 4 screens
- APIs for fetching and updating god statuses are working
- UI improvements have been made (sorting, bulk actions, buttons at top)
- Legacy files have been cleaned up (removed assets and chest_item_lists folders)
- Template management fully implemented and tested (save, load, delete)
- Delete template functionality confirmed working (April 8, 2025)

### Current State (End of Session, V1.4.2 COMPLETED)
- Completed search enhancements and bug fixes:
  - **V1.4:** Added advanced search modes, status filtering, case sensitivity, recent search history, metrics dashboard, search persistence.
  - **V1.4.1:** Initial fix for double-entry bug using form-based approach, added Clear Search button.
  - **V1.4.2:** Final fix for search bug by removing forms and using direct widget callbacks for immediate search updates.
- Core workflow remains fully functional with all previous features working correctly

### Next Steps
- Complete any additional UI improvements for version 1.4
- Test all search and filter functionality thoroughly
- Consider additional enhancements for user experience

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
- Delete Template functionality needs testing.
- Dark mode toggle doesn't apply theme.
- `god_rotation_manager.py` needs modularization.
- Sequential updates can be slow for large changes (batch update not feasible with known endpoints).
- No automated tests.
- Potential legacy code (`src/chest_*.py`).

## User Information
- Expected users: Team members managing god rotations.
- Requires: RallyHere developer auth token with permissions.

## Action Items for Next Session

1.  **TEST:** Verify the "Delete Template" functionality on Screen 3 works as expected.
2.  **Chunk 3: Advanced UI & Interaction**
    *   Implement Search/filter capabilities for the god list.
    *   (Optional) Implement Category/tag-based grouping (requires data source).
3.  **Refactoring & Testing:**
    *   Begin modularizing `god_rotation_manager.py`.
    *   Implement basic unit tests.

See `.cursor/notes/project_checklist.md` for detailed task list. 