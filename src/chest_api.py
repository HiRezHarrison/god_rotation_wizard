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

class ChestAPIClient:
    def __init__(self, auth_token: str, api_config: dict, api_template: dict):
        self.base_url = api_config['base_url']
        self.sandbox_id = api_config['sandbox_id']
        self.endpoints = api_config['endpoints']
        self.api_template = api_template
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        # Update sandbox_id in all static templates
        self._update_sandbox_id_in_templates()

    def _update_sandbox_id_in_templates(self):
        """Update sandbox_id in all static templates"""
        for template in self.api_template['static'].values():
            if isinstance(template, dict) and 'sandbox_id' in template:
                template['sandbox_id'] = self.sandbox_id

    def _get_current_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> APIResponse:
        """Make an API request and handle common error cases"""
        try:
            endpoint = endpoint.lstrip('/')
            url = f"{self.base_url}/{endpoint}"
            
            print(f"\nAPI Request:")
            print(f"URL: {url}")
            print(f"Method: {method}")
            print(f"Headers: {{'Content-Type': {self.headers['Content-Type']}}}")
            if data:
                print(f"Data: {json.dumps(data, indent=2)}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data if data else None
            )
            
            print(f"\nAPI Response:")
            print(f"Status: {response.status_code}")
            print(f"Body: {response.text}")
            
            response.raise_for_status()
            return APIResponse(success=True, data=response.json())
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f"\nResponse: {e.response.text}"
            return APIResponse(success=False, error=error_msg)

    def create_item(self, name: str, description: str = "", account_id: str = None) -> APIResponse:
        """Create a new item (chest or bonus chest)"""
        # Get the template from api_template.json
        template = self.api_template['templates']['items']['normal_chest']
        
        # Values for template variable substitution
        values = {
            "timestamp": self._get_current_timestamp(),
            "sandbox_id": self.sandbox_id,
            "name": name,
            "account_id": account_id
        }
        
        # Merge static template with specific template and format name using template
        data = {
            "data": [{
                **self.api_template['static']['item'],  # Get static fields from template
                **template,  # Merge with specific template
                "name": template['name_template'].format(name=name),  # Use template's name format
                "description": description
            }]
        }
        
        # Process all template variables (${variable} and {variable})
        data['data'][0] = self._process_template(data['data'][0], values)
        
        endpoint = self.endpoints['items'].format(sandbox_id=self.sandbox_id)
        response = self._make_request("POST", endpoint, data)
        
        if response.success and response.data:
            # Convert the first item in the response list to our response data
            response.data = response.data[0]
        
        return response

    def create_vendor(self, name: str, vendor_type: str, account_id: str = None) -> APIResponse:
        """Create a vendor (choice, content, or chance)"""
        # Get the template from api_template.json
        template = self.api_template['templates']['vendors'][vendor_type.lower()]
        
        # Values for template variable substitution
        values = {
            "timestamp": self._get_current_timestamp(),
            "sandbox_id": self.sandbox_id,
            "name": name,
            "account_id": account_id
        }
        
        # Merge static template with specific template and format name using template
        data = {
            "data": [{
                **self.api_template['static']['vendor'],  # Get static fields from template
                **template,  # Merge with specific template
                "name": template['name_template'].format(name=name)  # Use template's name format
            }]
        }
        
        # Process all template variables (${variable} and {variable})
        data['data'][0] = self._process_template(data['data'][0], values)
        
        endpoint = self.endpoints['vendors'].format(sandbox_id=self.sandbox_id)
        response = self._make_request("POST", endpoint, data)
        
        if response.success and response.data:
            # Convert the first item in the response list to our response data
            response.data = response.data[0]
        
        return response

    def create_loot(self, name: str, source_id: str, target_id: str,
                   connection_type: str, values: dict, account_id: str = None) -> APIResponse:
        """Create a loot connection between items/vendors"""
        # Get the template from api_template.json
        template = self.api_template['templates']['loots'][connection_type.lower()]
        
        # Add required values for template variable substitution
        values.update({
            "timestamp": self._get_current_timestamp(),
            "sandbox_id": self.sandbox_id,
            "name": name,
            "account_id": account_id
        })
        
        # Merge static template with specific template and format name using template
        loot_data = {
            **self.api_template['static']['loot'],  # Get static fields from template
            **template,  # Merge with specific template
            "name": template['name_template'].format(name=name)  # Use template's name format
        }
        
        # Process all template variables (${variable} and {variable})
        loot_data = self._process_template(loot_data, values)
        
        data = {
            "data": [loot_data]
        }
        
        endpoint = self.endpoints['loots'].format(sandbox_id=self.sandbox_id)
        response = self._make_request("POST", endpoint, data)
        
        if response.success and response.data:
            # Convert the first item in the response list to our response data
            response.data = response.data[0]
        
        return response

    def create_content_loot(self, vendor_id: str, item_id: str, item_name: str,
                           quantity: int = 1, account_id: str = None) -> APIResponse:
        """Create a content loot for a specific item"""
        # Get the template from api_template.json
        template = self.api_template['templates']['loots']['content']
        
        # Values for template variable substitution
        values = {
            "timestamp": self._get_current_timestamp(),
            "sandbox_id": self.sandbox_id,
            "item_name": item_name,
            "account_id": account_id,
            "content_vendor_id": vendor_id,
            "item_id": item_id
        }
        
        # Merge static template with specific template and format name using template
        loot_data = {
            **self.api_template['static']['loot'],  # Get static fields from template
            **template,  # Merge with specific template
            "name": template['name_template'].format(item_name=item_name),  # Use template's name format
            "quantity": quantity
        }
        
        # Process all template variables (${variable} and {variable})
        loot_data = self._process_template(loot_data, values)
        
        data = {
            "data": [loot_data]
        }
        
        endpoint = self.endpoints['loots'].format(sandbox_id=self.sandbox_id)
        response = self._make_request("POST", endpoint, data)
        
        if response.success and response.data:
            # Convert the first item in the response list to our response data
            response.data = response.data[0]
        
        return response

    def get_user_account(self) -> APIResponse:
        """Get user account information"""
        return self._make_request(
            method="GET",
            endpoint="v2/account/me",
            data=None
        )

    def _process_template(self, template: dict, values: dict) -> dict:
        """Process a template, replacing variables with actual values"""
        processed = {}
        for key, value in template.items():
            if isinstance(value, str):
                # Handle ${variable} substitutions
                if value.startswith("${") and value.endswith("}"):
                    var_name = value[2:-1]
                    processed[key] = values.get(var_name)
                # Handle {variable} format strings
                else:
                    processed[key] = value.format(**values)
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
