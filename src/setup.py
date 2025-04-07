import subprocess
import sys

def main():
    """Setup script to upgrade pip and install requirements"""
    print("Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    print("\nInstalling requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\nSetup complete!")

if __name__ == "__main__":
    main()