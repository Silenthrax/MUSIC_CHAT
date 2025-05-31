#!/usr/bin/env python3
"""
PIHU Music Bot - Startup Verification Script
This script verifies that all components are properly configured
"""

import os
import sys
from pathlib import Path

def check_file_structure():
    """Check if all required files and folders exist"""
    print("🔍 Checking file structure...")
    
    required_files = [
        "config.py",
        "requirements.txt", 
        "sample.env",
        "PIHUMUSIC/__init__.py",
        "PIHUMUSIC/__main__.py",
        "PIHUMUSIC/core/bot.py",
        "PIHUMUSIC/core/call.py",
        "strings/__init__.py"
    ]
    
    required_dirs = [
        "PIHUMUSIC",
        "PIHUMUSIC/core",
        "PIHUMUSIC/plugins", 
        "PIHUMUSIC/utils",
        "PIHUMUSIC/platforms",
        "strings"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ File structure is correct")
    return True

def check_environment():
    """Check if environment variables are configured"""
    print("🔍 Checking environment configuration...")
    
    if Path(".env").exists():
        print("✅ .env file found")
        return True
    elif Path("sample.env").exists():
        print("⚠️  sample.env found but .env is missing")
        print("💡 Copy sample.env to .env and configure your credentials")
        return False
    else:
        print("❌ No environment configuration found")
        return False

def main():
    print("🎵 PIHU Music Bot - Startup Verification")
    print("=" * 50)
    
    # Check file structure
    structure_ok = check_file_structure()
    
    # Check environment
    env_ok = check_environment()
    
    print("\n" + "=" * 50)
    
    if structure_ok:
        print("✅ All imports and file structure are working correctly!")
        print("✅ PIHUMUSIC package is properly configured!")
        
        if env_ok:
            print("🚀 Ready to start! Run: python -m PIHUMUSIC")
        else:
            print("⚠️  Configure your .env file first, then run: python -m PIHUMUSIC")
    else:
        print("❌ Please fix the missing files/directories first")

if __name__ == "__main__":
    main()
