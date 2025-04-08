# God Rotation Manager - Development Notebook

## Latest Updates (April 8, 2025 - End of V1.2 Cycle)

### Final Feature: Delete Template
- Added a "Delete Template" button to Screen 3 next to the Load/Save controls.
- This allows deletion of the currently selected template file from the `templates/` directory.
- Includes basic error handling (file not found, permissions).
- **Action Item:** This feature needs to be tested at the start of the next session.

### Chunk 2 Implementation & Revert
- **Load Template:** Added functionality on Screen 3 to load a saved JSON template (`templates/` dir) using a dropdown and button. Updates the current `god_selection` state, respecting only `loot_id`s present in the currently fetched `god_list`.
- **Batch Update Attempt:**
    - Explored using `PUT` and then `POST` on the `/v1/sandbox/{sid}/loot` endpoint with a `{"data": [...]}` payload to perform batch updates.
    - `PUT` failed with `405 Method Not Allowed`.
    - `POST` failed with `409 Conflict - loot_legacy_id_already_exists`.
    - **Conclusion:** This endpoint is confirmed for batch *creation*, not batch *update* of existing loot items.
    - **Action:** Reverted the API client and Screen 4 logic back to using sequential individual `PUT /v1/sandbox/{sid}/loot/{lid}` calls for each update.
- **Preview Mode:** Implemented preview mode on Screen 3b to show the potential batch payload. Removed this feature after the batch update approach was abandoned.
- **Performance Optimization:** Removed the `time.sleep(0.1)` delay between individual `PUT` calls in the update loop on Screen 4. Resulted in slightly faster processing, deemed acceptable for now.

### Chunk 1 Implementation (Completed Earlier)
- **Save Template:** Added functionality on Screen 3 to save the current `god_selection` dictionary to a user-named JSON file in the `templates/` directory.
- **Dark Mode Toggle:** Added a toggle widget to the sidebar (`st.session_state.dark_mode`). Note: Does not yet apply visual theme changes.
- **Confirmation Screen:** Implemented a new screen (Screen 3b) between selection and processing. This screen summarizes changes:
    - Counts for Activating, Deactivating, Remaining Active, Remaining Inactive gods.
    - An expander shows detailed lists (comma-separated names) for each category.
    - Requires explicit confirmation before proceeding to Screen 4.

### Bug Fixes & Improvements (During V1.2 Cycle)
- **Screen 4 Re-run:** Fixed a bug where the API update loop would re-execute on Screen 4 after interactions like Download Log or Start Over. Introduced `update_process_complete` flag to ensure the loop runs only once per confirmation cycle.
- **Confirmation Screen Clarity:** Improved the summary on Screen 3b to explicitly state counts and details for gods *not* changing state.
- **UI Layout:** Moved the "Save Template" UI elements to the top of Screen 3 for better workflow.
- **Code Structure:** Refactored update calculation logic into `calculate_update_summary` helper function. Moved `get_god_name` to global scope.

### Code Branching
- Created and pushed branch `V1.0` to mark the stable state before Chunk 1 development.
- Current state corresponds to planned `V1.2` commit/tag.

### Known Issues - Update Speed
- Updates are processed sequentially (one API call per god).
- Batch update not feasible with known endpoints.
- Speed is acceptable for now but could be slow for hundreds of changes.

## Previous Updates (April 7, 2025)

### UI Navigation Improvement
- Added navigation buttons to the top of Screen 3
- This eliminates the need to scroll through a long list of gods to navigate between screens
- Kept the form submit button at the bottom for logical flow

### Dependencies and First-Run Experience
- Created `run_app.py` with proper dependency checking that runs before Streamlit
- The script first checks for and installs required packages, then launches Streamlit
- This solves the circular dependency problem where Streamlit was needed to run the app that would check if Streamlit was installed
- The script also handles port conflicts by automatically finding an available port

### Cleanup and Optimization
- Removed legacy files and folders (chest_item_lists, assets) that were not needed for the god rotation functionality
- This reduces the codebase size and removes potential confusion

## API Findings

### God Data Structure
The API returns god data with these key fields:
- `loot_id`: Unique identifier (UUID format)
- `name`: The god's name (e.g., "Persephone")
- `item_name`: Sometimes contains the name, sometimes blank
- `active`: Boolean flag indicating if the god is in rotation
- Various other fields needed for the full PUT payload

To update a god's status, the entire object must be sent back with only the `active` field modified.

### Name Resolution Strategy
Created a function to resolve god names by checking multiple potential fields:
```python
def get_god_name(god):
    for field in ['item_name', 'name', 'god_name', 'title', 'display_name', 'inventory_item_name']:
        if field in god and god[field]:
            return god[field]
    return god['loot_id']  # Fallback
```

## Feature Ideas (Pre-V1.2 Development)

### Batch Operations
Key considerations:
- Format for saved templates (JSON with loot_ids and desired states) - [x] Save, [x] Load, [x] Delete (Delete needs testing)
- Validation to ensure loot_ids still exist - Handled during Load

### Search/Filter
Implementation ideas:
- Text search box above the god list
- Filter dropdowns for active/inactive status
- Pagination for better performance with large lists

### Integration API
Potential endpoints:
- GET /api/gods - List all gods and their status
- POST /api/gods/update - Batch update multiple gods
- GET /api/templates - List saved templates
- Safety considerations for authentication 

### Template Management Functionality Confirmed
- Tested the template deletion functionality - working as expected
- Complete template management flow now includes:
  - Saving current god selections as named templates
  - Loading templates to restore saved selections
  - Deleting unwanted templates from the system
  - Templates are stored as JSON files in the templates/ directory 