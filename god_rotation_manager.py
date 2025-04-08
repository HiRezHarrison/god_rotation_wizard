#!/usr/bin/env python
import subprocess
import sys
import os
import json
import streamlit as st
import time
import datetime
import uuid
import glob # Import glob for listing files

print("Script starting...")

# Define global variables
app_config = None
api_template = None
TEMPLATES_DIR = "templates" # Define templates directory path

# Setup logging
if 'api_logs' not in st.session_state:
    st.session_state.api_logs = []

# --- Helper Functions ---

def log_api_call(operation, loot_id, request_data, response_data, success):
    """Log API calls for later retrieval"""
    timestamp = datetime.datetime.now().isoformat()
    # For batch calls, loot_id might be None or a list
    log_loot_id = loot_id if loot_id else "BATCH"
    
    log_entry = {
        "timestamp": timestamp,
        "operation": operation,
        "loot_id": log_loot_id, # Use modified ID for logging clarity
        "request_data": request_data,
        "response_data": response_data,
        "success": success
    }
    st.session_state.api_logs.append(log_entry)
    return log_entry

def install_requirements(requirements_path="Requirements.txt"):
    """Checks if requirements are installed and installs them if not."""
    print("install_requirements function called")
    try:
        # Check if pip is available
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        st.error("pip is not available. Please ensure pip is installed and accessible.")
        sys.exit(1)
    except FileNotFoundError:
        st.error(f"Python executable not found at {sys.executable}.")
        sys.exit(1)
        
    try:
        # Check if requirements are met
        print("Checking requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "check"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Requirements already satisfied.")
    except subprocess.CalledProcessError:
        # If check fails, dependencies are missing or conflicting
        st.warning(f"Dependencies missing or conflicting. Installing from {requirements_path}...")
        print(f"Installing dependencies from {requirements_path}...")
        try:
            # Attempt installation
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
            st.success(f"Dependencies installed successfully from {requirements_path}.")
            print("Dependencies installed successfully.")
            # Optionally re-run check after install
            # subprocess.check_call([sys.executable, "-m", "pip", "check"])
        except subprocess.CalledProcessError as install_err:
            st.error(f"Failed to install dependencies from {requirements_path}. Error: {install_err}")
            print(f"Failed to install dependencies. Error: {install_err}")
            # Attempt to show pip's output for more details
            try:
                result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], capture_output=True, text=True, check=False)
                st.text_area("pip install output:", result.stdout + "\n" + result.stderr, height=300)
                print(result.stdout)
                print(result.stderr)
            except Exception as e:
                 st.error(f"Could not capture pip install output: {e}")
                 print(f"Could not capture pip install output: {e}")
            sys.exit(1)
        except Exception as e:
             st.error(f"An unexpected error occurred during installation: {e}")
             print(f"An unexpected error occurred during installation: {e}")
             sys.exit(1)
    except Exception as e:
        st.error(f"An unexpected error occurred during requirement check: {e}")
        print(f"An unexpected error occurred during requirement check: {e}")
        sys.exit(1)

def load_config(config_dir: str, config_name: str) -> dict:
    """Load a configuration file from the config directory"""
    print(f"Loading config: {config_dir}/{config_name}")
    config_path = os.path.join(config_dir, config_name)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            print(f"Successfully loaded {config_name}")
            return config
    except Exception as e:
        st.error(f"Error loading {config_name}: {str(e)}")
        print(f"Error loading {config_name}: {str(e)}") # Keep print for console debugging
        return None # Return None instead of exiting for Streamlit

# Moved helper function to global scope
def get_god_name(god):
    """Get the best available name for a god from its data dictionary."""
    # Try different possible name fields in order of preference
    for field in ['item_name', 'name', 'god_name', 'title', 'display_name', 'inventory_item_name']:
        if field in god and god[field]:
            return god[field]
    return god['loot_id']  # Fallback to loot_id if no name found

# Updated helper function to calculate changes and non-changes
def calculate_update_summary(god_list, god_selection):
    """Calculates lists of gods to update and gods remaining unchanged."""
    gods_to_update = []
    gods_unchanged = []
    
    if not god_list or not god_selection:
        return gods_to_update, gods_unchanged # Return empty lists if data is missing

    original_god_data_map = {item['loot_id']: item for item in god_list}

    for loot_id, desired_active_state in god_selection.items():
        if loot_id in original_god_data_map:
            original_data = original_god_data_map[loot_id]
            current_active_state = original_data.get('active', False) # Default if missing
            god_name = get_god_name(original_data) # Get name once

            if desired_active_state != current_active_state:
                gods_to_update.append({
                    'loot_id': loot_id,
                    'name': god_name,
                    'desired_active': desired_active_state,
                    'current_active': current_active_state,
                    'full_data': original_data
                })
            else:
                # Add to unchanged list if state matches selection
                gods_unchanged.append({
                    'loot_id': loot_id,
                    'name': god_name,
                    'current_active': current_active_state
                })
        else:
            # Log this potential issue, but don't display in UI here
            print(f"Warning: Loot ID {loot_id} from selection not found in original god list.")
            
    return gods_to_update, gods_unchanged

# --- Main Application Logic ---
def main():
    global app_config, api_template
    print("main() function called")
    # --- Dependency Check ---
    # Check/install requirements only once per run ideally
    # Using st.session_state to track if check was done
    if 'requirements_checked' not in st.session_state:
        with st.spinner("Checking dependencies..."):
            install_requirements()
        st.session_state.requirements_checked = True
        st.rerun() # Rerun after install/check to load app properly
    
    # --- Load Configurations --- 
    # Assuming configs are in a 'config' directory
    config_dir = "config"
    print("Loading app_config.json...")
    app_config = load_config(config_dir, "app_config.json")
    print("Loading api_template.json...")
    api_template = load_config(config_dir, "api_template.json")
    # logging_config = load_config(config_dir, "logging_config.json") # Assuming logging config exists
    
    if not app_config or not api_template: # or not logging_config:
        print("Config loading failed, stopping execution")
        st.stop() # Stop execution if configs failed to load

    # --- Streamlit App Title & Sidebar ---
    print("Setting up Streamlit title and sidebar")
    st.title("SMITE 2 God Rotation Manager")
    
    # Add Dark Mode Toggle to Sidebar
    st.sidebar.title("Options")
    st.session_state.dark_mode = st.sidebar.toggle("Dark Mode", key="dark_mode_toggle", value=st.session_state.get("dark_mode", False))
    # Note: Applying the theme based on this toggle requires Streamlit >= 1.20 and possibly config.toml setup or more complex logic.
    # For now, this just adds the control.

    # --- Screen Navigation Logic --- 
    if 'screen' not in st.session_state:
        print("Initializing screen to 'screen1'")
        st.session_state.screen = 'screen1'

    # --- Render Current Screen ---
    print(f"Current screen: {st.session_state.screen}")
    if st.session_state.screen == 'screen1':
        render_screen1()
    elif st.session_state.screen == 'screen2':
        render_screen2()
    elif st.session_state.screen == 'screen3':
        render_screen3()
    elif st.session_state.screen == 'screen3_confirm': # Add new confirmation screen
        render_screen3_confirm()
    elif st.session_state.screen == 'screen4':
        render_screen4()
    else:
        st.error("Invalid screen state!")
        st.session_state.screen = 'screen1' # Reset to default
        if st.button("Reset to Screen 1"): # Offer manual reset
             st.rerun()

# --- Screen Rendering Functions ---
def render_screen1():
    print("Rendering screen 1")
    st.header("Screen 1: Welcome")
    st.write("This tool will help you to manage god rotations in SMITE 2.")
    
    # Navigation Button
    if st.button("Start Configuration", key="start_config"):
        st.session_state.screen = 'screen2'
        st.rerun()

def render_screen2():
    st.header("Screen 2: Configuration")
    
    # Initialize state if not present
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = ""
    if 'sandbox_id' not in st.session_state:
        # Use sandbox_id from config as default, if available
        global app_config
        default_sandbox_id = app_config.get('api', {}).get('sandbox_id', "")
        st.session_state.sandbox_id = default_sandbox_id 

    # Input Fields
    st.session_state.auth_token = st.text_input(
        "RallyHere Auth Token", 
        value=st.session_state.auth_token, 
        type="password",
        help="Paste your temporary RallyHere developer auth token here."
    )
    st.session_state.sandbox_id = st.text_input(
        "Sandbox ID", 
        value=st.session_state.sandbox_id,
        help="Enter the Sandbox ID for the environment you want to modify."
    )

    st.write("--- ") # Separator

    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Welcome", key="back_to_s1"):
            st.session_state.screen = 'screen1'
            st.rerun()
    with col2:
        proceed_button = st.button("Proceed to God Selection", key="to_s3")
        
        # Validation
        token_valid = bool(st.session_state.auth_token)
        sandbox_id_valid = bool(st.session_state.sandbox_id) # Basic check, could add UUID format check

        if proceed_button:
            if token_valid and sandbox_id_valid:
                # Store validated values if needed elsewhere, maybe copy them
                # st.session_state.valid_auth_token = st.session_state.auth_token 
                # st.session_state.valid_sandbox_id = st.session_state.sandbox_id 
                st.session_state.screen = 'screen3'
                st.rerun()
            else:
                if not token_valid:
                    st.warning("Auth Token cannot be empty.")
                if not sandbox_id_valid:
                    st.warning("Sandbox ID cannot be empty.")

def render_screen3():
    print("Rendering screen 3")
    st.header("Screen 3: God Selection")

    # --- Navigation Buttons and Actions at the Top ---
    # Navigation
    st.write("Navigation:")
    nav_cols = st.columns(2)
    with nav_cols[0]:
        if st.button("Back to Configuration", key="back_to_s2_top"):
            # Clear god list and selection when going back to re-fetch
            if 'god_list' in st.session_state: del st.session_state['god_list']
            if 'god_selection' in st.session_state: del st.session_state['god_selection']
            st.session_state.screen = 'screen2'
            st.rerun()
    with nav_cols[1]:
        if st.button("Proceed to Confirm Update", key="to_s3_confirm_top"):
            st.session_state.screen = 'screen3_confirm'
            st.rerun()
            
    st.write("---")  # Separator

    # --- Template Loading Section ---
    st.subheader("Load Selection from Template")
    # Ensure templates directory exists
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)
        
    template_files = glob.glob(os.path.join(TEMPLATES_DIR, "*.json"))
    template_names = [os.path.basename(f) for f in template_files]
    
    # Add placeholder if no templates exist
    display_options = ["-- Select a Template --"] + template_names
    
    load_cols = st.columns([2, 1, 1]) # Adjust column ratios for 3 buttons
    with load_cols[0]:
        selected_template = st.selectbox(
            "Select Template", 
            options=display_options, 
            index=0, 
            key="template_select",
            label_visibility="collapsed"
        )
    with load_cols[1]:
        # Disable Load button if no template selected
        disable_load = selected_template == "-- Select a Template --"
        if st.button("Load Template", key="load_template", disabled=disable_load):
            if selected_template and selected_template != "-- Select a Template --": # Redundant check, but safe
                filepath = os.path.join(TEMPLATES_DIR, selected_template)
                try:
                    with open(filepath, 'r') as f:
                        loaded_selection = json.load(f)
                    
                    # Validate format (basic check)
                    if isinstance(loaded_selection, dict) and all(isinstance(v, bool) for v in loaded_selection.values()):
                        # Update session state, overriding existing selection
                        # Only update if god_list is already loaded
                        if 'god_list' in st.session_state and st.session_state.god_list:
                            current_god_ids = {god['loot_id'] for god in st.session_state.god_list}
                            # Create new selection dict based on template and current gods
                            new_selection = {}
                            loaded_count = 0
                            missing_count = 0
                            for god_id, active_state in loaded_selection.items():
                                if god_id in current_god_ids:
                                     new_selection[god_id] = active_state
                                     loaded_count += 1
                                else:
                                     missing_count += 1
                                     print(f"Warning: Loot ID {god_id} from template '{selected_template}' not found in current god list.")
                            
                            # Keep existing selections for gods not in the template?
                            # Current approach: replace entirely with template + known gods
                            st.session_state.god_selection = new_selection
                            st.success(f"Loaded '{selected_template}'. Applied state to {loaded_count} known gods.")
                            if missing_count > 0:
                                st.warning(f"{missing_count} IDs from template were not found in the current god list.")
                            st.rerun() # Rerun to update checkboxes
                        else:
                            st.warning("Cannot load template until God List is fetched.")
                    else:
                        st.error("Invalid template file format. Expected JSON dictionary with boolean values.")
                        
                except Exception as e:
                    st.error(f"Error loading template: {e}")
                    print(f"Error loading template '{selected_template}': {e}")
            # No need for else, button is disabled
            
    # Add Delete Button
    with load_cols[2]:
        # Disable Delete button if no template selected
        disable_delete = selected_template == "-- Select a Template --"
        if st.button("Delete Template", key="delete_template", disabled=disable_delete, type="secondary"):
            if selected_template and selected_template != "-- Select a Template --": # Redundant check
                filepath = os.path.join(TEMPLATES_DIR, selected_template)
                try:
                    os.remove(filepath)
                    st.success(f"Successfully deleted template '{selected_template}'.")
                    # Clear selection in dropdown after delete? Optional, rerun handles refresh.
                    # st.session_state.template_select = display_options[0] # Reset selectbox
                    st.rerun()
                except FileNotFoundError:
                     st.error(f"Error: Template file '{selected_template}' not found.")
                except Exception as e:
                     st.error(f"Error deleting template '{selected_template}': {e}")
                     print(f"Error deleting template '{selected_template}': {e}")
            # No need for else, button is disabled
                
    st.write("---")  # Separator

    # --- Save Template Section (Moved Up) ---
    st.subheader("Save Current Selection")
    save_cols = st.columns([3, 1]) # Wider input, smaller button
    with save_cols[0]:
        template_filename = st.text_input(
            "Template Filename (.json)", 
            key="template_filename",
            placeholder="e.g., default_rotation.json",
            label_visibility="collapsed" # Hide label as subheader is present
        )
    with save_cols[1]:
        if st.button("Save as Template", key="save_template"):
            if template_filename:
                filename = template_filename.strip()
                if not filename.endswith(".json"): filename += ".json"
                safe_filename = "".join(c for c in filename if c.isalnum() or c in ('_', '.', '-')).rstrip()
                if not safe_filename:
                    st.error("Invalid template filename.")
                else:
                    filepath = os.path.join(TEMPLATES_DIR, safe_filename)
                    try:
                        # Ensure directory exists (redundant check, but safe)
                        os.makedirs(TEMPLATES_DIR, exist_ok=True) 
                        with open(filepath, 'w') as f:
                            json.dump(st.session_state.god_selection, f, indent=4)
                        st.success(f"Saved as '{safe_filename}'")
                        # Refresh template list in selectbox after saving
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Error saving: {e}")
                        print(f"Error saving template '{safe_filename}': {e}")
            else:
                st.warning("Enter a filename.")

    st.write("---")  # Separator

    # --- API Call to Fetch Gods ---
    if 'god_list' not in st.session_state:
        st.session_state.god_list = None # Initialize
        st.session_state.god_selection_error = None

        # Ensure we have credentials
        auth_token = st.session_state.get('auth_token')
        sandbox_id = st.session_state.get('sandbox_id')
        god_vendor_id = "00000000-0000-0000-0000-00000000004e" # Hardcoded for now
        
        if not auth_token or not sandbox_id:
            st.error("Auth Token or Sandbox ID missing. Please go back to Screen 2.")
            st.stop()
            
        # Instantiate API client
        from src.rallyhere_api import RallyHereAPIClient 
        global app_config, api_template
        client = RallyHereAPIClient(auth_token, app_config['api'], api_template)

        with st.spinner(f"Fetching God list from vendor {god_vendor_id}..."):
            response = client.get_vendor_loot(vendor_id=god_vendor_id, sandbox_id=sandbox_id)
        
        if response.success and response.data and 'loot' in response.data:
            # Store the FULL loot dictionaries, filtering out any without loot_id
            god_list = [loot for loot in response.data['loot'] if loot.get('loot_id')]
            
            # Debug: Print the first god entry structure (can be removed later)
            if god_list:
                print("\n--- First God Entry Structure ---")
                print(json.dumps(god_list[0], indent=2))
                print("----------------------------\n")
                with st.expander("Debug: God Data Structure (First Entry)"):
                    st.json(god_list[0])
                    st.write("Available Fields:", list(god_list[0].keys()))

            st.session_state.god_list = god_list
            
            # Initialize selection state based on current active status IF NOT ALREADY SET (e.g. by loading template)
            if 'god_selection' not in st.session_state:
                st.session_state.god_selection = {god['loot_id']: god.get('active', False) for god in god_list}
            else:
                # Ensure selection state only contains current gods after initial fetch
                current_god_ids = {god['loot_id'] for god in god_list}
                st.session_state.god_selection = {k: v for k, v in st.session_state.god_selection.items() if k in current_god_ids}
            
            st.success(f"Successfully loaded {len(god_list)} gods.")
        else:
            error_msg = response.error if response.error else "Unknown error fetching god list."
            st.error(f"Failed to fetch gods: {error_msg}")
            st.session_state.god_selection_error = error_msg
            st.stop()

    # --- Display Gods For Selection ---
    if st.session_state.god_list:
        # Check if god_selection exists, initialize if it was cleared or never set
        if 'god_selection' not in st.session_state:
             st.session_state.god_selection = {god['loot_id']: god.get('active', False) for god in st.session_state.god_list}
             
        st.write("Select which gods should be active in the rotation:")
        
        # Add sorting options
        sort_options = ["Name (A-Z)", "Name (Z-A)", "Currently Active First", "Currently Inactive First"]
        sort_method = st.selectbox("Sort gods by:", sort_options, index=0)
            
        # Sort the list based on selection
        gods = st.session_state.god_list.copy()
        if sort_method == "Name (A-Z)":
            gods.sort(key=lambda x: get_god_name(x))
        elif sort_method == "Name (Z-A)":
            gods.sort(key=lambda x: get_god_name(x), reverse=True)
        elif sort_method == "Currently Active First":
            gods.sort(key=lambda x: (not x.get('active', False), get_god_name(x)))
        elif sort_method == "Currently Inactive First":
            gods.sort(key=lambda x: (x.get('active', False), get_god_name(x)))
        
        # Add Check/Uncheck All buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Check All Gods"):
                for god in gods:
                    # Only update selection for gods currently in the list
                    if god['loot_id'] in st.session_state.god_selection:
                         st.session_state.god_selection[god['loot_id']] = True
                st.rerun()
        with col2:
            if st.button("Uncheck All Gods"):
                for god in gods:
                     # Only update selection for gods currently in the list
                     if god['loot_id'] in st.session_state.god_selection:
                          st.session_state.god_selection[god['loot_id']] = False
                st.rerun()
        
        st.write("---")  # Separator
        
        # Create checkboxes for each god (No form needed anymore)
        # Make sure to use the current selection state
        current_selection = st.session_state.god_selection
        for god in gods:
            loot_id = god.get('loot_id')
            if loot_id not in current_selection:
                 # God exists in list but somehow not in selection? Initialize it.
                 current_selection[loot_id] = god.get('active', False)
                 
            item_name = get_god_name(god) # Use helper
            
            # Format the label to show if it's currently active
            current_status = "✓ Active" if god.get('active', False) else "✗ Inactive"
            checkbox_label = f"{item_name} ({current_status})"
            
            # Update the dictionary directly on checkbox interaction
            current_selection[loot_id] = st.checkbox(
                checkbox_label, 
                value=current_selection.get(loot_id, False), # Use current selection value
                key=f"god_{loot_id}" # Keep key for state persistence
            )
            
    elif st.session_state.god_selection_error:
         # Error already displayed during fetch, maybe add button to retry?
         if st.button("Retry Fetching Gods"):
             if 'god_list' in st.session_state: del st.session_state['god_list']
             if 'god_selection' in st.session_state: del st.session_state['god_selection']
             if 'god_selection_error' in st.session_state: del st.session_state['god_selection_error']
             st.rerun()
    else:
        # Should not happen if fetch logic is correct, but as a fallback:
        st.warning("God list is not available. Try going back and forth.")


# --- New Confirmation Screen ---
def render_screen3_confirm():
    st.header("Screen 3b: Confirm Updates")

    # Ensure required data exists
    if 'god_list' not in st.session_state or 'god_selection' not in st.session_state:
        st.error("God list or selection data missing. Please return to Screen 3.")
        if st.button("Back to God Selection"): 
            st.session_state.screen = 'screen3'
            st.rerun()
        st.stop()

    # Calculate changes and non-changes using the updated helper function
    gods_to_update, gods_unchanged = calculate_update_summary(
        st.session_state.god_list, 
        st.session_state.god_selection
    )
    total_changes = len(gods_to_update)
    total_unchanged = len(gods_unchanged)
    
    # Removed Preview Mode Toggle
    # preview_mode = st.checkbox("Preview Batch API Payload (Read-Only)", key="preview_mode", value=False)
    # st.write("---") 

    if total_changes == 0:
        st.info("No changes detected in God active status. Nothing to update.")
        st.write(f"All {total_unchanged} gods will remain in their current state.")
        if st.button("Back to Selection", key="back_to_s3_no_changes"):
            st.session_state.screen = 'screen3'
            st.rerun()
    # Removed preview_mode condition
    # elif preview_mode:
    #    ... preview logic removed ...
    else: # Normal confirmation view (changes exist)
        st.warning(f"You are about to submit {total_changes} change(s).")
        
        activating_gods = [g for g in gods_to_update if g['desired_active']]
        deactivating_gods = [g for g in gods_to_update if not g['desired_active']]
        remaining_active = [g for g in gods_unchanged if g['current_active']]
        remaining_inactive = [g for g in gods_unchanged if not g['current_active']]

        # Display Summary
        summary_cols = st.columns(2)
        with summary_cols[0]:
            st.metric("Activating", len(activating_gods))
            st.metric("Deactivating", len(deactivating_gods))
        with summary_cols[1]:
            st.metric("Remaining Active", len(remaining_active))
            st.metric("Remaining Inactive", len(remaining_inactive))
        
        with st.expander("View Details of Changes and Unchanged Gods"):
            if activating_gods:
                st.subheader(f"Gods to Activate ({len(activating_gods)}):")
                st.write(", ".join([f"{g['name']}" for g in activating_gods]))
            if deactivating_gods:
                st.subheader(f"Gods to Deactivate ({len(deactivating_gods)}):")
                st.write(", ".join([f"{g['name']}" for g in deactivating_gods]))
            if remaining_active:
                 st.subheader(f"Gods Remaining Active ({len(remaining_active)}):")
                 st.write(", ".join([f"{g['name']}" for g in remaining_active]))
            if remaining_inactive:
                 st.subheader(f"Gods Remaining Inactive ({len(remaining_inactive)}):")
                 st.write(", ".join([f"{g['name']}" for g in remaining_inactive]))

        st.write("---")

        # Navigation Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Selection", key="back_to_s3_confirm"):
                st.session_state.screen = 'screen3'
                st.rerun()
        with col2:
            if st.button("Confirm & Process Updates", key="confirm_updates_button"):
                # Clear flags before going to processing screen
                if 'update_process_complete' in st.session_state: del st.session_state['update_process_complete']
                if 'update_process_started' in st.session_state: del st.session_state['update_process_started']
                # Clear batch response state if it exists
                if 'batch_update_response' in st.session_state: del st.session_state['batch_update_response']
                st.session_state.screen = 'screen4'
                st.rerun()

def render_screen4():
    st.header("Screen 4: Processing Updates")

    # Ensure required data exists in session state
    if 'god_list' not in st.session_state or 'god_selection' not in st.session_state:
        st.error("God list or selection data missing. Please go back to Screen 3.")
        if st.button("Back to God Selection"): 
            st.session_state.screen = 'screen3'
            st.rerun()
        st.stop()
        
    auth_token = st.session_state.get('auth_token')
    sandbox_id = st.session_state.get('sandbox_id')
    
    if not auth_token or not sandbox_id:
        st.error("Auth Token or Sandbox ID missing. Please go back to Screen 2.")
        if st.button("Back to Configuration"): 
            st.session_state.screen = 'screen2'
            st.rerun()
        st.stop()

    # --- Run Update Process Only Once --- 
    if 'update_process_complete' not in st.session_state:
        # Calculate updates using helper function
        gods_to_update, _ = calculate_update_summary(st.session_state.god_list, st.session_state.god_selection)
        total_updates = len(gods_to_update)
        
        # Clear existing logs only when starting the *actual* update process
        if 'update_process_started' not in st.session_state:
            st.session_state.api_logs = [] # Clear logs specific to this run
            st.session_state.update_process_started = True # Mark that processing screen has started
            # Initialize result counters for individual updates
            st.session_state.update_success_count = 0
            st.session_state.update_error_list = []

        if total_updates == 0:
            st.info("No changes were requested.")
            st.session_state.update_process_complete = True # Mark as complete even if no updates
            st.rerun() # Rerun to show final summary/nav immediately
                
        else:
            st.write(f"Processing {total_updates} God status update(s)...")
            # Initialize API client
            from src.rallyhere_api import RallyHereAPIClient 
            global app_config, api_template
            client = RallyHereAPIClient(auth_token, app_config['api'], api_template)
            
            # Restore Progress Bar and loop for individual updates
            progress_bar = st.progress(0)
            status_area = st.container() 
            processed_count = 0 # Local counter for progress bar
            
            # Retrieve counts from session state
            success_count = st.session_state.update_success_count
            error_list = st.session_state.update_error_list
            
            # Run the update loop (restored from before batch attempt)
            for god_info in gods_to_update:
                # Check if already processed in a previous partial run (if needed, basic implementation just runs all)
                # More robust: check if loot_id is already in logs for this run?
                
                loot_id = god_info['loot_id']
                name = god_info['name']
                desired_active = god_info['desired_active']
                full_data = god_info['full_data']
                
                status_area.write(f"Updating {name} (Loot ID: {loot_id}) to {'Active' if desired_active else 'Inactive'}...")
                
                # --- Call API to update status (Single Update) ---
                response = client.update_loot_status(loot_id, sandbox_id, desired_active, full_data)
                
                # Log the API request
                log_api_call(
                    operation="UPDATE_LOOT_STATUS",
                    loot_id=loot_id,
                    request_data={"loot_id": loot_id, "active": desired_active}, 
                    response_data={"success": response.success, "data": response.data, "error": response.error},
                    success=response.success
                )
                
                if response.success:
                    success_count += 1
                else:
                    error_msg = f"Failed to update {name} ({loot_id}): {response.error}"
                    error_list.append(error_msg)
                    status_area.error(error_msg) # Display error prominently
                
                processed_count += 1
                progress_bar.progress(processed_count / total_updates)
                
                # Decide whether to keep the sleep or not
                # time.sleep(0.1) 
                
            # Store final counts and mark complete
            st.session_state.update_success_count = success_count
            st.session_state.update_error_list = error_list
            st.session_state.update_process_complete = True
            st.rerun() # Rerun immediately to show summary and stop the loop

    # --- Display Final Summary and Logs (After Update Process is Complete) --- 
    else: 
        # Retrieve results from session state
        # response = st.session_state.get('batch_update_response') # No longer batch response
        total_updates_processed = len(st.session_state.api_logs)
        success_count = st.session_state.get('update_success_count', 0)
        error_list = st.session_state.get('update_error_list', [])
        
        st.header("Update Summary")
        # if response is None: # Condition no longer needed
        #      st.warning("Update process did not run or state was lost.") 
        if total_updates_processed == 0:
             st.info("No updates were attempted.") # Or "No changes were requested" if initial total_updates was 0
        elif not error_list:
            st.success(f"All {success_count} God status updates completed successfully!")
        else:
            st.warning(f"Completed updates for {success_count} out of {total_updates_processed} Gods.")
            if error_list:
                st.subheader("Errors Encountered:")
                for error in error_list:
                    st.error(error)
            # Removed batch-specific error display
            # if response.data:
            #     st.subheader("Error Details from API:")
            #     st.json(response.data)
        
        st.write("--- ")

        # Navigation/Log Buttons (Always show after completion)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("View/Hide Log", key="view_log"):
                st.session_state.show_logs = not st.session_state.get('show_logs', False) # Toggle view
                st.rerun() # Rerun to show/hide logs
        
        with col2:
            # Use st.download_button directly
            log_data = json.dumps(st.session_state.api_logs, indent=2)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            st.download_button(
                 label="Download Log",
                 data=log_data,
                 file_name=f"god_rotation_log_{timestamp}.json",
                 mime="application/json",
                 key="download_log_button"
            )
        
        with col3:
            if st.button("Start Over", key="restart_app_s4"):
                # Clear relevant session state
                keys_to_clear = ['god_list', 'god_selection', 'update_process_started', 'update_process_complete', 'show_logs', 'batch_update_response', 'update_success_count', 'update_error_list'] # Added counters
                for key in keys_to_clear:
                    if key in st.session_state: del st.session_state[key]
                st.session_state.screen = 'screen1'
                st.rerun()
        
        # Display logs if view log was clicked
        if st.session_state.get('show_logs', False):
            st.header("API Logs")
            if st.session_state.api_logs:
                # Improve log display slightly
                log_display_area = st.container()
                with log_display_area:
                     for i, log in enumerate(reversed(st.session_state.api_logs)): # Show newest first
                        status_icon = "✅" if log['success'] else "❌"
                        # Adapt log entry display for batch (Reverted)
                        log_title = f"{status_icon} Log Entry #{len(st.session_state.api_logs)-i}: {log['operation']} - {log['loot_id']}"
                        # if log['operation'] == "BATCH_UPDATE_LOOT_STATUS":
                        #     count = log['request_data'].get('count', '?')
                        #     log_title = f"{status_icon} Log Entry #{len(st.session_state.api_logs)-i}: {log['operation']} ({count} items)"
                        
                        with st.expander(log_title):
                            st.json(log) # Display full log entry as JSON
            else:
                st.info("No API logs available for this run.")

# For script entry point
if __name__ == "__main__":
    print("Starting app via __main__")
    try:
        main()
        print("Application started successfully")
    except Exception as e:
        print(f"ERROR IN APP STARTUP: {e}")
        import traceback
        print(traceback.format_exc()) 