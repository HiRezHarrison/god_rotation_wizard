# Agent Notes: God Rotation Manager

## Project Status

The God Rotation Manager is a Streamlit-based application for managing the active status of gods in SMITE 2 via the RallyHere API.

### Current State
- Basic workflow is implemented with 4 screens
- APIs for fetching and updating god statuses are working
- UI improvements have been made (sorting, bulk actions, buttons at top)
- Legacy files have been cleaned up (removed assets and chest_item_lists folders)

### Key Files
- `god_rotation_manager.py`: Main application file
- `src/rallyhere_api.py`: API client for RallyHere
- `run_app.py`: Helper script with dependency handling
- `config/app_config.json`: Application configuration
- `config/api_template.json`: API templates

### Configuration
- **APIs**: RallyHere developer API for fetching/updating gods
- **Sandbox ID**: `5641ab90-cbee-4460-ad6d-e3bc1545adb3` (default in config)
- **God Vendor ID**: `00000000-0000-0000-0000-00000000004e` (hardcoded)

## Technical Details

### Data Structure
- Gods are stored with complete loot data dictionaries
- Names are resolved using various possible field names (item_name, name, etc.)
- Updates require the full loot object with modified 'active' field

### Known Issues
- Connectivity issues with Streamlit server occasionally require manual restarts
- Names may display as UUIDs if API doesn't provide name fields
- All gods should be loaded but testing is needed to confirm this

## User Information
- Expected users: Team members managing god rotations for SMITE 2
- Users need RallyHere developer auth token with appropriate permissions

## Next Steps
The following features have been prioritized for tomorrow:

1. **Batch Operations**
   - Loading predefined god lists from files
   - Saving selection templates
   
2. **UI Improvements**
   - Search/filter functionality
   - Category-based grouping
   - Dark mode
   
3. **Integration & Safety Features**
   - REST API wrapper
   - Confirmation screens
   - Preview mode
   - Rollback capability

See `.cursor/notes/project_checklist.md` for the complete list of prioritized features. 