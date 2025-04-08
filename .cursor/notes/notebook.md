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

## Version Tracking Implementation (April 8, 2025)

Added version tracking throughout the application to better track releases and make it clear to users which version is running:

1. **Configuration Storage**:
   - Added `version` field to `config/app_config.json` (set to `1.3` for current release)
   - This centralizes the version information in a single place

2. **Configuration Loading**:
   - Created `src/config_utils.py` to handle loading configuration
   - Implemented a caching mechanism to avoid repeated file reads
   - Added `get_version()` function to retrieve current version

3. **Terminal Display**:
   - Updated `run_app.py` to show version in startup banner
   - Format: `=== SMITE 2 God Rotation Manager v1.3 ===`
   - This makes it clear which version is running when starting from command line

4. **UI Display**:
   - Modified title in `god_rotation_manager.py` to include version
   - Displayed as: `SMITE 2 God Rotation Manager v1.3`
   - Removed hardcoded version from docstring to avoid duplication

5. **Documentation Updates**:
   - Updated checklist and agent notes to reflect current version (1.3)
   - Documented version changes in project history

This versioning system will make it easier to track changes across releases and ensure users are aware of which version they're using. Future updates should increment the version number in `app_config.json`. 

## Dark Mode Implementation Fixes (April 8, 2025)

The dark mode feature has been successfully implemented with the following improvements:

1. **Single-Click Activation**:
   - Fixed issue where toggle required two clicks to take effect
   - Added state comparison between previous and current dark mode setting
   - Implemented automatic page rerun when dark mode state changes
   - Code: `if dark_mode != previous_dark_mode: st.rerun()`

2. **Persistence Between Screens**:
   - Dark mode setting now properly stored in `st.session_state.dark_mode`
   - State persists across all screens in the application
   - Consistent experience maintained throughout the workflow

3. **Implementation Details**:
   - Dark mode toggle uses Streamlit's `st.sidebar.toggle()` control
   - CSS styling applied conditionally based on dark mode state
   - Visual feedback shows current mode (enabled/disabled) in sidebar

This implementation ensures a smooth user experience with dark mode that behaves consistently with user expectations. The toggle is responsive and the setting is maintained as users navigate through the application.

## Version 1.3 Completion

Version 1.3 has been successfully completed and tested with all planned features working correctly:
- Version tracking throughout the application
- Full god selection and update functionality
- Template management (save, load, delete)
- Dark mode with proper persistence
- Comprehensive error handling

Next phase of development can now proceed on solid foundations. 

## Enhanced Search & Filter Implementation (April 8, 2025)

Version 1.4 introduces a significantly enhanced search and filter system for the god list on Screen 3:

1. **Advanced Search Options**:
   - Multiple search modes:
     - **Contains**: Finds gods with names containing the search string (default)
     - **Exact Match**: Only matches gods with names exactly matching the search string
     - **Starts With**: Finds gods with names starting with the search string
   - Case sensitivity toggle for more precise searching
   - Support for partial name matches

2. **Status Filtering**:
   - Filter options to show:
     - All gods (default)
     - Only currently active gods
     - Only currently inactive gods
   - Combined with search for more targeted results

3. **Recent Searches**:
   - System remembers up to 5 recent searches with results
   - Recent searches shown in an expandable section
   - One-click restoration of previous search parameters

4. **Visual Feedback**:
   - Shows count of matching gods
   - Displays percentage of total gods matching criteria
   - Clear messaging when no results are found
   - Status indicators for search effectiveness

5. **Metrics Dashboard**:
   - Added metrics at the top of Screen 3 showing:
     - Total number of gods
     - Currently active gods (with percentage)
     - Selected to be active (with delta from current)

6. **Search State Persistence**:
   - Search parameters persist when navigating between screens
   - Automatically restores last used search when returning to Screen 3

7. **Bulk Actions**:
   - Renamed bulk action buttons to "Check All Results" and "Uncheck All Results"
   - Actions now apply only to filtered results for more precise batch operations

8. **Search Bug Fixes**:
   - Fixed issue where search required two attempts to apply
   - Implemented proper form handling with a submit button
   - Added "Clear Search" button for easier reset
   - Made search status more visible with current search display
   - Improved handling of Enter key in search field
   - Prevented duplicate entries in recent searches

This enhanced search system makes managing large god rosters much more efficient by allowing users to quickly find and modify exactly the gods they need. 

## Search Functionality Bug Fix (April 8, 2025) - Version 1.4.1

Version 1.4.1 addresses a critical usability issue with the search functionality implemented in version 1.4:

1. **Root Issue**:
   - The original implementation required two attempts to execute a search query
   - First attempt would clear the input field but not apply the search
   - Second attempt with the same query would finally execute the search
   - This created confusion and poor user experience

2. **Form-Based Solution**:
   - Implemented a proper Streamlit form with a dedicated "Apply Search" button
   - This correctly handles the submission process in a single operation
   - Form approach properly manages Enter key handling in input fields
   - Search is now properly applied on first submission

3. **UI Improvements**:
   - Added clear indication of current active search with text display
   - Added a "Clear Search" button for one-click search reset
   - Better organization of search controls in a logical form
   - Prevented duplicate entries in recent searches history

4. **Enhanced Status Feedback**:
   - More visible indicators when search is active
   - Clear confirmation of search parameters being applied
   - Consistent visual state between form submission and results

This bug fix substantially improves the usability of the search feature, making it behave as users would intuitively expect. The version number increment to 1.4.1 reflects this targeted fix to a specific feature without introducing new functionality. 

## Search Implementation Complete Redesign (April 8, 2025) - Version 1.4.2

Version 1.4.2 completely redesigns the search implementation to fix a persistent issue with search submission:

1. **Root Issue Identified**:
   - Even after the form-based implementation in 1.4.1, users still needed to press Enter twice
   - The first keypress would update the search field but not trigger the search
   - This created a confusing user experience as changes weren't immediately reflected

2. **Callback-Based Solution**:
   - Completely removed the form-based approach
   - Implemented individual callbacks on each search control (input field, radio buttons, checkbox)
   - Each user interaction now directly updates the session state and triggers a rerun
   - Changes take effect immediately without requiring explicit form submission

3. **Technical Implementation**:
   - Added `on_change` handlers to all search widgets
   - Created a dedicated callback function that updates session state
   - Automatically triggers a Streamlit rerun to apply changes immediately
   - No need for a separate "Apply Search" button - everything is immediate

4. **Advantages of New Approach**:
   - Single keypress or selection immediately applies the search
   - More intuitive and responsive user experience
   - No form submission delays or quirks
   - Consistent with standard search behavior in modern applications

This redesign represents a significant improvement in the search usability by leveraging Streamlit's callback system rather than trying to force traditional form behavior, which was causing the persistent issues. 