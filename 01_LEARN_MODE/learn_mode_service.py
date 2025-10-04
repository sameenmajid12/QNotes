"""
FEATURE 1: LEARN MODE (Read & Hover)
HackRU 2025 - 10Q Notes AI

Interactive reading with AI assistance:
- Students see extracted sections with simplified explanations
- Hover over jargon/ratios → plain-English definitions
- Optional ElevenLabs voice synthesis reads sections aloud
- Interactive AI guidance throughout learning process

API Endpoints:
- GET /api/session/{id}/learn
- GET /api/session/{id}/learn/section/{section}
- POST /api/session/{id}/voice/synthesize
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

@dataclass
class LearnModeContent:
    """Data structure for Learn Mode content delivery"""
    session_id: str
    company_info: Dict[str, str]
    sections: Dict[str, Dict[str, Any]]
    progress_status: Dict[str, Any]
    hover_definitions: Dict[str, str]
    voice_synthesis_available: bool

class LearnModeService:
    """
    Feature 1: Learn Mode Implementation
    Interactive reading with AI explanations and hover definitions
    """
    
    def __init__(self):
        """Initialize Learn Mode service"""
        print("📖 Learn Mode Service - Feature 1 Initialized")
        self.hover_definitions = self._load_hover_definitions()
        self.section_explanations = self._load_section_explanations()
    
    def enter_learn_mode(self, session_id: str, enhanced_smap) -> LearnModeContent:
        """
        Enter Learn Mode - Main entry point for Feature 1
        Students see extracted sections with simplified explanations
        """
        print(f"📖 LEARN MODE ACTIVATED - Session: {session_id}")
        print(f"   🏢 Company: {enhanced_smap.company_name}")
        print(f"   📊 Filing: {enhanced_smap.filing_type} - {enhanced_smap.filing_period}")
        
        # Create interactive learning content
        learn_content = LearnModeContent(
            session_id=session_id,
            company_info={
                'name': enhanced_smap.company_name,
                'ticker': enhanced_smap.ticker_symbol,
                'industry': enhanced_smap.industry,
                'period': enhanced_smap.filing_period
            },
            sections=self._create_interactive_sections(enhanced_smap),
            progress_status={
                'sections_available': 4,
                'estimated_time': '15-20 minutes',
                'difficulty_level': 'Intermediate'
            },
            hover_definitions=self.hover_definitions,
            voice_synthesis_available=True
        )
        
        print("✅ Learn Mode content prepared with hover definitions")
        return learn_content
    
    def _create_interactive_sections(self, enhanced_smap) -> Dict[str, Dict[str, Any]]:
        """Create interactive sections with explanations and hover definitions"""
        
        return {
            'subjective': {
                'title': 'Subjective (S) - What Management Said',
                'explanation': 'This section captures the narrative and tone from management, including strategic priorities and forward-looking statements.',
                'content': enhanced_smap.subjective,
                'key_concepts': ['Management tone', 'Strategic priorities', 'Forward guidance', 'Qualitative insights'],
                'hover_definitions': {
                    'fortress balance sheet': 'Strong financial position with high capital levels and low risk',
                    'operational efficiency': 'How well the company uses resources to generate profits',
                    'regulatory headwinds': 'Government policy changes that may negatively impact business',
                    'digital transformation': 'Company-wide adoption of digital technology to improve operations'
                },
                'learning_objectives': [
                    'Identify management\'s key strategic priorities',
                    'Recognize tone and confidence level in communication',
                    'Understand qualitative business insights'
                ]
            },
            'metrics': {
                'title': 'Metrics (M) - Key Financial Numbers',
                'explanation': 'Hard numbers, ratios, and financial data extracted directly from the filing.',
                'content': enhanced_smap.metrics,
                'key_concepts': ['Revenue growth', 'Profitability ratios', 'Balance sheet strength', 'Per-share metrics'],
                'hover_definitions': {
                    'ROE': 'Return on Equity - measures how efficiently the company uses shareholder money to generate profits',
                    'CET1 ratio': 'Common Equity Tier 1 - bank\'s core capital as % of risk-weighted assets, shows financial strength',
                    'NIM': 'Net Interest Margin - spread between interest earned and paid by a bank',
                    'efficiency ratio': 'Operating expenses ÷ Revenue - lower is better for banks',
                    'provision for credit losses': 'Money set aside for potential loan defaults'
                },
                'learning_objectives': [
                    'Extract key financial ratios and metrics',
                    'Understand year-over-year growth trends', 
                    'Recognize industry-specific metrics'
                ]
            },
            'assessment': {
                'title': 'Assessment (A) - What It All Means',
                'explanation': 'AI interprets the numbers and narrative to identify trends, strengths, and concerns.',
                'content': enhanced_smap.assessment,
                'key_concepts': ['Trend analysis', 'Competitive positioning', 'Risk factors', 'Growth drivers'],
                'hover_definitions': {
                    'operating leverage': 'When revenue grows faster than expenses, boosting profit margins',
                    'credit provisions': 'Money banks set aside for potential loan losses',
                    'market share': 'Company\'s portion of total industry sales or revenue',
                    'competitive moat': 'Sustainable competitive advantages that protect profits'
                },
                'learning_objectives': [
                    'Connect quantitative data to business performance',
                    'Identify competitive advantages and risks',
                    'Analyze trends and their implications'
                ]
            },
            'plan': {
                'title': 'Plan (P) - Recommended Next Steps',
                'explanation': 'Specific actionable recommendations for investors, analysts, or advisors.',
                'content': enhanced_smap.plan,
                'key_concepts': ['Monitoring priorities', 'Investment decisions', 'Risk management', 'Action items'],
                'hover_definitions': {
                    'valuation multiple': 'Ratio comparing company price to financial metrics like earnings',
                    'peer analysis': 'Comparing company performance to similar competitors',
                    'catalyst': 'Event that could significantly impact stock price positively or negatively',
                    'due diligence': 'Comprehensive research before making investment decisions'
                },
                'learning_objectives': [
                    'Develop actionable investment recommendations',
                    'Prioritize key monitoring areas',
                    'Think like a professional analyst'
                ]
            }
        }
    
    def _load_hover_definitions(self) -> Dict[str, str]:
        """Load comprehensive financial jargon definitions for hover functionality"""
        
        return {
            # Basic Financial Terms
            'revenue': 'Total income generated from business operations before expenses',
            'net income': 'Profit after all expenses, taxes, and costs are subtracted from revenue',
            'cash flow': 'Net amount of cash moving in and out of the business',
            'assets': 'Everything the company owns that has value',
            'liabilities': 'Everything the company owes to others',
            'equity': 'Ownership value in the company (Assets - Liabilities)',
            
            # Financial Ratios
            'P/E ratio': 'Price-to-Earnings ratio - how much investors pay per dollar of earnings',
            'debt-to-equity': 'Total debt divided by shareholder equity - measures financial leverage',
            'current ratio': 'Current assets ÷ current liabilities - measures short-term liquidity',
            'gross margin': '(Revenue - Cost of goods sold) ÷ Revenue - shows profitability before other expenses',
            'operating margin': 'Operating income ÷ Revenue - shows efficiency of core business operations',
            
            # Banking-Specific Terms  
            'net interest margin': 'Difference between interest earned and paid, divided by assets',
            'loan loss provisions': 'Money set aside for loans that may not be repaid',
            'tier 1 capital': 'Core capital including common stock and retained earnings',
            'risk-weighted assets': 'Bank assets adjusted for their risk level',
            
            # Business Strategy Terms
            'market capitalization': 'Total value of company shares in the stock market',
            'working capital': 'Current assets minus current liabilities - operational liquidity',
            'EBITDA': 'Earnings before interest, taxes, depreciation, amortization',
            'free cash flow': 'Operating cash flow minus capital expenditures',
            
            # Economic Context
            'macroeconomic': 'Large-scale economic factors affecting the entire economy',
            'monetary policy': 'Central bank actions to control money supply and interest rates',
            'inflation': 'General increase in prices reducing purchasing power',
            'recession': 'Period of declining economic activity and GDP',
        }
    
    def _load_section_explanations(self) -> Dict[str, str]:
        """Load detailed explanations for each SMAP section"""
        
        return {
            'subjective_purpose': 'Captures management perspective, strategic direction, and qualitative insights that numbers alone cannot convey.',
            'metrics_purpose': 'Provides quantitative foundation for analysis with key performance indicators and financial health measures.',
            'assessment_purpose': 'Synthesizes qualitative and quantitative information to form comprehensive business evaluation.',
            'plan_purpose': 'Translates analysis into specific, actionable recommendations for stakeholders and decision-makers.'
        }
    
    def get_section_details(self, session_id: str, section: str, enhanced_smap) -> Dict[str, Any]:
        """
        Get detailed content for specific SMAP section
        Enhanced with learning objectives and interactive elements
        """
        learn_content = self.enter_learn_mode(session_id, enhanced_smap)
        
        if section not in learn_content.sections:
            raise ValueError(f"Section '{section}' not found")
        
        section_data = learn_content.sections[section]
        
        return {
            'success': True,
            'section': section,
            'data': section_data,
            'interactive_features': {
                'hover_definitions': section_data.get('hover_definitions', {}),
                'key_concepts': section_data.get('key_concepts', []),
                'learning_objectives': section_data.get('learning_objectives', []),
                'explanation': section_data.get('explanation', ''),
                'voice_synthesis_available': True
            },
            'study_tips': self._get_section_study_tips(section)
        }
    
    def _get_section_study_tips(self, section: str) -> List[str]:
        """Provide study tips specific to each SMAP section"""
        
        tips = {
            'subjective': [
                "Look for confident vs. cautious language from management",
                "Identify strategic priorities and future plans",
                "Note any changes in tone from previous quarters"
            ],
            'metrics': [
                "Focus on year-over-year growth rates",
                "Compare ratios to industry benchmarks", 
                "Look for trends across multiple quarters"
            ],
            'assessment': [
                "Connect the numbers to the business story",
                "Consider both strengths and potential risks",
                "Think about competitive positioning"
            ],
            'plan': [
                "Make recommendations specific and actionable",
                "Prioritize the most important monitoring areas",
                "Consider different stakeholder perspectives"
            ]
        }
        
        return tips.get(section, ["Study the content carefully and take notes"])

# Test the Learn Mode service
def test_learn_mode_service():
    """Test Feature 1 - Learn Mode functionality"""
    print("🧪 Testing Feature 1 - Learn Mode Service")
    print("=" * 50)
    
    # Mock enhanced SMAP data for testing
    class MockSMAP:
        company_name = "JPMorgan Chase & Co."
        ticker_symbol = "JPM"  
        filing_type = "10-Q"
        filing_period = "Q1 2025"
        industry = "Banking"
        subjective = "Management expressed strong confidence in Q1 results..."
        metrics = "Revenue $42.5B (+6.8% YoY), Net income $13.4B..."
        assessment = "Strong fundamental performance with solid capital position..."
        plan = "Monitor credit provisions, assess rate sensitivity..."
    
    # Test Learn Mode service
    learn_service = LearnModeService()
    learn_content = learn_service.enter_learn_mode("test_session_123", MockSMAP())
    
    print(f"✅ Learn Mode Content Created:")
    print(f"   Company: {learn_content.company_info['name']}")
    print(f"   Sections: {len(learn_content.sections)}")
    print(f"   Hover definitions: {len(learn_content.hover_definitions)}")
    print(f"   Voice available: {learn_content.voice_synthesis_available}")
    
    # Test section details
    section_details = learn_service.get_section_details("test_session_123", "subjective", MockSMAP())
    print(f"   Section details: {len(section_details['interactive_features']['hover_definitions'])} definitions")
    
    print("🎉 Feature 1 - Learn Mode test complete!")

if __name__ == "__main__":
    test_learn_mode_service()