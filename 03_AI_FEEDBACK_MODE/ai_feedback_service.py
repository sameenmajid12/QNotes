"""
FEATURE 3: AI FEEDBACK MODE (Comparison & Learning)
HackRU 2025 - 10Q Notes AI

Smart comparison engine:
- Side-by-side expert SMAP vs student SMAP analysis
- Section-by-section feedback with improvement suggestions
- Personalized learning tips based on strengths/weaknesses
- Integration with voice agent for detailed explanations

API Endpoints:
- POST /api/session/{id}/feedback/generate
- GET /api/session/{id}/feedback
- POST /api/session/{id}/feedback/voice-explanation
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class ComparisonAnalysis:
    """Data structure for detailed comparison analysis"""
    section: str
    student_content: str
    expert_content: str
    alignment_score: float
    key_differences: List[str]
    strengths: List[str]
    improvements: List[str]
    missing_elements: List[str]

@dataclass
class FeedbackReport:
    """Comprehensive feedback report structure"""
    session_id: str
    overall_score: float
    section_analyses: Dict[str, ComparisonAnalysis]
    learning_priorities: List[str]
    personalized_tips: List[str]
    next_steps: List[str]
    estimated_improvement_time: int

class AIFeedbackService:
    """
    Feature 3: AI Feedback Mode Implementation
    Intelligent comparison and personalized learning feedback system
    """
    
    def __init__(self):
        """Initialize AI Feedback service"""
        print("🤖 AI Feedback Mode Service - Feature 3 Initialized")
        self.feedback_templates = self._load_feedback_templates()
        self.scoring_rubrics = self._load_scoring_rubrics()
        self.improvement_strategies = self._load_improvement_strategies()
    
    def generate_comprehensive_feedback(self, session_id: str, student_smap: Dict[str, str], 
                                     expert_smap: Dict[str, str]) -> FeedbackReport:
        """
        Generate comprehensive AI feedback comparing student vs expert SMAP
        Main entry point for Feature 3 - AI Feedback Mode
        """
        print(f"🤖 GENERATING AI FEEDBACK - Session: {session_id}")
        print(f"   📊 Comparing student analysis with expert SMAP")
        print(f"   🎯 Creating personalized learning feedback")
        
        # Perform section-by-section analysis
        section_analyses = {}
        total_score = 0
        
        for section in ['subjective', 'metrics', 'assessment', 'plan']:
            analysis = self._analyze_section_comparison(
                section, 
                student_smap.get(section, ""), 
                expert_smap.get(section, "")
            )
            section_analyses[section] = analysis
            total_score += analysis.alignment_score
        
        overall_score = total_score / 4  # Average across sections
        
        # Generate personalized learning insights
        learning_priorities = self._identify_learning_priorities(section_analyses)
        personalized_tips = self._generate_personalized_tips(section_analyses, overall_score)
        next_steps = self._recommend_next_steps(section_analyses, overall_score)
        improvement_time = self._estimate_improvement_timeline(section_analyses)
        
        feedback_report = FeedbackReport(
            session_id=session_id,
            overall_score=round(overall_score, 1),
            section_analyses=section_analyses,
            learning_priorities=learning_priorities,
            personalized_tips=personalized_tips,
            next_steps=next_steps,
            estimated_improvement_time=improvement_time
        )
        
        print(f"✅ AI Feedback generated successfully")
        print(f"   📈 Overall score: {overall_score:.1f}/100")
        print(f"   🎯 Learning priorities identified: {len(learning_priorities)}")
        print(f"   💡 Personalized tips: {len(personalized_tips)}")
        
        return feedback_report
    
    def _analyze_section_comparison(self, section: str, student_content: str, 
                                  expert_content: str) -> ComparisonAnalysis:
        """Perform detailed analysis comparing student vs expert content for a section"""
        
        print(f"   🔍 Analyzing {section.upper()} section...")
        
        # Calculate alignment score based on multiple factors
        alignment_score = self._calculate_alignment_score(section, student_content, expert_content)
        
        # Identify key differences
        key_differences = self._identify_key_differences(section, student_content, expert_content)
        
        # Identify strengths in student's work
        strengths = self._identify_section_strengths(section, student_content, expert_content)
        
        # Identify improvement opportunities
        improvements = self._identify_section_improvements(section, student_content, expert_content)
        
        # Identify missing elements
        missing_elements = self._identify_missing_elements(section, student_content, expert_content)
        
        return ComparisonAnalysis(
            section=section,
            student_content=student_content,
            expert_content=expert_content,
            alignment_score=alignment_score,
            key_differences=key_differences,
            strengths=strengths,
            improvements=improvements,
            missing_elements=missing_elements
        )
    
    def _calculate_alignment_score(self, section: str, student_content: str, expert_content: str) -> float:
        """Calculate how well student content aligns with expert analysis"""
        
        if not student_content.strip():
            return 0
        
        score = 40  # Base score for attempting the section
        
        # Content length appropriateness (10 points)
        student_words = len(student_content.split())
        expert_words = len(expert_content.split())
        
        if expert_words > 0:
            length_ratio = min(student_words / expert_words, 1.0)
            if length_ratio >= 0.7:  # At least 70% of expert length
                score += 10
            elif length_ratio >= 0.5:
                score += 5
        
        # Key concept coverage (20 points)
        concept_coverage = self._calculate_concept_coverage(section, student_content, expert_content)
        score += concept_coverage * 20
        
        # Financial data accuracy (15 points)
        data_accuracy = self._calculate_data_accuracy(student_content, expert_content)
        score += data_accuracy * 15
        
        # Professional language and structure (10 points)
        language_score = self._assess_language_quality(student_content)
        score += language_score * 10
        
        # Section-specific criteria (5 points)
        section_score = self._assess_section_specific_criteria(section, student_content, expert_content)
        score += section_score * 5
        
        return min(100, max(0, score))
    
    def _calculate_concept_coverage(self, section: str, student_content: str, expert_content: str) -> float:
        """Calculate what percentage of key concepts are covered"""
        
        # Extract key concepts from expert content
        expert_concepts = self._extract_key_concepts(section, expert_content)
        
        if not expert_concepts:
            return 0.5  # Default score if no concepts identified
        
        # Check how many concepts are covered in student content
        covered_concepts = 0
        student_lower = student_content.lower()
        
        for concept in expert_concepts:
            if any(keyword in student_lower for keyword in concept['keywords']):
                covered_concepts += 1
        
        return covered_concepts / len(expert_concepts)
    
    def _extract_key_concepts(self, section: str, expert_content: str) -> List[Dict[str, Any]]:
        """Extract key financial concepts from expert content"""
        
        concepts = []
        content_lower = expert_content.lower()
        
        # Common financial concepts by section
        concept_patterns = {
            'subjective': [
                {'name': 'Management Tone', 'keywords': ['confident', 'optimistic', 'cautious', 'positive', 'strong']},
                {'name': 'Strategic Focus', 'keywords': ['strategy', 'initiative', 'priority', 'focus', 'transformation']},
                {'name': 'Outlook', 'keywords': ['outlook', 'guidance', 'expectations', 'forecast', 'future']}
            ],
            'metrics': [
                {'name': 'Revenue Growth', 'keywords': ['revenue', 'sales', 'income', 'growth', '%']},
                {'name': 'Profitability', 'keywords': ['profit', 'margin', 'earnings', 'roe', 'roa']},
                {'name': 'Financial Ratios', 'keywords': ['ratio', 'leverage', 'liquidity', 'efficiency', 'return']}
            ],
            'assessment': [
                {'name': 'Performance Analysis', 'keywords': ['performance', 'results', 'strong', 'weak', 'improved']},
                {'name': 'Competitive Position', 'keywords': ['competitive', 'market', 'position', 'advantage', 'peer']},
                {'name': 'Risk Assessment', 'keywords': ['risk', 'concern', 'challenge', 'headwind', 'pressure']}
            ],
            'plan': [
                {'name': 'Monitoring', 'keywords': ['monitor', 'track', 'watch', 'follow', 'observe']},
                {'name': 'Recommendations', 'keywords': ['recommend', 'suggest', 'advise', 'consider', 'evaluate']},
                {'name': 'Next Steps', 'keywords': ['next', 'action', 'step', 'plan', 'strategy']}
            ]
        }
        
        section_concepts = concept_patterns.get(section, [])
        
        for concept in section_concepts:
            if any(keyword in content_lower for keyword in concept['keywords']):
                concepts.append(concept)
        
        return concepts
    
    def _calculate_data_accuracy(self, student_content: str, expert_content: str) -> float:
        """Calculate accuracy of financial data and numbers"""
        
        # Extract numbers from both contents
        student_numbers = re.findall(r'\d+\.?\d*', student_content)
        expert_numbers = re.findall(r'\d+\.?\d*', expert_content)
        
        if not expert_numbers:
            return 0.5  # Default score if no numbers to compare
        
        # Simple heuristic: check if student includes similar numbers
        matching_numbers = 0
        for expert_num in expert_numbers:
            if expert_num in student_numbers:
                matching_numbers += 1
        
        accuracy = matching_numbers / len(expert_numbers) if expert_numbers else 0.5
        return min(1.0, accuracy)
    
    def _assess_language_quality(self, content: str) -> float:
        """Assess professional language and structure quality"""
        
        if not content.strip():
            return 0
        
        score = 0.5  # Base score
        
        # Check for professional financial terms
        financial_terms = ['revenue', 'profit', 'margin', 'growth', 'performance', 'capital', 
                          'earnings', 'ratio', 'strategy', 'market', 'competitive', 'analysis']
        
        content_lower = content.lower()
        terms_used = sum(1 for term in financial_terms if term in content_lower)
        
        if terms_used >= 3:
            score += 0.3
        elif terms_used >= 1:
            score += 0.1
        
        # Check for quantitative elements (numbers, percentages)
        if re.search(r'\d+', content):
            score += 0.1
        
        if '%' in content:
            score += 0.1
        
        return min(1.0, score)
    
    def _assess_section_specific_criteria(self, section: str, student_content: str, expert_content: str) -> float:
        """Assess section-specific quality criteria"""
        
        content_lower = student_content.lower()
        
        if section == 'subjective':
            # Look for management perspective indicators
            mgmt_indicators = ['management', 'ceo', 'leadership', 'executives', 'tone', 'confident']
            return min(1.0, sum(0.2 for indicator in mgmt_indicators if indicator in content_lower))
        
        elif section == 'metrics':
            # Look for quantitative data
            has_currency = '$' in student_content or 'billion' in content_lower or 'million' in content_lower
            has_percentages = '%' in student_content
            has_comparisons = 'vs' in student_content or 'compared' in content_lower
            return (has_currency * 0.4 + has_percentages * 0.3 + has_comparisons * 0.3)
        
        elif section == 'assessment':
            # Look for analytical depth
            analytical_terms = ['demonstrates', 'indicates', 'suggests', 'reflects', 'implies']
            analysis_score = sum(0.2 for term in analytical_terms if term in content_lower)
            return min(1.0, analysis_score)
        
        elif section == 'plan':
            # Look for actionable recommendations
            action_words = ['monitor', 'track', 'assess', 'evaluate', 'consider', 'recommend']
            action_score = sum(0.17 for word in action_words if word in content_lower)
            return min(1.0, action_score)
        
        return 0.5  # Default score
    
    def _identify_key_differences(self, section: str, student_content: str, expert_content: str) -> List[str]:
        """Identify key differences between student and expert analysis"""
        
        differences = []
        
        # Length difference
        student_words = len(student_content.split())
        expert_words = len(expert_content.split())
        
        if expert_words > 0 and student_words < expert_words * 0.6:
            differences.append(f"Analysis is shorter than expected ({student_words} vs {expert_words} words)")
        
        # Content focus differences
        expert_lower = expert_content.lower()
        student_lower = student_content.lower()
        
        if section == 'metrics':
            if '$' in expert_content and '$' not in student_content:
                differences.append("Missing specific dollar amounts mentioned by expert")
            if '%' in expert_content and '%' not in student_content:
                differences.append("Missing percentage figures highlighted by expert")
        
        if section == 'subjective':
            mgmt_terms = ['management', 'ceo', 'leadership', 'executives']
            if any(term in expert_lower for term in mgmt_terms) and not any(term in student_lower for term in mgmt_terms):
                differences.append("Less focus on management perspective compared to expert")
        
        if section == 'assessment':
            risk_terms = ['risk', 'concern', 'challenge', 'headwind']
            if any(term in expert_lower for term in risk_terms) and not any(term in student_lower for term in risk_terms):
                differences.append("Missing risk assessment covered by expert")
        
        if section == 'plan':
            if expert_content.count('.') > student_content.count('.'):
                differences.append("Fewer specific recommendations than expert provided")
        
        if not differences:
            differences.append("Generally good alignment with expert analysis")
        
        return differences[:3]  # Limit to top 3 differences
    
    def _identify_section_strengths(self, section: str, student_content: str, expert_content: str) -> List[str]:
        """Identify strengths in student's section analysis"""
        
        strengths = []
        content_lower = student_content.lower()
        
        # Universal strengths
        if len(student_content.split()) >= 50:
            strengths.append("Good level of detail and analysis")
        
        if re.search(r'\d+', student_content):
            strengths.append("Includes specific quantitative data")
        
        # Section-specific strengths
        if section == 'subjective':
            tone_words = ['confident', 'optimistic', 'strong', 'positive', 'cautious']
            if any(word in content_lower for word in tone_words):
                strengths.append("Captures management tone and sentiment")
        
        elif section == 'metrics':
            if '%' in student_content:
                strengths.append("Uses percentage comparisons effectively")
            if 'vs' in student_content or 'compared' in content_lower:
                strengths.append("Includes comparative analysis")
        
        elif section == 'assessment':
            insight_words = ['demonstrates', 'indicates', 'reflects', 'suggests']
            if any(word in content_lower for word in insight_words):
                strengths.append("Shows analytical thinking and insight")
        
        elif section == 'plan':
            numbered_list = bool(re.search(r'\d+\.', student_content))
            if numbered_list:
                strengths.append("Well-organized recommendations with clear structure")
        
        if not strengths:
            strengths.append("Follows the required SMAP framework structure")
        
        return strengths[:2]  # Limit to top 2 strengths per section
    
    def _identify_section_improvements(self, section: str, student_content: str, expert_content: str) -> List[str]:
        """Identify specific improvement opportunities"""
        
        improvements = []
        content_lower = student_content.lower()
        expert_lower = expert_content.lower()
        
        # Universal improvements
        word_count = len(student_content.split())
        if word_count < 40:
            improvements.append("Expand analysis with more detail and context")
        
        if not re.search(r'\d+', student_content) and re.search(r'\d+', expert_content):
            improvements.append("Include more specific financial numbers and data")
        
        # Section-specific improvements
        if section == 'subjective':
            if 'management' not in content_lower and 'management' in expert_lower:
                improvements.append("Focus more on management's perspective and messaging")
        
        elif section == 'metrics':
            if '%' not in student_content and '%' in expert_content:
                improvements.append("Add percentage growth rates and comparisons")
            if 'yoy' not in content_lower and ('year' in expert_lower or 'yoy' in expert_lower):
                improvements.append("Include year-over-year trend analysis")
        
        elif section == 'assessment':
            if len([w for w in content_lower.split() if w in ['strong', 'weak', 'good', 'poor', 'excellent']]) == 0:
                improvements.append("Provide clearer performance judgments and evaluations")
        
        elif section == 'plan':
            if not re.search(r'\d+\.', student_content):
                improvements.append("Structure recommendations as numbered, actionable items")
        
        return improvements[:2]  # Limit to top 2 improvements per section
    
    def _identify_missing_elements(self, section: str, student_content: str, expert_content: str) -> List[str]:
        """Identify key elements present in expert analysis but missing from student work"""
        
        missing = []
        content_lower = student_content.lower()
        expert_lower = expert_content.lower()
        
        # Extract key phrases from expert content that are missing from student
        if section == 'metrics':
            expert_numbers = re.findall(r'\$[\d.,]+\s*(?:billion|million|B|M)', expert_content)
            student_numbers = re.findall(r'\$[\d.,]+\s*(?:billion|million|B|M)', student_content)
            
            for num in expert_numbers:
                if num not in student_content:
                    missing.append(f"Key financial figure: {num}")
                    break  # Only show one example
        
        # Look for important keywords in expert but missing in student
        important_keywords = {
            'subjective': ['guidance', 'outlook', 'strategy', 'priorities', 'transformation'],
            'metrics': ['margin', 'ratio', 'efficiency', 'return', 'leverage'],
            'assessment': ['competitive', 'market', 'trends', 'risks', 'opportunities'],
            'plan': ['monitor', 'evaluate', 'assess', 'track', 'recommend']
        }
        
        section_keywords = important_keywords.get(section, [])
        missing_keywords = [kw for kw in section_keywords if kw in expert_lower and kw not in content_lower]
        
        if missing_keywords:
            missing.append(f"Key concepts: {', '.join(missing_keywords[:2])}")
        
        return missing[:2]  # Limit to top 2 missing elements
    
    def _identify_learning_priorities(self, section_analyses: Dict[str, ComparisonAnalysis]) -> List[str]:
        """Identify the most important areas for learning improvement"""
        
        priorities = []
        
        # Find lowest scoring sections
        section_scores = [(section, analysis.alignment_score) for section, analysis in section_analyses.items()]
        section_scores.sort(key=lambda x: x[1])  # Sort by score, lowest first
        
        # Priority 1: Lowest scoring section
        if section_scores:
            lowest_section, lowest_score = section_scores[0]
            if lowest_score < 60:
                priorities.append(f"Strengthen {lowest_section.title()} section analysis (current score: {lowest_score:.0f})")
        
        # Priority 2: Common missing elements
        all_missing = []
        for analysis in section_analyses.values():
            all_missing.extend(analysis.missing_elements)
        
        if 'Key financial figure' in ' '.join(all_missing):
            priorities.append("Include more specific financial data and figures")
        
        # Priority 3: Section with most improvements needed
        improvement_counts = [(section, len(analysis.improvements)) for section, analysis in section_analyses.items()]
        improvement_counts.sort(key=lambda x: x[1], reverse=True)
        
        if improvement_counts and improvement_counts[0][1] > 1:
            section_with_most_improvements = improvement_counts[0][0]
            priorities.append(f"Focus on improving analytical depth in {section_with_most_improvements.title()} section")
        
        # Ensure we have at least one priority
        if not priorities:
            priorities.append("Continue developing comprehensive financial analysis skills")
        
        return priorities[:3]  # Limit to top 3 priorities
    
    def _generate_personalized_tips(self, section_analyses: Dict[str, ComparisonAnalysis], overall_score: float) -> List[str]:
        """Generate personalized learning tips based on performance"""
        
        tips = []
        
        # Overall performance tips
        if overall_score >= 80:
            tips.append("🌟 Excellent work! Focus on fine-tuning analytical insights and industry-specific terminology")
        elif overall_score >= 60:
            tips.append("📈 Good foundation! Work on expanding analysis depth and including more specific data points")
        else:
            tips.append("💪 Keep practicing! Focus on structure, key concepts, and quantitative analysis")
        
        # Section-specific tips based on weakest areas
        section_scores = [(section, analysis.alignment_score) for section, analysis in section_analyses.items()]
        section_scores.sort(key=lambda x: x[1])
        
        if section_scores:
            weakest_section = section_scores[0][0]
            
            section_tips = {
                'subjective': "💡 For Subjective: Focus on management's tone, key messages, and strategic priorities",
                'metrics': "📊 For Metrics: Always include specific numbers, percentages, and year-over-year comparisons",
                'assessment': "🔍 For Assessment: Connect the data to business implications and competitive context",
                'plan': "🎯 For Plan: Make recommendations specific, actionable, and prioritized"
            }
            
            if weakest_section in section_tips:
                tips.append(section_tips[weakest_section])
        
        # Study recommendations based on performance
        if overall_score < 70:
            tips.append("📚 Study Tip: Review sample SMAP analyses from similar companies in this industry")
        
        tips.append("🎧 Try using the Voice Agent for detailed explanations of any concepts you found challenging")
        
        return tips[:4]  # Limit to 4 tips for readability
    
    def _recommend_next_steps(self, section_analyses: Dict[str, ComparisonAnalysis], overall_score: float) -> List[str]:
        """Recommend specific next steps for improvement"""
        
        next_steps = []
        
        # Immediate next steps based on performance
        if overall_score >= 75:
            next_steps.append("🎓 Practice with a different company/industry to broaden your analytical skills")
            next_steps.append("📈 Focus on developing more nuanced insights and forward-looking analysis")
        elif overall_score >= 50:
            next_steps.append("🔄 Retry this analysis incorporating the feedback suggestions")
            next_steps.append("📖 Study the expert analysis to understand the analytical approach")
        else:
            next_steps.append("📚 Review SMAP framework basics and practice with guided templates")
            next_steps.append("💬 Use Voice Agent to get explanations of key financial concepts")
        
        # Section-specific next steps
        sections_needing_work = [section for section, analysis in section_analyses.items() 
                               if analysis.alignment_score < 60]
        
        if sections_needing_work:
            next_steps.append(f"🎯 Prioritize improving: {', '.join(sections_needing_work)} sections")
        
        # Learning resources
        next_steps.append("🎤 Ask the Voice Agent to explain any challenging concepts from this analysis")
        
        return next_steps[:4]  # Limit to 4 next steps
    
    def _estimate_improvement_timeline(self, section_analyses: Dict[str, ComparisonAnalysis]) -> int:
        """Estimate time needed for significant improvement in minutes"""
        
        # Base time estimates per section based on score
        total_time = 0
        
        for analysis in section_analyses.values():
            if analysis.alignment_score < 50:
                total_time += 15  # 15 minutes for major improvement needed
            elif analysis.alignment_score < 75:
                total_time += 8   # 8 minutes for moderate improvement
            else:
                total_time += 3   # 3 minutes for minor refinement
        
        # Add base review time
        total_time += 10  # 10 minutes for overall review and practice
        
        return min(60, max(15, total_time))  # Between 15-60 minutes
    
    def prepare_voice_explanation(self, session_id: str, feedback_report: FeedbackReport, 
                                section: Optional[str] = None) -> Dict[str, Any]:
        """
        Prepare content for Voice Agent explanation
        Integration point with Feature 4 (Voice Agent)
        """
        print(f"🎤 Preparing voice explanation for session: {session_id}")
        
        if section:
            # Section-specific explanation
            section_analysis = feedback_report.section_analyses.get(section)
            if not section_analysis:
                return {"error": "Section not found"}
            
            voice_content = {
                "type": "section_explanation",
                "section": section,
                "content": f"Let me explain the feedback for your {section.title()} section analysis.",
                "key_points": [
                    f"Your alignment score was {section_analysis.alignment_score:.0f} out of 100",
                    f"Strengths: {', '.join(section_analysis.strengths)}",
                    f"Areas for improvement: {', '.join(section_analysis.improvements)}",
                    f"Key differences from expert: {', '.join(section_analysis.key_differences[:2])}"
                ],
                "detailed_explanation": self._create_section_explanation(section_analysis)
            }
        else:
            # Overall feedback explanation
            voice_content = {
                "type": "overall_explanation", 
                "content": f"Here's your comprehensive feedback overview.",
                "key_points": [
                    f"Overall score: {feedback_report.overall_score:.0f} out of 100",
                    f"Top learning priorities: {', '.join(feedback_report.learning_priorities[:2])}",
                    f"Estimated improvement time: {feedback_report.estimated_improvement_time} minutes"
                ],
                "detailed_explanation": self._create_overall_explanation(feedback_report)
            }
        
        print(f"   🎯 Voice content prepared for {'section: ' + section if section else 'overall feedback'}")
        return voice_content
    
    def _create_section_explanation(self, analysis: ComparisonAnalysis) -> str:
        """Create detailed explanation for a specific section"""
        
        explanation = f"For your {analysis.section.title()} section, here's what I found. "
        
        if analysis.strengths:
            explanation += f"Your strengths include: {'. '.join(analysis.strengths)}. "
        
        if analysis.improvements:
            explanation += f"To improve, consider: {'. '.join(analysis.improvements)}. "
        
        if analysis.missing_elements:
            explanation += f"You might also add: {'. '.join(analysis.missing_elements)}. "
        
        explanation += f"This would help you move closer to the expert-level analysis approach."
        
        return explanation
    
    def _create_overall_explanation(self, feedback_report: FeedbackReport) -> str:
        """Create detailed explanation for overall feedback"""
        
        explanation = f"Your overall performance scored {feedback_report.overall_score:.0f} out of 100. "
        
        if feedback_report.overall_score >= 75:
            explanation += "This is strong work that demonstrates good analytical thinking. "
        elif feedback_report.overall_score >= 50:
            explanation += "You're on the right track with room for meaningful improvement. "
        else:
            explanation += "There's significant opportunity to strengthen your analysis. "
        
        if feedback_report.learning_priorities:
            explanation += f"Your top priorities should be: {'. '.join(feedback_report.learning_priorities[:2])}. "
        
        explanation += f"With focused practice, you can improve these areas in about {feedback_report.estimated_improvement_time} minutes."
        
        return explanation
    
    def _load_feedback_templates(self) -> Dict[str, str]:
        """Load feedback message templates"""
        
        return {
            'high_performance': "Excellent analytical work! Your SMAP demonstrates strong understanding of financial analysis principles.",
            'good_performance': "Solid foundation with good insights. Focus on expanding depth and including more specific data.",
            'needs_improvement': "Good effort! Let's work on strengthening your analytical approach and attention to key metrics.",
            'section_strength': "This section shows {strengths} which demonstrates good analytical thinking.",
            'section_improvement': "To enhance this section, consider {improvements} for more comprehensive analysis."
        }
    
    def _load_scoring_rubrics(self) -> Dict[str, Dict[str, int]]:
        """Load scoring rubrics for each section"""
        
        return {
            'subjective': {
                'management_perspective': 25,
                'tone_identification': 20,
                'strategic_themes': 25,
                'forward_guidance': 20,
                'language_quality': 10
            },
            'metrics': {
                'key_financial_data': 30,
                'growth_comparisons': 25,
                'industry_ratios': 25,
                'quantitative_accuracy': 20
            },
            'assessment': {
                'performance_analysis': 30,
                'business_implications': 25,
                'risk_identification': 25,
                'competitive_context': 20
            },
            'plan': {
                'actionable_recommendations': 35,
                'monitoring_priorities': 25,
                'stakeholder_considerations': 20,
                'implementation_specifics': 20
            }
        }
    
    def _load_improvement_strategies(self) -> Dict[str, List[str]]:
        """Load improvement strategies for different performance levels"""
        
        return {
            'beginner': [
                "Focus on SMAP structure and framework understanding",
                "Practice identifying key financial metrics",
                "Study management tone and messaging patterns",
                "Learn basic financial ratio interpretation"
            ],
            'intermediate': [
                "Develop deeper analytical insights",
                "Enhance quantitative analysis skills", 
                "Improve business implication assessment",
                "Strengthen recommendation specificity"
            ],
            'advanced': [
                "Refine industry-specific analysis techniques",
                "Develop forward-looking perspective",
                "Enhance competitive benchmarking",
                "Master nuanced financial interpretation"
            ]
        }

# Test the AI Feedback service
def test_ai_feedback_service():
    """Test Feature 3 - AI Feedback functionality"""
    print("🧪 Testing Feature 3 - AI Feedback Service")
    print("=" * 50)
    
    # Mock SMAP data for testing
    student_smap = {
        "subjective": "Management was confident about Q1 results with strong revenue growth.",
        "metrics": "Revenue $42.5B up 6.8% YoY. Net income $13.4B up 6.1%. ROE 17.8%.",
        "assessment": "Strong performance with good fundamentals and solid balance sheet.",
        "plan": "Monitor credit trends and assess competitive position going forward."
    }
    
    expert_smap = {
        "subjective": "Management expressed strong confidence in Q1 performance, emphasizing disciplined execution and robust revenue growth across key segments. CEO highlighted the fortress balance sheet strategy and ability to navigate economic uncertainty while continuing strategic investments.",
        "metrics": "Total revenue $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY). ROE improved to 17.8% vs 16.9% prior quarter. CET1 ratio strong at 15.9%. Net interest margin 2.45% (+12 bps). Efficiency ratio 56% shows operational discipline.",
        "assessment": "Results demonstrate fundamental strength with diversified revenue growth and industry-leading profitability metrics. The fortress balance sheet provides strategic flexibility during economic volatility. Credit quality remains solid though provisions increased as expected for normalized environment.",
        "plan": "1. Monitor credit provision trends for early cycle indicators. 2. Track interest rate sensitivity impact on NIM expansion. 3. Evaluate investment banking recovery timeline vs peers. 4. Assess digital transformation ROI and market share gains."
    }
    
    # Test AI Feedback service
    feedback_service = AIFeedbackService()
    feedback_report = feedback_service.generate_comprehensive_feedback("test_session_789", student_smap, expert_smap)
    
    print(f"✅ AI Feedback Report Generated:")
    print(f"   Overall Score: {feedback_report.overall_score}/100")
    print(f"   Section Analyses: {len(feedback_report.section_analyses)}")
    print(f"   Learning Priorities: {len(feedback_report.learning_priorities)}")
    print(f"   Personalized Tips: {len(feedback_report.personalized_tips)}")
    print(f"   Improvement Time: {feedback_report.estimated_improvement_time} minutes")
    
    # Test voice explanation preparation
    voice_content = feedback_service.prepare_voice_explanation("test_session_789", feedback_report, "metrics")
    print(f"   Voice Explanation: {'✅ Ready' if 'detailed_explanation' in voice_content else '❌ Failed'}")
    
    print("🎉 Feature 3 - AI Feedback test complete!")

if __name__ == "__main__":
    test_ai_feedback_service()