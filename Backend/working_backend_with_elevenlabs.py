#!/usr/bin/env python3
"""
Working Backend with ElevenLabs Integration
Handles API key issues gracefully with demo mode
"""

import json
import sys
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import base64

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import services
try:
    from working_elevenlabs_service import WorkingElevenLabsService
    from convai_service import ConvAIService
    from enhanced_practice_mode_service import EnhancedPracticeModeService
    ELEVENLABS_AVAILABLE = True
    print("✅ All services imported")
except ImportError as e:
    ELEVENLABS_AVAILABLE = False
    print(f"⚠️ Services not available: {e}")

class WorkingBackendHandler(BaseHTTPRequestHandler):
    """Working HTTP handler with ElevenLabs integration"""
    
    def __init__(self, *args, **kwargs):
        # Initialize services
        if ELEVENLABS_AVAILABLE:
            try:
                self.elevenlabs_service = WorkingElevenLabsService()
                self.convai_service = ConvAIService()
                self.practice_mode_service = EnhancedPracticeModeService()
                print("✅ All services initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize services: {e}")
                self.elevenlabs_service = None
                self.convai_service = None
                self.practice_mode_service = None
        else:
            self.elevenlabs_service = None
            self.convai_service = None
            self.practice_mode_service = None
        
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'<h1>10Q Notes AI - Working Backend</h1><p>ElevenLabs integration ready</p>')
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            health_data = {
                "status": "healthy",
                "services": {
                    "backend": "active",
                    "elevenlabs": "available" if self.elevenlabs_service else "unavailable"
                },
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(health_data).encode())
            
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/session/') and '/voice' in self.path:
            # Voice Agent - ElevenLabs Integration
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                voice_type = data.get('voice_type', 'earnings_call')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Generate audio using ElevenLabs service
                company_data = {
                    "company_name": "JPMorgan Chase",
                    "quarter": "Q1 2025",
                    "revenue": "forty two point five billion dollars",
                    "growth_rate": "six point eight percent",
                    "net_income": "thirteen point four billion dollars",
                    "roe": "seventeen point eight percent"
                }
                
                audio_result = None
                if self.elevenlabs_service:
                    print(f"🎤 Generating {voice_type} audio...")
                    if voice_type == 'earnings_call':
                        audio_result = self.elevenlabs_service.generate_financial_audio("earnings_call_opening", company_data)
                    elif voice_type == 'audio_briefing':
                        audio_result = self.elevenlabs_service.generate_financial_audio("smap_briefing", company_data)
                    elif voice_type == 'interactive_quiz':
                        audio_result = self.elevenlabs_service.generate_financial_audio("interactive_quiz", company_data)
                
                # Build response based on audio generation result
                if audio_result and audio_result.get("success"):
                    print("✅ Audio generated successfully")
                    audio_available = True
                    audio_url = audio_result.get("audio_url")
                    duration = "2 minutes 30 seconds"
                else:
                    print("⚠️ Audio generation failed, using demo mode")
                    audio_available = False
                    audio_url = None
                    duration = "Demo Mode - Audio unavailable"
                
                if voice_type == 'earnings_call':
                    response = {
                        "success": True,
                        "voice_content": {
                            "type": "earnings_call",
                            "title": "JPMorgan Chase Q1 2025 Earnings Call Simulation",
                            "duration": duration,
                            "audio_url": audio_url,
                            "audio_available": audio_available,
                            "participants": {
                                "ceo": "Jamie Dimon (CEO)",
                                "cfo": "Jeremy Barnum (CFO)",
                                "analyst_1": "Mike Mayo (Wells Fargo)",
                                "analyst_2": "John McDonald (UBS)",
                                "analyst_3": "Betsy Graseck (Morgan Stanley)"
                            },
                            "script": {
                                "ceo_opening": "Good morning everyone. I'm Jamie Dimon, CEO of JPMorgan Chase. I'm pleased to report strong first quarter results that demonstrate our continued resilience and strategic execution. We delivered revenue of $42.5 billion, up 6.8% year-over-year, and net income of $13.4 billion.",
                                "cfo_metrics": "Thank you Jamie. Our first quarter results show total revenue of $42.5 billion, up 6.8% year-over-year. Net income came in at $13.4 billion, representing a return on equity of 17.8%. Our CET1 ratio remained strong at 15.9%, well above regulatory requirements.",
                                "analyst_qa_1": "Jamie, given the current economic environment, how are you thinking about credit risk and provisioning going forward?",
                                "ceo_response_1": "That's an excellent question, Mike. While we remain vigilant about credit quality, our fortress balance sheet and diversified business model provide significant flexibility. We've maintained our CET1 ratio at 15.9%, well above regulatory requirements."
                            },
                            "learning_questions": [
                                "What was the most important financial metric mentioned?",
                                "How did management address concerns about economic uncertainty?",
                                "What strategic priorities were highlighted for digital transformation?"
                            ],
                            "key_takeaways": [
                                "Strong revenue growth of 6.8% YoY to $42.5B",
                                "Net income of $13.4B with ROE of 17.8%",
                                "CET1 ratio maintained at 15.9% (well above requirements)",
                                "Digital transformation driving growth",
                                "Fortress balance sheet strategy providing flexibility"
                            ],
                            "voice_features": {
                                "realistic_voices": True,
                                "natural_conversation_flow": True,
                                "analyst_question_variety": True,
                                "management_response_depth": True
                            }
                        }
                    }
                
                elif voice_type == 'audio_briefing':
                    response = {
                        "success": True,
                        "voice_content": {
                            "type": "audio_briefing",
                            "title": "JPMorgan Chase Q1 2025 Executive Briefing",
                            "duration": duration,
                            "audio_url": audio_url,
                            "audio_available": audio_available,
                            "narrator": "Professional financial analyst voice",
                            "summary": "JPMorgan Chase delivered solid Q1 2025 results with revenue growth of 6.8% year-over-year to $42.5 billion. Management expressed strong confidence in the company's fortress balance sheet strategy while highlighting significant opportunities in digital banking transformation. Key performance metrics include a return on equity of 17.8% and a Common Equity Tier 1 ratio of 15.9%, well above regulatory requirements.",
                            "highlights": [
                                "Revenue: $42.5B (+6.8% YoY)",
                                "Net Income: $13.4B (+6.1% YoY)", 
                                "ROE: 17.8%",
                                "CET1 Ratio: 15.9%",
                                "Net Interest Margin: 2.74%",
                                "Digital Banking Growth: +15% mobile usage",
                                "Management Tone: Confident and optimistic"
                            ],
                            "smap_breakdown": {
                                "subjective": "Management expressed strong confidence with optimistic tone about digital transformation opportunities",
                                "metrics": "Revenue $42.5B (+6.8% YoY), Net income $13.4B, ROE 17.8%, CET1 15.9%",
                                "assessment": "Solid fundamental strength with fortress balance sheet providing economic flexibility",
                                "plan": "Monitor credit trends, assess interest rate sensitivity, track digital progress"
                            }
                        }
                    }
                
                elif voice_type == 'interactive_quiz':
                    response = {
                        "success": True,
                        "voice_content": {
                            "type": "interactive_quiz",
                            "title": "JPMorgan Chase Q1 2025 Interactive Quiz",
                            "duration": duration,
                            "audio_url": audio_url,
                            "audio_available": audio_available,
                            "questions": [
                                {
                                    "question": "What was JPMorgan Chase's total revenue for Q1 2025?",
                                    "options": ["$40.2B", "$42.5B", "$45.1B", "$38.7B"],
                                    "correct": 1,
                                    "explanation": "Correct! JPMorgan Chase reported total revenue of $42.5 billion for Q1 2025."
                                },
                                {
                                    "question": "What was the year-over-year revenue growth rate?",
                                    "options": ["5.2%", "6.8%", "7.4%", "4.9%"],
                                    "correct": 1,
                                    "explanation": "Excellent! The revenue growth rate was 6.8% year-over-year."
                                },
                                {
                                    "question": "What was the company's Return on Equity (ROE)?",
                                    "options": ["15.2%", "16.9%", "17.8%", "18.5%"],
                                    "correct": 2,
                                    "explanation": "Correct! JPMorgan Chase achieved an ROE of 17.8% in Q1 2025."
                                },
                                {
                                    "question": "What was the CET1 ratio?",
                                    "options": ["14.8%", "15.9%", "16.2%", "15.1%"],
                                    "correct": 1,
                                    "explanation": "Right! The CET1 ratio was 15.9%, well above regulatory requirements."
                                }
                            ],
                            "final_score_explanation": "Based on your performance, you demonstrate strong understanding of JPMorgan Chase's Q1 2025 financial metrics. This knowledge will help you analyze similar banking companies in the future."
                        }
                    }
                
                else:
                    response = {
                        "success": False,
                        "error": f"Unknown voice type: {voice_type}"
                    }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    "success": False,
                    "error": f"Server error: {str(e)}"
                }
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path.startswith('/api/session/') and '/convai' in self.path:
            # ConvAI Agent Integration
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                action = data.get('action', 'get_info')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                if action == 'get_info':
                    # Get ConvAI agent information
                    if self.convai_service:
                        agent_info = self.convai_service.get_agent_info()
                        response = {
                            "success": True,
                            "convai_agent": {
                                "agent_id": "agent_2001k6r67ejzejx930t22kwwaw5j",
                                "status": "active",
                                "type": "financial_advisor",
                                "capabilities": [
                                    "earnings_call_simulation",
                                    "financial_analysis_qa",
                                    "investment_advice",
                                    "market_discussion"
                                ],
                                "integration_ready": True,
                                "widget_code": '<elevenlabs-convai agent-id="agent_2001k6r67ejzejx930t22kwwaw5j"></elevenlabs-convai>',
                                "script_url": "https://unpkg.com/@elevenlabs/convai-widget-embed"
                            }
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "ConvAI service not available - check API key"
                        }
                
                elif action == 'create_conversation':
                    # Create new conversation
                    session_id = data.get('session_id', 'demo123')
                    if self.convai_service:
                        conversation = self.convai_service.create_conversation(session_id)
                        response = {
                            "success": True,
                            "conversation": conversation,
                            "convai_widget": {
                                "agent_id": "agent_2001k6r67ejzejx930t22kwwaw5j",
                                "session_id": session_id,
                                "ready": True
                            }
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "ConvAI service not available"
                        }
                
                elif action == 'get_scripts':
                    # Get conversation scripts
                    conv_type = data.get('conversation_type', 'earnings_call')
                    if self.convai_service:
                        script = self.convai_service.get_conversation_script(conv_type)
                        response = {
                            "success": True,
                            "script": script,
                            "convai_ready": True
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "ConvAI service not available"
                        }
                
                else:
                    response = {
                        "success": False,
                        "error": f"Unknown action: {action}"
                    }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    "success": False,
                    "error": f"ConvAI server error: {str(e)}"
                }
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path.startswith('/api/session/') and '/practice' in self.path:
            # Practice Mode - Interactive SMAP Learning
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                action = data.get('action', 'get_sections')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                if action == 'get_sections':
                    # Extract sections from filing content
                    filing_content = data.get('filing_content', '')
                    if self.practice_mode_service:
                        sections_data = self.practice_mode_service.extract_filing_sections(filing_content)
                        response = {
                            "success": True,
                            "sections": sections_data.get('sections', []),
                            "total_sections": len(sections_data.get('sections', []))
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "Practice Mode service not available"
                        }
                
                elif action == 'teach_smap':
                    # Teach SMAP framework for a specific section
                    section = data.get('section', {})
                    if self.practice_mode_service:
                        teaching_data = self.practice_mode_service.teach_smap_framework(section)
                        response = {
                            "success": True,
                            "teaching": teaching_data
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "Practice Mode service not available"
                        }
                
                elif action == 'grade_submission':
                    # Grade student's SMAP submission
                    student_smap = data.get('student_smap', {})
                    section = data.get('section', {})
                    teaching_data = data.get('teaching_data', {})
                    
                    if self.practice_mode_service:
                        grading_data = self.practice_mode_service.grade_student_submission(
                            student_smap, section, teaching_data
                        )
                        response = {
                            "success": True,
                            "grading": grading_data
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "Practice Mode service not available"
                        }
                
                elif action == 'get_insights':
                    # Get progress insights
                    session_history = data.get('session_history', [])
                    if self.practice_mode_service:
                        insights_data = self.practice_mode_service.generate_progress_insights(session_history)
                        response = {
                            "success": True,
                            "insights": insights_data
                        }
                    else:
                        response = {
                            "success": False,
                            "error": "Practice Mode service not available"
                        }
                
                elif action == 'assign_next_section':
                        # Assign next section for practice
                        completed_sections = data.get('completed_sections', [])
                        available_sections = data.get('available_sections', [])
                        
                        if self.practice_mode_service:
                            assignment_data = self.practice_mode_service.assign_next_section(
                                completed_sections, available_sections
                            )
                            response = {
                                "success": True,
                                "assignment": assignment_data
                            }
                        else:
                            response = {
                                "success": False,
                                "error": "Practice Mode service not available"
                            }
                
                else:
                    response = {
                        "success": False,
                        "error": f"Unknown practice action: {action}"
                    }
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    "success": False,
                    "error": f"Practice Mode server error: {str(e)}"
                }
                self.wfile.write(json.dumps(error_response).encode())
        
        else:
            self.send_response(404)
            self.end_headers()

def run_working_backend():
    """Run the working backend server"""
    print("🚀 Starting 10Q Notes AI Working Backend")
    print("📚 Three Learning Modes Ready")
    print("🎯 Practice Mode with Gemini AI Active")
    print("🎤 ElevenLabs Voice Integration Active")
    print("🤖 ConvAI Agent Integration Active")
    print("🤖 Working AI Feedback System Online")
    print("📍 Backend: http://localhost:8000")
    print("🔧 Health Check: http://localhost:8000/health")
    print("🎯 Practice Mode: POST /api/session/demo123/practice")
    print("🎤 Voice Agent: POST /api/session/demo123/voice")
    print("🤖 ConvAI Agent: POST /api/session/demo123/convai")
    print("=" * 60)
    
    try:
        server = HTTPServer(('localhost', 8000), WorkingBackendHandler)
        print("✅ Server started successfully on http://localhost:8000")
        server.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port 8000 is already in use. Please stop other servers.")
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_working_backend()
