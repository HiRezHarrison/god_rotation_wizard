#!/usr/bin/env python3

import sys
import os
import json
from chest_gui import ChestCreationWizard

def load_config(config_dir: str, config_name: str) -> dict:
    """Load a configuration file from the config directory"""
    config_path = os.path.join(config_dir, config_name)
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {config_name}: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point for the SMITE 2 Treasure Chest Creation Wizard"""
    try:
        # Get the project root directory (one level up from src)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Set up paths
        icons_path = os.path.join(project_root, "assets", "icons")
        config_dir = os.path.join(project_root, "config")
        
        # Ensure required directories exist
        if not os.path.exists(icons_path):
            print(f"Error: Icons directory not found at {icons_path}")
            sys.exit(1)
        if not os.path.exists(config_dir):
            print(f"Error: Config directory not found at {config_dir}")
            sys.exit(1)
            
        # Load configurations
        app_config = load_config(config_dir, "app_config.json")
        api_template = load_config(config_dir, "api_template.json")
        logging_config = load_config(config_dir, "logging_config.json")
        
        # Create and run the wizard
        wizard = ChestCreationWizard(
            icons_dir=icons_path,
            app_config=app_config,
            api_template=api_template,
            logging_config=logging_config
        )
        wizard.run()
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
