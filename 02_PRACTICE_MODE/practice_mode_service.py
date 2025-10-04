"""
FEATURE 2: PRACTICE MODE (Student Writes SMAP)
HackRU 2025 - 10Q Notes AI

Hands-on analysis practice:
- Students fill in their own Subjective, Metrics, Assessment, Plan boxes
- Guided templates with word count targets and real-time tips
- Draft auto-saving and completion progress tracking
- Practice identifying key narrative points, ratios, risks, and next steps

API Endpoints:
- GET /api/session/{id}/practice
- PUT /api/session/{id}/practice/save-draft
- POST /api/session/{id}/practice/submit
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PracticeModeContent:
    """Data structure for Practice Mode content and templates"""
    session_id: str
    instructions: Dict[str, Any]
    practice_areas: Dict[str, Dict[str, Any]]
    current_draft: Dict[str, str]
    progress: Dict[str, Any]

@dataclass 
class StudentProgress:
    """Track student's practice progress and completion status"""
    sections_completed: int
    total_sections: int
    completion_percentage: float
    estimated_time_remaining: int
    last_saved: str

class PracticeModeService:
    """
    Feature 2: Practice Mode Implementation
    Students write their own SMAP analysis with guided assistance
    """
    
    def __init__(self):
        """Initialize Practice Mode service"""
        print("✍️ Practice Mode Service - Feature 2 Initialized")
        self.templates = self._load_practice_templates()
        self.writing_tips = self._load_writing_tips()
        self.examples = self._load_example_responses()
    
    def enter_practice_mode(self, session_id: str, enhanced_smap) -> PracticeModeContent:
        """
        Enter Practice Mode - Main entry point for Feature 2
        Students fill in their own SMAP analysis boxes
        """
        print(f"✍️ PRACTICE MODE ACTIVATED - Session: {session_id}")
        print(f"   🏢 Company: {enhanced_smap.company_name}")
        print(f"   📝 Student ready to write SMAP analysis")
        
        practice_content = PracticeModeContent(
            session_id=session_id,
            instructions=self._create_practice_instructions(),
            practice_areas=self._create_practice_areas(enhanced_smap),
            current_draft={"subjective": "", "metrics": "", "assessment": "", "plan": ""},
            progress={
                "sections_available": 4,
                "estimated_time": "20-25 minutes",
                "difficulty_level": "Intermediate",
                "completion_percentage": 0
            }
        )
        
        print("✅ Practice Mode initialized with guided templates")
        return practice_content
    
    def _create_practice_instructions(self) -> Dict[str, Any]:
        """Create comprehensive instructions for practice mode"""
        
        return {
            'overview': 'Now it\'s your turn! Write your own SMAP notes for this filing. Use the guidance below to create professional-quality financial analysis.',
            'sections': {
                'subjective': 'What did management emphasize? What was their tone and strategic focus? Look for confidence levels, priorities, and forward-looking statements.',
                'metrics': 'What are the key financial numbers and ratios? Include growth rates, profitability metrics, and industry-specific indicators.',
                'assessment': 'What do these numbers and narratives mean for the business? Connect the data to performance, trends, and competitive position.',
                'plan': 'What should an investor or analyst do next? Be specific with monitoring priorities and actionable recommendations.'
            },
            'general_tips': [
                'Use specific numbers and percentages when available',
                'Look for management\'s tone - optimistic, cautious, confident?',
                'Connect metrics to business performance and strategy',
                'Make your plan actionable with clear next steps',
                'Write as if you\'re briefing a senior analyst or investor'
            ],
            'success_criteria': {
                'clarity': 'Write in clear, professional language',
                'completeness': 'Address all key areas comprehensively',
                'accuracy': 'Use correct financial terminology and data',
                'insight': 'Provide meaningful analysis beyond just restating facts'
            }
        }
    
    def _create_practice_areas(self, enhanced_smap) -> Dict[str, Dict[str, Any]]:
        """Create guided practice areas with templates and examples"""
        
        return {
            'subjective': {
                'title': 'Subjective (S) - Management Perspective',
                'placeholder': 'Example: Management expressed strong confidence in Q1 results, highlighting robust revenue growth and disciplined expense management. The tone was optimistic about future opportunities in digital banking, with CEO emphasizing the company\'s fortress balance sheet strategy...',
                'word_target': '100-150 words',
                'focus_areas': [
                    'Management tone and confidence level',
                    'Strategic priorities and initiatives', 
                    'Key themes and messaging',
                    'Forward-looking statements'
                ],
                'writing_prompts': [
                    'How did management describe their performance this quarter?',
                    'What strategic priorities did they emphasize?',
                    'What tone did they use - confident, cautious, optimistic?',
                    'What did they say about future prospects?'
                ],
                'quality_checklist': [
                    '✓ Captures management\'s main messages',
                    '✓ Identifies tone and confidence level',
                    '✓ Mentions key strategic themes',
                    '✓ Notes forward-looking guidance'
                ]
            },
            'metrics': {
                'title': 'Metrics (M) - Key Financial Data',
                'placeholder': 'Example: Total revenue of $42.5 billion (+6.8% YoY), Net income of $13.4 billion (+6.1% YoY). ROE improved to 17.8% vs 16.9% prior quarter. CET1 ratio strong at 15.9%, well above regulatory minimums. Efficiency ratio of 56% shows operational discipline...',
                'word_target': '80-120 words',
                'focus_areas': [
                    'Revenue and growth rates',
                    'Profitability metrics (margins, ROE)', 
                    'Key ratios and industry metrics',
                    'Year-over-year comparisons'
                ],
                'writing_prompts': [
                    'What were the headline revenue and profit numbers?',
                    'How did key metrics change vs. last year?',
                    'What ratios are most important for this industry?',
                    'Are there any standout performance indicators?'
                ],
                'quality_checklist': [
                    '✓ Includes revenue and profit figures',
                    '✓ Shows year-over-year growth rates',
                    '✓ Mentions key financial ratios',
                    '✓ Uses specific numbers and percentages'
                ]
            },
            'assessment': {
                'title': 'Assessment (A) - Analysis & Interpretation', 
                'placeholder': 'Example: The results demonstrate strong fundamental performance with revenue growth across key segments. The fortress balance sheet provides flexibility during economic uncertainty, while maintaining industry-leading profitability metrics. Credit quality remains solid though provisions increased as expected...',
                'word_target': '120-180 words',
                'focus_areas': [
                    'Performance analysis and trends',
                    'Strengths and competitive advantages',
                    'Areas of concern or risk',
                    'Business implications'
                ],
                'writing_prompts': [
                    'What do the numbers tell us about business performance?',
                    'What are the company\'s main strengths?',
                    'Are there any areas of concern?',
                    'How does this compare to competitors?'
                ],
                'quality_checklist': [
                    '✓ Connects metrics to business performance',
                    '✓ Identifies key strengths and advantages',
                    '✓ Notes potential risks or concerns',
                    '✓ Provides meaningful business insights'
                ]
            },
            'plan': {
                'title': 'Plan (P) - Next Steps & Recommendations',
                'placeholder': 'Example: 1. Monitor credit provisions for trend changes in next 2 quarters. 2. Track interest rate sensitivity impact on NIM expansion. 3. Evaluate investment banking recovery timeline vs peers. 4. Assess digital transformation ROI and competitive positioning...',
                'word_target': '80-120 words',
                'focus_areas': [
                    'Specific monitoring priorities',
                    'Actionable recommendations',
                    'Investment decision factors',
                    'Risk management considerations'
                ],
                'writing_prompts': [
                    'What should investors monitor going forward?',
                    'What are the key risks to watch?',
                    'What decisions need to be made?',
                    'What would you recommend to stakeholders?'
                ],
                'quality_checklist': [
                    '✓ Provides specific action items',
                    '✓ Prioritizes monitoring areas',
                    '✓ Offers actionable recommendations',
                    '✓ Considers stakeholder perspectives'
                ]
            }
        }
    
    def save_draft(self, session_id: str, draft_data: Dict[str, str]) -> StudentProgress:
        """
        Save student's work-in-progress with progress tracking
        Auto-save functionality for draft protection
        """
        print(f"💾 Saving draft for session: {session_id}")
        
        # Calculate completion metrics
        sections_completed = sum(1 for text in draft_data.values() if text.strip())
        total_sections = 4
        completion_percentage = (sections_completed / total_sections) * 100
        
        # Estimate time remaining based on typical writing speed
        words_written = sum(len(text.split()) for text in draft_data.values())
        target_words = 400  # Total target across all sections
        estimated_remaining = max(0, (target_words - words_written) // 20)  # ~20 words per minute
        
        progress = StudentProgress(
            sections_completed=sections_completed,
            total_sections=total_sections,
            completion_percentage=completion_percentage,
            estimated_time_remaining=estimated_remaining,
            last_saved=datetime.now().isoformat()
        )
        
        print(f"   📊 Progress: {completion_percentage:.0f}% complete ({sections_completed}/{total_sections} sections)")
        print(f"   ⏱️  Estimated time remaining: {estimated_remaining} minutes")
        
        return progress
    
    def submit_for_feedback(self, session_id: str, student_smap: Dict[str, str]) -> Dict[str, Any]:
        """
        Submit completed SMAP for AI feedback
        Validates completeness and prepares for Feature 3 (Feedback Mode)
        """
        print(f"📤 SUBMITTING STUDENT SMAP - Session: {session_id}")
        
        # Validate submission completeness
        validation_results = self._validate_submission(student_smap)
        
        if not validation_results['is_complete']:
            return {
                'success': False,
                'error': 'incomplete_submission',
                'validation': validation_results,
                'message': f"Please complete the following sections: {', '.join(validation_results['empty_sections'])}"
            }
        
        # Calculate quality metrics
        quality_assessment = self._assess_submission_quality(student_smap)
        
        print(f"✅ Submission validated and ready for AI feedback")
        print(f"   📝 Total words: {quality_assessment['total_words']}")
        print(f"   📊 Quality score: {quality_assessment['preliminary_score']}/100")
        
        return {
            'success': True,
            'submitted': True,
            'validation': validation_results,
            'quality': quality_assessment,
            'ready_for_feedback': True,
            'message': "SMAP analysis submitted successfully! AI feedback will be generated."
        }
    
    def _validate_submission(self, student_smap: Dict[str, str]) -> Dict[str, Any]:
        """Validate that student has completed all required sections"""
        
        empty_sections = []
        section_word_counts = {}
        
        for section, content in student_smap.items():
            word_count = len(content.strip().split()) if content.strip() else 0
            section_word_counts[section] = word_count
            
            if word_count < 10:  # Minimum threshold
                empty_sections.append(section)
        
        return {
            'is_complete': len(empty_sections) == 0,
            'empty_sections': empty_sections,
            'section_word_counts': section_word_counts,
            'total_words': sum(section_word_counts.values()),
            'meets_minimum_length': sum(section_word_counts.values()) >= 200
        }
    
    def _assess_submission_quality(self, student_smap: Dict[str, str]) -> Dict[str, Any]:
        """Preliminary quality assessment before AI feedback"""
        
        quality_metrics = {}
        total_words = 0
        
        for section, content in student_smap.items():
            word_count = len(content.split())
            total_words += word_count
            
            # Basic quality indicators
            has_numbers = any(char.isdigit() for char in content)
            has_percentages = '%' in content
            has_financial_terms = any(term in content.lower() for term in ['revenue', 'profit', 'margin', 'ratio', 'growth'])
            
            quality_metrics[section] = {
                'word_count': word_count,
                'has_numbers': has_numbers,
                'has_percentages': has_percentages,
                'has_financial_terms': has_financial_terms,
                'section_score': self._calculate_section_score(content, section)
            }
        
        # Overall preliminary score
        section_scores = [metrics['section_score'] for metrics in quality_metrics.values()]
        preliminary_score = sum(section_scores) / len(section_scores)
        
        return {
            'total_words': total_words,
            'section_metrics': quality_metrics,
            'preliminary_score': round(preliminary_score, 1),
            'strengths': self._identify_strengths(quality_metrics),
            'areas_for_improvement': self._identify_improvements(quality_metrics)
        }
    
    def _calculate_section_score(self, content: str, section: str) -> float:
        """Calculate preliminary score for individual section"""
        
        if not content.strip():
            return 0
        
        score = 50  # Base score
        content_lower = content.lower()
        
        # Length appropriateness
        word_count = len(content.split())
        if section == 'subjective' and 80 <= word_count <= 200:
            score += 10
        elif section == 'metrics' and 60 <= word_count <= 150:
            score += 10
        elif section == 'assessment' and 100 <= word_count <= 200:
            score += 10
        elif section == 'plan' and 60 <= word_count <= 150:
            score += 10
        
        # Content quality indicators
        if any(char.isdigit() for char in content):
            score += 10  # Contains numbers
        
        if '%' in content or 'billion' in content_lower or 'million' in content_lower:
            score += 10  # Contains financial figures
        
        # Section-specific quality checks
        if section == 'metrics' and any(term in content_lower for term in ['revenue', 'income', 'margin', 'ratio']):
            score += 10
        
        if section == 'plan' and any(term in content_lower for term in ['monitor', 'track', 'assess', 'recommend']):
            score += 10
        
        return min(100, max(0, score))
    
    def _identify_strengths(self, quality_metrics: Dict[str, Any]) -> List[str]:
        """Identify strengths in student's submission"""
        
        strengths = []
        
        total_words = sum(metrics['word_count'] for metrics in quality_metrics.values())
        if total_words >= 300:
            strengths.append("Comprehensive analysis with good detail")
        
        if all(metrics['has_numbers'] for metrics in quality_metrics.values()):
            strengths.append("Good use of specific numbers and data")
        
        if quality_metrics.get('metrics', {}).get('has_financial_terms'):
            strengths.append("Appropriate use of financial terminology")
        
        if not strengths:
            strengths.append("Clear structure following SMAP framework")
        
        return strengths
    
    def _identify_improvements(self, quality_metrics: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        
        improvements = []
        
        # Check for missing elements
        sections_without_numbers = [section for section, metrics in quality_metrics.items() 
                                  if not metrics['has_numbers']]
        
        if 'metrics' in sections_without_numbers:
            improvements.append("Include more specific financial numbers in Metrics section")
        
        if quality_metrics.get('assessment', {}).get('word_count', 0) < 80:
            improvements.append("Expand Assessment section with deeper analysis")
        
        if quality_metrics.get('plan', {}).get('word_count', 0) < 60:
            improvements.append("Provide more specific recommendations in Plan section")
        
        if not improvements:
            improvements.append("Continue to enhance analytical depth and specificity")
        
        return improvements
    
    def _load_practice_templates(self) -> Dict[str, str]:
        """Load practice templates for each SMAP section"""
        
        return {
            'subjective_template': "Management [tone/confidence] regarding [key topics]. Emphasized [strategic priorities] and expressed [outlook] about [future prospects].",
            'metrics_template': "Revenue: $[amount] ([+/-]% YoY). Net income: $[amount] ([+/-]% YoY). Key ratios: [ratio1], [ratio2]. [Other metrics].",
            'assessment_template': "Performance demonstrates [strengths]. Key advantages include [factors]. Areas of attention: [concerns]. Overall: [conclusion].",
            'plan_template': "1. Monitor [key metric/trend]. 2. Assess [risk factor]. 3. Evaluate [opportunity]. 4. Recommend [action]."
        }
    
    def _load_writing_tips(self) -> Dict[str, List[str]]:
        """Load writing tips for each section"""
        
        return {
            'subjective': [
                "Start with management's overall tone",
                "Quote key phrases when impactful", 
                "Note changes from previous quarters"
            ],
            'metrics': [
                "Lead with headline numbers (revenue, profit)",
                "Always include year-over-year comparisons",
                "Use industry-specific ratios"
            ],
            'assessment': [
                "Connect metrics to business story",
                "Balance strengths with concerns",
                "Consider competitive context"
            ],
            'plan': [
                "Make recommendations specific and actionable",
                "Prioritize most critical items first",
                "Consider different stakeholder needs"
            ]
        }
    
    def _load_example_responses(self) -> Dict[str, str]:
        """Load example SMAP responses for reference"""
        
        return {
            'subjective_example': "Management expressed strong confidence in Q1 performance, emphasizing disciplined execution and strategic investments. CEO highlighted the company's fortress balance sheet and ability to navigate economic uncertainty while continuing to invest in growth opportunities.",
            'metrics_example': "Total revenue $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY). ROE improved to 17.8% vs 16.9% prior quarter. CET1 ratio strong at 15.9%. Efficiency ratio of 56% reflects operational discipline.",
            'assessment_example': "Results demonstrate fundamental strength with diversified revenue growth. Solid capital position provides flexibility during volatility while maintaining industry-leading profitability. Credit quality stable though provisions increased as expected.",
            'plan_example': "1. Monitor credit provision trends for early indicators. 2. Track interest rate sensitivity on NIM expansion. 3. Assess competitive positioning in key markets. 4. Evaluate investment opportunities from strong balance sheet."
        }

# Test the Practice Mode service
def test_practice_mode_service():
    """Test Feature 2 - Practice Mode functionality"""
    print("🧪 Testing Feature 2 - Practice Mode Service")
    print("=" * 50)
    
    # Mock enhanced SMAP data for testing
    class MockSMAP:
        company_name = "JPMorgan Chase & Co."
        ticker_symbol = "JPM"
        filing_type = "10-Q"
        filing_period = "Q1 2025"
        industry = "Banking"
    
    # Test Practice Mode service
    practice_service = PracticeModeService()
    practice_content = practice_service.enter_practice_mode("test_session_456", MockSMAP())
    
    print(f"✅ Practice Mode Content Created:")
    print(f"   Instructions: {len(practice_content.instructions['sections'])} sections")
    print(f"   Practice areas: {len(practice_content.practice_areas)}")
    print(f"   Tips available: {len(practice_content.instructions['general_tips'])}")
    
    # Test draft saving
    sample_draft = {
        "subjective": "Management was confident about results",
        "metrics": "Revenue $42.5B up 6.8%, ROE 17.8%", 
        "assessment": "Strong performance overall",
        "plan": "Monitor credit trends"
    }
    
    progress = practice_service.save_draft("test_session_456", sample_draft)
    print(f"   Draft progress: {progress.completion_percentage:.0f}% complete")
    
    # Test submission
    submission_result = practice_service.submit_for_feedback("test_session_456", sample_draft)
    print(f"   Submission: {'✅ Success' if submission_result['success'] else '❌ Failed'}")
    
    print("🎉 Feature 2 - Practice Mode test complete!")

if __name__ == "__main__":
    test_practice_mode_service()