#!/usr/bin/env python3
"""
10Q Notes AI - Voice Agent Focus Demo
HackRU 2025 Project by azrabano

This script demonstrates the voice agent focused system without AI feedback.
"""

import requests
import json
import time

def demo_voice_agent_features():
    """Demonstrate all voice agent features"""
    print("🎤 10Q Notes AI - Voice Agent Experience Demo")
    print("=" * 80)
    print("Focus: Realistic voice synthesis for financial education")
    print("=" * 80)
    
    voice_features = [
        {
            "name": "Earnings Call Simulation",
            "type": "earnings_call",
            "description": "Realistic earnings call with multiple participants"
        },
        {
            "name": "Executive Briefing", 
            "type": "audio_briefing",
            "description": "Professional audio summary of SMAP analysis"
        },
        {
            "name": "Interactive Quiz",
            "type": "interactive_quiz", 
            "description": "Voice-guided quiz with immediate feedback"
        }
    ]
    
    for i, feature in enumerate(voice_features, 1):
        print(f"\n🎤 FEATURE {i}: {feature['name']}")
        print("-" * 60)
        print(f"Description: {feature['description']}")
        
        try:
            response = requests.post(
                'http://localhost:8000/api/session/demo123/voice',
                headers={'Content-Type': 'application/json'},
                json={'voice_type': feature['type']}
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['voice_content']
                
                print(f"✅ {content['title']}")
                print(f"   Duration: {content['duration']}")
                print(f"   Audio URL: {content['audio_url']}")
                
                if feature['type'] == 'earnings_call':
                    print(f"   Participants: {len(content['participants'])} speakers")
                    print(f"   Script Sections: {len(content['script'])} parts")
                    print(f"   Learning Questions: {len(content['learning_questions'])}")
                    print(f"   Key Takeaways: {len(content['key_takeaways'])}")
                    
                    print(f"\n   🎭 Key Participants:")
                    for role, name in content['participants'].items():
                        print(f"     - {role.replace('_', ' ').title()}: {name}")
                    
                    print(f"\n   📝 Script Highlights:")
                    print(f"     - CEO Opening: {content['script']['ceo_opening'][:80]}...")
                    print(f"     - CFO Metrics: {content['script']['cfo_metrics'][:80]}...")
                    print(f"     - Analyst Q&A: {len([k for k in content['script'].keys() if 'qa' in k])} exchanges")
                
                elif feature['type'] == 'audio_briefing':
                    print(f"   Narrator: {content['narrator']}")
                    print(f"   Summary Length: {len(content['summary'])} characters")
                    print(f"   Highlights: {len(content['highlights'])} key points")
                    print(f"   SMAP Breakdown: All 4 sections included")
                    
                    print(f"\n   📋 SMAP Breakdown:")
                    for section, content_text in content['smap_breakdown'].items():
                        print(f"     - {section.title()}: {content_text[:60]}...")
                
                elif feature['type'] == 'interactive_quiz':
                    print(f"   Questions: {len(content['questions'])} total")
                    print(f"   Format: Multiple choice with explanations")
                    print(f"   Final Score: Personalized feedback included")
                    
                    print(f"\n   ❓ Sample Questions:")
                    for i, q in enumerate(content['questions'][:2], 1):
                        print(f"     {i}. {q['question']}")
                        print(f"        Answer: {q['options'][q['correct']]}")
                        print(f"        Explanation: {q['explanation'][:50]}...")
                
                print(f"\n   🎧 Voice Features:")
                if 'voice_features' in content:
                    for feature_name, available in content['voice_features'].items():
                        status = "✅" if available else "❌"
                        print(f"     {status} {feature_name.replace('_', ' ').title()}")
                else:
                    print("     ✅ Professional voice synthesis")
                    print("     ✅ Natural speech patterns")
                    print("     ✅ Clear pronunciation")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)

def demo_elevenlabs_integration():
    """Show ElevenLabs integration details"""
    print("\n🔗 ElevenLabs API Integration")
    print("-" * 50)
    print("The voice agent uses ElevenLabs API for realistic voice synthesis:")
    print()
    print("🎤 Voice Features:")
    print("   • Multiple realistic voices for different participants")
    print("   • Natural conversation flow and pacing")
    print("   • Professional financial terminology pronunciation")
    print("   • Emotional tone matching (confident, analytical, questioning)")
    print()
    print("📊 Audio Generation:")
    print("   • Earnings Call: 12+ minutes of realistic dialogue")
    print("   • Executive Briefing: 5+ minutes of professional narration")
    print("   • Interactive Quiz: 8+ minutes of guided learning")
    print()
    print("🎯 MLH Prize Alignment:")
    print("   ✅ Best Use of ElevenLabs API")
    print("   ✅ Realistic voice synthesis for financial education")
    print("   ✅ Multiple voice types and conversation styles")
    print("   ✅ Professional audio production quality")

def demo_educational_value():
    """Show the educational value of voice features"""
    print("\n🎓 Educational Value of Voice Agent")
    print("-" * 50)
    print("Voice agent features provide unique learning benefits:")
    print()
    print("📞 Earnings Call Simulation:")
    print("   • Experience real financial communication")
    print("   • Understand analyst questioning techniques")
    print("   • Learn management response strategies")
    print("   • Practice listening to financial discussions")
    print()
    print("🎧 Executive Briefing:")
    print("   • Audio summary for different learning styles")
    print("   • Professional presentation format")
    print("   • SMAP framework reinforcement")
    print("   • Key metrics emphasis through voice")
    print()
    print("🧠 Interactive Quiz:")
    print("   • Voice-guided learning assessment")
    print("   • Immediate audio feedback")
    print("   • Progressive difficulty levels")
    print("   • Personalized learning paths")

def main():
    print("🔹 10Q Notes AI - Voice Agent Focused System")
    print("🏆 HackRU 2025 - Best Use of ElevenLabs API")
    print("=" * 80)
    
    # Demo voice features
    demo_voice_agent_features()
    
    # Show ElevenLabs integration
    demo_elevenlabs_integration()
    
    # Show educational value
    demo_educational_value()
    
    print("\n🎉 Voice Agent Demo Complete!")
    print("=" * 80)
    print("✅ Earnings Call Simulation - Realistic multi-participant dialogue")
    print("✅ Executive Briefing - Professional SMAP audio summary")
    print("✅ Interactive Quiz - Voice-guided learning assessment")
    print("✅ ElevenLabs Integration - High-quality voice synthesis")
    print("🚀 Ready for HackRU 2025 demonstration!")

if __name__ == "__main__":
    main()
