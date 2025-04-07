#!/usr/bin/env python
import subprocess
import sys
import os
import json
import streamlit as st
import time
import datetime
import uuid

print("Script starting...")

# Define global variables
app_config = None
api_template = None

# Setup logging
if 'api_logs' not in st.session_state:
    st.session_state.api_logs = []

def log_api_call(operation, loot_id, request_data, response_data, success):
    """Log API calls for later retrieval"""
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

    # --- Streamlit App Title ---
    print("Setting up Streamlit title")
    st.title("SMITE 2 God Rotation Manager")

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
    elif st.session_state.screen == 'screen4':
        render_screen4()
    else:
        st.error("Invalid screen state!")
        st.session_state.screen = 'screen1' # Reset to default
        st.button("Reset to Screen 1") # Offer manual reset

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

    # --- Navigation Buttons at the Top ---
    st.write("Navigation:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Configuration", key="back_to_s2_top"):
            st.session_state.screen = 'screen2'
            st.rerun()
    with col2:
        if st.button("Proceed to Update", key="to_s4_top"):
            st.session_state.screen = 'screen4'
            st.rerun()
    
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
            
        # Instantiate API client (consider doing this once and storing in session_state?)
        # Need to import ChestAPIClient and load configs if not global
        from src.rallyhere_api import RallyHereAPIClient # UPDATED IMPORT
        global app_config, api_template
        client = RallyHereAPIClient(auth_token, app_config['api'], api_template) # UPDATED CLASS NAME

        with st.spinner(f"Fetching God list from vendor {god_vendor_id}..."):
            response = client.get_vendor_loot(vendor_id=god_vendor_id, sandbox_id=sandbox_id)
        
        if response.success and response.data and 'loot' in response.data:
            # Store the FULL loot dictionaries, filtering out any without loot_id
            god_list = [loot for loot in response.data['loot'] if loot.get('loot_id')]
            
            # Debug: Print the first god entry to see its structure
            if god_list:
                import json
                print("\n--- First God Entry Structure ---")
                print(json.dumps(god_list[0], indent=2))
                print("--- Available Fields ---")
                print(list(god_list[0].keys()))
                print("----------------------------\n")
                
                # Also display this information on the UI for debugging
                with st.expander("Debug: God Data Structure"):
                    st.write("First God Entry:")
                    st.json(god_list[0])
                    st.write("Available Fields:")
                    st.write(list(god_list[0].keys()))
                    
                    # Try to identify name fields
                    name_fields = []
                    first_god = god_list[0]
                    for key, value in first_god.items():
                        if isinstance(value, str) and key.lower().endswith('name'):
                            name_fields.append(key)
                            st.write(f"Potential name field: '{key}' = '{value}'")
            
            # Sort the list by item_name for better usability
            god_list.sort(key=lambda x: x.get('item_name', '') or x.get('loot_id', ''))
            
            st.session_state.god_list = god_list
            
            # Initialize selection state based on current active status
            st.session_state.god_selection = {god['loot_id']: god.get('active', False) for god in god_list}
            
            st.success(f"Successfully loaded {len(god_list)} gods.")
        else:
            error_msg = response.error if response.error else "Unknown error fetching god list."
            st.error(f"Failed to fetch gods: {error_msg}")
            st.session_state.god_selection_error = error_msg
            st.stop()

    # --- Display Gods For Selection ---
    if st.session_state.god_list:
        st.write("Select which gods should be active in the rotation:")
        
        # Add sorting options
        sort_options = ["Name (A-Z)", "Name (Z-A)", "Currently Active First", "Currently Inactive First"]
        sort_method = st.selectbox("Sort gods by:", sort_options, index=0)
        
        # Function to get best available name
        def get_god_name(god):
            # Try different possible name fields in order of preference
            for field in ['item_name', 'name', 'god_name', 'title', 'display_name', 'inventory_item_name']:
                if field in god and god[field]:
                    return god[field]
            return god['loot_id']  # Fallback to loot_id if no name found
            
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
                    st.session_state.god_selection[god['loot_id']] = True
                st.rerun()
        with col2:
            if st.button("Uncheck All Gods"):
                for god in gods:
                    st.session_state.god_selection[god['loot_id']] = False
                st.rerun()
        
        st.write("---")  # Separator
        
        # Create checkboxes for each god
        with st.form(key="god_selection_form"):
            for god in gods:
                loot_id = god.get('loot_id')
                # Use the function to get the best name
                item_name = get_god_name(god)
                
                # Format the label to show if it's currently active
                current_status = "✓ Active" if god.get('active', False) else "✗ Inactive"
                checkbox_label = f"{item_name} ({current_status})"
                
                st.session_state.god_selection[loot_id] = st.checkbox(
                    checkbox_label, 
                    value=st.session_state.god_selection.get(loot_id, False),
                    key=f"god_{loot_id}"
                )
            
            # Submit button for the form
            submit_button = st.form_submit_button("Update God Rotation")
    else:
        st.warning("No gods available for selection. Please try again.")

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

    # Find gods that need updating
    gods_to_update = []
    # Now original_god_data_map holds the full dictionaries
    original_god_data_map = {item['loot_id']: item for item in st.session_state.god_list} 
    
    # Clear existing logs when starting a new update
    if 'update_started' not in st.session_state:
        st.session_state.api_logs = []
        st.session_state.update_started = True
    
    # Display debug info about the selection count
    st.write(f"Total gods in selection: {len(st.session_state.god_selection)}")
    st.write(f"Total gods in original list: {len(original_god_data_map)}")
    
    # Count of selections by desired state
    active_selections = sum(1 for v in st.session_state.god_selection.values() if v)
    inactive_selections = len(st.session_state.god_selection) - active_selections
    st.write(f"Selections: {active_selections} active, {inactive_selections} inactive")
    
    for loot_id, desired_active_state in st.session_state.god_selection.items():
        if loot_id in original_god_data_map:
            original_data = original_god_data_map[loot_id]
            current_active_state = original_data.get('active', False) # Default if missing
            
            if desired_active_state != current_active_state:
                gods_to_update.append({
                    'loot_id': loot_id,
                    'name': original_data.get('name', original_data.get('item_name', loot_id)),
                    'desired_active': desired_active_state,
                    'full_data': original_data # Pass the full original data
                })
        else:
            st.warning(f"Loot ID {loot_id} from selection not found in original god list. Skipping.")

    total_updates = len(gods_to_update)
    st.write(f"Found {total_updates} God(s) requiring status updates.")

    if total_updates == 0:
        st.info("No changes detected in God active status.")
    else:
        # Initialize API client
        from src.rallyhere_api import RallyHereAPIClient 
        global app_config, api_template
        client = RallyHereAPIClient(auth_token, app_config['api'], api_template)
        
        # Progress Bar
        progress_bar = st.progress(0)
        processed_count = 0
        success_count = 0
        error_list = []

        st.write("Starting updates...")
        status_area = st.container() # Use a container to update status text in place

        for god_info in gods_to_update:
            loot_id = god_info['loot_id']
            name = god_info['name']
            desired_active = god_info['desired_active']
            full_data = god_info['full_data'] # Now contains the actual full data
            
            status_area.write(f"Updating {name} (Loot ID: {loot_id}) to {'Active' if desired_active else 'Inactive'}...")
            
            # --- Call API to update status ---
            # No longer need the placeholder check for full_data
            response = client.update_loot_status(loot_id, sandbox_id, desired_active, full_data)
            
            # Log the API request
            log_api_call(
                operation="UPDATE_LOOT_STATUS",
                loot_id=loot_id,
                request_data={"loot_id": loot_id, "active": desired_active, "full_data": full_data},
                response_data={"success": response.success, "data": response.data, "error": response.error},
                success=response.success
            )
            
            if response.success:
                success_count += 1
                status_area.write(f"Successfully updated {name}.") 
            else:
                error_msg = f"Failed to update {name} ({loot_id}): {response.error}"
                error_list.append(error_msg)
                status_area.error(error_msg)
            
            processed_count += 1
            progress_bar.progress(processed_count / total_updates)
            
            # Small delay to ensure UI updates
            time.sleep(0.1)

        # Final Summary
        st.write("--- ")
        st.header("Update Summary")
        if success_count == total_updates:
            st.success(f"All {total_updates} God status updates completed successfully!")
        else:
            st.warning(f"Completed updates for {success_count} out of {total_updates} Gods.")
            if error_list:
                st.subheader("Errors Encountered:")
                for error in error_list:
                    st.error(error)

    # Navigation/Log Buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("View Log", key="view_log"):
            st.session_state.show_logs = True
    
    with col2:
        if st.button("Download Log", key="download_log"):
            log_data = json.dumps(st.session_state.api_logs, indent=2)
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            st.download_button(
                label="Download JSON Log",
                data=log_data,
                file_name=f"god_rotation_log_{timestamp}.json",
                mime="application/json"
            )
    
    with col3:
        # Changed Exit to Restart to fit Streamlit model better
        if st.button("Start Over", key="restart_app"):
            # Clear session state before going back
            for key in ['god_list', 'god_selection', 'update_started']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.screen = 'screen1'
            st.rerun()
    
    # Display logs if view log was clicked
    if st.session_state.get('show_logs', False):
        st.header("API Logs")
        if st.session_state.api_logs:
            for i, log in enumerate(st.session_state.api_logs):
                with st.expander(f"Log Entry {i+1}: {log['operation']} - {log['loot_id']} - {'Success' if log['success'] else 'Failed'}"):
                    st.write("**Timestamp:** ", log['timestamp'])
                    st.write("**Operation:** ", log['operation'])
                    st.write("**Loot ID:** ", log['loot_id'])
                    st.write("**Request Data:** ")
                    st.json(log['request_data'])
                    st.write("**Response Data:** ")
                    st.json(log['response_data'])
        else:
            st.info("No API logs available.")

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