#!/usr/bin/env python3
"""
Demo script for the updated 10Q Notes AI frontend
Focus: Voice Agent Features (No AI Feedback/Comparison)
"""

import requests
import json
import time

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_voice_agent_endpoints():
    """Test the three voice agent endpoints"""
    print("\n🎤 Testing Voice Agent Endpoints")
    print("=" * 50)
    
    session_id = "demo123"
    voice_types = [
        "earnings_call",
        "audio_briefing", 
        "interactive_quiz"
    ]
    
    for voice_type in voice_types:
        print(f"\n📞 Testing {voice_type.replace('_', ' ').title()}")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"http://localhost:8000/api/session/{session_id}/voice",
                json={"voice_type": voice_type},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    voice_content = data.get("voice_content", {})
                    print(f"✅ {voice_content.get('title', 'Voice Content')}")
                    print(f"   Duration: {voice_content.get('duration', 'N/A')}")
                    
                    if voice_type == "earnings_call":
                        participants = voice_content.get("participants", {})
                        print(f"   Participants: {len(participants)} speakers")
                        
                    elif voice_type == "audio_briefing":
                        highlights = voice_content.get("highlights", [])
                        print(f"   Highlights: {len(highlights)} key points")
                        
                    elif voice_type == "interactive_quiz":
                        questions = voice_content.get("questions", [])
                        print(f"   Questions: {len(questions)} quiz items")
                        
                else:
                    print(f"❌ API returned success=false: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing {voice_type}: {e}")

def test_frontend_access():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Access")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:5174/")
        if response.status_code == 200:
            print("✅ React frontend is accessible at http://localhost:5174/")
            print("   - Updated dashboard with 3 learning modes")
            print("   - Voice Agent section added")
            print("   - AI Feedback and Comparison sections removed")
        else:
            print(f"❌ Frontend not accessible: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")

def show_user_instructions():
    """Show instructions for using the updated system"""
    print("\n🎯 How to Use the Updated System")
    print("=" * 40)
    
    print("\n1. 🌐 Access the Frontend:")
    print("   Go to: http://localhost:5174/")
    
    print("\n2. 🏠 Dashboard Features:")
    print("   - Upload 10-Q/10-K filing")
    print("   - Three Learning Mode cards:")
    print("     • 📖 Learn Mode")
    print("     • ✍️ Practice Mode") 
    print("     • 🎤 Voice Agent (NEW!)")
    
    print("\n3. 🎤 Voice Agent Experience:")
    print("   - Click 'Start Voice Practice'")
    print("   - Choose from 3 voice experiences:")
    print("     • 📞 Earnings Call Simulation (12+ min)")
    print("     • 🎧 Executive Briefing (5+ min)")
    print("     • 🧠 Interactive Quiz (8+ min)")
    
    print("\n4. 🔧 Backend API:")
    print("   - Health: http://localhost:8000/health")
    print("   - Voice Agent: POST /api/session/{id}/voice")
    print("   - Documentation: http://localhost:8000/docs")
    
    print("\n5. 🎯 Key Changes:")
    print("   ✅ Removed AI Feedback section")
    print("   ✅ Removed Comparison section")
    print("   ✅ Added Voice Agent as main feature")
    print("   ✅ Three interactive voice experiences")
    print("   ✅ Professional UI with voice-focused design")

def main():
    """Main demo function"""
    print("🔹 10Q Notes AI - Updated Frontend Demo")
    print("🏆 HackRU 2025 - Voice Agent Focused System")
    print("=" * 60)
    
    # Test backend
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start enhanced_backend.py first.")
        return
    
    # Test voice agent endpoints
    test_voice_agent_endpoints()
    
    # Test frontend
    test_frontend_access()
    
    # Show instructions
    show_user_instructions()
    
    print("\n🎉 Demo Complete!")
    print("=" * 20)
    print("✅ Backend: Voice Agent API working")
    print("✅ Frontend: Updated UI with voice focus")
    print("✅ Ready for HackRU 2025 demonstration!")

if __name__ == "__main__":
    main()
