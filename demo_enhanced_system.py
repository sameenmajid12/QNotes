#!/usr/bin/env python3
"""
Enhanced 10Q Notes AI Demo
HackRU 2025 Project by azrabano

This script demonstrates the enhanced feedback system and voice agent.
"""

import requests
import json
import time

def test_enhanced_feedback():
    """Test the enhanced feedback system"""
    print("🧪 Testing Enhanced AI Feedback System")
    print("=" * 60)
    
    # Test cases with different quality levels
    test_cases = [
        {
            "name": "Poor Quality (I don't know responses)",
            "data": {
                "subjective": "I don't know what management said",
                "metrics": "I don't know the numbers",
                "assessment": "I don't know what it means",
                "plan": "I don't know what to do"
            }
        },
        {
            "name": "Basic Quality (Simple responses)",
            "data": {
                "subjective": "Management was confident about results",
                "metrics": "Revenue was $42.5 billion",
                "assessment": "The company is doing well",
                "plan": "Buy the stock"
            }
        },
        {
            "name": "Good Quality (Detailed responses)",
            "data": {
                "subjective": "Management expressed strong confidence in Q1 performance, highlighting robust revenue growth and disciplined expense management. The tone was optimistic about future opportunities in digital banking.",
                "metrics": "Total revenue of $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%, Net interest margin 2.74%",
                "assessment": "JPMorgan demonstrates solid fundamental strength with revenue growth across segments. The fortress balance sheet provides flexibility for economic volatility while maintaining strong profitability metrics.",
                "plan": "Monitor credit provision trends, assess interest rate sensitivity, evaluate investment banking recovery, track digital transformation progress"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                'http://localhost:8000/api/session/demo123/feedback',
                headers={'Content-Type': 'application/json'},
                json={'student_work': test_case['data']}
            )
            
            if response.status_code == 200:
                result = response.json()
                feedback = result['feedback']
                
                print(f"📊 Overall Score: {feedback['overall_score']}/100 (Grade: {feedback['grade']})")
                print(f"📈 Section Scores:")
                for section, score in feedback['section_scores'].items():
                    print(f"   - {section.title()}: {score}/100")
                
                print(f"\n💬 Detailed Feedback:")
                for section, details in feedback['detailed_feedback'].items():
                    print(f"\n   {section.upper()}:")
                    print(f"     Score: {details['score']}/100")
                    print(f"     Feedback: {details['feedback']}")
                    if details['strengths']:
                        print(f"     Strengths: {', '.join(details['strengths'])}")
                    if details['weaknesses']:
                        print(f"     Weaknesses: {', '.join(details['weaknesses'])}")
                
                if feedback['improvements']:
                    print(f"\n🚀 Improvements:")
                    for improvement in feedback['improvements']:
                        print(f"   - {improvement}")
                
                print(f"\n📋 Next Steps:")
                for step in feedback['next_steps']:
                    print(f"   - {step}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)

def test_voice_agent():
    """Test the voice agent functionality"""
    print("\n🎤 Testing Voice Agent Features")
    print("=" * 60)
    
    voice_types = [
        {
            "name": "Earnings Call Simulation",
            "type": "earnings_call"
        },
        {
            "name": "Audio Briefing",
            "type": "audio_briefing"
        }
    ]
    
    for i, voice_test in enumerate(voice_types, 1):
        print(f"\n🎤 Test {i}: {voice_test['name']}")
        print("-" * 50)
        
        try:
            response = requests.post(
                'http://localhost:8000/api/session/demo123/voice',
                headers={'Content-Type': 'application/json'},
                json={'voice_type': voice_test['type']}
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['voice_content']
                
                print(f"📞 Title: {content['title']}")
                print(f"⏱️ Duration: {content['duration']}")
                print(f"🔗 Audio URL: {content['audio_url']}")
                
                if voice_test['type'] == 'earnings_call':
                    print(f"\n📝 Script Preview:")
                    for role, text in content['script'].items():
                        print(f"   {role.replace('_', ' ').title()}: {text}")
                    
                    print(f"\n❓ Learning Questions:")
                    for question in content['learning_questions']:
                        print(f"   - {question}")
                    
                    print(f"\n🎯 Key Takeaways:")
                    for takeaway in content['key_takeaways']:
                        print(f"   - {takeaway}")
                
                elif voice_test['type'] == 'audio_briefing':
                    print(f"\n📋 Summary:")
                    print(f"   {content['summary']}")
                    
                    print(f"\n⭐ Highlights:")
                    for highlight in content['highlights']:
                        print(f"   - {highlight}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*60)

def main():
    print("🔹 Enhanced 10Q Notes AI Demo")
    print("🏆 HackRU 2025 - Improved Feedback & Voice Agent")
    print("=" * 80)
    
    # Test enhanced feedback
    test_enhanced_feedback()
    
    # Test voice agent
    test_voice_agent()
    
    print("\n🎉 Demo Complete!")
    print("=" * 80)
    print("✅ Enhanced AI Feedback System - Detailed, helpful feedback")
    print("✅ Voice Agent - Earnings call simulation and audio briefings")
    print("✅ MLH Prize Features - Gemini API, ElevenLabs, Snowflake")
    print("🚀 Ready for HackRU 2025 demonstration!")

if __name__ == "__main__":
    main()
