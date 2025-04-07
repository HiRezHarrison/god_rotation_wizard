# God Rotation Wizard - Technical Details

## Architecture Overview

The God Rotation Wizard follows a modular architecture with the following key components:

1. **User Interface (Streamlit)**
   - Screen-based navigation system with session state management
   - Form controls for user input and data display
   - Progress tracking and status reporting

2. **API Client**
   - Encapsulated RallyHere API interactions
   - Authentication and request handling
   - Response parsing and error management

3. **Configuration Management**
   - External JSON configuration files
   - Runtime configuration validation
   - Dependency management

4. **Logging System**
   - API request/response logging
   - Operation status tracking
   - Downloadable log exports

## Key Implementation Details

### Streamlit Application Structure

The application is built around a screen-based model with the following screens:

1. **Screen 1 (Welcome)**: Introduction and initialization
2. **Screen 2 (Configuration)**: Auth token and sandbox ID input
3. **Screen 3 (God Selection)**: Display and selection of gods to update
4. **Screen 4 (Processing)**: Update execution and status tracking

State is managed using Streamlit's `st.session_state` dictionary, which persists across page refreshes. Key state variables include:

- `st.session_state.screen`: Current screen identifier
- `st.session_state.auth_token`: User's API authentication token
- `st.session_state.sandbox_id`: Target environment ID
- `st.session_state.god_list`: Complete list of gods fetched from the API
- `st.session_state.god_selection`: User selections for god active states

### RallyHere API Integration

The `RallyHereAPIClient` class manages all interactions with the RallyHere API:

```python
class RallyHereAPIClient:
    def __init__(self, auth_token: str, api_config: dict, api_template: dict):
        self.base_url = api_config['base_url']
        self.endpoints = api_config['endpoints']
        self.api_template = api_template
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    def get_vendor_loot(self, vendor_id: str, sandbox_id: str) -> APIResponse:
        # Fetches all loot (gods) from a specific vendor
        
    def update_loot_status(self, loot_id: str, sandbox_id: str, is_active: bool, full_loot_data: dict) -> APIResponse:
        # Updates the active status of a specific loot item (god)
```

Key API operations:

1. **GET Vendor Loot**: Retrieves all gods associated with the vendor
   - Endpoint: `v1/sandbox/{sandbox_id}/vendor/{vendor_id}`
   - Important Fields: `loot_id`, `name`, `item_name`, `active`

2. **PUT Loot Update**: Updates a god's active status
   - Endpoint: `v1/sandbox/{sandbox_id}/loot/{loot_id}`
   - Requires: Full loot object with modified `active` field

### God Data Management

God data is managed through several key processes:

1. **Data Fetching**:
   ```python
   response = client.get_vendor_loot(vendor_id=god_vendor_id, sandbox_id=sandbox_id)
   god_list = [loot for loot in response.data['loot'] if loot.get('loot_id')]
   ```

2. **Name Resolution**:
   ```python
   def get_god_name(god):
       # Try different possible name fields in order of preference
       for field in ['item_name', 'name', 'god_name', 'title', 'display_name']:
           if field in god and god[field]:
               return god[field]
       return god['loot_id']  # Fallback to loot_id if no name found
   ```

3. **Update Preparation**:
   ```python
   original_god_data_map = {item['loot_id']: item for item in st.session_state.god_list}
   
   for loot_id, desired_active_state in st.session_state.god_selection.items():
       original_data = original_god_data_map[loot_id]
       current_active_state = original_data.get('active', False)
       
       if desired_active_state != current_active_state:
           gods_to_update.append({
               'loot_id': loot_id,
               'name': get_god_name(original_data),
               'desired_active': desired_active_state,
               'full_data': original_data
           })
   ```

### Logging System

The application implements a comprehensive logging system:

```python
def log_api_call(operation, loot_id, request_data, response_data, success):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "operation": operation,
        "loot_id": loot_id,
        "request_data": request_data,
        "response_data": response_data,
        "success": success
    }
    st.session_state.api_logs.append(log_entry)
    return log_entry
```

Logs are stored in session state and can be:
- Viewed in an expandable UI component
- Downloaded as a JSON file for further analysis

### Application Launch Process

The application uses a custom launcher (`run_app.py`) to:
1. Kill any existing Streamlit processes
2. Find an available port for the application
3. Configure Streamlit with optimal settings
4. Launch the application with proper error handling

```python
def find_free_port(start_port=8888, max_attempts=10):
    port = start_port
    attempts = 0
    
    while attempts < max_attempts:
        if not is_port_in_use(port):
            return port
        port += 1
        attempts += 1
    
    return 0  # Let streamlit choose a port
```

## Error Handling Strategy

The application implements a multi-layered error handling approach:

1. **API Error Handling**:
   - Structured API responses with success/error flags
   - Detailed error messages from API responses
   - Graceful handling of network and server errors

2. **UI Error Handling**:
   - Clear error messages with user-friendly explanations
   - State validation before operations
   - Recovery options for error states

3. **Configuration Error Handling**:
   - Validation of required configuration files
   - Graceful fallbacks for missing configuration
   - Detailed error reporting for configuration issues

## Development Decisions

1. **Streamlit vs. Traditional Web Framework**:
   - Streamlit was chosen for rapid development and simplified state management
   - The simple UI requirements aligned well with Streamlit's capabilities
   - The application's workflow fits naturally with Streamlit's refresh model

2. **API Client Design**:
   - A dedicated class was implemented to encapsulate API interactions
   - Standardized response objects ensure consistent error handling
   - Logging is integrated directly into the client for comprehensive tracking

3. **Data Management Approach**:
   - Full god data is retained to ensure proper API updates
   - Names are resolved through multiple possible fields for flexibility
   - Sorting and filtering options are implemented for improved usability 