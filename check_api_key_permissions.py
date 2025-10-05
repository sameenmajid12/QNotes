#!/usr/bin/env python3
"""
Check ElevenLabs API Key Permissions
"""

import requests
import json

def check_api_key_permissions():
    """Check what permissions the API key has"""
    api_key = "53715d9ad565308e547ed43a4506f39359bfc7b4d725927448de874a80c3973a"
    
    print("🔑 Checking ElevenLabs API Key Permissions")
    print("=" * 45)
    
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_key
    }
    
    # Test 1: Check if we can access the API at all
    print("\n1. 🔗 Testing API Access...")
    try:
        response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
        if response.status_code == 200:
            print("✅ API key is valid and can access voices")
            voices = response.json()
            print(f"   Available voices: {len(voices.get('voices', []))}")
        else:
            print(f"❌ API key issue: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error accessing API: {e}")
    
    # Test 2: Try TTS with minimal request
    print("\n2. 🎤 Testing Text-to-Speech Permission...")
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        payload = {
            "text": "Test",
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("✅ Text-to-Speech permission is WORKING!")
            print(f"   Audio size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Text-to-Speech permission MISSING")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TTS: {e}")
        return False

def show_fix_instructions():
    """Show how to fix the API key"""
    print("\n🔧 How to Fix API Key Permissions")
    print("=" * 40)
    
    print("\n📋 Step-by-Step Fix:")
    print("\n1. 🌐 Go to ElevenLabs Dashboard:")
    print("   https://elevenlabs.io/app/settings/api-keys")
    
    print("\n2. 🔍 Find Your API Key:")
    print("   53715d9ad565308e547ed43a4506f39359bfc7b4d725927448de874a80c3973a")
    
    print("\n3. ⚙️ Edit API Key:")
    print("   - Click 'Edit' or 'Manage' next to your key")
    print("   - Look for 'Permissions' section")
    print("   - Check the box for 'Text to Speech'")
    print("   - Click 'Save' or 'Update'")
    
    print("\n4. 🆕 Alternative - Create New Key:")
    print("   - Click 'Create API Key'")
    print("   - Name: '10Q Notes AI TTS'")
    print("   - Enable: 'Text to Speech'")
    print("   - Copy the new key")
    
    print("\n5. 🔄 Update Code:")
    print("   - Open: working_elevenlabs_service.py")
    print("   - Line 18: Replace with new API key")
    print("   - Save file")
    
    print("\n6. 🚀 Restart Backend:")
    print("   - Stop current backend (Ctrl+C)")
    print("   - Run: python working_backend_with_elevenlabs.py")
    print("   - Audio will work immediately!")

def main():
    """Main function"""
    has_permission = check_api_key_permissions()
    
    if has_permission:
        print("\n🎉 Great! Your API key already has TTS permission!")
        print("✅ Audio should be working")
        print("🔧 If still showing demo mode, restart the backend")
    else:
        print("\n⚠️ API key needs permission update")
        show_fix_instructions()
        
        print("\n💡 Quick Test After Fix:")
        print("   1. Update API key in code")
        print("   2. Restart backend")
        print("   3. Test: python check_api_key_permissions.py")
        print("   4. Should see '✅ Text-to-Speech permission is WORKING!'")

if __name__ == "__main__":
    main()
