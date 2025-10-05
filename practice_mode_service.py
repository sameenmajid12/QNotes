#!/usr/bin/env python3
"""
Practice Mode Service - Interactive SMAP Notes Learning with Gemini API
"""

import os
import json
import random
from typing import Dict, Any, List, Optional
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PracticeModeService:
    """Service for interactive SMAP notes practice with Gemini AI"""
    
    def __init__(self):
        """Initialize Practice Mode with Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.gemini_available = True
            print("✅ Practice Mode: Gemini API initialized")
        else:
            self.gemini_available = False
            print("⚠️ Practice Mode: Gemini API key not found")
    
    def extract_filing_sections(self, filing_content: str) -> Dict[str, Any]:
        """Extract different sections from the 10-Q filing"""
        if not self.gemini_available:
            return self._get_demo_sections()
        
        try:
            prompt = f"""
            Analyze this 10-Q filing and extract the main sections that would be good for SMAP note practice.
            Return a JSON object with sections and their content.
            
            Filing content: {filing_content[:8000]}  # Limit for API
            
            Return format:
            {{
                "sections": [
                    {{
                        "id": "section_1",
                        "title": "Revenue Analysis",
                        "description": "Brief description of what this section covers",
                        "content": "The actual content from the filing",
                        "difficulty": "beginner|intermediate|advanced",
                        "learning_objectives": ["objective1", "objective2"],
                        "smap_focus": "Which SMAP components this section best teaches"
                    }}
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            sections_data = json.loads(response.text)
            return sections_data
            
        except Exception as e:
            print(f"⚠️ Error extracting sections: {e}")
            return self._get_demo_sections()
    
    def _get_demo_sections(self) -> Dict[str, Any]:
        """Get demo sections when Gemini is not available"""
        return {
            "sections": [
                {
                    "id": "revenue_analysis",
                    "title": "Revenue Analysis",
                    "description": "Analysis of company revenue streams and growth",
                    "content": "The company reported total revenue of $42.5 billion, up 6.8% year-over-year. Revenue growth was driven primarily by strong performance in our core business segments.",
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Understand revenue recognition principles",
                        "Analyze revenue growth trends",
                        "Identify key revenue drivers"
                    ],
                    "smap_focus": "Metrics and Assessment"
                },
                {
                    "id": "risk_factors",
                    "title": "Risk Factors",
                    "description": "Identification and analysis of business risks",
                    "content": "The company faces various risks including market volatility, regulatory changes, and competitive pressures. Management has implemented strategies to mitigate these risks.",
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Identify and categorize business risks",
                        "Assess risk impact on business performance",
                        "Understand risk mitigation strategies"
                    ],
                    "smap_focus": "Subjective and Plan"
                },
                {
                    "id": "cash_flow",
                    "title": "Cash Flow Analysis",
                    "description": "Operating, investing, and financing cash flows",
                    "content": "Operating cash flow increased to $15.2 billion, driven by improved working capital management. Investing activities included $8.1 billion in capital expenditures.",
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Analyze cash flow statement components",
                        "Evaluate cash generation quality",
                        "Assess capital allocation efficiency"
                    ],
                    "smap_focus": "Metrics and Assessment"
                }
            ]
        }
    
    def teach_smap_framework(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Teach the student about SMAP framework for the specific section"""
        if not self.gemini_available:
            return self._get_demo_smap_teaching(section)
        
        try:
            prompt = f"""
            Create a comprehensive SMAP framework teaching guide for this 10-Q section.
            
            Section: {section['title']}
            Content: {section['content']}
            SMAP Focus: {section['smap_focus']}
            
            Return a JSON object with:
            {{
                "smap_explanation": {{
                    "subjective": {{
                        "definition": "Clear definition of what Subjective means",
                        "examples": ["example1", "example2"],
                        "how_to_identify": "How to identify subjective elements",
                        "for_this_section": "Specific guidance for this section"
                    }},
                    "metrics": {{
                        "definition": "Clear definition of what Metrics means",
                        "examples": ["example1", "example2"],
                        "how_to_identify": "How to identify key metrics",
                        "for_this_section": "Specific guidance for this section"
                    }},
                    "assessment": {{
                        "definition": "Clear definition of what Assessment means",
                        "examples": ["example1", "example2"],
                        "how_to_identify": "How to assess performance",
                        "for_this_section": "Specific guidance for this section"
                    }},
                    "plan": {{
                        "definition": "Clear definition of what Plan means",
                        "examples": ["example1", "example2"],
                        "how_to_identify": "How to identify action plans",
                        "for_this_section": "Specific guidance for this section"
                    }}
                }},
                "example_smap": {{
                    "subjective": "Example subjective analysis for this section",
                    "metrics": "Example metrics to extract",
                    "assessment": "Example assessment of performance",
                    "plan": "Example action plan or recommendations"
                }},
                "learning_tips": [
                    "tip1", "tip2", "tip3"
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            teaching_data = json.loads(response.text)
            return teaching_data
            
        except Exception as e:
            print(f"⚠️ Error teaching SMAP: {e}")
            return self._get_demo_smap_teaching(section)
    
    def _get_demo_smap_teaching(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Get demo SMAP teaching when Gemini is not available"""
        return {
            "smap_explanation": {
                "subjective": {
                    "definition": "Management's opinions, tone, and qualitative statements",
                    "examples": ["Management expresses confidence", "Optimistic outlook", "Concern about market conditions"],
                    "how_to_identify": "Look for opinion words, tone indicators, and qualitative statements",
                    "for_this_section": f"For {section['title']}, focus on management's tone and opinions"
                },
                "metrics": {
                    "definition": "Quantitative data, ratios, and measurable performance indicators",
                    "examples": ["Revenue growth of 6.8%", "ROE of 17.8%", "Debt-to-equity ratio"],
                    "how_to_identify": "Look for numbers, percentages, and quantitative comparisons",
                    "for_this_section": f"For {section['title']}, identify key financial metrics and trends"
                },
                "assessment": {
                    "definition": "Analysis and evaluation of performance against benchmarks",
                    "examples": ["Above industry average", "Improved efficiency", "Declining margins"],
                    "how_to_identify": "Compare metrics to historical data, competitors, or industry standards",
                    "for_this_section": f"For {section['title']}, assess performance quality and trends"
                },
                "plan": {
                    "definition": "Strategic initiatives, future actions, and recommendations",
                    "examples": ["Digital transformation plan", "Cost reduction initiatives", "Market expansion strategy"],
                    "how_to_identify": "Look for forward-looking statements and strategic initiatives",
                    "for_this_section": f"For {section['title']}, identify management's plans and strategies"
                }
            },
            "example_smap": {
                "subjective": "Management expresses strong confidence in the company's strategic direction and market position",
                "metrics": "Revenue increased 6.8% YoY to $42.5B, with ROE of 17.8%",
                "assessment": "Performance exceeds industry averages with strong profitability metrics",
                "plan": "Continue digital transformation investments and market expansion initiatives"
            },
            "learning_tips": [
                "Start with metrics - they're the easiest to identify",
                "Look for management's tone in their statements",
                "Compare current performance to historical data",
                "Identify specific action items or strategic initiatives"
            ]
        }
    
    def grade_student_submission(self, student_smap: Dict[str, str], section: Dict[str, Any], teaching_data: Dict[str, Any]) -> Dict[str, Any]:
        """Grade student's SMAP submission with detailed feedback"""
        if not self.gemini_available:
            return self._get_demo_grading(student_smap, section)
        
        try:
            prompt = f"""
            Grade this student's SMAP notes submission and provide detailed, constructive feedback.
            
            Section: {section['title']}
            Section Content: {section['content']}
            SMAP Focus: {section['smap_focus']}
            
            Student's SMAP:
            Subjective: {student_smap.get('subjective', 'Not provided')}
            Metrics: {student_smap.get('metrics', 'Not provided')}
            Assessment: {student_smap.get('assessment', 'Not provided')}
            Plan: {student_smap.get('plan', 'Not provided')}
            
            Grade each component (0-100) and provide detailed feedback:
            {{
                "overall_score": 85,
                "component_scores": {{
                    "subjective": {{
                        "score": 80,
                        "feedback": "Good identification of management tone, but could be more specific",
                        "strengths": ["strength1", "strength2"],
                        "improvements": ["improvement1", "improvement2"]
                    }},
                    "metrics": {{
                        "score": 90,
                        "feedback": "Excellent identification of key metrics",
                        "strengths": ["strength1"],
                        "improvements": ["improvement1"]
                    }},
                    "assessment": {{
                        "score": 75,
                        "feedback": "Assessment needs more comparison to benchmarks",
                        "strengths": ["strength1"],
                        "improvements": ["improvement1", "improvement2"]
                    }},
                    "plan": {{
                        "score": 85,
                        "feedback": "Good identification of strategic initiatives",
                        "strengths": ["strength1"],
                        "improvements": ["improvement1"]
                    }}
                }},
                "detailed_feedback": {{
                    "what_you_did_well": [
                        "specific positive feedback"
                    ],
                    "areas_for_improvement": [
                        "specific improvement suggestions"
                    ],
                    "next_steps": [
                        "actionable next steps"
                    ],
                    "learning_insights": "Overall learning insights and recommendations"
                }},
                "grade_letter": "B+",
                "encouragement": "Encouraging message for the student"
            }}
            """
            
            response = self.model.generate_content(prompt)
            grading_data = json.loads(response.text)
            return grading_data
            
        except Exception as e:
            print(f"⚠️ Error grading submission: {e}")
            return self._get_demo_grading(student_smap, section)
    
    def _get_demo_grading(self, student_smap: Dict[str, str], section: Dict[str, Any]) -> Dict[str, Any]:
        """Get demo grading when Gemini is not available"""
        # Simple scoring logic
        scores = {}
        total_score = 0
        
        for component in ['subjective', 'metrics', 'assessment', 'plan']:
            content = student_smap.get(component, '').strip()
            if len(content) > 50:
                scores[component] = 85
            elif len(content) > 20:
                scores[component] = 70
            elif len(content) > 0:
                scores[component] = 50
            else:
                scores[component] = 0
            total_score += scores[component]
        
        overall_score = total_score // 4
        
        return {
            "overall_score": overall_score,
            "component_scores": {
                component: {
                    "score": scores[component],
                    "feedback": f"Good effort on {component} analysis",
                    "strengths": ["Identified key elements"] if scores[component] > 70 else [],
                    "improvements": ["Provide more detail"] if scores[component] < 80 else ["Keep up the good work"]
                }
                for component in ['subjective', 'metrics', 'assessment', 'plan']
            },
            "detailed_feedback": {
                "what_you_did_well": [
                    "Showed understanding of SMAP framework",
                    "Identified key elements from the section"
                ],
                "areas_for_improvement": [
                    "Provide more specific examples",
                    "Add quantitative analysis where possible"
                ],
                "next_steps": [
                    "Review the SMAP framework explanation",
                    "Practice with another section"
                ],
                "learning_insights": "Good foundation understanding of SMAP analysis"
            },
            "grade_letter": "B" if overall_score >= 80 else "C" if overall_score >= 70 else "D",
            "encouragement": "Great job on your first SMAP analysis! Keep practicing to improve your financial analysis skills."
        }
    
    def generate_progress_insights(self, session_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about student's overall progress"""
        if not self.gemini_available or not session_history:
            return self._get_demo_insights(session_history)
        
        try:
            # Prepare session data for analysis
            sessions_summary = []
            for session in session_history[-10:]:  # Last 10 sessions
                sessions_summary.append({
                    "section": session.get('section_title', 'Unknown'),
                    "score": session.get('overall_score', 0),
                    "difficulty": session.get('difficulty', 'beginner'),
                    "date": session.get('date', 'Unknown')
                })
            
            prompt = f"""
            Analyze this student's SMAP practice session history and provide comprehensive insights.
            
            Session History: {json.dumps(sessions_summary)}
            
            Provide insights on:
            {{
                "overall_progress": {{
                    "trend": "improving|stable|declining",
                    "average_score": 82,
                    "total_sessions": 5,
                    "improvement_rate": "+5%"
                }},
                "strengths": [
                    "specific strength areas"
                ],
                "weaknesses": [
                    "specific areas needing improvement"
                ],
                "recommendations": [
                    "specific actionable recommendations"
                ],
                "learning_insights": {{
                    "best_performing_sections": ["section1", "section2"],
                    "challenging_areas": ["area1", "area2"],
                    "skill_development": "analysis of skill progression"
                }},
                "next_focus": [
                    "recommended next practice areas"
                ]
            }}
            """
            
            response = self.model.generate_content(prompt)
            insights_data = json.loads(response.text)
            return insights_data
            
        except Exception as e:
            print(f"⚠️ Error generating insights: {e}")
            return self._get_demo_insights(session_history)
    
    def _get_demo_insights(self, session_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get demo insights when Gemini is not available"""
        if not session_history:
            return {
                "overall_progress": {
                    "trend": "new_student",
                    "average_score": 0,
                    "total_sessions": 0,
                    "improvement_rate": "0%"
                },
                "strengths": [],
                "weaknesses": [],
                "recommendations": ["Start practicing with beginner sections"],
                "learning_insights": {
                    "best_performing_sections": [],
                    "challenging_areas": [],
                    "skill_development": "New to SMAP analysis"
                },
                "next_focus": ["Begin with revenue analysis section"]
            }
        
        # Simple analysis
        scores = [s.get('overall_score', 0) for s in session_history]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "overall_progress": {
                "trend": "improving" if len(scores) > 1 and scores[-1] > scores[0] else "stable",
                "average_score": round(avg_score),
                "total_sessions": len(session_history),
                "improvement_rate": "+10%" if avg_score > 75 else "+5%"
            },
            "strengths": ["Good understanding of metrics identification"],
            "weaknesses": ["Need more practice with assessment analysis"],
            "recommendations": [
                "Focus on intermediate difficulty sections",
                "Practice more subjective analysis"
            ],
            "learning_insights": {
                "best_performing_sections": ["Revenue Analysis"],
                "challenging_areas": ["Risk Assessment"],
                "skill_development": "Showing steady improvement in SMAP analysis"
            },
            "next_focus": ["Cash Flow Analysis", "Risk Factors"]
        }
    
    def assign_next_section(self, completed_sections: List[str], available_sections: List[Dict[str, Any]], mode: str = "sequential") -> Dict[str, Any]:
        """Assign the next section for practice"""
        if mode == "random":
            # Random selection
            available = [s for s in available_sections if s['id'] not in completed_sections]
            if not available:
                return {"message": "All sections completed!", "section": None}
            selected = random.choice(available)
        else:
            # Sequential selection
            available = [s for s in available_sections if s['id'] not in completed_sections]
            if not available:
                return {"message": "All sections completed!", "section": None}
            selected = available[0]
        
        return {
            "message": f"Next section: {selected['title']}",
            "section": selected
        }

def main():
    """Test the Practice Mode service"""
    print("🎯 Testing Practice Mode Service")
    print("=" * 40)
    
    service = PracticeModeService()
    
    # Test section extraction
    print("\n1. 📄 Testing Section Extraction...")
    demo_content = "Revenue increased 6.8% year-over-year to $42.5 billion..."
    sections = service.extract_filing_sections(demo_content)
    print(f"✅ Extracted {len(sections['sections'])} sections")
    
    # Test SMAP teaching
    print("\n2. 📚 Testing SMAP Teaching...")
    section = sections['sections'][0]
    teaching = service.teach_smap_framework(section)
    print("✅ SMAP framework teaching generated")
    print(f"   Components: {len(teaching['smap_explanation'])}")
    
    # Test grading
    print("\n3. 📝 Testing Student Grading...")
    student_submission = {
        "subjective": "Management is confident about future growth",
        "metrics": "Revenue grew 6.8% to $42.5B",
        "assessment": "Strong performance above industry average",
        "plan": "Continue strategic investments"
    }
    grading = service.grade_student_submission(student_submission, section, teaching)
    print(f"✅ Grading complete: {grading['overall_score']}/100 ({grading['grade_letter']})")
    
    # Test insights
    print("\n4. 📊 Testing Progress Insights...")
    session_history = [
        {"section_title": "Revenue Analysis", "overall_score": 85, "difficulty": "beginner"},
        {"section_title": "Risk Factors", "overall_score": 78, "difficulty": "intermediate"}
    ]
    insights = service.generate_progress_insights(session_history)
    print(f"✅ Insights generated: {insights['overall_progress']['trend']} trend")
    
    print("\n🎉 Practice Mode Service test complete!")

if __name__ == "__main__":
    main()
