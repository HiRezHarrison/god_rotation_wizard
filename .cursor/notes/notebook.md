# God Rotation Manager - Development Notebook

## Latest Updates (April 8, 2025 - End of Chunk 1)

### Chunk 1 Implementation
- **Save Template:** Added functionality on Screen 3 to save the current `god_selection` dictionary to a user-named JSON file in the `templates/` directory.
- **Dark Mode Toggle:** Added a toggle widget to the sidebar (`st.session_state.dark_mode`). Note: Does not yet apply visual theme changes.
- **Confirmation Screen:** Implemented a new screen (Screen 3b) between selection and processing. This screen summarizes changes:
    - Counts for Activating, Deactivating, Remaining Active, Remaining Inactive gods.
    - An expander shows detailed lists (comma-separated names) for each category.
    - Requires explicit confirmation before proceeding to Screen 4.

### Bug Fixes & Improvements
- **Screen 4 Re-run:** Fixed a bug where the API update loop would re-execute on Screen 4 after interactions like Download Log or Start Over. Introduced `update_process_complete` flag to ensure the loop runs only once per confirmation cycle.
- **Confirmation Screen Clarity:** Improved the summary on Screen 3b to explicitly state counts and details for gods *not* changing state.
- **UI Layout:** Moved the "Save Template" UI elements to the top of Screen 3 for better workflow.
- **Code Structure:** Refactored update calculation logic into `calculate_update_summary` helper function. Moved `get_god_name` to global scope.

### Code Branching
- Created and pushed branch `V1.0` to mark the stable state before Chunk 1 development.

### Known Issue - Update Speed
- Updates are processed sequentially (one API call per god).
- A `time.sleep(0.1)` exists between each call.
- Next potential optimization: Remove the sleep delay.

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

## Feature Ideas (Pre-Chunk 1)

### Batch Operations
Key considerations:
- Format for saved templates (JSON with loot_ids and desired states) - Implemented Save
- UI for importing/exporting templates - Load needed
- Validation to ensure loot_ids still exist

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