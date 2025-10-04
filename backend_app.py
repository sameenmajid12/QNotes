"""
10Q Notes AI - FastAPI Backend Application
HackRU 2025 Project by azrabano

Complete backend implementation with three main learning features:
1. Learn Mode (Read & Hover) - Students see extracted sections + simplified explanations
2. Practice Mode (Student Writes SMAP) - Students fill in their own S, M, A, P boxes
3. AI Feedback Mode - Gemini compares student notes to Gold Standard

Integrates all existing services: EducationService, VoiceAgentService, GeminiService
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uuid
import io
import json
from datetime import datetime

# Import our existing services
from education_service import EducationService, StudentProfile, LearningSession
from voice_agent_service import VoiceAgentService
from document_processor import DocumentProcessor
from enhanced_gemini_service import EnhancedGeminiService
from gemini_service import GeminiService

# Pydantic models for API requests/responses
class StudentAuth(BaseModel):
    email: str = Field(..., description="Student .edu email address")
    name: Optional[str] = Field(None, description="Student name")

class StartSessionRequest(BaseModel):
    student_id: str
    company_name: Optional[str] = None
    ticker: Optional[str] = None
    filing_type: str = "10-Q"
    filing_period: Optional[str] = None

class StudentSMAPSubmission(BaseModel):
    session_id: str
    subjective: str = Field(..., description="Student's subjective analysis")
    metrics: str = Field(..., description="Student's metrics analysis") 
    assessment: str = Field(..., description="Student's assessment")
    plan: str = Field(..., description="Student's plan/recommendations")

class VoiceGenerationRequest(BaseModel):
    session_id: str
    text: Optional[str] = None
    voice_type: str = "management"  # management or analyst

# Initialize FastAPI app
app = FastAPI(
    title="10Q Notes AI Backend",
    description="HackRU 2025 - AI-powered SEC filing learning platform with SMAP framework",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
education_service = EducationService()
voice_agent = VoiceAgentService()
document_processor = DocumentProcessor()

# In-memory storage for demo (production would use database)
active_sessions: Dict[str, LearningSession] = {}
student_data: Dict[str, StudentProfile] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize backend services on startup"""
    print("🚀 10Q Notes AI Backend Starting Up")
    print("📚 Three Learning Modes: Learn, Practice, Feedback")
    print("🎤 ElevenLabs Voice Integration Ready")
    print("🤖 Gemini AI Analysis Engine Active")
    print("=" * 60)

# =============================================================================
# AUTHENTICATION & SESSION MANAGEMENT
# =============================================================================

@app.post("/api/auth/login")
async def authenticate_student(auth_data: StudentAuth):
    """Authenticate student with .edu email"""
    try:
        student = education_service.authenticate_student(auth_data.email, auth_data.name)
        student_data[student.student_id] = student
        
        return {
            "success": True,
            "student": {
                "student_id": student.student_id,
                "name": student.name,
                "email": student.email,
                "university": student.university,
                "total_sessions": student.total_sessions,
                "average_score": student.total_score,
                "streak_days": student.streak_days
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

@app.get("/api/student/{student_id}/dashboard")
async def get_student_dashboard(student_id: str):
    """Get student progress dashboard"""
    try:
        if student_id not in student_data:
            raise HTTPException(status_code=404, detail="Student not found")
        
        dashboard = education_service.get_student_dashboard(student_id)
        return {"success": True, "dashboard": dashboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

# =============================================================================
# FILE UPLOAD & DOCUMENT PROCESSING
# =============================================================================

@app.post("/api/upload/filing")
async def upload_sec_filing(
    file: UploadFile = File(...),
    student_id: str = Form(...),
    company_name: Optional[str] = Form(None),
    ticker: Optional[str] = Form(None),
    filing_type: str = Form("10-Q"),
    filing_period: Optional[str] = Form(None)
):
    """Upload and process SEC filing (10Q/10K) to start learning session"""
    try:
        if student_id not in student_data:
            raise HTTPException(status_code=404, detail="Student not authenticated")
        
        # Read file content
        content = await file.read()
        
        # Process based on file type
        if file.filename.endswith('.pdf'):
            # Save temporarily for PDF processing
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(content)
                tmp_file.flush()
                
                # Extract text from PDF
                filing_text = document_processor.extract_text_from_pdf(tmp_file.name)
        else:
            # Assume text file
            filing_text = content.decode('utf-8')
        
        if not filing_text:
            raise HTTPException(status_code=400, detail="No text could be extracted from file")
        
        # Auto-detect company name and ticker if not provided
        if not company_name or not ticker:
            # Simple extraction from filing text (enhance as needed)
            lines = filing_text[:2000].split('\n')
            for line in lines:
                if any(keyword in line.upper() for keyword in ['COMPANY NAME', 'FORM 10-Q', 'FORM 10-K']):
                    # Extract company info (simplified logic)
                    if not company_name:
                        company_name = line.strip()[:50]
                    break
            
            if not company_name:
                company_name = "Unknown Company"
            if not ticker:
                ticker = "UNK"
        
        # Start learning session
        student = student_data[student_id]
        session = education_service.start_learning_session(
            student=student,
            company_name=company_name,
            ticker=ticker,
            filing_text=filing_text,
            filing_type=filing_type,
            filing_period=filing_period or "Recent Period"
        )
        
        # Store session
        active_sessions[session.session_id] = session
        
        return {
            "success": True,
            "session": {
                "session_id": session.session_id,
                "company_name": session.company_name,
                "ticker": session.ticker,
                "filing_type": session.filing_type,
                "filing_period": session.filing_period,
                "status": session.status
            },
            "message": "Filing uploaded and processed successfully. Ready to begin learning!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")

@app.post("/api/upload/text")
async def upload_text_filing(request: StartSessionRequest, filing_text: str = Form(...)):
    """Upload SEC filing as raw text"""
    try:
        if request.student_id not in student_data:
            raise HTTPException(status_code=404, detail="Student not authenticated")
        
        student = student_data[request.student_id]
        
        # Auto-detect company info if not provided
        company_name = request.company_name or "Unknown Company"
        ticker = request.ticker or "UNK"
        
        session = education_service.start_learning_session(
            student=student,
            company_name=company_name,
            ticker=ticker,
            filing_text=filing_text,
            filing_type=request.filing_type,
            filing_period=request.filing_period or "Recent Period"
        )
        
        active_sessions[session.session_id] = session
        
        return {
            "success": True,
            "session": {
                "session_id": session.session_id,
                "company_name": session.company_name,
                "ticker": session.ticker,
                "filing_type": session.filing_type,
                "filing_period": session.filing_period,
                "status": session.status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text processing error: {str(e)}")

# =============================================================================
# LEARN MODE (Read & Hover) - Feature #1
# =============================================================================

@app.get("/api/session/{session_id}/learn")
async def enter_learn_mode(session_id: str):
    """Enter Learn Mode - student sees extracted sections + simplified explanations"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get learn mode content from education service
        learn_content = education_service.enter_learn_mode(session_id)
        
        return {
            "success": True,
            "mode": "learn",
            "content": learn_content,
            "features": {
                "hover_definitions": True,
                "simplified_explanations": True,
                "voice_synthesis_available": True,
                "progress_tracking": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learn mode error: {str(e)}")

@app.get("/api/session/{session_id}/learn/section/{section}")
async def get_learn_section_details(session_id: str, section: str):
    """Get detailed content for a specific SMAP section in Learn Mode"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        learn_content = education_service.enter_learn_mode(session_id)
        
        if section not in learn_content['sections']:
            raise HTTPException(status_code=404, detail=f"Section '{section}' not found")
        
        section_data = learn_content['sections'][section]
        
        return {
            "success": True,
            "section": section,
            "data": section_data,
            "interactive_features": {
                "hover_definitions": section_data.get('hover_definitions', {}),
                "key_concepts": section_data.get('key_concepts', []),
                "explanation": section_data.get('explanation', ''),
                "voice_synthesis_available": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Section details error: {str(e)}")

@app.post("/api/session/{session_id}/voice/synthesize")
async def synthesize_section_voice(session_id: str, request: VoiceGenerationRequest):
    """Generate voice synthesis for Learn Mode content using ElevenLabs"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get the text to synthesize
        text = request.text
        if not text:
            # Default to section content
            learn_content = education_service.enter_learn_mode(session_id)
            section_content = learn_content['sections']['subjective']['content'][:500]  # Limit length
            text = f"Here's the subjective analysis: {section_content}"
        
        # Generate voice using ElevenLabs
        audio_data = voice_agent.synthesize_voice(text, request.voice_type)
        
        if not audio_data or audio_data == b"SIMULATED_AUDIO_DATA":
            return {
                "success": True,
                "simulation_mode": True,
                "message": "Voice synthesis simulated (add ElevenLabs API key for real audio)",
                "text_length": len(text),
                "estimated_duration": len(text) // 10
            }
        
        # Return audio as streaming response
        audio_stream = io.BytesIO(audio_data)
        return StreamingResponse(
            io.BytesIO(audio_data), 
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename=section_audio_{session_id}.mp3"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice synthesis error: {str(e)}")

# =============================================================================
# PRACTICE MODE (Student Writes SMAP) - Feature #2  
# =============================================================================

@app.get("/api/session/{session_id}/practice")
async def enter_practice_mode(session_id: str):
    """Enter Practice Mode - student fills in their own S, M, A, P boxes"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        practice_content = education_service.enter_practice_mode(session_id)
        
        return {
            "success": True,
            "mode": "practice",
            "content": practice_content,
            "features": {
                "guided_templates": True,
                "word_count_targets": True,
                "real_time_tips": True,
                "draft_auto_save": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Practice mode error: {str(e)}")

@app.put("/api/session/{session_id}/practice/save-draft")
async def save_practice_draft(session_id: str, draft: StudentSMAPSubmission):
    """Save student's work-in-progress SMAP notes"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        
        # Update session with draft
        session.student_smap = {
            "subjective": draft.subjective,
            "metrics": draft.metrics,
            "assessment": draft.assessment,
            "plan": draft.plan
        }
        
        # Calculate completion percentage
        sections_completed = sum(1 for text in session.student_smap.values() if text.strip())
        completion_percentage = (sections_completed / 4) * 100
        
        return {
            "success": True,
            "draft_saved": True,
            "completion_percentage": completion_percentage,
            "sections_completed": sections_completed,
            "total_sections": 4,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Draft save error: {str(e)}")

@app.post("/api/session/{session_id}/practice/submit")
async def submit_student_smap(session_id: str, submission: StudentSMAPSubmission):
    """Submit student's completed SMAP notes for AI feedback"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Validate submission completeness
        student_smap = {
            "subjective": submission.subjective.strip(),
            "metrics": submission.metrics.strip(),
            "assessment": submission.assessment.strip(),
            "plan": submission.plan.strip()
        }
        
        # Check if all sections have content
        empty_sections = [k for k, v in student_smap.items() if not v]
        if empty_sections:
            return {
                "success": False,
                "error": "incomplete_submission",
                "empty_sections": empty_sections,
                "message": f"Please complete the following sections: {', '.join(empty_sections)}"
            }
        
        # Submit for feedback
        feedback_results = education_service.submit_student_work(session_id, student_smap)
        
        return {
            "success": True,
            "submitted": True,
            "session_id": session_id,
            "feedback_available": True,
            "overall_score": feedback_results["overall_score"],
            "message": "SMAP notes submitted successfully! AI feedback is ready.",
            "next_step": "view_feedback"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Submission error: {str(e)}")

# =============================================================================
# AI FEEDBACK MODE - Feature #3
# =============================================================================

@app.get("/api/session/{session_id}/feedback")
async def get_ai_feedback(session_id: str):
    """Get AI feedback comparing student notes to Gold Standard"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        
        if session.status != "completed":
            raise HTTPException(status_code=400, detail="Session not completed yet")
        
        # Return comprehensive feedback
        feedback_response = {
            "success": True,
            "session_id": session_id,
            "overall_score": session.overall_score,
            "section_scores": session.scores,
            "feedback": {
                "strengths": session.feedback.get("strengths", []),
                "improvements": session.feedback.get("improvements", []),
                "suggestions": session.feedback.get("next_steps", [])
            },
            "detailed_analysis": {
                "completeness": "✅ Good coverage of key areas",
                "accuracy": "✅ Factually correct information",
                "insight_depth": "⚠️ Could use deeper analysis",
                "clarity": "✅ Clear and well-structured"
            },
            "score_breakdown": {
                "subjective_analysis": session.scores.get("subjective", 0),
                "metrics_extraction": session.scores.get("metrics", 0), 
                "assessment_quality": session.scores.get("assessment", 0),
                "action_planning": session.scores.get("plan", 0)
            },
            "next_steps": [
                "Review AI feedback suggestions",
                "Try another company analysis",
                "Listen to earnings call simulation",
                "Practice specific weak areas"
            ]
        }
        
        return feedback_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")

@app.get("/api/session/{session_id}/gold-standard")
async def get_gold_standard_comparison(session_id: str):
    """Get AI-generated Gold Standard SMAP for comparison"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get gold standard from education service
        if session_id not in education_service.gold_standard_smap:
            raise HTTPException(status_code=404, detail="Gold standard not available")
        
        gold_standard = education_service.gold_standard_smap[session_id]
        session = active_sessions[session_id]
        
        return {
            "success": True,
            "comparison": {
                "gold_standard": {
                    "subjective": gold_standard.subjective,
                    "metrics": gold_standard.metrics,
                    "assessment": gold_standard.assessment,
                    "plan": gold_standard.plan
                },
                "student_work": session.student_smap,
                "analysis": {
                    "subjective": {
                        "score": session.scores.get("subjective", 0),
                        "feedback": "Compare management tone and strategic priorities"
                    },
                    "metrics": {
                        "score": session.scores.get("metrics", 0), 
                        "feedback": "Check for missing key financial ratios"
                    },
                    "assessment": {
                        "score": session.scores.get("assessment", 0),
                        "feedback": "Enhance connection between data and business implications"
                    },
                    "plan": {
                        "score": session.scores.get("plan", 0),
                        "feedback": "Make recommendations more specific and actionable"
                    }
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gold standard comparison error: {str(e)}")

# =============================================================================
# VOICE AGENT FEATURES (ElevenLabs Integration)
# =============================================================================

@app.get("/api/session/{session_id}/earnings-call")
async def generate_earnings_call_experience(session_id: str):
    """Generate immersive earnings call experience with ElevenLabs voices"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        earnings_call = education_service.generate_earnings_call_experience(session_id)
        
        # Convert audio bytes to base64 for JSON response (if real audio)
        if earnings_call['audio']['management'] != b"SIMULATED_AUDIO_DATA":
            earnings_call['audio']['management_base64'] = base64.b64encode(
                earnings_call['audio']['management']
            ).decode('utf-8')
            earnings_call['audio']['analyst_base64'] = base64.b64encode(
                earnings_call['audio']['analyst']
            ).decode('utf-8')
        
        return {
            "success": True,
            "earnings_call": earnings_call,
            "features": {
                "realistic_voices": True,
                "management_presentation": True,
                "analyst_commentary": True,
                "interactive_questions": True,
                "learning_exercises": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Earnings call error: {str(e)}")

@app.get("/api/session/{session_id}/audio-briefing")
async def generate_smap_audio_briefing(session_id: str):
    """Generate audio briefing of SMAP notes for study purposes"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if session_id not in education_service.gold_standard_smap:
            raise HTTPException(status_code=404, detail="SMAP analysis not available")
        
        enhanced_smap = education_service.gold_standard_smap[session_id]
        briefing = voice_agent.generate_smap_audio_briefing(enhanced_smap)
        
        return {
            "success": True,
            "briefing": briefing,
            "features": {
                "professional_narration": True,
                "structured_summary": True,
                "downloadable_audio": True,
                "study_companion": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio briefing error: {str(e)}")

# =============================================================================
# SESSION MANAGEMENT & UTILITIES
# =============================================================================

@app.get("/api/session/{session_id}/status")
async def get_session_status(session_id: str):
    """Get current session status and progress"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = active_sessions[session_id]
        
        return {
            "success": True,
            "session": {
                "session_id": session.session_id,
                "student_id": session.student_id,
                "company_name": session.company_name,
                "ticker": session.ticker,
                "filing_type": session.filing_type,
                "filing_period": session.filing_period,
                "status": session.status,
                "current_mode": session.current_mode,
                "sections_completed": session.sections_completed,
                "overall_score": session.overall_score,
                "started_at": session.started_at,
                "completed_at": session.completed_at
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session status error: {str(e)}")

@app.delete("/api/session/{session_id}")
async def end_session(session_id: str):
    """End learning session and cleanup"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Archive session data (in production, save to database)
        session = active_sessions[session_id]
        
        # Remove from active sessions
        del active_sessions[session_id]
        
        if session_id in education_service.gold_standard_smap:
            del education_service.gold_standard_smap[session_id]
        
        return {
            "success": True,
            "message": "Session ended successfully",
            "session_summary": {
                "company": session.company_name,
                "final_score": session.overall_score,
                "status": session.status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session end error: {str(e)}")

# =============================================================================
# HEALTH CHECK & INFO ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """API root endpoint with information"""
    return {
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "education_service": "active",
            "voice_agent": "active" if not voice_agent.simulation_mode else "simulation_mode", 
            "gemini_service": "active",
            "document_processor": "active"
        },
        "active_sessions": len(active_sessions),
        "authenticated_students": len(student_data)
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting 10Q Notes AI Backend Server")
    print("📚 Three Learning Modes Ready")
    print("🎤 ElevenLabs Voice Integration Active")
    print("🤖 Gemini AI Feedback System Online")
    uvicorn.run(app, host="0.0.0.0", port=8000)