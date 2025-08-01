#!/usr/bin/env python3
"""
CEO Dashboard Setup Script

This script helps set up the CEO Dashboard project.
"""

import os
import sys
import subprocess
import venv

def main():
    """Setup the CEO Dashboard project"""
    
    print("🚀 CEO Dashboard Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("venv"):
        print("📦 Creating virtual environment...")
        venv.create("venv", with_pip=True)
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    # Install requirements
    print("📥 Installing dependencies...")
    try:
        if os.name == 'nt':  # Windows
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        else:  # Unix/Linux/macOS
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)
    
    # Generate sample data
    print("📊 Generating sample business data...")
    try:
        subprocess.run([sys.executable, "utils/data_loader.py"], check=True)
        print("✅ Sample data generated")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating data: {e}")
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Run the dashboard: python run_dashboard.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. For AI features, add your OpenAI API key in the dashboard")
    print("\n📚 Documentation:")
    print("- README.md: Project overview and features")
    print("- notebooks/: Jupyter notebooks for data exploration")
    print("- app/: Dashboard application files")
    print("- utils/: Utility functions and data processing")

if __name__ == "__main__":
    main() 