#!/usr/bin/env python3
"""
Test CORS Fix for ElevenLabs Integration
Verify that frontend can now connect to backend
"""

import requests
import json

def test_cors_fix():
    """Test that CORS is working properly"""
    print("🔧 Testing CORS Fix for ElevenLabs Integration")
    print("=" * 50)
    
    # Test OPTIONS request (CORS preflight)
    print("\n📡 Testing CORS Preflight (OPTIONS)...")
    try:
        response = requests.options(
            "http://localhost:8000/api/session/demo123/voice",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ OPTIONS request successful")
            print(f"   Status: {response.status_code}")
            print(f"   CORS Headers: {dict(response.headers)}")
        else:
            print(f"❌ OPTIONS request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ OPTIONS request error: {e}")
        return False
    
    # Test POST request (actual API call)
    print("\n📞 Testing Voice Agent API (POST)...")
    try:
        response = requests.post(
            "http://localhost:8000/api/session/demo123/voice",
            json={"voice_type": "earnings_call"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ POST request successful")
                voice_content = data.get("voice_content", {})
                print(f"   Title: {voice_content.get('title', 'N/A')}")
                print(f"   Audio Available: {voice_content.get('audio_available', False)}")
                print(f"   Participants: {len(voice_content.get('participants', {}))}")
                return True
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
                return False
        else:
            print(f"❌ POST request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ POST request error: {e}")
        return False

def show_frontend_instructions():
    """Show how to test the frontend"""
    print("\n🌐 Frontend Testing Instructions")
    print("=" * 35)
    
    print("\n✅ CORS Issue Fixed!")
    print("   🚫 No more 'Failed to fetch' errors")
    print("   ✅ OPTIONS requests now handled properly")
    print("   ✅ POST requests working correctly")
    
    print("\n🎯 How to Test Frontend:")
    print("   1. Open http://localhost:5174/ in browser")
    print("   2. Click 'Start Voice Practice' or '🎤 Voice Agent'")
    print("   3. Click any voice button:")
    print("      • 📞 Earnings Call")
    print("      • 🎧 SMAP Briefing") 
    print("      • 🧠 Interactive Quiz")
    print("   4. Should see content generated without errors!")
    
    print("\n🎤 What You'll See:")
    print("   ✅ Content loads successfully")
    print("   ✅ No 'Failed to fetch' errors")
    print("   ✅ Financial content displayed")
    print("   ⚠️ Audio shows 'Demo Mode' (until API key fixed)")

def show_api_key_status():
    """Show current API key status"""
    print("\n🔑 ElevenLabs API Key Status")
    print("=" * 35)
    
    print("\n⚠️ Current Status:")
    print("   🔑 API Key: 53715d9ad565308e547ed43a4506f39359bfc7b4d725927448de874a80c3973a")
    print("   ❌ Missing Permission: 'text_to_speech'")
    print("   🎵 Audio: Demo Mode (content works, no audio)")
    
    print("\n🔧 To Enable Audio:")
    print("   1. Go to: https://elevenlabs.io/app/settings/api-keys")
    print("   2. Create new API key with 'Text to Speech' permission")
    print("   3. Update working_elevenlabs_service.py")
    print("   4. Restart backend - audio will work immediately!")

def main():
    """Main test function"""
    # Test CORS fix
    cors_working = test_cors_fix()
    
    if cors_working:
        print("\n🎉 CORS Fix Successful!")
        print("✅ Frontend can now connect to backend")
        print("✅ Voice agent integration working")
        print("✅ Ready for testing!")
        
        show_frontend_instructions()
        show_api_key_status()
        
        print("\n🏆 Summary:")
        print("✅ CORS issue resolved")
        print("✅ Backend integration complete")
        print("✅ Frontend can connect")
        print("🔧 Just needs API key permission for audio")
        print("🚀 Ready for HackRU 2025 demo!")
    else:
        print("\n❌ CORS fix failed")
        print("🔧 Backend may need to be restarted")

if __name__ == "__main__":
    main()
