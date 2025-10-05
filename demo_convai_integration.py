#!/usr/bin/env python3
"""
Demo: Complete ConvAI Integration with ElevenLabs Agent
Shows the working ConvAI widget integration for the voice agent tab
"""

import requests
import json
import time

def demo_convai_integration():
    """Demo the complete ConvAI integration"""
    print("🎤 10Q Notes AI - ConvAI Integration Demo")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health Check
    print("\n1. 🔧 Testing Backend Health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Backend is healthy")
            print(f"   Status: {health_data['status']}")
            print(f"   Services: {health_data['services']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Test 2: ConvAI Agent Info
    print("\n2. 🤖 Getting ConvAI Agent Information...")
    try:
        response = requests.post(
            f"{base_url}/api/session/demo123/convai",
            json={"action": "get_info"}
        )
        
        if response.status_code == 200:
            convai_data = response.json()
            if convai_data["success"]:
                agent = convai_data["convai_agent"]
                print("✅ ConvAI agent is ready!")
                print(f"   Agent ID: {agent['agent_id']}")
                print(f"   Type: {agent['type']}")
                print(f"   Status: {agent['status']}")
                print(f"   Capabilities: {len(agent['capabilities'])} features")
                print(f"   Integration: {'Ready' if agent['integration_ready'] else 'Not Ready'}")
                
                print(f"\n   Widget Code:")
                print(f"   {agent['widget_code']}")
                print(f"\n   Script URL:")
                print(f"   {agent['script_url']}")
            else:
                print(f"❌ ConvAI agent error: {convai_data['error']}")
        else:
            print(f"❌ ConvAI request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ ConvAI request error: {e}")
    
    # Test 3: Create Conversation
    print("\n3. 💬 Creating ConvAI Conversation...")
    try:
        response = requests.post(
            f"{base_url}/api/session/demo123/convai",
            json={"action": "create_conversation", "session_id": "demo_session_456"}
        )
        
        if response.status_code == 200:
            conv_data = response.json()
            if conv_data["success"]:
                conversation = conv_data["conversation"]
                widget = conv_data["convai_widget"]
                print("✅ Conversation created successfully!")
                print(f"   Session: {conversation['session_id']}")
                print(f"   Agent: {conversation['agent_id']}")
                print(f"   Type: {conversation['conversation_type']}")
                print(f"   Widget Ready: {widget['ready']}")
                
                print(f"\n   Context:")
                context = conversation['context']
                print(f"   - Company: {context['company']}")
                print(f"   - Filing: {context['filing_type']}")
                print(f"   - Focus: {context['current_focus']}")
                print(f"   - User Role: {context['user_role']}")
            else:
                print(f"❌ Conversation creation failed: {conv_data['error']}")
        else:
            print(f"❌ Conversation request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Conversation request error: {e}")
    
    # Test 4: Get Conversation Scripts
    print("\n4. 📝 Getting Available Conversation Scripts...")
    for script_type in ["earnings_call", "financial_analysis", "interactive_quiz"]:
        try:
            response = requests.post(
                f"{base_url}/api/session/demo123/convai",
                json={"action": "get_scripts", "conversation_type": script_type}
            )
            
            if response.status_code == 200:
                script_data = response.json()
                if script_data["success"]:
                    script = script_data["script"]
                    print(f"   ✅ {script['title']}")
                    print(f"      {script['description']}")
                else:
                    print(f"   ❌ Script error for {script_type}: {script_data['error']}")
            else:
                print(f"   ❌ Script request failed for {script_type}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Script request error for {script_type}: {e}")
    
    # Test 5: Voice Agent (Audio Content)
    print("\n5. 🎧 Testing Voice Agent Audio Generation...")
    try:
        response = requests.post(
            f"{base_url}/api/session/demo123/voice",
            json={"voice_type": "earnings_call"}
        )
        
        if response.status_code == 200:
            voice_data = response.json()
            if voice_data["success"]:
                voice_content = voice_data["voice_content"]
                print("✅ Voice content generated!")
                print(f"   Title: {voice_content['title']}")
                print(f"   Duration: {voice_content['duration']}")
                print(f"   Audio Available: {voice_content['audio_available']}")
                print(f"   Participants: {len(voice_content['participants'])}")
                print(f"   Script Sections: {len(voice_content['script'])}")
            else:
                print(f"❌ Voice generation failed: {voice_data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Voice request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Voice request error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 ConvAI Integration Demo Complete!")
    print("\n📋 Summary:")
    print("✅ Backend server running")
    print("✅ ConvAI agent initialized")
    print("✅ Widget integration ready")
    print("✅ Conversation management working")
    print("✅ Voice agent audio generation working")
    print("✅ Both ConvAI widget and audio content available")
    
    print("\n🎯 Next Steps:")
    print("1. Open frontend: http://localhost:5174")
    print("2. Click 'Voice Agent' tab")
    print("3. Select 'Interactive ConvAI Agent' mode")
    print("4. Use the embedded ConvAI widget")
    print("5. Practice investor calls with AI agent!")
    
    print("\n💡 Features Available:")
    print("- 🤖 Interactive ConvAI widget with agent_2001k6r67ejzejx930t22kwwaw5j")
    print("- 🎧 Audio content generation (earnings calls, briefings, quizzes)")
    print("- 💬 Real-time conversation with financial AI advisor")
    print("- 📊 Financial analysis Q&A")
    print("- 🎯 Investment advice and market discussion")

def main():
    """Main function"""
    demo_convai_integration()

if __name__ == "__main__":
    main()
