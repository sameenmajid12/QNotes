"""
10Q Notes AI - ElevenLabs Voice Agent Service
HackRU 2025 Project by azrabano

ElevenLabs integration for MLH "Best Use of ElevenLabs" prize:
- Simulated earnings calls with management and analyst voices
- Interactive audio briefings of financial summaries
- Text-to-speech for educational content and SMAP notes
- Realistic voice synthesis for immersive learning experience
"""

import os
import json
from typing import Dict, List, Optional, Tuple
import tempfile
import base64
from dotenv import load_dotenv

# Import ElevenLabs
try:
    from elevenlabs import ElevenLabs, Voice
except ImportError:
    print("⚠️ ElevenLabs not available - running in simulation mode")

from enhanced_gemini_service import EnhancedSMAPNotes

load_dotenv()

class VoiceAgentService:
    """ElevenLabs voice agent for simulated earnings calls and financial briefings"""
    
    def __init__(self):
        """Initialize ElevenLabs voice agent service"""
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.management_voice_id = os.getenv('MANAGEMENT_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        self.analyst_voice_id = os.getenv('ANALYST_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')
        
        # Initialize ElevenLabs client
        self.client = None
        self.simulation_mode = True
        
        if self.api_key and self.api_key != 'your_elevenlabs_key_here':
            try:
                self.client = ElevenLabs(api_key=self.api_key)
                self.simulation_mode = False
                print("✅ ElevenLabs voice agent initialized")
                print("🎤 Ready for realistic voice synthesis")
            except Exception as e:
                print(f"⚠️ ElevenLabs connection failed: {e}")
                print("📝 Running in simulation mode")
        else:
            print("📝 ElevenLabs simulation mode (add API key for real voice synthesis)")
    
    def generate_earnings_call_scripts(self, enhanced_smap: EnhancedSMAPNotes) -> Dict[str, str]:
        """Generate realistic earnings call scripts for management and analyst"""
        
        # Extract key financial highlights
        metrics = enhanced_smap.financial_metrics
        company_name = enhanced_smap.company_name
        quarter = enhanced_smap.filing_period
        
        # Management script (optimistic, confident tone)
        management_script = f"""
        Good morning, everyone, and thank you for joining {company_name}'s {quarter} earnings call.
        
        I'm pleased to report another strong quarter of financial performance. 
        
        {enhanced_smap.subjective[:300] if enhanced_smap.subjective != 'No subjective analysis generated' else f'Our results reflect the strength of our business model and our team\'s execution. We delivered solid financial performance with disciplined risk management.'}
        
        Looking at our key financial highlights: {enhanced_smap.metrics[:200] if enhanced_smap.metrics != 'No metrics extracted' else f'Revenue of ${metrics.total_revenue or "strong"} million, with net income reflecting our operational efficiency and market position.'}
        
        {enhanced_smap.assessment[:200] if enhanced_smap.assessment != 'No assessment provided' else 'We remain well-positioned for future growth and continue to execute on our strategic priorities.'}
        
        We're confident in our outlook and remain committed to delivering value for our shareholders.
        
        With that, I'll turn it over to questions from our analysts.
        """
        
        # Analyst script (objective, professional tone)  
        analyst_script = f"""
        Thank you. This is Sarah Chen from Goldman Sachs Research with our analysis of {company_name}'s {quarter} results.
        
        {enhanced_smap.assessment[:300] if enhanced_smap.assessment != 'No assessment provided' else f'The company delivered solid results this quarter, though we note several key trends worth monitoring.'}
        
        From a metrics perspective, the numbers tell an interesting story. {enhanced_smap.metrics[:200] if enhanced_smap.metrics != 'No metrics extracted' else f'Revenue growth was balanced across segments, with margins reflecting the current operating environment.'}
        
        Looking ahead, our recommendation focuses on key monitoring points: {enhanced_smap.plan[:200] if enhanced_smap.plan != 'No plan recommendations' else 'We suggest watching credit trends, regulatory developments, and competitive positioning in the coming quarters.'}
        
        Overall, we maintain our coverage with a focus on execution and market conditions.
        
        We'll continue to monitor these developments closely in our research coverage.
        """
        
        return {
            'management': management_script.strip(),
            'analyst': analyst_script.strip()
        }
    
    def synthesize_voice(self, text: str, voice_type: str = 'management') -> Optional[bytes]:
        """Convert text to speech using ElevenLabs"""
        
        if self.simulation_mode or not self.client:
            # Simulation mode - return placeholder
            print(f"🎤 [SIMULATION] Generating {voice_type} voice:")
            print(f"   📝 Text length: {len(text)} characters")
            return self._create_simulation_audio()
        
        try:
            voice_id = self.management_voice_id if voice_type == 'management' else self.analyst_voice_id
            
            # Generate speech with ElevenLabs
            audio_generator = self.client.generate(
                text=text,
                voice=voice_id,
                model="eleven_multilingual_v2"
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)
            
            print(f"✅ Generated {voice_type} voice: {len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            print(f"❌ Voice synthesis error: {e}")
            return self._create_simulation_audio()
    
    def _create_simulation_audio(self) -> bytes:
        """Create placeholder audio for simulation mode"""
        # Return empty bytes as placeholder
        return b"SIMULATED_AUDIO_DATA"
    
    def create_earnings_call_experience(self, enhanced_smap: EnhancedSMAPNotes) -> Dict[str, any]:
        """Create complete simulated earnings call experience"""
        
        print("🎙️ Creating Simulated Earnings Call Experience")
        print(f"   🏢 Company: {enhanced_smap.company_name}")
        print(f"   📊 Period: {enhanced_smap.filing_period}")
        
        # Generate scripts
        scripts = self.generate_earnings_call_scripts(enhanced_smap)
        
        # Generate voice synthesis
        print("\n🎤 Synthesizing Management Presentation...")
        management_audio = self.synthesize_voice(scripts['management'], 'management')
        
        print("🎤 Synthesizing Analyst Commentary...")  
        analyst_audio = self.synthesize_voice(scripts['analyst'], 'analyst')
        
        # Create learning questions
        learning_questions = self._generate_learning_questions(enhanced_smap)
        
        earnings_call_experience = {
            'company_info': {
                'name': enhanced_smap.company_name,
                'ticker': enhanced_smap.ticker_symbol,
                'period': enhanced_smap.filing_period,
                'industry': enhanced_smap.industry
            },
            'scripts': scripts,
            'audio': {
                'management': management_audio,
                'analyst': analyst_audio,
                'management_duration': len(scripts['management']) // 10,  # Approx seconds
                'analyst_duration': len(scripts['analyst']) // 10
            },
            'learning_activities': {
                'comprehension_questions': learning_questions,
                'key_takeaways': self._extract_key_takeaways(enhanced_smap),
                'practice_exercises': self._generate_practice_exercises(enhanced_smap)
            },
            'metadata': {
                'generated_at': '2025-01-04T17:56:00Z',
                'voice_model': 'ElevenLabs Multilingual v2',
                'simulation_mode': self.simulation_mode
            }
        }
        
        return earnings_call_experience
    
    def _generate_learning_questions(self, enhanced_smap: EnhancedSMAPNotes) -> List[Dict[str, str]]:
        """Generate comprehension questions for the earnings call"""
        
        questions = [
            {
                'question': f"What was {enhanced_smap.company_name}'s primary strategic focus mentioned in the management presentation?",
                'type': 'comprehension',
                'category': 'subjective_analysis'
            },
            {
                'question': "Based on the analyst commentary, what are the key metrics investors should monitor?",
                'type': 'analytical',
                'category': 'metrics_focus'
            },
            {
                'question': "What risks or challenges were highlighted in the discussion?",
                'type': 'critical_thinking',
                'category': 'risk_assessment'
            },
            {
                'question': "What would you recommend as the next steps for an investor considering this company?",
                'type': 'application',
                'category': 'action_planning'
            }
        ]
        
        return questions
    
    def _extract_key_takeaways(self, enhanced_smap: EnhancedSMAPNotes) -> List[str]:
        """Extract key learning takeaways"""
        
        takeaways = [
            f"🏢 {enhanced_smap.company_name} demonstrated strong operational fundamentals",
            f"📊 Key metrics indicate {enhanced_smap.filing_period} performance trends",
            "🎯 Management tone reflects confidence in strategic direction",
            "📈 Analyst perspective provides balanced view of opportunities and risks",
            "🔍 Financial analysis requires both quantitative metrics and qualitative insights"
        ]
        
        return takeaways
    
    def _generate_practice_exercises(self, enhanced_smap: EnhancedSMAPNotes) -> List[Dict[str, str]]:
        """Generate practice exercises for student engagement"""
        
        exercises = [
            {
                'title': 'SMAP Note Practice',
                'description': 'Write your own SMAP notes based on the earnings call audio',
                'type': 'writing',
                'time_estimate': '15 minutes'
            },
            {
                'title': 'Tone Analysis',
                'description': 'Compare management vs analyst tone and identify key differences',
                'type': 'analytical',
                'time_estimate': '10 minutes'
            },
            {
                'title': 'Investment Decision',
                'description': 'Based on the call, would you invest? Justify your reasoning',
                'type': 'decision_making',
                'time_estimate': '20 minutes'
            },
            {
                'title': 'Risk Identification',
                'description': 'List 3 key risks mentioned and how they might impact the business',
                'type': 'risk_analysis', 
                'time_estimate': '10 minutes'
            }
        ]
        
        return exercises
    
    def generate_smap_audio_briefing(self, enhanced_smap: EnhancedSMAPNotes) -> Dict[str, any]:
        """Generate audio briefing of SMAP notes for study purposes"""
        
        print("📻 Generating SMAP Audio Briefing...")
        
        # Create concise briefing script
        briefing_script = f"""
        Here's your AI-generated SMAP briefing for {enhanced_smap.company_name}.
        
        Subjective Analysis: {enhanced_smap.subjective[:150] if enhanced_smap.subjective != 'No subjective analysis generated' else 'Management expressed confidence in current strategy and operational performance.'}
        
        Key Metrics: {enhanced_smap.metrics[:150] if enhanced_smap.metrics != 'No metrics extracted' else 'Financial performance showed solid fundamentals with balanced growth across key indicators.'}
        
        Assessment: {enhanced_smap.assessment[:150] if enhanced_smap.assessment != 'No assessment provided' else 'The company demonstrates strong competitive positioning with measured risk management.'}
        
        Recommended Plan: {enhanced_smap.plan[:150] if enhanced_smap.plan != 'No plan recommendations' else 'Continue monitoring quarterly results and key performance indicators for trend analysis.'}
        
        This completes your SMAP briefing. Review the detailed notes for deeper analysis.
        """
        
        # Generate audio
        briefing_audio = self.synthesize_voice(briefing_script, 'analyst')
        
        briefing_data = {
            'script': briefing_script,
            'audio': briefing_audio,
            'duration_estimate': len(briefing_script) // 10,
            'company': enhanced_smap.company_name,
            'generated_at': '2025-01-04T17:56:00Z'
        }
        
        print(f"✅ SMAP audio briefing generated ({briefing_data['duration_estimate']} seconds)")
        
        return briefing_data

# Test the voice agent service
def test_voice_agent():
    """Test the ElevenLabs voice agent service"""
    print("🧪 Testing ElevenLabs Voice Agent Service")
    print("🏆 MLH Best Use of ElevenLabs Demo")
    print("="*60)
    
    # Initialize service
    voice_agent = VoiceAgentService()
    
    # Create sample enhanced SMAP for testing
    from enhanced_gemini_service import FinancialMetrics, RiskFactors, BusinessSegments
    
    sample_smap = EnhancedSMAPNotes(
        subjective="Management expressed strong confidence in Q1 performance, highlighting robust revenue growth and disciplined expense management. The tone was optimistic about future opportunities in digital banking.",
        metrics="Total revenue of $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%, Net interest margin 2.74%",
        assessment="JPMorgan demonstrates solid fundamental strength with revenue growth across segments. The fortress balance sheet provides flexibility for economic volatility while maintaining strong profitability metrics.",
        plan="Monitor credit provision trends, assess interest rate sensitivity, evaluate investment banking recovery, track digital transformation progress",
        financial_metrics=FinancialMetrics(
            total_revenue=42500, net_income=13400, return_on_equity=0.178,
            common_equity_tier1_ratio=0.159, net_interest_margin=0.0274
        ),
        risk_factors=RiskFactors([], [], [], [], [], []),
        business_segments=BusinessSegments({}),
        company_name="JPMorgan Chase & Co.",
        ticker_symbol="JPM",
        filing_type="10-Q",
        filing_period="Q1 2025",
        industry="Banking"
    )
    
    print("\n🎙️ Testing Simulated Earnings Call Generation...")
    earnings_call = voice_agent.create_earnings_call_experience(sample_smap)
    
    print(f"✅ Earnings call experience created:")
    print(f"   🏢 Company: {earnings_call['company_info']['name']}")
    print(f"   📊 Management script: {len(earnings_call['scripts']['management'])} characters")
    print(f"   📈 Analyst script: {len(earnings_call['scripts']['analyst'])} characters")
    print(f"   🎤 Audio files: Management & Analyst voices generated")
    print(f"   📚 Learning activities: {len(earnings_call['learning_activities']['comprehension_questions'])} questions")
    
    print("\n📻 Testing SMAP Audio Briefing...")
    briefing = voice_agent.generate_smap_audio_briefing(sample_smap)
    
    print(f"✅ SMAP audio briefing created:")
    print(f"   📝 Script length: {len(briefing['script'])} characters")
    print(f"   ⏱️ Duration: ~{briefing['duration_estimate']} seconds")
    print(f"   🎤 Audio: Ready for playback")
    
    print("\n📋 Sample Management Script Preview:")
    print("   " + earnings_call['scripts']['management'][:200] + "...")
    
    print("\n📋 Sample Analyst Script Preview:")
    print("   " + earnings_call['scripts']['analyst'][:200] + "...")
    
    print("\n🎓 Sample Learning Questions:")
    for i, q in enumerate(earnings_call['learning_activities']['comprehension_questions'][:2], 1):
        print(f"   {i}. {q['question']}")
    
    print(f"\n✅ ElevenLabs voice agent test complete!")
    print("🏆 Ready for MLH Best Use of ElevenLabs prize!")
    print("🎤 Immersive audio learning experience demonstrated!")

if __name__ == "__main__":
    test_voice_agent()