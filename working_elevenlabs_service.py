#!/usr/bin/env python3
"""
Working ElevenLabs Text-to-Speech Service
Fixed integration with proper API handling
"""

import requests
import json
import base64
from typing import Dict, Any, Optional

class WorkingElevenLabsService:
    """Working ElevenLabs Text-to-Speech integration"""
    
    def __init__(self, api_key: str = "53715d9ad565308e547ed43a4506f39359bfc7b4d725927448de874a80c3973a"):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Use a known working voice ID
        self.default_voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam voice (known to work)
        self.default_model = "eleven_monolingual_v1"
    
    def text_to_speech(self, text: str, voice_id: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to speech using ElevenLabs API"""
        try:
            voice_id = voice_id or self.default_voice_id
            
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            payload = {
                "text": text,
                "model_id": self.default_model,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8
                }
            }
            
            print(f"🎤 Making request to ElevenLabs API...")
            print(f"   URL: {url}")
            print(f"   Voice ID: {voice_id}")
            print(f"   Text length: {len(text)} characters")
            
            response = requests.post(url, json=payload, headers=headers)
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                # Convert audio to base64 for web playback
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                
                return {
                    "success": True,
                    "audio_data": response.content,
                    "audio_url": f"data:audio/mpeg;base64,{audio_base64}",
                    "voice_id": voice_id,
                    "model": self.default_model,
                    "text": text,
                    "content_type": "audio/mpeg",
                    "size_bytes": len(response.content)
                }
            else:
                error_msg = f"TTS failed: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text}"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception in text_to_speech: {str(e)}"
            }
    
    def generate_financial_audio(self, content_type: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial audio content"""
        
        if content_type == "earnings_call_opening":
            text = f"""Good morning, and welcome to {company_data.get('company_name', 'our company')}'s earnings call for {company_data.get('quarter', 'Q1 2025')}. I'm pleased to report strong financial performance with revenue of {company_data.get('revenue', 'forty two point five billion dollars')}, representing year-over-year growth of {company_data.get('growth_rate', 'six point eight percent')}. Our net income came in at {company_data.get('net_income', 'thirteen point four billion dollars')}, demonstrating the strength of our diversified business model."""
        
        elif content_type == "smap_briefing":
            text = f"""Let me provide you with a comprehensive SMAP analysis of {company_data.get('company_name', 'our company')}'s performance. From a Subjective perspective, management expressed strong confidence in the quarter's results. Key Metrics include revenue of {company_data.get('revenue', 'forty two point five billion dollars')}, net income of {company_data.get('net_income', 'thirteen point four billion dollars')}, and a return on equity of {company_data.get('roe', 'seventeen point eight percent')}. Our Assessment shows solid fundamental strength with a fortress balance sheet. Looking ahead, our Plan focuses on continued digital transformation and maintaining our strong capital position."""
        
        elif content_type == "interactive_quiz":
            text = f"""Welcome to the financial analysis quiz. Question one: What was {company_data.get('company_name', 'our company')}'s total revenue for {company_data.get('quarter', 'Q1 2025')}? Option A: Forty point two billion dollars. Option B: Forty two point five billion dollars. Option C: Forty five point one billion dollars. Option D: Thirty eight point seven billion dollars. Please select your answer."""
        
        else:
            text = f"""Welcome to the financial analysis session for {company_data.get('company_name', 'our company')}. Today we'll be discussing the company's {company_data.get('quarter', 'Q1 2025')} performance and outlook. Let's begin with a review of the key financial metrics and strategic initiatives."""
        
        return self.text_to_speech(text)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the ElevenLabs API connection"""
        try:
            print("🔗 Testing ElevenLabs API connection...")
            result = self.text_to_speech("Testing ElevenLabs integration for 10Q Notes AI. This is a test of the text to speech functionality.")
            
            if result.get("success"):
                return {
                    "success": True,
                    "message": "ElevenLabs API connection successful",
                    "voice_id": result.get("voice_id"),
                    "model": result.get("model"),
                    "audio_size": result.get("size_bytes")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection test failed: {str(e)}"
            }

def main():
    """Test the working ElevenLabs service"""
    print("🎤 Testing Working ElevenLabs Service")
    print("=" * 40)
    
    # Initialize service
    service = WorkingElevenLabsService()
    
    # Test connection
    print("\n🔗 Testing API Connection...")
    connection_test = service.test_connection()
    
    if connection_test.get("success"):
        print("✅ ElevenLabs API connection successful")
        print(f"   Voice ID: {connection_test.get('voice_id')}")
        print(f"   Model: {connection_test.get('model')}")
        print(f"   Audio size: {connection_test.get('audio_size')} bytes")
        
        # Test financial audio generation
        print("\n💰 Testing Financial Audio Generation...")
        
        company_data = {
            "company_name": "JPMorgan Chase",
            "quarter": "Q1 2025",
            "revenue": "forty two point five billion dollars",
            "growth_rate": "six point eight percent",
            "net_income": "thirteen point four billion dollars",
            "roe": "seventeen point eight percent"
        }
        
        # Test SMAP briefing
        smap_result = service.generate_financial_audio("smap_briefing", company_data)
        if smap_result.get("success"):
            print("✅ SMAP briefing audio generated successfully")
            print(f"   Audio URL: {smap_result.get('audio_url')[:50]}...")
            print(f"   Size: {smap_result.get('size_bytes')} bytes")
        else:
            print(f"❌ SMAP briefing failed: {smap_result.get('error')}")
            
    else:
        print(f"❌ Connection failed: {connection_test.get('error')}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if API key is valid")
        print("   2. Verify internet connection")
        print("   3. Check ElevenLabs account status")
        print("   4. Try with a different voice ID")
    
    print("\n🎉 ElevenLabs Service Test Complete!")

if __name__ == "__main__":
    main()
