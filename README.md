# SMITE 2 God Rotation Manager

A Streamlit-based tool for managing the active rotation of gods in SMITE 2 using the RallyHere API.

## Overview

The God Rotation Manager allows authorized users to:
- View the complete list of gods available in SMITE 2
- View their current active/inactive status in the rotation
- Easily select which gods should be active/inactive
- Process updates in batch with detailed logging and status tracking

## Prerequisites

- Python 3.6+ (Recommended: Python 3.9+)
- Internet connection to access the RallyHere API
- RallyHere developer auth token with appropriate permissions
- Sandbox ID for the target environment

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd god-rotation-wizard
   ```

2. Install the required dependencies:
   ```
   pip install -r Requirements.txt
   ```

3. Run the application:
   ```
   python run_app.py
   ```

The application will automatically open in your default web browser. If it doesn't, navigate to the URL displayed in the console (typically http://localhost:8888).

## Features

### Authentication and Configuration
- Secure input for RallyHere auth token
- Sandbox ID configuration for targeting specific environments
- Configuration file support for API endpoints and application settings

### God Selection Interface
- Complete list of gods with current active/inactive status
- Sorting options (alphabetical, by current status)
- Bulk operations (Check All, Uncheck All)
- Visual indicators for current status

### Update Processing
- Batch processing of god rotation updates
- Real-time progress tracking
- Detailed success/error reporting
- Comprehensive logging of API calls

### Logging and Debugging
- View detailed logs of all API operations
- Download logs in JSON format for troubleshooting
- Debug information for configuration and data structures

## Application Structure

- **god_rotation_manager.py**: Main application file containing UI and business logic
- **src/rallyhere_api.py**: API client for interacting with RallyHere services
- **run_app.py**: Helper script for launching the application with proper configuration
- **config/**: Directory containing configuration files
  - **app_config.json**: Application settings including API endpoints
  - **api_template.json**: Templates for API requests

## Usage Guide

### Screen 1: Welcome
The landing page provides an introduction to the application's purpose and functionality.

### Screen 2: Configuration
Enter your RallyHere auth token and the Sandbox ID for the environment you want to modify.

### Screen 3: God Selection
- View the complete list of gods with their current active/inactive status
- Use sorting options to organize the list as needed
- Select gods to be active in the rotation (checked = active, unchecked = inactive)
- Use the "Check All" or "Uncheck All" buttons for bulk operations

### Screen 4: Processing Updates
- View the progress of updates in real-time
- See a summary of successful updates and any errors encountered
- View detailed logs of API operations
- Download logs for record-keeping or troubleshooting

## Error Handling

The application handles several error conditions:
- Missing/invalid configuration files
- Authentication failures
- API request errors
- Network connectivity issues

Error messages are displayed in the UI with guidance on how to resolve common issues.

## Development and Extension

The code is structured to allow for easy extension and modification:
- Screen rendering functions are modular and independent
- API operations are encapsulated in a dedicated client class
- Configuration is externalized in JSON files

## Support and Troubleshooting

If you encounter issues:
1. Check the logs for API errors or unexpected responses
2. Verify your auth token and sandbox ID are correct
3. Ensure you have the necessary permissions for the RallyHere API

## License

[Insert appropriate license information]
