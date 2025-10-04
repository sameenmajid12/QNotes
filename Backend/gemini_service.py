"""
10Q Notes AI - Gemini API Service
HackRU 2025 Project by azrabano

This module handles all interactions with Google's Gemini API for:
- SMAP note generation (Subjective, Metrics, Assessment, Plan)
- AI feedback and grading
- Educational content generation (flashcards, quizzes)
"""

import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class SMAPNotes:
    """Structure to hold SMAP notes data"""
    subjective: str
    metrics: str
    assessment: str
    plan: str
    company_name: str = ""
    filing_type: str = ""

@dataclass
class FeedbackScore:
    """Structure to hold feedback and scoring data"""
    completeness: int  # Score out of 100
    accuracy: int
    insight_depth: int
    clarity: int
    overall_score: int
    feedback_comments: List[str]
    suggestions: List[str]

class GeminiService:
    """Main service class for Gemini API interactions"""
    
    def __init__(self):
        """Initialize Gemini service with API key"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Initialize the model - using gemini-2.5-pro (latest stable version)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        print("✅ Gemini API service initialized successfully")
    
    def test_connection(self) -> bool:
        """Test the connection to Gemini API"""
        try:
            response = self.model.generate_content("Hello, this is a test message.")
            print(f"✅ API Connection Test Successful: {response.text[:50]}...")
            return True
        except Exception as e:
            print(f"❌ API Connection Test Failed: {str(e)}")
            return False
    
    def extract_company_info(self, filing_text: str) -> Dict[str, str]:
        """Extract basic company information from SEC filing"""
        prompt = f"""
        Extract key company information from this SEC filing excerpt:
        
        {filing_text[:2000]}...
        
        Please return a JSON object with the following fields:
        - company_name: The company's name
        - ticker: Stock ticker symbol
        - filing_type: Type of filing (10-Q, 10-K, etc.)
        - quarter_year: Quarter and year if applicable
        - industry: Company's industry/sector
        
        Return only valid JSON, no additional text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean response text to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            company_info = json.loads(response_text)
            return company_info
        except Exception as e:
            print(f"Error extracting company info: {e}")
            return {
                "company_name": "Unknown Company",
                "ticker": "N/A",
                "filing_type": "SEC Filing",
                "quarter_year": "N/A",
                "industry": "N/A"
            }
    
    def generate_smap_notes(self, filing_text: str) -> SMAPNotes:
        """Generate SMAP notes from SEC filing text"""
        
        # First extract company info
        company_info = self.extract_company_info(filing_text)
        
        prompt = f"""
        You are an expert financial analyst. Analyze this SEC filing and create structured SMAP notes.
        
        SMAP Framework:
        - S (Subjective): What management said - narratives, tone, qualitative insights
        - M (Metrics): Hard numbers, ratios, financials pulled directly from filings
        - A (Assessment): AI interprets meaning of metrics + narrative
        - P (Plan): Next steps for investor/analyst, compliance or strategy
        
        SEC Filing Text:
        {filing_text}
        
        Please generate comprehensive SMAP notes following this structure:
        
        **SUBJECTIVE (S):**
        [Focus on management's tone, strategic priorities, forward-looking statements, and qualitative insights]
        
        **METRICS (M):**
        [Extract specific financial numbers, ratios, percentage changes, and quantitative data]
        
        **ASSESSMENT (A):**
        [Provide analytical interpretation connecting the metrics to business performance and risks]
        
        **PLAN (P):**
        [Recommend specific next steps for investors, analysts, or advisors]
        
        Make each section substantial and insightful, suitable for finance students and professionals.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Parse the response to extract sections
            sections = self._parse_smap_response(text)
            
            return SMAPNotes(
                subjective=sections.get('subjective', 'No subjective analysis generated'),
                metrics=sections.get('metrics', 'No metrics extracted'),
                assessment=sections.get('assessment', 'No assessment provided'),
                plan=sections.get('plan', 'No plan recommendations'),
                company_name=company_info.get('company_name', 'Unknown Company'),
                filing_type=company_info.get('filing_type', 'SEC Filing')
            )
            
        except Exception as e:
            print(f"Error generating SMAP notes: {e}")
            return SMAPNotes(
                subjective="Error generating subjective analysis",
                metrics="Error extracting metrics",
                assessment="Error in assessment",
                plan="Error in planning recommendations"
            )
    
    def _parse_smap_response(self, response_text: str) -> Dict[str, str]:
        """Parse the Gemini response to extract SMAP sections"""
        sections = {}
        current_section = None
        current_content = []
        
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detect section headers
            if line.upper().startswith('**SUBJECTIVE') or line.upper().startswith('SUBJECTIVE'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'subjective'
                current_content = []
            elif line.upper().startswith('**METRICS') or line.upper().startswith('METRICS'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'metrics'
                current_content = []
            elif line.upper().startswith('**ASSESSMENT') or line.upper().startswith('ASSESSMENT'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'assessment'
                current_content = []
            elif line.upper().startswith('**PLAN') or line.upper().startswith('PLAN'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'plan'
                current_content = []
            elif current_section and line:
                # Skip section headers and add content
                if not line.startswith('**') and not line.startswith('['):
                    current_content.append(line)
        
        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def provide_feedback(self, user_smap: SMAPNotes, gold_standard_smap: SMAPNotes) -> FeedbackScore:
        """Provide AI feedback comparing user's SMAP notes to gold standard"""
        
        prompt = f"""
        You are an expert financial education instructor. Compare these SMAP notes and provide detailed feedback.
        
        GOLD STANDARD SMAP NOTES:
        Subjective: {gold_standard_smap.subjective}
        Metrics: {gold_standard_smap.metrics}
        Assessment: {gold_standard_smap.assessment}
        Plan: {gold_standard_smap.plan}
        
        STUDENT'S SMAP NOTES:
        Subjective: {user_smap.subjective}
        Metrics: {user_smap.metrics}
        Assessment: {user_smap.assessment}
        Plan: {user_smap.plan}
        
        Please provide scores (0-100) and feedback for:
        1. Completeness - How complete are the notes?
        2. Accuracy - Are the facts and numbers correct?
        3. Insight Depth - Quality of analytical thinking
        4. Clarity - How clear and well-written are the notes?
        
        Return your response as JSON with this structure:
        {{
            "completeness": score,
            "accuracy": score,
            "insight_depth": score,
            "clarity": score,
            "overall_score": average_score,
            "feedback_comments": ["comment1", "comment2"],
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean response text to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            feedback_data = json.loads(response_text)
            
            return FeedbackScore(
                completeness=feedback_data.get('completeness', 0),
                accuracy=feedback_data.get('accuracy', 0),
                insight_depth=feedback_data.get('insight_depth', 0),
                clarity=feedback_data.get('clarity', 0),
                overall_score=feedback_data.get('overall_score', 0),
                feedback_comments=feedback_data.get('feedback_comments', []),
                suggestions=feedback_data.get('suggestions', [])
            )
            
        except Exception as e:
            print(f"Error providing feedback: {e}")
            return FeedbackScore(
                completeness=0, accuracy=0, insight_depth=0, clarity=0,
                overall_score=0, feedback_comments=["Error generating feedback"],
                suggestions=["Please try again"]
            )
    
    def generate_flashcards(self, smap_notes: SMAPNotes, num_cards: int = 5) -> List[Dict[str, str]]:
        """Generate educational flashcards from SMAP notes"""
        
        prompt = f"""
        Create {num_cards} educational flashcards based on these SMAP notes for {smap_notes.company_name}.
        
        SMAP Notes:
        Subjective: {smap_notes.subjective}
        Metrics: {smap_notes.metrics}
        Assessment: {smap_notes.assessment}
        Plan: {smap_notes.plan}
        
        Generate flashcards that test understanding of:
        - Financial concepts and ratios
        - Company-specific insights
        - Industry analysis
        - Investment decision-making
        
        Return as JSON array with this structure:
        [
            {{
                "question": "What is the company's debt-to-equity ratio?",
                "answer": "1.5x, indicating moderate leverage",
                "category": "Metrics",
                "difficulty": "Easy"
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean response text to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            flashcards = json.loads(response_text)
            return flashcards
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return [{"question": "Error generating flashcard", "answer": "Please try again", "category": "Error", "difficulty": "N/A"}]

# Test function
def test_gemini_service():
    """Test function to verify Gemini service functionality"""
    print("🚀 Testing 10Q Notes AI - Gemini Service")
    
    try:
        # Initialize service
        service = GeminiService()
        
        # Test connection
        if service.test_connection():
            print("✅ All tests passed! Ready for HackRU demo.")
        else:
            print("❌ Connection test failed. Please check API key.")
            
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")

if __name__ == "__main__":
    test_gemini_service()