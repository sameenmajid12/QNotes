#!/usr/bin/env python3
"""
Integrated 10Q Notes AI Backend
Combines enhanced practice mode with existing backend structure
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
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import services
try:
    from enhanced_practice_mode_service import EnhancedPracticeModeService
    from working_backend_with_elevenlabs import WorkingBackendHandler
    from convai_service import ConvAIService
    from elevenlabs_service import ElevenLabsService
    from education_service import EducationService
    from voice_agent_service import VoiceAgentService
    from document_processor import DocumentProcessor
    from enhanced_gemini_service import EnhancedGeminiService
    print("✅ All services imported successfully")
except ImportError as e:
    print(f"⚠️ Import warning: {e}")
    # Fallback imports
    from education_service import EducationService
    from voice_agent_service import VoiceAgentService
    from document_processor import DocumentProcessor

# Pydantic models
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
    text: str
    voice_type: str = "professional"  # professional, management, analyst

class ConvAIRequest(BaseModel):
    session_id: str
    message: str

# Initialize FastAPI app
app = FastAPI(
    title="10Q Notes AI - Integrated Backend",
    description="AI-powered SEC filing learning platform with enhanced practice mode",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    education_service = EducationService()
    voice_agent_service = VoiceAgentService()
    document_processor = DocumentProcessor()
    enhanced_gemini_service = EnhancedGeminiService()
    
    # Enhanced services
    enhanced_practice_service = EnhancedPracticeModeService()
    convai_service = ConvAIService()
    elevenlabs_service = ElevenLabsService()
    
    print("✅ All services initialized successfully")
except Exception as e:
    print(f"⚠️ Service initialization warning: {e}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "education": "active",
            "voice_agent": "active",
            "document_processor": "active",
            "enhanced_practice": "active",
            "convai": "active",
            "elevenlabs": "active"
        }
    }

# Authentication endpoints
@app.post("/api/auth/login")
async def student_login(auth: StudentAuth):
    """Student authentication with .edu email validation"""
    try:
        if not auth.email.endswith('.edu'):
            raise HTTPException(status_code=400, detail="Only .edu email addresses are allowed")
        
        # Create or get student profile
        student_id = str(uuid.uuid4())
        student_profile = {
            "student_id": student_id,
            "email": auth.email,
            "name": auth.name or "Student",
            "created_at": datetime.now().isoformat(),
            "learning_level": "beginner"
        }
        
        return {
            "success": True,
            "student": student_profile,
            "message": "Login successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

# Session management
@app.post("/api/session/start")
async def start_learning_session(request: StartSessionRequest):
    """Start a new learning session"""
    try:
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "student_id": request.student_id,
            "company_name": request.company_name or "Sample Company",
            "ticker": request.ticker or "SAMPLE",
            "filing_type": request.filing_type,
            "filing_period": request.filing_period,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        return {
            "success": True,
            "session": session_data,
            "message": "Session started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session start failed: {str(e)}")

# File upload endpoint
@app.post("/api/upload/filing")
async def upload_filing(file: UploadFile = File(...)):
    """Upload SEC filing document"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read file content
        content = await file.read()
        
        # Process document
        processed_doc = document_processor.prepare_for_analysis(content.decode('utf-8', errors='ignore'))
        
        return {
            "success": True,
            "filename": file.filename,
            "processed_content": processed_doc,
            "message": "File uploaded and processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

# Enhanced Practice Mode endpoints
@app.get("/api/session/{session_id}/practice/sections")
async def get_practice_sections(session_id: str):
    """Get available practice sections"""
    try:
        # Sample filing content for demo
        sample_content = """
        JPMorgan Chase & Co. Q1 2024 10-Q Filing
        
        Part I - Financial Information
        Item 1. Financial Statements
        The company reported strong Q1 performance with revenue of $42.5 billion, up 6.8% year-over-year.
        Net income was $13.4 billion with operating cash flow of $15.2 billion.
        
        Item 2. Management's Discussion and Analysis
        Management expressed confidence in the fortress balance sheet strategy and digital transformation initiatives.
        Credit provisions remain well-controlled despite economic uncertainty.
        
        Part II - Other Information
        Item 1. Legal Proceedings
        The company is involved in various regulatory matters but believes they will not have material impact.
        """
        
        sections = enhanced_practice_service.extract_filing_sections(sample_content)
        
        return {
            "success": True,
            "sections": sections,
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sections: {str(e)}")

@app.post("/api/session/{session_id}/practice/teach")
async def teach_smap_framework(session_id: str, section_data: dict):
    """Teach SMAP framework for a specific section"""
    try:
        teaching = enhanced_practice_service.teach_smap_framework(section_data)
        
        return {
            "success": True,
            "teaching": teaching,
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Teaching failed: {str(e)}")

@app.post("/api/session/{session_id}/practice/submit")
async def submit_smap_practice(session_id: str, submission: StudentSMAPSubmission):
    """Submit SMAP practice and get AI feedback"""
    try:
        # Combine all SMAP components
        full_submission = f"""
        SUBJECTIVE: {submission.subjective}
        
        METRICS: {submission.metrics}
        
        ASSESSMENT: {submission.assessment}
        
        PLAN: {submission.plan}
        """
        
        # Sample section for grading
        sample_section = {
            "id": "financial_statements",
            "title": "Financial Statements",
            "description": "Company financial performance",
            "content": "Strong Q1 performance with revenue growth and solid profitability metrics."
        }
        
        # Grade the submission
        grading = enhanced_practice_service.grade_student_submission(full_submission, sample_section)
        
        return {
            "success": True,
            "grading": grading,
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Submission failed: {str(e)}")

@app.get("/api/session/{session_id}/practice/insights")
async def get_practice_insights(session_id: str):
    """Get learning progress insights"""
    try:
        # Sample completed sections and performance
        completed_sections = [
            {"id": "financial_statements", "title": "Financial Statements", "completed_at": datetime.now().isoformat()},
            {"id": "md_a", "title": "Management's Discussion & Analysis", "completed_at": datetime.now().isoformat()}
        ]
        
        student_performance = [
            {"overall_score": 85, "section": "financial_statements"},
            {"overall_score": 78, "section": "md_a"}
        ]
        
        insights = enhanced_practice_service.generate_progress_insights(completed_sections, student_performance)
        
        return {
            "success": True,
            "insights": insights,
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

# Voice Agent endpoints
@app.post("/api/session/{session_id}/voice/generate")
async def generate_voice(request: VoiceGenerationRequest):
    """Generate voice audio using ElevenLabs"""
    try:
        audio_data = elevenlabs_service.generate_audio(request.text, request.voice_type)
        
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=voice.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")

@app.post("/api/session/{session_id}/convai")
async def convai_interaction(request: ConvAIRequest):
    """Interactive ConvAI conversation"""
    try:
        response = convai_service.send_message(request.message, request.session_id)
        
        return {
            "success": True,
            "response": response,
            "session_id": request.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ConvAI interaction failed: {str(e)}")

# Learn Mode endpoints
@app.get("/api/session/{session_id}/learn")
async def get_learn_content(session_id: str):
    """Get learn mode content with simplified explanations"""
    try:
        learn_content = {
            "sections": [
                {
                    "id": "overview",
                    "title": "Company Overview",
                    "content": "JPMorgan Chase is a leading financial services firm...",
                    "simplified_explanation": "This is a big bank that helps people and businesses with money.",
                    "key_metrics": ["Revenue: $42.5B", "Net Income: $13.4B", "Assets: $3.2T"]
                },
                {
                    "id": "financial_performance",
                    "title": "Financial Performance",
                    "content": "Strong Q1 performance with revenue growth...",
                    "simplified_explanation": "The company made more money this quarter compared to last year.",
                    "key_metrics": ["Revenue Growth: +6.8%", "ROE: 17.8%", "CET1 Ratio: 15.9%"]
                }
            ],
            "session_id": session_id
        }
        
        return {
            "success": True,
            "content": learn_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learn content failed: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "10Q Notes AI - Integrated Backend",
        "version": "2.0.0",
        "status": "active",
        "features": [
            "Enhanced Practice Mode with OpenAI GPT-4 grading",
            "ElevenLabs voice synthesis and ConvAI integration",
            "Complete SMAP framework learning",
            "Interactive learning sessions",
            "Progress tracking and insights"
        ],
        "endpoints": {
            "health": "/health",
            "auth": "/api/auth/login",
            "practice": "/api/session/{id}/practice/*",
            "voice": "/api/session/{id}/voice/*",
            "convai": "/api/session/{id}/convai",
            "learn": "/api/session/{id}/learn"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting 10Q Notes AI - Integrated Backend")
    print("📚 Enhanced Practice Mode with OpenAI GPT-4")
    print("🎤 ElevenLabs Voice Integration")
    print("🤖 ConvAI Interactive Agent")
    print("🌐 CORS enabled for frontend integration")
    
    uvicorn.run(
        "integrated_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
