"""
MIT License

Copyright (c) 2025 Alae-Eddine Dahane

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#!/usr/bin/env python3
"""
CEO Dashboard Launcher

This script launches the CEO Dashboard application.
"""

import subprocess
import sys
import os

def main():
    """Launch the CEO Dashboard"""
    
    print("🚀 Starting CEO Dashboard...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app/dashboard.py"):
        print("❌ Error: dashboard.py not found!")
        print("Please run this script from the ceo-dashboard directory.")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements with: pip install -r requirements.txt")
        sys.exit(1)
    
    # Launch the dashboard
    print("🌐 Launching dashboard at http://localhost:8501")
    print("📊 Press Ctrl+C to stop the dashboard")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app/dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")

if __name__ == "__main__":
    main() 