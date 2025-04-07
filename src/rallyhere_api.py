import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
import base64
from datetime import datetime, timezone

@dataclass
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Renamed class
class RallyHereAPIClient:
    def __init__(self, auth_token: str, api_config: dict, api_template: dict):
        self.base_url = api_config['base_url']
        # Sandbox ID might change per request, store config default but allow override?
        self.config_sandbox_id = api_config.get('sandbox_id') 
        self.endpoints = api_config['endpoints']
        self.api_template = api_template # Still needed for PUT/POST templates?
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        # Removed automatic sandbox ID update in templates as it might vary

    def _get_current_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> APIResponse:
        """Make an API request and handle common error cases"""
        try:
            endpoint = endpoint.lstrip('/')
            url = f"{self.base_url}/{endpoint}"
            
            # Basic logging
            print(f"\n--- RallyHere API Request ---")
            print(f"URL: {url}")
            print(f"Method: {method}")
            # print(f"Headers: {self.headers}") # Avoid printing token
            print(f"Headers: {{'Content-Type': '{self.headers.get('Content-Type')}', 'Authorization': 'Bearer ***'}}") 
            if params:
                 print(f"Params: {params}")
            if data:
                print(f"Data: {json.dumps(data, indent=2)}")
            print("---------------------------")
            
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data if data else None,
                params=params if params else None # Added params handling
            )
            
            print(f"\n--- RallyHere API Response ---")
            print(f"Status: {response.status_code}")
            # Limit printing large response bodies
            response_text = response.text
            if len(response_text) > 1000:
                 print(f"Body: {response_text[:1000]}... (truncated)")
            else:
                 print(f"Body: {response_text}")
            print("----------------------------")
            
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            # Handle potential empty success response body
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                 response_data = None # Or {} or some indicator of success with no body

            return APIResponse(success=True, data=response_data)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                 error_msg += f" | Status: {e.response.status_code} | Response: {e.response.text}"
            print(f"Error making API request: {error_msg}") # Ensure error is logged
            return APIResponse(success=False, error=error_msg)
        except Exception as e: # Catch other potential errors
            error_msg = f"An unexpected error occurred during API request: {str(e)}"
            print(error_msg)
            return APIResponse(success=False, error=error_msg)

    def get_vendor_loot(self, vendor_id: str, sandbox_id: str) -> APIResponse:
        """Get loot details for a specific vendor using the configured endpoint."""
        if 'vendor_by_id' not in self.endpoints:
             error_msg = "Configuration Error: 'vendor_by_id' endpoint not defined in app_config.json"
             print(error_msg)
             return APIResponse(success=False, error=error_msg)

        endpoint_structure = self.endpoints['vendor_by_id']
        try:
            endpoint = endpoint_structure.format(sandbox_id=sandbox_id, vendor_id=vendor_id)
        except KeyError as e:
             error_msg = f"Configuration Error: Missing placeholder {e} in 'vendor_by_id' endpoint structure."
             print(error_msg)
             return APIResponse(success=False, error=error_msg)
        
        return self._make_request("GET", endpoint)

    def get_user_account(self) -> APIResponse:
        """Get user account information using the configured endpoint."""
        if 'account' not in self.endpoints:
             error_msg = "Configuration Error: 'account' endpoint not defined in app_config.json"
             print(error_msg)
             return APIResponse(success=False, error=error_msg)

        endpoint = self.endpoints['account']
        return self._make_request("GET", endpoint)

    # --- Placeholder for Update Loot ---
    def update_loot_status(self, loot_id: str, sandbox_id: str, is_active: bool, full_loot_data: dict) -> APIResponse:
        """Update the active status of a specific loot item using PUT."""
        if 'loot_by_id' not in self.endpoints:
            error_msg = "Configuration Error: 'loot_by_id' endpoint not defined in app_config.json"
            print(error_msg)
            return APIResponse(success=False, error=error_msg)
            
        endpoint_structure = self.endpoints['loot_by_id']
        try:
            endpoint = endpoint_structure.format(sandbox_id=sandbox_id, loot_id=loot_id)
        except KeyError as e:
             error_msg = f"Configuration Error: Missing placeholder {e} in 'loot_by_id' endpoint structure."
             print(error_msg)
             return APIResponse(success=False, error=error_msg)
        
        # Prepare payload - NEED TO SEND THE ENTIRE OBJECT, not just 'active'
        # We fetched the full object earlier in get_vendor_loot, use that as base
        payload = full_loot_data.copy() # Avoid modifying the original dict
        payload['active'] = is_active
        
        # Remove fields that should not be sent back in PUT? Check API docs. Common ones:
        # Read-only fields like created_timestamp, last_modified*, *_name fields derived from IDs.
        read_only_fields = [
             'sandbox_id', 'last_modified_account_id', 'last_modified_timestamp', 
             'created_timestamp', 'loot_id', 'vendor_name', 'sub_vendor_name', 
             'item_name', 'required_item_name', 'quantity_multi_inventory_item_name',
             'current_price_point_name', 'pre_sale_price_point_name'
        ]
        for field in read_only_fields:
             payload.pop(field, None) # Remove if exists

        return self._make_request("PUT", endpoint, data=payload)

    # --- Obsolete Chest Methods (Keep for reference or remove?) ---
    # ... (create_item, create_vendor, create_loot, create_content_loot) ...
    
    # --- Template Processing (Keep if PUT/POST templates are used) ---
    def _process_template(self, template: dict, values: dict) -> dict:
        """Process a template, replacing variables with actual values"""
        processed = {}
        for key, value in template.items():
            if isinstance(value, str):
                # Handle ${variable} substitutions (less common now?)
                if value.startswith("${") and value.endswith("}"):
                    var_name = value[2:-1]
                    processed[key] = values.get(var_name)
                # Handle {variable} format strings (more common)
                else:
                    try:
                         # Attempt format, but handle cases where value is not a template string
                         processed[key] = value.format(**values)
                    except KeyError: # If a key in the format string isn't in values
                         processed[key] = value # Keep original string
                    except ValueError: # If format specifier is invalid
                         processed[key] = value # Keep original string
            elif isinstance(value, dict):
                processed[key] = self._process_template(value, values)
            elif isinstance(value, list):
                processed[key] = [
                    self._process_template(item, values) if isinstance(item, dict) else item 
                    for item in value
                ]
            else:
                processed[key] = value
        return processed 