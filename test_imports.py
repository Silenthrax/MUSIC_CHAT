#!/usr/bin/env python3
"""
Test script to verify all critical imports work correctly
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.getcwd())

def test_imports():
    try:
        # Test pytgcalls imports
        print("Testing pytgcalls imports...")
        from pytgcalls import PyTgCalls, StreamType
        from pytgcalls.exceptions import NoActiveGroupCall, AlreadyJoinedError
        from pytgcalls.types import Update
        from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
        from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
        from pytgcalls.types.stream import StreamAudioEnded
        print("✅ pytgcalls imports successful")
        
        # Test pyrogram imports
        print("Testing pyrogram imports...")
        from pyrogram import Client, filters
        from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
        print("✅ pyrogram imports successful")
        
        # Test basic Python imports that the bot uses
        print("Testing other dependencies...")
        import asyncio
        import aiohttp
        import motor
        import psutil
        import yt_dlp
        print("✅ Other dependencies successful")
        
        print("\n🎉 All critical imports are working correctly!")
        print("The music bot should be able to start once environment variables are configured.")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing PIHU Music Bot imports...\n")
    success = test_imports()
    
    if success:
        print("\n📝 Next steps:")
        print("1. Copy 'sample.env' to '.env'")
        print("2. Fill in your API credentials in the .env file")
        print("3. Run the bot with: python -m PIHUMUSIC")
    else:
        print("\n❌ Please fix the import issues before running the bot.")
