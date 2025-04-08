import json
import os

# Default config values
_DEFAULT_CONFIG = {
    "version": "1.0"
}

# Cached config
_config = None

def load_config():
    """Load and cache the application configuration"""
    global _config
    
    if _config is not None:
        return _config
        
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "app_config.json")
    
    try:
        with open(config_path, 'r') as f:
            _config = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config file: {e}")
        _config = _DEFAULT_CONFIG
        
    return _config

def get_version():
    """Get the application version"""
    config = load_config()
    return config.get("version", _DEFAULT_CONFIG["version"]) 