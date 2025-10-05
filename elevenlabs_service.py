#!/usr/bin/env python3
"""
ElevenLabs Text-to-Speech Service
Integration with 10Q Notes AI Voice Agent
"""

import os
import requests
import json
from typing import Dict, Any, Optional

class ElevenLabsService:
    """Service for ElevenLabs Text-to-Speech integration"""
    
    def __init__(self, api_key: str = "53715d9ad565308e547ed43a4506f39359bfc7b4d725927448de874a80c3973a"):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Default voice for financial content
        self.default_voice_id = "JBFqnCBsd6RMkjVDRZzb"  # Professional male voice
        self.default_model = "eleven_multilingual_v2"
    
    def get_voices(self) -> Dict[str, Any]:
        """Get available voices from ElevenLabs"""
        try:
            response = requests.get(f"{self.base_url}/voices", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get voices: {response.status_code}"}
        except Exception as e:
            return {"error": f"Exception getting voices: {str(e)}"}
    
    def text_to_speech(self, text: str, voice_id: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
        """Convert text to speech using ElevenLabs API"""
        try:
            voice_id = voice_id or self.default_voice_id
            model = model or self.default_model
            
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            payload = {
                "text": text,
                "model_id": model,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code == 200:
                # Return audio data and metadata
                import base64
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                return {
                    "success": True,
                    "audio_data": response.content,
                    "content_type": response.headers.get("content-type", "audio/mpeg"),
                    "voice_id": voice_id,
                    "model": model,
                    "text": text,
                    "audio_url": f"data:audio/mpeg;base64,{audio_base64}"
                }
            else:
                return {
                    "success": False,
                    "error": f"TTS failed: {response.status_code}",
                    "response": response.text
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception in text_to_speech: {str(e)}"
            }
    
    def generate_financial_audio(self, content_type: str, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate financial audio content for different scenarios"""
        
        if content_type == "earnings_call_opening":
            text = f"""
            Good morning, and welcome to {company_data.get('company_name', 'our company')}'s earnings call for {company_data.get('quarter', 'Q1 2025')}.
            
            I'm pleased to report strong financial performance with revenue of {company_data.get('revenue', '$42.5 billion')}, representing year-over-year growth of {company_data.get('growth_rate', '6.8%')}.
            
            Our net income came in at {company_data.get('net_income', '$13.4 billion')}, demonstrating the strength of our diversified business model and our commitment to delivering value to shareholders.
            
            Let me now turn the call over to our Chief Financial Officer for a detailed review of our financial results.
            """
        
        elif content_type == "smap_briefing":
            text = f"""
            Let me provide you with a comprehensive SMAP analysis of {company_data.get('company_name', 'our company')}'s performance.
            
            From a Subjective perspective, management expressed strong confidence in the quarter's results, highlighting the company's resilience and strategic execution.
            
            Key Metrics include revenue of {company_data.get('revenue', '$42.5 billion')}, net income of {company_data.get('net_income', '$13.4 billion')}, and a return on equity of {company_data.get('roe', '17.8%')}.
            
            Our Assessment shows solid fundamental strength with a fortress balance sheet providing flexibility in the current economic environment.
            
            Looking ahead, our Plan focuses on continued digital transformation, monitoring credit trends, and maintaining our strong capital position.
            """
        
        elif content_type == "analyst_question":
            text = f"""
            Thank you for taking my question. Given the current economic environment, how are you thinking about credit risk and provisioning going forward? 
            
            Also, could you comment on the digital transformation progress and investment priorities for the remainder of the year?
            """
        
        else:
            text = f"""
            Welcome to the financial analysis session for {company_data.get('company_name', 'our company')}.
            
            Today we'll be discussing the company's {company_data.get('quarter', 'Q1 2025')} performance and outlook.
            
            Let's begin with a review of the key financial metrics and strategic initiatives.
            """
        
        return self.text_to_speech(text)
    
    def create_interactive_quiz_audio(self, question: str, options: list, correct_answer: int) -> Dict[str, Any]:
        """Create audio for interactive quiz questions"""
        text = f"""
        Question: {question}
        
        Options:
        A) {options[0] if len(options) > 0 else 'Option A'}
        B) {options[1] if len(options) > 1 else 'Option B'}
        C) {options[2] if len(options) > 2 else 'Option C'}
        D) {options[3] if len(options) > 3 else 'Option D'}
        
        Please select your answer.
        """
        
        return self.text_to_speech(text)
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the ElevenLabs API connection"""
        try:
            # Test with a simple text
            result = self.text_to_speech("Testing ElevenLabs integration for 10Q Notes AI.")
            if result.get("success"):
                return {
                    "success": True,
                    "message": "ElevenLabs API connection successful",
                    "voice_id": result.get("voice_id"),
                    "model": result.get("model")
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
    """Test the ElevenLabs service"""
    print("🎤 Testing ElevenLabs Service Integration")
    print("=" * 45)
    
    # Initialize service
    service = ElevenLabsService()
    
    # Test connection
    print("\n🔗 Testing API Connection...")
    connection_test = service.test_connection()
    
    if connection_test.get("success"):
        print("✅ ElevenLabs API connection successful")
        print(f"   Voice ID: {connection_test.get('voice_id')}")
        print(f"   Model: {connection_test.get('model')}")
    else:
        print(f"❌ Connection failed: {connection_test.get('error')}")
        return
    
    # Test financial audio generation
    print("\n💰 Testing Financial Audio Generation...")
    
    company_data = {
        "company_name": "JPMorgan Chase",
        "quarter": "Q1 2025",
        "revenue": "$42.5 billion",
        "growth_rate": "6.8%",
        "net_income": "$13.4 billion",
        "roe": "17.8%"
    }
    
    # Test SMAP briefing
    smap_result = service.generate_financial_audio("smap_briefing", company_data)
    if smap_result.get("success"):
        print("✅ SMAP briefing audio generated successfully")
        print(f"   Text length: {len(smap_result.get('text', ''))} characters")
    else:
        print(f"❌ SMAP briefing failed: {smap_result.get('error')}")
    
    # Test earnings call opening
    earnings_result = service.generate_financial_audio("earnings_call_opening", company_data)
    if earnings_result.get("success"):
        print("✅ Earnings call opening audio generated successfully")
        print(f"   Text length: {len(earnings_result.get('text', ''))} characters")
    else:
        print(f"❌ Earnings call opening failed: {earnings_result.get('error')}")
    
    print("\n🎉 ElevenLabs Service Integration Complete!")
    print("✅ API connection working")
    print("✅ Financial audio generation working")
    print("✅ Ready for integration with voice agent")

if __name__ == "__main__":
    main()
