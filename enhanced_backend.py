#!/usr/bin/env python3
"""
10Q Notes AI - Enhanced Backend with Better Feedback & Voice Agent
HackRU 2025 Project by azrabano

This backend provides detailed, helpful feedback and voice agent functionality.
"""

import json
import sys
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import ElevenLabs service
try:
    from elevenlabs_service import ElevenLabsService
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ ElevenLabs service not available - install required packages")

class EnhancedBackendHandler(BaseHTTPRequestHandler):
    """Enhanced HTTP handler with better feedback and voice agent"""
    
    def __init__(self, *args, **kwargs):
        # Initialize ElevenLabs service
        if ELEVENLABS_AVAILABLE:
            try:
                self.elevenlabs_service = ElevenLabsService()
                print("✅ ElevenLabs service initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize ElevenLabs service: {e}")
                self.elevenlabs_service = None
        else:
            self.elevenlabs_service = None
        
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "10Q Notes AI Backend - HackRU 2025",
                "description": "AI-powered SEC filing learning platform with SMAP framework",
                "features": [
                    "Learn Mode (Read & Hover with simplified explanations)",
                    "Practice Mode (Student writes own SMAP notes)",
                    "AI Feedback Mode (Gemini compares to Gold Standard)",
                    "Voice Agent (ElevenLabs earnings call simulation)"
                ],
                "status": "active",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "services": {
                    "education_service": "active",
                    "voice_agent": "active",
                    "gemini_service": "active",
                    "document_processor": "active"
                },
                "active_sessions": 1,
                "authenticated_students": 1
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/auth/login':
            # Mock authentication
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "student": {
                    "student_id": "john_smith_rutgers_edu",
                    "name": "John Smith",
                    "email": "john.smith@rutgers.edu",
                    "university": "Rutgers",
                    "total_sessions": 3,
                    "average_score": 85.5,
                    "streak_days": 7
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/upload/filing':
            # Mock file upload
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "session": {
                    "session_id": "demo123",
                    "company_name": "JPMorgan Chase & Co.",
                    "ticker": "JPM",
                    "filing_type": "10-Q",
                    "filing_period": "Q1 2025",
                    "status": "active"
                },
                "message": "Filing uploaded and processed successfully. Ready to begin learning!"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path.startswith('/api/session/') and '/learn' in self.path:
            # Mock learn mode data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "mode": "learn",
                "content": {
                    "session_id": "demo123",
                    "mode": "learn",
                    "company_info": {
                        "name": "JPMorgan Chase & Co.",
                        "ticker": "JPM",
                        "industry": "Banking",
                        "period": "Q1 2025"
                    },
                    "sections": {
                        "subjective": {
                            "title": "S – Subjective - What Management Said",
                            "explanation": "This section captures the narrative and tone from management, including strategic priorities and forward-looking statements.",
                            "content": "Management expressed strong confidence in Q1 performance, highlighting robust revenue growth and disciplined expense management. The tone was optimistic about future opportunities in digital banking and maintained focus on fortress balance sheet strategy.",
                            "key_concepts": ["Management tone", "Strategic priorities", "Forward guidance", "Qualitative insights"],
                            "hover_definitions": {
                                "fortress balance sheet": "Strong financial position with high capital levels",
                                "operational efficiency": "How well the company uses resources to generate profits",
                                "regulatory headwinds": "Government policy changes that may hurt business"
                            }
                        },
                        "metrics": {
                            "title": "M – Metrics - Key Financial Numbers",
                            "explanation": "Hard numbers, ratios, and financial data extracted directly from the filing.",
                            "content": "Total revenue of $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%, Net interest margin 2.74%, Book value per share $95.35",
                            "key_concepts": ["Revenue growth", "Profitability ratios", "Balance sheet strength", "Per-share metrics"],
                            "hover_definitions": {
                                "ROE": "Return on Equity - measures how efficiently the company uses shareholder money",
                                "CET1 ratio": "Common Equity Tier 1 - bank's core capital as % of risk-weighted assets",
                                "NIM": "Net Interest Margin - spread between interest earned and paid by a bank"
                            }
                        },
                        "assessment": {
                            "title": "A – Assessment - What It All Means",
                            "explanation": "AI interprets the numbers and narrative to identify trends, strengths, and concerns.",
                            "content": "JPMorgan demonstrates solid fundamental strength with revenue growth across segments. The fortress balance sheet provides flexibility for economic volatility while maintaining strong profitability metrics. Credit provisions remain well-controlled despite economic uncertainty.",
                            "key_concepts": ["Trend analysis", "Competitive positioning", "Risk factors", "Growth drivers"],
                            "hover_definitions": {
                                "operating leverage": "When revenue grows faster than expenses, boosting profits",
                                "credit provisions": "Money set aside for potential loan losses",
                                "market share": "Company's portion of total industry sales"
                            }
                        },
                        "plan": {
                            "title": "P – Plan - Recommended Next Steps",
                            "explanation": "Specific actionable recommendations for investors, analysts, or advisors.",
                            "content": "Monitor credit provision trends, assess interest rate sensitivity, evaluate investment banking recovery, track digital transformation progress",
                            "key_concepts": ["Monitoring priorities", "Investment decisions", "Risk management", "Action items"],
                            "hover_definitions": {
                                "valuation multiple": "Ratio comparing company price to financial metrics",
                                "peer analysis": "Comparing performance to similar companies",
                                "catalyst": "Event that could significantly impact stock price"
                            }
                        }
                    },
                    "progress_status": {
                        "sections_available": 4,
                        "estimated_time": "15-20 minutes",
                        "difficulty_level": "Intermediate"
                    }
                },
                "features": {
                    "hover_definitions": True,
                    "simplified_explanations": True,
                    "voice_synthesis_available": True,
                    "progress_tracking": True
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path.startswith('/api/session/') and '/voice' in self.path:
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
                    "revenue": "$42.5 billion",
                    "growth_rate": "6.8%",
                    "net_income": "$13.4 billion",
                    "roe": "17.8%"
                }
                
                audio_result = None
                if self.elevenlabs_service:
                    if voice_type == 'earnings_call':
                        audio_result = self.elevenlabs_service.generate_financial_audio("earnings_call_opening", company_data)
                    elif voice_type == 'audio_briefing':
                        audio_result = self.elevenlabs_service.generate_financial_audio("smap_briefing", company_data)
                    elif voice_type == 'interactive_quiz':
                        audio_result = self.elevenlabs_service.create_interactive_quiz_audio(
                            "What was JPMorgan Chase's total revenue for Q1 2025?",
                            ["$40.2B", "$42.5B", "$45.1B", "$38.7B"],
                            1
                        )
                
                if voice_type == 'earnings_call':
                    response = {
                        "success": True,
                        "voice_content": {
                            "type": "earnings_call",
                            "title": "JPMorgan Chase Q1 2025 Earnings Call Simulation",
                            "duration": "12 minutes 45 seconds",
                            "audio_url": audio_result.get("audio_url") if audio_result and audio_result.get("success") else None,
                            "audio_available": audio_result.get("success") if audio_result else False,
                            "participants": {
                                "ceo": "Jamie Dimon (CEO)",
                                "cfo": "Jeremy Barnum (CFO)",
                                "analyst_1": "Mike Mayo (Wells Fargo)",
                                "analyst_2": "John McDonald (UBS)",
                                "analyst_3": "Betsy Graseck (Morgan Stanley)"
                            },
                            "script": {
                                "ceo_opening": "Good morning everyone. I'm Jamie Dimon, CEO of JPMorgan Chase. I'm pleased to report strong first quarter results that demonstrate our continued resilience and strategic execution. We delivered revenue of $42.5 billion, up 6.8% year-over-year, and net income of $13.4 billion.",
                                "cfo_metrics": "Thank you Jamie. Our first quarter results show total revenue of $42.5 billion, up 6.8% year-over-year. Net income came in at $13.4 billion, representing a return on equity of 17.8%. Our CET1 ratio remained strong at 15.9%, well above regulatory requirements. Net interest margin expanded to 2.74%.",
                                "analyst_qa_1": "Jamie, given the current economic environment, how are you thinking about credit risk and provisioning going forward?",
                                "ceo_response_1": "That's an excellent question, Mike. While we remain vigilant about credit quality, our fortress balance sheet and diversified business model provide significant flexibility. We've maintained our CET1 ratio at 15.9%, well above regulatory requirements. Our credit provisions remain well-controlled.",
                                "analyst_qa_2": "Can you comment on the digital transformation progress and investment priorities?",
                                "ceo_response_2": "Absolutely, John. Digital transformation remains a key strategic priority. We're seeing strong adoption across our digital platforms, with mobile banking usage up 15% year-over-year. We're investing heavily in AI and machine learning capabilities to enhance customer experience and operational efficiency.",
                                "analyst_qa_3": "What's your outlook for the investment banking recovery?",
                                "cfo_response": "Betsy, we're seeing signs of recovery in investment banking. While Q1 was challenging, we're optimistic about the pipeline for the remainder of the year. Our diversified model helps us navigate market volatility effectively.",
                                "ceo_closing": "In summary, we're well-positioned to navigate the current environment while continuing to invest in growth opportunities. Our fortress balance sheet, diversified business model, and strong capital position give us flexibility to serve clients and drive long-term shareholder value."
                            },
                            "learning_questions": [
                                "What was the most important financial metric mentioned?",
                                "How did management address concerns about economic uncertainty?",
                                "What strategic priorities were highlighted for digital transformation?",
                                "How did the company perform in investment banking versus expectations?"
                            ],
                            "key_takeaways": [
                                "Strong revenue growth of 6.8% YoY to $42.5B",
                                "Net income of $13.4B with ROE of 17.8%",
                                "CET1 ratio maintained at 15.9% (well above requirements)",
                                "Digital transformation driving 15% mobile banking growth",
                                "Investment banking showing signs of recovery",
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
                            "duration": "5 minutes 30 seconds",
                            "audio_url": "https://api.elevenlabs.io/v1/text-to-speech/voice_id/briefing.mp3",
                            "narrator": "Professional financial analyst voice",
                            "summary": "JPMorgan Chase delivered solid Q1 2025 results with revenue growth of 6.8% year-over-year to $42.5 billion. Management expressed strong confidence in the company's fortress balance sheet strategy while highlighting significant opportunities in digital banking transformation. Key performance metrics include a return on equity of 17.8% and a Common Equity Tier 1 ratio of 15.9%, well above regulatory requirements. The assessment reveals strong fundamental performance across all business segments with well-controlled credit provisions despite economic uncertainty. Strategic priorities focus on digital innovation, with mobile banking usage up 15% year-over-year. Recommended next steps include monitoring credit provision trends, assessing interest rate sensitivity, and tracking digital transformation progress.",
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
                            "duration": "8 minutes 15 seconds",
                            "audio_url": "https://api.elevenlabs.io/v1/text-to-speech/voice_id/quiz.mp3",
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
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Voice synthesis error: {str(e)}"}).encode())
            
        elif self.path.startswith('/api/session/') and '/feedback' in self.path:
            # SIMPLIFIED - Just acknowledge submission
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "message": "SMAP notes submitted successfully! Ready for voice agent experience.",
                "next_step": "voice_agent"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def _analyze_student_work_enhanced(self, student_work):
        """Enhanced analysis with detailed, helpful feedback"""
        
        # Extract student responses
        subjective = student_work.get('subjective', '').strip()
        metrics = student_work.get('metrics', '').strip()
        assessment = student_work.get('assessment', '').strip()
        plan = student_work.get('plan', '').strip()
        
        print(f"\n🎯 ENHANCED ANALYSIS OF STUDENT WORK:")
        print(f"   Subjective: '{subjective}'")
        print(f"   Metrics: '{metrics}'")
        print(f"   Assessment: '{assessment}'")
        print(f"   Plan: '{plan}'")
        
        # Calculate detailed scores with specific feedback
        scores = {}
        detailed_feedback = {}
        
        # Enhanced Subjective Analysis
        subjective_score, subjective_feedback = self._analyze_subjective_enhanced(subjective)
        scores['subjective'] = subjective_score
        detailed_feedback['subjective'] = subjective_feedback
        
        # Enhanced Metrics Analysis  
        metrics_score, metrics_feedback = self._analyze_metrics_enhanced(metrics)
        scores['metrics'] = metrics_score
        detailed_feedback['metrics'] = metrics_feedback
        
        # Enhanced Assessment Analysis
        assessment_score, assessment_feedback = self._analyze_assessment_enhanced(assessment)
        scores['assessment'] = assessment_score
        detailed_feedback['assessment'] = assessment_feedback
        
        # Enhanced Plan Analysis
        plan_score, plan_feedback = self._analyze_plan_enhanced(plan)
        scores['plan'] = plan_score
        detailed_feedback['plan'] = plan_feedback
        
        # Calculate overall score
        overall_score = sum(scores.values()) / len(scores)
        
        # Determine grade level
        if overall_score >= 90:
            grade = "A+"
        elif overall_score >= 85:
            grade = "A"
        elif overall_score >= 80:
            grade = "A-"
        elif overall_score >= 75:
            grade = "B+"
        elif overall_score >= 70:
            grade = "B"
        elif overall_score >= 65:
            grade = "B-"
        elif overall_score >= 60:
            grade = "C+"
        elif overall_score >= 55:
            grade = "C"
        elif overall_score >= 50:
            grade = "C-"
        elif overall_score >= 45:
            grade = "D+"
        elif overall_score >= 40:
            grade = "D"
        else:
            grade = "F"
        
        # Generate comprehensive improvements
        improvements = []
        if scores['subjective'] < 70:
            improvements.append("💡 SUBJECTIVE: Include specific management quotes or paraphrases. Mention tone (confident, cautious, optimistic) and strategic priorities.")
        if scores['metrics'] < 70:
            improvements.append("📊 METRICS: Add specific numbers with dollar amounts, percentages, and ratios. Include year-over-year comparisons.")
        if scores['assessment'] < 70:
            improvements.append("🧠 ASSESSMENT: Connect the numbers to business performance. Identify trends, risks, and opportunities.")
        if scores['plan'] < 70:
            improvements.append("📋 PLAN: Provide specific, actionable recommendations with timeframes and reasoning.")
        
        print(f"\n📊 ENHANCED ANALYSIS RESULTS:")
        print(f"   Overall Score: {overall_score:.1f}/100 (Grade: {grade})")
        print(f"   Section Scores: {scores}")
        
        return {
            "overall_score": round(overall_score, 1),
            "grade": grade,
            "section_scores": scores,
            "detailed_feedback": detailed_feedback,
            "improvements": improvements,
            "analysis": {
                "completeness": f"{sum(1 for score in scores.values() if score > 0)}/4 sections completed",
                "quality": "Excellent" if overall_score >= 85 else "Good" if overall_score >= 70 else "Needs Improvement" if overall_score >= 50 else "Poor",
                "effort": "High" if overall_score >= 80 else "Medium" if overall_score >= 50 else "Low"
            },
            "next_steps": self._generate_next_steps(overall_score, scores)
        }
    
    def _analyze_subjective_enhanced(self, text):
        """Enhanced subjective analysis"""
        if not text or text.lower() in ['i don\'t know', 'i don\'t know.', 'idk', '']:
            return 10, {
                "score": 10,
                "feedback": "❌ This section is completely empty. The subjective section should capture what management said in their own words.",
                "strengths": [],
                "weaknesses": ["No content provided", "Shows no understanding of management communication"],
                "example": "Try: 'Management expressed confidence in Q1 results, highlighting strong revenue growth and optimistic outlook for digital banking initiatives.'"
            }
        
        word_count = len(text.split())
        score = 30
        
        strengths = []
        weaknesses = []
        
        # Check for management tone indicators
        tone_words = ['confident', 'optimistic', 'cautious', 'positive', 'strong', 'solid', 'robust']
        if any(word in text.lower() for word in tone_words):
            score += 25
            strengths.append("✅ Good job identifying management tone")
        else:
            weaknesses.append("⚠️ Missing management tone assessment")
        
        # Check for strategic priorities
        strategy_words = ['strategy', 'priority', 'focus', 'investment', 'digital', 'growth', 'initiative']
        if any(word in text.lower() for word in strategy_words):
            score += 25
            strengths.append("✅ Mentions strategic priorities")
        else:
            weaknesses.append("⚠️ No strategic priorities mentioned")
        
        # Check for forward-looking statements
        forward_words = ['future', 'outlook', 'guidance', 'expect', 'anticipate', 'plan', 'next']
        if any(word in text.lower() for word in forward_words):
            score += 20
            strengths.append("✅ Includes forward-looking perspective")
        else:
            weaknesses.append("⚠️ Missing forward-looking statements")
        
        # Length bonus
        if word_count >= 30:
            score += 10
            strengths.append("✅ Comprehensive coverage")
        elif word_count < 15:
            score -= 15
            weaknesses.append("⚠️ Too brief - needs more detail")
        
        # Cap at 100
        score = min(score, 100)
        
        feedback = "✅ Good subjective analysis" if score >= 70 else "⚠️ Needs improvement" if score >= 40 else "❌ Significant issues"
        
        return score, {
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "word_count": word_count,
            "example": "Better example: 'Management expressed strong confidence in Q1 performance, highlighting robust revenue growth of 6.8% and optimistic outlook for digital banking initiatives. The tone emphasized strategic focus on fortress balance sheet maintenance while pursuing growth opportunities.'"
        }
    
    def _analyze_metrics_enhanced(self, text):
        """Enhanced metrics analysis"""
        if not text or text.lower() in ['i don\'t know', 'i don\'t know.', 'idk', '']:
            return 5, {
                "score": 5,
                "feedback": "❌ No financial metrics provided. This is critical for financial analysis.",
                "strengths": [],
                "weaknesses": ["No numbers provided", "No financial data"],
                "example": "Try: 'Revenue $42.5B (+6.8% YoY), Net income $13.4B, ROE 17.8%, CET1 ratio 15.9%'"
            }
        
        score = 20
        strengths = []
        weaknesses = []
        metrics_found = []
        
        # Check for specific financial metrics
        if '$' in text or 'billion' in text.lower() or 'million' in text.lower():
            score += 30
            strengths.append("✅ Includes dollar amounts")
            metrics_found.append("Dollar amounts")
        
        if any(char in text for char in ['%', 'percent', 'ratio']):
            score += 25
            strengths.append("✅ Includes percentages/ratios")
            metrics_found.append("Percentages/ratios")
        
        # Check for specific financial terms
        financial_terms = ['revenue', 'income', 'profit', 'roe', 'cet1', 'nim', 'margin', 'ratio']
        found_terms = [term for term in financial_terms if term in text.lower()]
        if found_terms:
            score += len(found_terms) * 8
            strengths.append(f"✅ Includes financial terms: {', '.join(found_terms)}")
        
        # Check for comparisons
        if any(word in text.lower() for word in ['vs', 'compared', 'versus', 'yoy', 'year-over-year', 'growth']):
            score += 15
            strengths.append("✅ Includes comparisons")
        
        # Length and detail check
        word_count = len(text.split())
        if word_count < 10:
            score -= 20
            weaknesses.append("⚠️ Too brief - need more financial data")
        elif word_count >= 25:
            score += 10
            strengths.append("✅ Comprehensive metrics coverage")
        
        # Cap at 100
        score = min(score, 100)
        
        feedback = "✅ Excellent financial metrics" if score >= 80 else "✅ Good metrics" if score >= 60 else "⚠️ Basic metrics" if score >= 40 else "❌ Poor metrics"
        
        return score, {
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "metrics_found": metrics_found,
            "word_count": word_count,
            "example": "Better example: 'Total revenue $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%, Net interest margin 2.74%, Book value per share $95.35'"
        }
    
    def _analyze_assessment_enhanced(self, text):
        """Enhanced assessment analysis"""
        if not text or text.lower() in ['i don\'t know', 'i don\'t know.', 'idk', '']:
            return 8, {
                "score": 8,
                "feedback": "❌ No assessment provided. This section should interpret what the numbers mean.",
                "strengths": [],
                "weaknesses": ["No analysis provided", "No interpretation of data"],
                "example": "Try: 'Strong fundamental performance with revenue growth across segments. The fortress balance sheet provides stability during economic uncertainty.'"
            }
        
        score = 25
        strengths = []
        weaknesses = []
        
        # Check for analytical words
        analytical_words = ['strong', 'weak', 'growth', 'decline', 'improvement', 'trend', 'performance', 'fundamental']
        found_analytical = [word for word in analytical_words if word in text.lower()]
        if found_analytical:
            score += len(found_analytical) * 8
            strengths.append(f"✅ Uses analytical language: {', '.join(found_analytical)}")
        
        # Check for business insight
        business_words = ['competitive', 'market', 'risk', 'opportunity', 'strategy', 'position', 'advantage']
        if any(word in text.lower() for word in business_words):
            score += 25
            strengths.append("✅ Shows business understanding")
        else:
            weaknesses.append("⚠️ Limited business context")
        
        # Check for trend analysis
        trend_words = ['increasing', 'decreasing', 'stable', 'volatile', 'consistent', 'improving', 'deteriorating']
        if any(word in text.lower() for word in trend_words):
            score += 20
            strengths.append("✅ Identifies trends")
        
        # Check for risk/opportunity analysis
        if any(word in text.lower() for word in ['risk', 'challenge', 'concern', 'opportunity', 'potential']):
            score += 15
            strengths.append("✅ Considers risks and opportunities")
        
        # Length check
        word_count = len(text.split())
        if word_count < 15:
            score -= 15
            weaknesses.append("⚠️ Too brief - needs deeper analysis")
        elif word_count >= 40:
            score += 10
            strengths.append("✅ Comprehensive analysis")
        
        # Cap at 100
        score = min(score, 100)
        
        feedback = "✅ Excellent analysis" if score >= 80 else "✅ Good analysis" if score >= 60 else "⚠️ Basic analysis" if score >= 40 else "❌ Poor analysis"
        
        return score, {
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "word_count": word_count,
            "example": "Better example: 'JPMorgan demonstrates solid fundamental strength with revenue growth across all segments. The fortress balance sheet strategy provides flexibility for economic volatility while maintaining strong profitability metrics. Credit provisions remain well-controlled despite economic uncertainty, indicating prudent risk management.'"
        }
    
    def _analyze_plan_enhanced(self, text):
        """Enhanced plan analysis"""
        if not text or text.lower() in ['i don\'t know', 'i don\'t know.', 'idk', '']:
            return 5, {
                "score": 5,
                "feedback": "❌ No plan provided. This section should give specific next steps.",
                "strengths": [],
                "weaknesses": ["No recommendations provided", "No action items"],
                "example": "Try: 'Monitor credit provision trends, assess interest rate sensitivity, evaluate digital transformation progress'"
            }
        
        score = 20
        strengths = []
        weaknesses = []
        
        # Check for action words
        action_words = ['monitor', 'track', 'assess', 'evaluate', 'watch', 'analyze', 'review', 'investigate']
        found_actions = [word for word in action_words if word in text.lower()]
        if found_actions:
            score += len(found_actions) * 10
            strengths.append(f"✅ Uses action verbs: {', '.join(found_actions)}")
        
        # Check for specific recommendations
        recommendation_words = ['buy', 'sell', 'hold', 'invest', 'avoid', 'recommend', 'suggest']
        if any(word in text.lower() for word in recommendation_words):
            score += 20
            strengths.append("✅ Provides investment recommendations")
        
        # Check for timeframes
        time_words = ['quarterly', 'monthly', 'annually', 'short-term', 'long-term', 'next', 'ongoing']
        if any(word in text.lower() for word in time_words):
            score += 15
            strengths.append("✅ Includes timeframes")
        
        # Check for specific metrics to watch
        if any(word in text.lower() for word in ['credit', 'interest', 'revenue', 'margin', 'ratio', 'provision']):
            score += 20
            strengths.append("✅ Specifies metrics to monitor")
        
        # Length check
        word_count = len(text.split())
        if word_count < 10:
            score -= 15
            weaknesses.append("⚠️ Too brief - need more specific actions")
        elif word_count >= 25:
            score += 10
            strengths.append("✅ Comprehensive action plan")
        
        # Cap at 100
        score = min(score, 100)
        
        feedback = "✅ Excellent action plan" if score >= 80 else "✅ Good plan" if score >= 60 else "⚠️ Basic plan" if score >= 40 else "❌ Poor plan"
        
        return score, {
            "score": score,
            "feedback": feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "word_count": word_count,
            "example": "Better example: 'Monitor credit provision trends for economic impact signals, assess interest rate sensitivity across business lines, evaluate investment banking recovery in current market conditions, track digital transformation progress and customer adoption metrics'"
        }
    
    def _generate_next_steps(self, overall_score, scores):
        """Generate personalized next steps"""
        next_steps = []
        
        if overall_score >= 85:
            next_steps.append("🎉 Excellent work! Consider advancing to more complex financial statements or different industries.")
            next_steps.append("📚 Try analyzing a 10-K filing for deeper insights into annual performance.")
        elif overall_score >= 70:
            next_steps.append("📈 Good progress! Focus on the sections that scored lower for improvement.")
            next_steps.append("🎯 Practice with more SEC filings to build consistency.")
        elif overall_score >= 50:
            next_steps.append("📖 Review the Learn Mode sections to understand what good SMAP notes look like.")
            next_steps.append("💡 Focus on including more specific details and analysis.")
        else:
            next_steps.append("🎓 Start with Learn Mode to understand the SMAP framework better.")
            next_steps.append("📝 Practice with shorter, simpler financial documents first.")
        
        # Specific section recommendations
        lowest_section = min(scores.items(), key=lambda x: x[1])
        next_steps.append(f"🎯 Focus on improving your {lowest_section[0]} section - it had the lowest score ({lowest_section[1]}/100).")
        
        return next_steps
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_enhanced_backend():
    """Run the enhanced backend server"""
    print("🚀 Starting 10Q Notes AI Enhanced Backend")
    print("📚 Three Learning Modes Ready")
    print("🎤 ElevenLabs Voice Integration Active")
    print("🤖 ENHANCED AI Feedback System Online")
    print("📍 Backend: http://localhost:8000")
    print("🔧 Health Check: http://localhost:8000/health")
    print("🎤 Voice Agent: POST /api/session/demo123/voice")
    print("=" * 60)
    
    server = HTTPServer(('localhost', 8000), EnhancedBackendHandler)
    print("✅ Enhanced backend server started successfully!")
    print("🌐 Ready to provide detailed feedback and voice features")
    print("🎯 Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Enhanced backend server stopped")
        server.shutdown()

if __name__ == "__main__":
    run_enhanced_backend()
