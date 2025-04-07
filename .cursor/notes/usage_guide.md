# God Rotation Wizard - User Guide

## Application Overview

The God Rotation Wizard is a tool for managing which gods are active in the SMITE 2 rotation. It provides a simple interface to view all gods, select which ones should be active or inactive, and process these updates in batch.

## Getting Started

### Prerequisites

Before using the application, you will need:

1. A valid RallyHere developer auth token with permission to modify god rotations
2. The Sandbox ID for the environment you want to update (e.g., development, staging, production)

If you don't have these credentials, please contact your team lead or the development team.

### Installation

1. Ensure Python 3.6+ is installed on your system
2. Install the application dependencies:
   ```
   pip install -r Requirements.txt
   ```
3. Launch the application:
   ```
   python run_app.py
   ```

The application should automatically open in your default web browser. If not, navigate to the URL displayed in the console (typically http://localhost:8888).

## Using the Application

### Screen 1: Welcome

The first screen provides a brief introduction to the application. Click "Start Configuration" to proceed.

### Screen 2: Configuration

Enter your credentials:

1. **RallyHere Auth Token**: Paste your temporary developer auth token (this is not stored permanently)
2. **Sandbox ID**: Enter the ID for the target environment you want to modify

Click "Proceed to God Selection" to continue.

### Screen 3: God Selection

This screen displays all available gods and their current status in the rotation:

1. **Sorting Options**: Use the dropdown to sort gods by:
   - Name (A-Z)
   - Name (Z-A)
   - Currently Active First
   - Currently Inactive First

2. **Bulk Actions**:
   - Click "Check All Gods" to select all gods for active status
   - Click "Uncheck All Gods" to deselect all gods for inactive status

3. **Individual Selection**:
   - Each god has a checkbox - check it to make the god active, uncheck to make it inactive
   - Current status is shown next to each god name (✓ Active or ✗ Inactive)

4. **Navigation**:
   - Click "Back to Configuration" if you need to change your credentials
   - Click "Proceed to Update" when your selection is complete

### Screen 4: Processing Updates

This screen processes your changes and shows the results:

1. **Update Progress**:
   - A progress bar shows the status of update operations
   - Each god update is displayed as it happens
   - Success or failure messages appear for each update

2. **Summary**:
   - After processing, a summary shows successful and failed updates
   - Any errors encountered are displayed for troubleshooting

3. **Log Options**:
   - Click "View Log" to see detailed information about the API operations
   - Click "Download Log" to save a JSON file with all operation details
   - Click "Start Over" to return to the beginning of the application

## Common Tasks

### Activating All Gods

1. On Screen 3, click the "Check All Gods" button
2. Click "Proceed to Update"
3. Monitor the update progress on Screen 4

### Deactivating All Gods

1. On Screen 3, click the "Uncheck All Gods" button
2. Click "Proceed to Update"
3. Monitor the update progress on Screen 4

### Updating Specific Gods

1. On Screen 3, use the sorting options to find the gods you want to update
2. Check or uncheck each god as needed
3. Click "Proceed to Update"
4. Monitor the update progress on Screen 4

### Reviewing Update Logs

1. After updates are processed on Screen 4, click "View Log"
2. Expand any log entry to see the full request and response details
3. Click "Download Log" to save the logs for future reference

## Troubleshooting

### Connection Issues

If the application doesn't open automatically:
1. Check the console output for the URL (e.g., http://localhost:8888)
2. Open this URL manually in your browser
3. If still unsuccessful, restart the application with `python run_app.py`

### Authentication Errors

If you see authentication errors:
1. Verify your auth token is correct and not expired
2. Ensure you have the necessary permissions for the target sandbox
3. Try generating a new auth token if issues persist

### Update Failures

If god updates fail:
1. Check the error messages in the update summary
2. View the logs for detailed API response information
3. Common issues include:
   - Expired authentication token
   - Insufficient permissions
   - Network connectivity problems

### Application Startup Issues

If the application fails to start:
1. Verify Python and required packages are installed
2. Check for any existing Streamlit processes that might be using the port
3. Try specifying a different port:
   ```
   python run_app.py --port 8889
   ```

## Best Practices

1. **Reviewing Before Updating**:
   - Always verify your selection before proceeding to updates
   - Use sorting to help organize and review your selections

2. **Handling Large Updates**:
   - The application can handle updating all gods at once
   - For very large changes, consider breaking them into smaller batches

3. **Logging and Documentation**:
   - Download logs for important updates for record-keeping
   - Document the changes you've made for team reference 