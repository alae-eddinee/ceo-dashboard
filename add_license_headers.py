#!/usr/bin/env python3
"""
Script to add MIT License headers to Python files in the CEO Dashboard project.
"""

import os
import glob

LICENSE_HEADER = '''"""
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

'''

def add_license_header(file_path):
    """Add license header to a Python file if it doesn't already have one."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has a license header
        if 'MIT License' in content and 'Copyright (c) 2025 Alae-Eddine Dahane' in content:
            print(f"✅ {file_path} - Already has license header")
            return
        
        # Add license header at the beginning
        new_content = LICENSE_HEADER + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {file_path} - License header added")
        
    except Exception as e:
        print(f"❌ {file_path} - Error: {str(e)}")

def main():
    """Add license headers to all Python files in the project."""
    
    # Directories to search for Python files
    directories = ['app', 'utils']
    
    print("🔧 Adding MIT License headers to Python files...")
    print("=" * 50)
    
    total_files = 0
    processed_files = 0
    
    for directory in directories:
        if os.path.exists(directory):
            python_files = glob.glob(os.path.join(directory, '*.py'))
            total_files += len(python_files)
            
            for file_path in python_files:
                add_license_header(file_path)
                processed_files += 1
    
    # Also process root Python files
    root_python_files = glob.glob('*.py')
    total_files += len(root_python_files)
    
    for file_path in root_python_files:
        add_license_header(file_path)
        processed_files += 1
    
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   Total Python files found: {total_files}")
    print(f"   Files processed: {processed_files}")
    print(f"   License headers added successfully! 🎉")

if __name__ == "__main__":
    main() 