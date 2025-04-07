# God Rotation Manager - Development Notebook

## Latest Updates (April 7, 2025)

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

## Feature Ideas for Tomorrow

### Batch Operations
Key considerations:
- Format for saved templates (JSON with loot_ids and desired states)
- UI for importing/exporting templates
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