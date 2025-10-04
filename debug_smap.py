"""
Debug SMAP generation to see what's happening
"""

from gemini_service import GeminiService
from document_processor import DocumentProcessor
import time

def debug_smap_generation():
    """Debug the SMAP generation process"""
    print("🔧 Debugging SMAP Generation Process")
    print("=" * 50)
    
    # Initialize services
    service = GeminiService()
    processor = DocumentProcessor()
    
    # Process the JPMorgan PDF
    jpmc_pdf_path = "/Users/azrabano/Downloads/jpmc_10q.pdf"
    
    print("📄 Extracting text from JPMorgan Chase 10-Q PDF...")
    raw_text = processor.extract_text_from_pdf(jpmc_pdf_path)
    
    print(f"✅ Text extracted: {len(raw_text)} characters")
    
    # Prepare for analysis
    processed_doc = processor.prepare_for_analysis(raw_text)
    analysis_text = processed_doc["analysis_text"]
    
    print(f"📋 Analysis text prepared: {len(analysis_text)} characters")
    print(f"🔍 First 500 characters:\n{analysis_text[:500]}...")
    
    print("\n" + "="*50)
    print("🤖 Testing Gemini SMAP generation...")
    
    # Test with a smaller, focused excerpt first
    test_excerpt = analysis_text[:5000]  # First 5000 characters
    
    print(f"📝 Testing with {len(test_excerpt)} character excerpt")
    
    try:
        start_time = time.time()
        smap_notes = service.generate_smap_notes(test_excerpt)
        generation_time = time.time() - start_time
        
        print(f"✅ Generation completed in {generation_time:.2f} seconds")
        print(f"🏢 Company detected: {smap_notes.company_name}")
        print(f"📋 Filing type: {smap_notes.filing_type}")
        
        print(f"\n📝 SUBJECTIVE Section ({len(smap_notes.subjective)} chars):")
        print(smap_notes.subjective[:200] + "..." if len(smap_notes.subjective) > 200 else smap_notes.subjective)
        
        print(f"\n🔢 METRICS Section ({len(smap_notes.metrics)} chars):")
        print(smap_notes.metrics[:200] + "..." if len(smap_notes.metrics) > 200 else smap_notes.metrics)
        
        print(f"\n🔍 ASSESSMENT Section ({len(smap_notes.assessment)} chars):")
        print(smap_notes.assessment[:200] + "..." if len(smap_notes.assessment) > 200 else smap_notes.assessment)
        
        print(f"\n📋 PLAN Section ({len(smap_notes.plan)} chars):")
        print(smap_notes.plan[:200] + "..." if len(smap_notes.plan) > 200 else smap_notes.plan)
        
    except Exception as e:
        print(f"❌ Error during SMAP generation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_smap_generation()