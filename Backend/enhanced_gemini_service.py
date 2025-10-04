"""
Enhanced 10Q Notes AI - Advanced Gemini API Service
HackRU 2025 Project by azrabano

Enhanced Gemini service for MLH "Best Use of Gemini API" prize:
- Extracts Risk Factors, segment data, and structured metrics
- Powers advanced SMAP Notes with deeper financial insights
- Integrates with Snowflake for data storage and benchmarking
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FinancialMetrics:
    """Structured financial metrics for Snowflake storage"""
    # Core Financial Data
    total_revenue: Optional[float] = None
    revenue_yoy_growth: Optional[float] = None
    net_income: Optional[float] = None
    net_income_yoy_growth: Optional[float] = None
    
    # Banking Specific
    net_interest_income: Optional[float] = None
    noninterest_revenue: Optional[float] = None
    net_interest_margin: Optional[float] = None
    efficiency_ratio: Optional[float] = None
    return_on_equity: Optional[float] = None
    common_equity_tier1_ratio: Optional[float] = None
    provision_credit_losses: Optional[float] = None
    book_value_per_share: Optional[float] = None
    
    # General Ratios
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    
    # Per Share Data
    earnings_per_share: Optional[float] = None
    diluted_eps: Optional[float] = None
    
    # Extracted timestamp
    quarter: Optional[str] = None
    year: Optional[int] = None
    filing_date: Optional[str] = None

@dataclass
class RiskFactors:
    """Structured risk factors extraction"""
    credit_risk: List[str]
    market_risk: List[str]
    operational_risk: List[str]
    regulatory_risk: List[str]
    strategic_risk: List[str]
    other_risks: List[str]

@dataclass
class BusinessSegments:
    """Business segment performance data"""
    segments: Dict[str, Dict[str, float]]  # segment_name -> {revenue: x, income: y, etc}

@dataclass
class EnhancedSMAPNotes:
    """Enhanced SMAP notes with structured data for Snowflake"""
    # Original SMAP
    subjective: str
    metrics: str
    assessment: str
    plan: str
    
    # Enhanced structured data
    financial_metrics: FinancialMetrics
    risk_factors: RiskFactors
    business_segments: BusinessSegments
    
    # Metadata
    company_name: str = ""
    ticker_symbol: str = ""
    filing_type: str = ""
    filing_period: str = ""
    industry: str = ""
    market_cap_category: str = ""  # Large Cap, Mid Cap, etc.

class EnhancedGeminiService:
    """Enhanced Gemini service for advanced financial extraction"""
    
    def __init__(self):
        """Initialize enhanced Gemini service"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        print("✅ Enhanced Gemini API service initialized")
        print("🎯 Ready for advanced financial data extraction")
    
    def extract_structured_metrics(self, filing_text: str) -> FinancialMetrics:
        """Extract structured financial metrics using advanced Gemini prompting"""
        
        prompt = f"""
        You are a expert financial data analyst. Extract specific financial metrics from this SEC filing.
        
        SEC Filing Text:
        {filing_text[:10000]}
        
        Extract the following financial metrics and return as JSON. Use null for any metric not found.
        Be very precise with numbers - include decimal places where provided.
        
        {{
            "total_revenue": [revenue in millions, as number],
            "revenue_yoy_growth": [year-over-year growth percentage as decimal, e.g. 0.068 for 6.8%],
            "net_income": [net income in millions],
            "net_income_yoy_growth": [YoY growth as decimal],
            "net_interest_income": [for banks - NII in millions],
            "noninterest_revenue": [for banks - noninterest revenue in millions],
            "net_interest_margin": [NIM as decimal, e.g. 0.0274 for 2.74%],
            "efficiency_ratio": [efficiency ratio as decimal],
            "return_on_equity": [ROE as decimal, e.g. 0.178 for 17.8%],
            "common_equity_tier1_ratio": [CET1 ratio as decimal],
            "provision_credit_losses": [provisions in millions],
            "book_value_per_share": [BVPS as number],
            "debt_to_equity": [D/E ratio],
            "current_ratio": [current ratio],
            "gross_margin": [gross margin as decimal],
            "operating_margin": [operating margin as decimal],
            "earnings_per_share": [basic EPS],
            "diluted_eps": [diluted EPS],
            "quarter": ["Q1", "Q2", "Q3", "Q4"],
            "year": [year as integer, e.g. 2025],
            "filing_date": ["YYYY-MM-DD format if available"]
        }}
        
        Return ONLY valid JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean JSON response
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            metrics_data = json.loads(response_text)
            return FinancialMetrics(**metrics_data)
            
        except Exception as e:
            print(f"Error extracting financial metrics: {e}")
            return FinancialMetrics()
    
    def extract_risk_factors(self, filing_text: str) -> RiskFactors:
        """Extract and categorize risk factors from SEC filing"""
        
        prompt = f"""
        Extract and categorize risk factors from this SEC filing into specific categories.
        
        Filing Text:
        {filing_text[:8000]}
        
        Categorize risks into these specific buckets and return as JSON:
        
        {{
            "credit_risk": ["list of credit-related risks"],
            "market_risk": ["list of market/economic risks"],
            "operational_risk": ["list of operational/technology risks"],
            "regulatory_risk": ["list of regulatory/compliance risks"],
            "strategic_risk": ["list of strategic/competitive risks"],
            "other_risks": ["any other significant risks"]
        }}
        
        Each risk should be a concise 1-2 sentence description.
        Return ONLY valid JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean JSON response
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            risk_data = json.loads(response_text)
            return RiskFactors(**risk_data)
            
        except Exception as e:
            print(f"Error extracting risk factors: {e}")
            return RiskFactors(
                credit_risk=[], market_risk=[], operational_risk=[],
                regulatory_risk=[], strategic_risk=[], other_risks=[]
            )
    
    def extract_business_segments(self, filing_text: str) -> BusinessSegments:
        """Extract business segment performance data"""
        
        prompt = f"""
        Extract business segment financial performance from this SEC filing.
        
        Filing Text:
        {filing_text[:8000]}
        
        Return segment data as JSON in this format:
        
        {{
            "segments": {{
                "Consumer & Community Banking": {{
                    "revenue": [revenue in millions],
                    "net_income": [net income in millions],
                    "assets": [assets in millions if available]
                }},
                "Corporate & Investment Bank": {{
                    "revenue": [revenue in millions],
                    "net_income": [net income in millions]
                }}
            }}
        }}
        
        Include all segments mentioned with their financial metrics.
        Use null for unavailable metrics.
        Return ONLY valid JSON, no other text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean JSON response
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            segment_data = json.loads(response_text)
            return BusinessSegments(**segment_data)
            
        except Exception as e:
            print(f"Error extracting business segments: {e}")
            return BusinessSegments(segments={})
    
    def generate_enhanced_smap_notes(self, filing_text: str) -> EnhancedSMAPNotes:
        """Generate enhanced SMAP notes with structured data extraction"""
        
        print("🤖 Generating enhanced SMAP notes with structured data extraction...")
        
        # Extract company metadata first
        company_info = self._extract_company_metadata(filing_text)
        
        # Generate traditional SMAP notes
        smap_prompt = f"""
        Generate comprehensive SMAP notes for this SEC filing:
        
        {filing_text[:12000]}
        
        **SUBJECTIVE (S):**
        [Management tone, strategic priorities, forward-looking statements]
        
        **METRICS (M):**
        [Key financial numbers, ratios, YoY changes]
        
        **ASSESSMENT (A):**
        [Connect metrics to business performance, identify trends and risks]
        
        **PLAN (P):**
        [Specific actionable next steps for investors/analysts]
        """
        
        try:
            # Generate SMAP content
            smap_response = self.model.generate_content(smap_prompt)
            smap_sections = self._parse_smap_response(smap_response.text)
            
            # Extract structured data in parallel
            print("📊 Extracting structured financial metrics...")
            financial_metrics = self.extract_structured_metrics(filing_text)
            
            print("⚠️ Extracting risk factors...")
            risk_factors = self.extract_risk_factors(filing_text)
            
            print("🏢 Extracting business segment data...")
            business_segments = self.extract_business_segments(filing_text)
            
            return EnhancedSMAPNotes(
                subjective=smap_sections.get('subjective', 'No subjective analysis generated'),
                metrics=smap_sections.get('metrics', 'No metrics extracted'),
                assessment=smap_sections.get('assessment', 'No assessment provided'),
                plan=smap_sections.get('plan', 'No plan recommendations'),
                financial_metrics=financial_metrics,
                risk_factors=risk_factors,
                business_segments=business_segments,
                company_name=company_info.get('company_name', 'Unknown Company'),
                ticker_symbol=company_info.get('ticker', 'N/A'),
                filing_type=company_info.get('filing_type', 'SEC Filing'),
                filing_period=company_info.get('quarter_year', 'N/A'),
                industry=company_info.get('industry', 'Financial Services')
            )
            
        except Exception as e:
            print(f"Error generating enhanced SMAP notes: {e}")
            return EnhancedSMAPNotes(
                subjective="Error generating analysis",
                metrics="Error extracting metrics",
                assessment="Error in assessment",
                plan="Error in planning",
                financial_metrics=FinancialMetrics(),
                risk_factors=RiskFactors([], [], [], [], [], []),
                business_segments=BusinessSegments({}),
                company_name="Unknown Company"
            )
    
    def _extract_company_metadata(self, filing_text: str) -> Dict[str, str]:
        """Extract company metadata"""
        prompt = f"""
        Extract company metadata from this SEC filing:
        
        {filing_text[:2000]}
        
        Return JSON:
        {{
            "company_name": "Full company name",
            "ticker": "Stock symbol",
            "filing_type": "10-Q or 10-K",
            "quarter_year": "Q1 2025",
            "industry": "Industry sector"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            return json.loads(response_text)
        except:
            return {
                "company_name": "Unknown Company",
                "ticker": "N/A",
                "filing_type": "SEC Filing",
                "quarter_year": "N/A",
                "industry": "Financial Services"
            }
    
    def _parse_smap_response(self, response_text: str) -> Dict[str, str]:
        """Parse SMAP sections from Gemini response"""
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
                if not line.startswith('**') and not line.startswith('['):
                    current_content.append(line)
        
        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections

# Test the enhanced service
def test_enhanced_gemini():
    """Test the enhanced Gemini service"""
    print("🧪 Testing Enhanced Gemini Service")
    print("🎯 MLH Best Use of Gemini API Demo")
    print("="*50)
    
    service = EnhancedGeminiService()
    
    # Sample banking text for testing
    sample_text = """
    JPMORGAN CHASE & CO.
    FORM 10-Q
    
    CONSOLIDATED STATEMENT OF INCOME
    Three Months Ended March 31, 2025
    
    Total net revenue: $42,550 million (2024: $39,880 million)
    Net interest income: $23,900 million
    Noninterest revenue: $18,650 million
    Net income: $13,420 million
    
    Return on equity: 17.8%
    Common equity Tier 1 ratio: 15.9%
    Net interest margin: 2.74%
    Book value per share: $95.35
    
    RISK FACTORS:
    Credit risk from potential economic downturn affecting loan portfolios.
    Market risk from interest rate volatility and trading positions.
    Regulatory changes could impact capital requirements and operations.
    
    BUSINESS SEGMENTS:
    Consumer & Community Banking revenue: $17.2 billion
    Corporate & Investment Bank revenue: $12.1 billion
    """
    
    enhanced_smap = service.generate_enhanced_smap_notes(sample_text)
    
    print(f"\n📈 COMPANY: {enhanced_smap.company_name}")
    print(f"📊 TICKER: {enhanced_smap.ticker_symbol}")
    print(f"📋 FILING: {enhanced_smap.filing_type}")
    
    print(f"\n💰 FINANCIAL METRICS:")
    metrics = enhanced_smap.financial_metrics
    print(f"   Revenue: ${metrics.total_revenue}M")
    print(f"   Net Income: ${metrics.net_income}M")
    print(f"   ROE: {metrics.return_on_equity}")
    print(f"   CET1: {metrics.common_equity_tier1_ratio}")
    
    print(f"\n⚠️ RISK FACTORS:")
    risks = enhanced_smap.risk_factors
    print(f"   Credit Risks: {len(risks.credit_risk)} identified")
    print(f"   Market Risks: {len(risks.market_risk)} identified")
    print(f"   Regulatory Risks: {len(risks.regulatory_risk)} identified")
    
    print(f"\n🏢 BUSINESS SEGMENTS:")
    for segment, data in enhanced_smap.business_segments.segments.items():
        print(f"   {segment}: ${data.get('revenue', 'N/A')}M revenue")
    
    print("\n✅ Enhanced Gemini extraction complete!")
    print("🏆 Ready for MLH Best Use of Gemini API prize!")

if __name__ == "__main__":
    test_enhanced_gemini()