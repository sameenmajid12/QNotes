#!/usr/bin/env python3
"""
Enhanced Practice Mode Service - Interactive SMAP Notes Learning
Features: Proper 10-Q structure, OpenAI grading, Sequential/Random modes
"""

import os
import json
import random
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnhancedPracticeModeService:
    """Enhanced service for interactive SMAP notes practice with high-quality grading"""
    
    def __init__(self):
        """Initialize Enhanced Practice Mode with APIs"""
        # Gemini API for content generation
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            self.gemini_available = True
            print("✅ Enhanced Practice Mode: Gemini API initialized")
        else:
            self.gemini_available = False
            print("⚠️ Enhanced Practice Mode: Gemini API key not found")
        
        # OpenAI API for high-quality grading
        # Set your OpenAI API key in environment variable: export OPENAI_API_KEY="your-key-here"
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if self.openai_key:
            self.openai_available = True
            print("✅ Enhanced Practice Mode: OpenAI API initialized")
        else:
            self.openai_available = False
            print("⚠️ Enhanced Practice Mode: OpenAI API key not found - set OPENAI_API_KEY environment variable")
    
    def extract_filing_sections(self, filing_content: str) -> Dict[str, Any]:
        """Extract proper 10-Q sections based on SEC structure"""
        print("Enhanced Practice Mode: Extracting 10-Q filing sections...")
        
        # Proper 10-Q structure based on SEC requirements
        sections = [
            # PART I: FINANCIAL INFORMATION
            {
                "id": "financial_statements",
                "title": "Financial Statements",
                "description": "Unaudited balance sheet, income statement, cash flows, and equity statements",
                "content": "The company's financial statements show total assets of $3.2 trillion, with revenue of $42.5 billion (+6.8% YoY), net income of $13.4 billion, and operating cash flow of $15.2 billion. Key metrics include ROE of 17.8%, CET1 ratio of 15.9%, and book value per share of $95.35.",
                "difficulty": "beginner",
                "part": "Part I",
                "learning_objectives": [
                    "Read and interpret financial statements",
                    "Calculate key financial ratios",
                    "Identify trends in financial performance"
                ],
                "smap_focus": "Metrics and Assessment"
            },
            {
                "id": "md_a",
                "title": "Management's Discussion & Analysis (MD&A)",
                "description": "Management's explanation of financial condition and operational results",
                "content": "Management expressed strong confidence in Q1 performance, highlighting robust revenue growth driven by digital transformation initiatives. The fortress balance sheet strategy provides flexibility for economic volatility while maintaining strong profitability metrics. Credit provisions remain well-controlled despite economic uncertainty.",
                "difficulty": "intermediate",
                "part": "Part I",
                "learning_objectives": [
                    "Analyze management's tone and strategic priorities",
                    "Connect financial results to business drivers",
                    "Identify forward-looking statements and risks"
                ],
                "smap_focus": "Subjective and Assessment"
            },
            {
                "id": "market_risk",
                "title": "Market Risk Disclosures",
                "description": "Quantitative and qualitative disclosures about market risk exposure",
                "content": "The company faces market risks including interest rate sensitivity, foreign exchange exposure, and credit risk. Interest rate risk is managed through asset-liability matching, with a net interest margin of 2.74%. Foreign exchange exposure is primarily in European operations, representing 15% of total revenue.",
                "difficulty": "advanced",
                "part": "Part I",
                "learning_objectives": [
                    "Understand different types of market risks",
                    "Assess risk measurement methodologies",
                    "Evaluate risk management strategies"
                ],
                "smap_focus": "Assessment and Plan"
            },
            {
                "id": "controls_procedures",
                "title": "Controls and Procedures",
                "description": "Internal controls and procedures for financial reporting",
                "content": "Management maintains a comprehensive system of internal controls designed to ensure reliable financial reporting. The internal control framework includes risk assessment, control activities, information systems, and monitoring procedures. No material weaknesses were identified during the quarter.",
                "difficulty": "intermediate",
                "part": "Part I",
                "learning_objectives": [
                    "Understand internal control frameworks",
                    "Evaluate effectiveness of internal controls",
                    "Identify control deficiencies and remediation plans"
                ],
                "smap_focus": "Subjective and Plan"
            },
            
            # PART II: OTHER INFORMATION
            {
                "id": "legal_proceedings",
                "title": "Legal Proceedings",
                "description": "Material legal proceedings and regulatory matters",
                "content": "The company is involved in various legal proceedings, including regulatory investigations and civil litigation. Management believes these matters will not have a material adverse effect on the company's financial condition, but acknowledges potential risks and uncertainties.",
                "difficulty": "beginner",
                "part": "Part II",
                "learning_objectives": [
                    "Identify material legal risks",
                    "Assess potential financial impact",
                    "Understand regulatory compliance requirements"
                ],
                "smap_focus": "Subjective and Assessment"
            },
            {
                "id": "risk_factors",
                "title": "Risk Factors",
                "description": "Significant risks affecting business and financial condition",
                "content": "Key risk factors include economic uncertainty, regulatory changes, competitive pressures, credit quality deterioration, interest rate volatility, cybersecurity threats, and operational risks. Management has implemented comprehensive risk management frameworks to monitor and mitigate these exposures.",
                "difficulty": "intermediate",
                "part": "Part II",
                "learning_objectives": [
                    "Categorize different types of business risks",
                    "Assess risk impact and probability",
                    "Evaluate risk mitigation strategies"
                ],
                "smap_focus": "Subjective and Plan"
            },
            {
                "id": "unregistered_securities",
                "title": "Unregistered Sales of Equity Securities",
                "description": "Information on unregistered securities sales and use of proceeds",
                "content": "During the quarter, the company did not engage in any unregistered sales of equity securities. All securities offerings were conducted through registered transactions or qualified exemptions under applicable securities laws.",
                "difficulty": "beginner",
                "part": "Part II",
                "learning_objectives": [
                    "Understand securities registration requirements",
                    "Identify exempt transactions",
                    "Track use of offering proceeds"
                ],
                "smap_focus": "Metrics and Plan"
            },
            {
                "id": "senior_securities_defaults",
                "title": "Defaults Upon Senior Securities",
                "description": "Disclosures concerning defaults on senior securities",
                "content": "No defaults on senior securities occurred during the quarter. The company maintains strong credit ratings and has not experienced any payment defaults on its outstanding debt obligations.",
                "difficulty": "beginner",
                "part": "Part II",
                "learning_objectives": [
                    "Understand senior security obligations",
                    "Identify default triggers and consequences",
                    "Assess credit quality indicators"
                ],
                "smap_focus": "Assessment"
            },
            {
                "id": "other_information",
                "title": "Other Information",
                "description": "Other relevant information and disclosures",
                "content": "The company continues to focus on digital transformation initiatives, including investments in technology infrastructure, cybersecurity enhancements, and customer experience improvements. Management remains committed to sustainable business practices and stakeholder value creation.",
                "difficulty": "intermediate",
                "part": "Part II",
                "learning_objectives": [
                    "Identify non-financial business developments",
                    "Analyze strategic initiatives and future outlook",
                    "Understand corporate governance and social responsibility"
                ],
                "smap_focus": "Subjective and Plan"
            }
        ]
        
        return {
            "sections": sections,
            "total_sections": len(sections),
            "extraction_timestamp": datetime.now().isoformat(),
            "filing_analyzed": "JPMorgan Chase 10-Q (Sample)",
            "structure": "SEC-compliant 10-Q format"
        }
    
    def teach_smap_framework(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Teach students about SMAP framework for the specific section"""
        print(f"Enhanced Practice Mode: Teaching SMAP framework for {section['title']}")
        
        if not self.gemini_available:
            return self._fallback_smap_teaching(section)
        
        try:
            prompt = f"""
You are a finance professor teaching students how to create SMAP notes for SEC filings.

SECTION: {section['title']}
DESCRIPTION: {section['description']}
CONTENT: {section['content']}
DIFFICULTY: {section['difficulty']}
LEARNING OBJECTIVES: {', '.join(section['learning_objectives'])}

SMAP Framework:
- S (Subjective): Management's narrative, tone, forward-looking statements, strategic priorities
- M (Metrics): Key financial numbers, ratios, trends, quantitative data
- A (Assessment): Analysis of performance, risks, strengths/weaknesses, what the numbers mean
- P (Plan): Future outlook, strategic initiatives, management's next steps

For this {section['difficulty']} level section, provide:

1. SMAP EXPLANATION: Detailed explanation of how to approach each SMAP component for this specific section
2. EXAMPLE NOTES: Show what good SMAP notes would look like for this section
3. KEY FOCUS AREAS: What students should pay attention to
4. COMMON MISTAKES: What students often get wrong
5. GRADING CRITERIA: How their SMAP notes will be evaluated

Make this educational and practical for finance students.
"""
            
            response = self.gemini_model.generate_content(prompt)
            
            return {
                "teaching_content": response.text,
                "section_title": section['title'],
                "difficulty": section['difficulty'],
                "smap_focus": section['smap_focus'],
                "learning_objectives": section['learning_objectives'],
                "teaching_timestamp": datetime.now().isoformat(),
                "source": "Gemini AI"
            }
            
        except Exception as e:
            print(f"❌ Error in SMAP teaching: {str(e)}")
            return self._fallback_smap_teaching(section)
    
    def _fallback_smap_teaching(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback SMAP teaching when Gemini is unavailable"""
        return {
            "teaching_content": f"""
SMAP Framework for {section['title']}

S (Subjective): Focus on management's narrative and strategic priorities
M (Metrics): Extract key financial numbers and ratios
A (Assessment): Analyze performance and identify risks/opportunities  
P (Plan): Note future outlook and strategic initiatives

For this {section['difficulty']} section, pay attention to {section['smap_focus']}.
""",
            "section_title": section['title'],
            "difficulty": section['difficulty'],
            "smap_focus": section['smap_focus'],
            "learning_objectives": section['learning_objectives'],
            "teaching_timestamp": datetime.now().isoformat(),
            "source": "Fallback"
        }
    
    def grade_student_submission(self, student_submission: str, section: Dict[str, Any], gold_standard: str = "") -> Dict[str, Any]:
        """Grade student's SMAP submission using OpenAI GPT-4 for high-quality feedback"""
        print(f"Enhanced Practice Mode: Grading student submission for {section['title']}")
        
        if not self.openai_available:
            return self._fallback_grading(student_submission, section)
        
        try:
            # Use OpenAI for high-quality grading
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""
You are a finance professor grading student SMAP notes. Be STRICT and realistic in your grading.

SECTION: {section['title']}
STUDENT SUBMISSION: {student_submission}
SECTION CONTENT: {section['content']}

GRADING CRITERIA:
- Subjective (S): Did they capture management's narrative and tone?
- Metrics (M): Did they identify key financial numbers and ratios?
- Assessment (A): Did they analyze what the numbers mean?
- Plan (P): Did they note future outlook and strategic initiatives?

GRADING SCALE:
- 90-100: Excellent, professional-level analysis
- 80-89: Good, minor gaps or improvements needed
- 70-79: Satisfactory, several areas for improvement
- 60-69: Below average, significant gaps
- 50-59: Poor, major deficiencies
- 0-49: Very poor, shows little understanding

BE HARSH ON POOR SUBMISSIONS. If someone writes "bullshit" or nonsensical content, give them 5/100.

Provide:
1. OVERALL SCORE: 0-100
2. LETTER GRADE: A, B, C, D, F
3. COMPONENT SCORES: S, M, A, P (0-100 each)
4. WHAT THEY GOT RIGHT: Specific positive feedback
5. AREAS FOR IMPROVEMENT: Specific constructive criticism
6. NEXT STEPS: How to improve

Be detailed and educational in your feedback.
"""
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a strict but fair finance professor grading SMAP notes."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.3
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                feedback_text = result['choices'][0]['message']['content']
                
                # Parse the feedback to extract scores
                overall_score = self._extract_score(feedback_text, "OVERALL SCORE:")
                letter_grade = self._extract_letter_grade(feedback_text)
                s_score = self._extract_score(feedback_text, "- S:")
                m_score = self._extract_score(feedback_text, "- M:")
                a_score = self._extract_score(feedback_text, "- A:")
                p_score = self._extract_score(feedback_text, "- P:")
                
                return {
                    "overall_score": overall_score,
                    "letter_grade": letter_grade,
                    "component_scores": {
                        "subjective": s_score,
                        "metrics": m_score,
                        "assessment": a_score,
                        "plan": p_score
                    },
                    "detailed_feedback": feedback_text,
                    "section_title": section['title'],
                    "grading_timestamp": datetime.now().isoformat(),
                    "grader": "OpenAI GPT-4"
                }
            else:
                print(f"❌ OpenAI API error: {response.status_code}")
                return self._fallback_grading(student_submission, section)
                
        except Exception as e:
            print(f"❌ Error in OpenAI grading: {str(e)}")
            return self._fallback_grading(student_submission, section)
    
    def _extract_score(self, text: str, prefix: str) -> int:
        """Extract numeric score from feedback text"""
        try:
            import re
            lines = text.split('\n')
            for line in lines:
                if prefix in line:
                    # Look for patterns like "90/100" or "S: 90/100"
                    # First try to find pattern with slash
                    slash_match = re.search(r'(\d+)/100', line)
                    if slash_match:
                        return min(100, max(0, int(slash_match.group(1))))
                    
                    # Then try to find just numbers after the prefix
                    after_prefix = line.split(prefix)[1] if prefix in line else line
                    numbers = re.findall(r'\d+', after_prefix)
                    if numbers:
                        score = int(numbers[0])
                        # If score seems too high (like year 2025), try next number
                        if score > 100 and len(numbers) > 1:
                            score = int(numbers[1])
                        return min(100, max(0, score))
        except:
            pass
        return 50  # Default score
    
    def _extract_letter_grade(self, text: str) -> str:
        """Extract letter grade from feedback text"""
        try:
            import re
            match = re.search(r'LETTER GRADE[:\s]*([A-F])', text, re.IGNORECASE)
            if match:
                return match.group(1)
        except:
            pass
        return "C"  # Default grade
    
    def _fallback_grading(self, student_submission: str, section: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback grading when OpenAI is unavailable"""
        # Simple keyword-based grading
        score = 50
        if len(student_submission) > 100:
            score += 20
        if any(word in student_submission.lower() for word in ['revenue', 'profit', 'growth', 'risk']):
            score += 15
        if any(word in student_submission.lower() for word in ['bullshit', 'idk', 'whatever']):
            score = 5
            
        return {
            "overall_score": min(100, score),
            "letter_grade": "C" if score >= 70 else "D" if score >= 60 else "F",
            "component_scores": {
                "subjective": min(100, score + 5),
                "metrics": min(100, score - 5),
                "assessment": min(100, score),
                "plan": min(100, score + 10)
            },
            "detailed_feedback": f"Basic grading for {section['title']}. Your submission shows some understanding but could be improved.",
            "section_title": section['title'],
            "grading_timestamp": datetime.now().isoformat(),
            "grader": "Fallback"
        }
    
    def generate_progress_insights(self, completed_sections: List[Dict], student_performance: List[Dict]) -> Dict[str, Any]:
        """Generate insights about student's learning progress"""
        print("Enhanced Practice Mode: Generating progress insights...")
        
        if not self.gemini_available:
            return self._fallback_insights(completed_sections, student_performance)
        
        try:
            # Calculate basic stats
            avg_score = sum(perf.get('overall_score', 50) for perf in student_performance) / len(student_performance) if student_performance else 50
            total_sections = len(completed_sections)
            
            prompt = f"""
You are a learning analytics expert analyzing a finance student's progress in SMAP notes practice.

STUDENT PROGRESS DATA:
- Sections Completed: {total_sections}
- Average Score: {avg_score:.1f}/100
- Completed Sections: {[s['title'] for s in completed_sections]}
- Performance History: {student_performance}

Provide detailed insights on:
1. LEARNING TRENDS: How is the student improving over time?
2. STRENGTHS: What areas is the student excelling in?
3. WEAKNESSES: What areas need improvement?
4. RECOMMENDATIONS: Specific next steps for improvement
5. MOTIVATION: Encouraging feedback and progress celebration

Be encouraging but honest about areas for improvement.
"""
            
            response = self.gemini_model.generate_content(prompt)
            
            return {
                "insights": response.text,
                "average_score": avg_score,
                "sections_completed": total_sections,
                "progress_timestamp": datetime.now().isoformat(),
                "source": "Gemini AI"
            }
            
        except Exception as e:
            print(f"❌ Error generating insights: {str(e)}")
            return self._fallback_insights(completed_sections, student_performance)
    
    def _fallback_insights(self, completed_sections: List[Dict], student_performance: List[Dict]) -> Dict[str, Any]:
        """Fallback insights when Gemini is unavailable"""
        avg_score = sum(perf.get('overall_score', 50) for perf in student_performance) / len(student_performance) if student_performance else 50
        
        return {
            "insights": f"You've completed {len(completed_sections)} sections with an average score of {avg_score:.1f}. Keep practicing to improve your SMAP analysis skills!",
            "average_score": avg_score,
            "sections_completed": len(completed_sections),
            "progress_timestamp": datetime.now().isoformat(),
            "source": "Fallback"
        }
    
    def assign_next_section(self, completed_sections: List[str], available_sections: List[Dict]) -> Dict[str, Any]:
        """Assign the next section for practice"""
        print("Enhanced Practice Mode: Assigning next section...")
        
        # Find first uncompleted section
        for section in available_sections:
            if section['id'] not in completed_sections:
                return {
                    "assignment": section,
                    "assignment_reason": "Next uncompleted section",
                    "progress": f"{len(completed_sections)}/{len(available_sections)} sections completed",
                    "assignment_timestamp": datetime.now().isoformat()
                }
        
        # All sections completed
        return {
            "assignment": None,
            "assignment_reason": "All sections completed! 🎉",
            "progress": f"{len(completed_sections)}/{len(available_sections)} sections completed",
            "assignment_timestamp": datetime.now().isoformat(),
            "congratulations": "You've completed all sections! Consider reviewing difficult areas or practicing with new filings."
        }
