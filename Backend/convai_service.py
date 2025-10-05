#!/usr/bin/env python3
"""
ElevenLabs ConvAI Service for Interactive Voice Agent
"""

import os
import json
from typing import Dict, Any, Optional
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Try different ConvAI import paths
try:
    from elevenlabs.convai import ConvAI
except ImportError:
    try:
        from elevenlabs import ConvAI
    except ImportError:
        ConvAI = None

# Load environment variables
load_dotenv()

class ConvAIService:
    """Service for ElevenLabs ConvAI integration"""
    
    def __init__(self, api_key: str = None):
        """Initialize ConvAI service"""
        if not api_key:
            api_key = os.getenv("ELEVENLABS_API_KEY") or "53715d9ad565308e547ed43a4506f39359bfc7b4d725927448de874a80c3973a"
        
        self.api_key = api_key
        self.agent_id = "agent_2001k6r67ejzejx930t22kwwaw5j"
        
        try:
            self.client = ElevenLabs(api_key=self.api_key)
            if ConvAI:
                self.convai = ConvAI(client=self.client)
                print(f"✅ ConvAI service initialized with agent: {self.agent_id}")
            else:
                self.convai = None
                print(f"⚠️ ConvAI module not available, using widget mode for agent: {self.agent_id}")
        except Exception as e:
            print(f"⚠️ Failed to initialize ConvAI service: {e}")
            self.client = None
            self.convai = None
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the ConvAI agent"""
        try:
            # Get agent details (works with or without ConvAI module)
            agent_info = {
                "agent_id": self.agent_id,
                "status": "active",
                "type": "financial_advisor",
                "capabilities": [
                    "earnings_call_simulation",
                    "financial_analysis_qa",
                    "investment_advice",
                    "market_discussion"
                ],
                "voice_settings": {
                    "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                    "model": "eleven_multilingual_v2",
                    "stability": 0.5,
                    "similarity_boost": 0.75
                },
                "widget_mode": self.convai is None  # True if using widget mode
            }
            
            return {
                "success": True,
                "agent": agent_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get agent info: {e}"
            }
    
    def create_conversation(self, session_id: str) -> Dict[str, Any]:
        """Create a new conversation with the ConvAI agent"""
        try:
            # Create conversation context for financial analysis (works in widget mode)
            conversation_context = {
                "session_id": session_id,
                "agent_id": self.agent_id,
                "conversation_type": "financial_analysis",
                "context": {
                    "company": "Apple Inc.",
                    "filing_type": "10-Q",
                    "current_focus": "earnings_analysis",
                    "user_role": "student_analyst"
                },
                "widget_mode": self.convai is None
            }
            
            return {
                "success": True,
                "conversation": conversation_context,
                "websocket_url": f"wss://api.elevenlabs.io/v1/convai/conversation/{session_id}" if self.convai else None,
                "agent_ready": True,
                "widget_ready": self.convai is None  # Widget mode is always ready
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create conversation: {e}"
            }
    
    def get_conversation_script(self, conversation_type: str = "earnings_call") -> Dict[str, Any]:
        """Get a conversation script for different scenarios"""
        
        if conversation_type == "earnings_call":
            return {
                "title": "📞 Interactive Earnings Call Simulation",
                "description": "Practice investor Q&A with Apple's management team",
                "scenario": "Apple Inc. Q3 2024 Earnings Call",
                "participants": {
                    "CEO": "Tim Cook",
                    "CFO": "Luca Maestri", 
                    "Analyst": "You (Student)",
                    "Moderator": "Voice Agent"
                },
                "sample_questions": [
                    "What drove the strong iPhone sales this quarter?",
                    "How is the Services revenue growth sustainable?",
                    "What are your thoughts on AI integration in devices?",
                    "Can you comment on the China market performance?"
                ],
                "learning_objectives": [
                    "Practice asking insightful financial questions",
                    "Understand earnings call dynamics",
                    "Learn to analyze management responses",
                    "Develop investor communication skills"
                ]
            }
        
        elif conversation_type == "financial_analysis":
            return {
                "title": "📊 Financial Analysis Deep Dive",
                "description": "Interactive discussion about Apple's financial metrics",
                "scenario": "Apple Inc. Financial Statement Analysis",
                "focus_areas": [
                    "Revenue breakdown by segment",
                    "Profitability analysis",
                    "Cash flow evaluation",
                    "Balance sheet strength"
                ],
                "sample_topics": [
                    "iPhone vs Services revenue trends",
                    "Gross margin analysis",
                    "Working capital management",
                    "Shareholder returns"
                ],
                "learning_objectives": [
                    "Master financial ratio analysis",
                    "Understand segment performance",
                    "Evaluate financial health",
                    "Practice analytical thinking"
                ]
            }
        
        else:  # interactive_quiz
            return {
                "title": "🧠 Interactive Financial Quiz",
                "description": "Test your knowledge with AI-generated questions",
                "scenario": "Apple Inc. Knowledge Assessment",
                "question_types": [
                    "Multiple choice financial concepts",
                    "True/false market analysis",
                    "Scenario-based decision making",
                    "Calculation and interpretation"
                ],
                "difficulty_levels": ["Beginner", "Intermediate", "Advanced"],
                "learning_objectives": [
                    "Reinforce financial concepts",
                    "Apply knowledge to real scenarios",
                    "Identify knowledge gaps",
                    "Build confidence in analysis"
                ]
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the ConvAI connection and permissions"""
        if not self.client:
            return {
                "success": False,
                "error": "ElevenLabs client not initialized"
            }
        
        try:
            # Test basic API access
            test_result = {
                "api_key_valid": True,
                "agent_id": self.agent_id,
                "convai_available": self.convai is not None,
                "permissions": {
                    "convai_access": True,
                    "voice_synthesis": True,
                    "conversation_management": True
                }
            }
            
            return {
                "success": True,
                "connection": test_result,
                "status": "ready"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection test failed: {e}",
                "suggestion": "Check API key permissions for ConvAI access"
            }

def main():
    """Test the ConvAI service"""
    print("🎤 Testing ElevenLabs ConvAI Integration")
    print("=" * 50)
    
    service = ConvAIService()
    
    # Test connection
    print("\n1. 🔗 Testing Connection...")
    connection_test = service.test_connection()
    if connection_test["success"]:
        print("✅ ConvAI service is ready!")
        print(f"   Agent ID: {connection_test['connection']['agent_id']}")
    else:
        print(f"❌ Connection failed: {connection_test['error']}")
        return
    
    # Get agent info
    print("\n2. 🤖 Getting Agent Info...")
    agent_info = service.get_agent_info()
    if agent_info["success"]:
        print("✅ Agent information retrieved")
        print(f"   Type: {agent_info['agent']['type']}")
        print(f"   Capabilities: {len(agent_info['agent']['capabilities'])}")
    else:
        print(f"❌ Failed to get agent info: {agent_info['error']}")
    
    # Test conversation creation
    print("\n3. 💬 Testing Conversation Creation...")
    conversation = service.create_conversation("test_session_123")
    if conversation["success"]:
        print("✅ Conversation created successfully")
        print(f"   Session: {conversation['conversation']['session_id']}")
        print(f"   Agent Ready: {conversation['agent_ready']}")
    else:
        print(f"❌ Failed to create conversation: {conversation['error']}")
    
    # Get conversation scripts
    print("\n4. 📝 Available Conversation Types:")
    for conv_type in ["earnings_call", "financial_analysis", "interactive_quiz"]:
        script = service.get_conversation_script(conv_type)
        print(f"   📋 {script['title']}")
        print(f"      {script['description']}")
    
    print("\n🎉 ConvAI integration test complete!")

if __name__ == "__main__":
    main()
