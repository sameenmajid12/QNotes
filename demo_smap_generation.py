"""
10Q Notes AI - Demo Script
HackRU 2025 Project by azrabano

This demo showcases the core SMAP generation functionality
with sample SEC filing text for judges and presentation.
"""

from gemini_service import GeminiService, SMAPNotes
import json
import time

# Sample 10-Q filing text (simulated for demo purposes)
SAMPLE_FILING_TEXT = """
APPLE INC.
CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS
(Unaudited)
(In millions, except number of shares which are reflected in thousands and per share amounts)

Three Months Ended March 31, 2024

Net sales:
Products                    $60,584
Services                    $23,870
Total net sales             $84,454

Cost of sales:
Products                    $36,098
Services                    $6,417
Total cost of sales         $42,515

Gross margin                $41,939

Operating expenses:
Research and development    $7,442
Selling, general and administrative  $6,321
Total operating expenses    $13,763

Operating income            $28,176

Other income, net           $1,063
Income before provision for income taxes  $29,239
Provision for income taxes  $4,386
Net income                  $24,853

Earnings per share:
Basic                       $1.53
Diluted                     $1.52

Management Discussion and Analysis:
Our financial performance for the second quarter of fiscal 2024 demonstrates continued strength across all product categories and geographical segments. Revenue grew 4.9% year-over-year, driven primarily by strong iPhone sales in emerging markets and continued expansion of our Services business.

We maintained healthy gross margins at 49.6%, reflecting our focus on premium products and operational efficiency. Operating expenses increased 8.1% year-over-year, primarily due to continued investments in research and development for artificial intelligence capabilities and expansion of our Services infrastructure.

Looking forward, we remain optimistic about growth opportunities in artificial intelligence, augmented reality, and services expansion. However, we continue to monitor macroeconomic headwinds and foreign exchange volatility that could impact future results.

Key risks include supply chain disruptions, increasing competition in smartphone markets, and regulatory scrutiny in various jurisdictions regarding our App Store policies and market position.
"""

def format_section_output(title: str, content: str, max_length: int = 200):
    """Format section output for better display"""
    print(f"\n{'='*50}")
    print(f"{title.upper()}")
    print(f"{'='*50}")
    
    if len(content) > max_length:
        print(f"{content[:max_length]}...")
        print(f"\n[Content truncated - showing first {max_length} characters]")
    else:
        print(content)

def demo_smap_generation():
    """Main demo function showcasing SMAP generation"""
    print("🍎 10Q Notes AI - Live SMAP Generation Demo")
    print("📊 HackRU 2025 Project - Democratizing Finance Education")
    print(f"{'='*60}\n")
    
    print("📄 Processing Apple Inc. Q2 2024 10-Q Filing...")
    print("🤖 Generating AI-powered SMAP Notes...")
    print("⏳ Please wait...\n")
    
    try:
        # Initialize Gemini service
        service = GeminiService()
        
        # Generate SMAP notes
        start_time = time.time()
        smap_notes = service.generate_smap_notes(SAMPLE_FILING_TEXT)
        generation_time = time.time() - start_time
        
        print(f"✅ SMAP Generation Complete! ({generation_time:.2f} seconds)")
        print(f"🏢 Company: {smap_notes.company_name}")
        print(f"📋 Filing Type: {smap_notes.filing_type}")
        
        # Display each section
        format_section_output("Subjective (S) - What Management Said", smap_notes.subjective)
        format_section_output("Metrics (M) - Key Financial Numbers", smap_notes.metrics)
        format_section_output("Assessment (A) - AI Analysis & Insights", smap_notes.assessment)
        format_section_output("Plan (P) - Recommended Next Steps", smap_notes.plan)
        
        print(f"\n{'='*60}")
        print("🎯 DEMO HIGHLIGHTS FOR JUDGES:")
        print("• ⚡ Instant transformation of dense SEC filings into structured insights")
        print("• 🎓 Educational SMAP framework (medical SOAP notes for finance)")
        print("• 🤖 AI-powered analysis using Google Gemini 2.5 Pro")
        print("• 📈 Perfect for students, analysts, and retail investors")
        print("• 🏆 Democratizes access to professional financial analysis")
        
        # Generate sample flashcards
        print(f"\n{'='*60}")
        print("🎓 EDUCATIONAL FEATURES DEMO")
        print("📚 Generating Sample Flashcards...")
        
        flashcards = service.generate_flashcards(smap_notes, 3)
        
        for i, card in enumerate(flashcards, 1):
            print(f"\n📖 Flashcard #{i}:")
            print(f"   Q: {card.get('question', 'N/A')}")
            print(f"   A: {card.get('answer', 'N/A')}")
            print(f"   Category: {card.get('category', 'N/A')} | Difficulty: {card.get('difficulty', 'N/A')}")
        
        print(f"\n{'='*60}")
        print("🚀 NEXT STEPS FOR HACKRU DEMO:")
        print("1. 🌐 Build React frontend with card-based UI")
        print("2. 📊 Integrate Snowflake for financial data storage")
        print("3. 🔊 Add ElevenLabs for audio briefings")
        print("4. 📝 Implement user feedback and grading system")
        print("5. 🏆 Deploy on qnotes.tech domain")
        
        return smap_notes
        
    except Exception as e:
        print(f"❌ Demo Error: {str(e)}")
        return None

def demo_feedback_system():
    """Demo the feedback and grading functionality"""
    print(f"\n{'='*60}")
    print("🎯 AI FEEDBACK & GRADING DEMO")
    print("📝 Simulating Student vs. AI Gold Standard Comparison")
    print("⏳ Analyzing student performance...\n")
    
    try:
        service = GeminiService()
        
        # Generate gold standard
        gold_standard = service.generate_smap_notes(SAMPLE_FILING_TEXT)
        
        # Create a simulated student version (with some missing elements)
        student_smap = SMAPNotes(
            subjective="Management seems optimistic about AI and AR opportunities. They mentioned strong iPhone sales.",
            metrics="Revenue was $84.4 billion, up 4.9% YoY. Net income was $24.9 billion. EPS was $1.53.",
            assessment="The company is doing well with good revenue growth and profitability.",
            plan="Continue monitoring the stock. Maybe buy more shares.",
            company_name="Apple Inc.",
            filing_type="10-Q"
        )
        
        # Get feedback
        feedback = service.provide_feedback(student_smap, gold_standard)
        
        print("📊 STUDENT PERFORMANCE SCORECARD:")
        print(f"   Completeness: {feedback.completeness}/100")
        print(f"   Accuracy: {feedback.accuracy}/100") 
        print(f"   Insight Depth: {feedback.insight_depth}/100")
        print(f"   Clarity: {feedback.clarity}/100")
        print(f"   📈 OVERALL SCORE: {feedback.overall_score}/100")
        
        print(f"\n💬 AI FEEDBACK COMMENTS:")
        for i, comment in enumerate(feedback.feedback_comments, 1):
            print(f"   {i}. {comment}")
            
        print(f"\n💡 IMPROVEMENT SUGGESTIONS:")
        for i, suggestion in enumerate(feedback.suggestions, 1):
            print(f"   {i}. {suggestion}")
            
    except Exception as e:
        print(f"❌ Feedback Demo Error: {str(e)}")

if __name__ == "__main__":
    # Run the main demo
    smap_result = demo_smap_generation()
    
    if smap_result:
        # Run feedback demo
        demo_feedback_system()
        
        print(f"\n{'='*60}")
        print("🏆 10Q NOTES AI DEMO COMPLETE!")
        print("🎉 Ready for HackRU judges presentation!")
        print("📧 Built by azrabano for HackRU 2025")
        print(f"{'='*60}")