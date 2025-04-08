import os
import subprocess
import sys
import socket
from src.config_utils import get_version

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_free_port(start_port=8888, max_attempts=10):
    """Find a free port starting from start_port"""
    port = start_port
    attempts = 0
    
    while attempts < max_attempts:
        if not is_port_in_use(port):
            return port
        port += 1
        attempts += 1
    
    # If we couldn't find a free port, use a random high port
    return 0  # Let streamlit choose a port

def check_install_requirements(requirements_path="Requirements.txt"):
    """Check and install required packages before running the app"""
    print("Checking Python dependencies...")
    
    try:
        # Check if pip is available
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: pip is not available. Please ensure pip is installed.")
        return False
    
    # Check for streamlit specifically since it's our main dependency
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "show", "streamlit"], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Streamlit is already installed.")
    except subprocess.CalledProcessError:
        print("Streamlit not found. Installing dependencies from Requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
            print("Please install requirements manually with: pip install -r Requirements.txt")
            return False
    
    # Check for other dependencies
    try:
        with open(requirements_path, 'r') as f:
            requirements = f.read().strip().split('\n')
        
        for req in requirements:
            if req and not req.startswith('#'):
                package = req.split('==')[0].split('>=')[0].strip()
                if package.lower() != 'streamlit':  # Skip streamlit as we already checked it
                    try:
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "show", package],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE
                        )
                    except subprocess.CalledProcessError:
                        print(f"Installing {package}...")
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", req],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE
                        )
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        print("Continuing anyway, but the application might fail if dependencies are missing.")
    
    return True

def main():
    """Main entry point for the application"""
    version = get_version()
    print(f"\n=== SMITE 2 God Rotation Manager v{version} ===\n")
    
    # First check and install dependencies
    if not check_install_requirements():
        print("Failed to ensure all dependencies are installed. Exiting.")
        sys.exit(1)
    
    # Kill any existing Streamlit processes
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(["taskkill", "/f", "/im", "streamlit.exe"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Also try to kill Python processes that might be running Streamlit
            subprocess.run(["taskkill", "/f", "/im", "python.exe", "/fi", "windowtitle eq streamlit"], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:  # Unix/Linux/Mac
            subprocess.run(["pkill", "-f", "streamlit"], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Note: Could not kill existing Streamlit processes. {e}")
    
    # Find a free port
    port = find_free_port()
    port_arg = str(port) if port else "8888"  # Use default if we couldn't find a free port
    
    # Run the application with Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "god_rotation_manager.py",
        "--server.port", port_arg,
        "--browser.serverAddress", "localhost",
        "--server.headless", "false",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    print(f"\nStarting Streamlit application at http://localhost:{port_arg}")
    print(f"If the browser doesn't open automatically, please open http://localhost:{port_arg}")
    print("Press Ctrl+C to exit\n")
    
    # Run Streamlit with all output visible
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"\nError running Streamlit: {e}")
        print("\nIf you're seeing an error about 'streamlit' not being found, try:")
        print(f"  {sys.executable} -m pip install streamlit")
        print("And then run this script again.")

if __name__ == "__main__":
    main() 