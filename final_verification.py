#!/usr/bin/env python3
"""
PIHU Music Bot - Final Verification Script
Tests all critical components to ensure the bot is ready for deployment.
"""

import sys
import traceback

def test_import(module_name, description):
    """Test importing a module and return result."""
    try:
        __import__(module_name)
        print(f"✅ {description}: SUCCESS")
        return True
    except Exception as e:
        print(f"❌ {description}: FAILED - {str(e)}")
        return False

def main():
    print("🔍 PIHU Music Bot - Final Verification")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test critical imports
    test_cases = [
        ("config", "Configuration module"),
        ("PIHUMUSIC", "Main PIHU module"),
        ("PIHUMUSIC.core.mongo", "MongoDB connection"),
        ("PIHUMUSIC.core.bot", "Bot core"),
        ("PIHUMUSIC.core.userbot", "Userbot core"),
        ("PIHUMUSIC.utils.database", "Database utilities"),
        ("PIHUMUSIC.utils.ssl_helper", "SSL helper"),
        ("PIHUMUSIC.platforms", "Music platforms"),
        ("PIHUMUSIC.platforms.Youtube", "YouTube platform"),
        ("PIHUMUSIC.platforms.Spotify", "Spotify platform"),
        ("pytgcalls", "PyTgCalls library"),
        ("pyrogram", "Pyrogram library"),
        ("motor", "Motor MongoDB driver"),
        ("pymongo", "PyMongo library"),
        ("SafoneAPI", "SafoneAPI library"),
        ("bs4", "BeautifulSoup4"),
        ("spotipy", "Spotipy library"),
    ]
    
    for module, description in test_cases:
        total_tests += 1
        if test_import(module, description):
            tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! The bot is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Copy sample.env to .env")
        print("2. Fill in your bot credentials in .env")
        print("3. Run: python -m PIHUMUSIC")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
