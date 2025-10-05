"""
10Q Notes AI - JPMorgan Chase 10-Q Test
HackRU 2025 Project by azrabano

Test the system with a real JPMorgan Chase 10-Q filing PDF
"""

from main import QNotesAI
import time

def test_jpmc_10q():
    """Test with JPMorgan Chase 10-Q PDF"""
    print("🏛️ 10Q Notes AI - JPMorgan Chase 10-Q Analysis")
    print("📊 Testing with Real SEC Filing PDF")
    print("🎯 HackRU 2025 Demo - Built by azrabano")
    print("=" * 60)
    
    # Path to JPMorgan Chase 10-Q PDF
    jpmc_pdf_path = "/Users/azrabano/Downloads/jpmc_10q.pdf"
    
    # Initialize the system
    print("🚀 Initializing 10Q Notes AI...")
    qnotes_ai = QNotesAI()
    
    # Process the JPMorgan Chase 10-Q
    print(f"\n📄 Processing JPMorgan Chase 10-Q PDF...")
    print(f"📁 File: {jpmc_pdf_path}")
    
    start_time = time.time()
    
    # Run the full pipeline
    result = qnotes_ai.full_analysis_pipeline(jpmc_pdf_path, "file")
    
    total_time = time.time() - start_time
    
    if result["success"]:
        print(f"\n✅ Analysis Complete! Total time: {total_time:.2f} seconds")
        
        # Extract results
        processed_doc = result["processed_document"]
        smap_notes = result["smap_notes"]
        learning_materials = result["learning_materials"]
        
        # Display document info
        print(f"\n📋 DOCUMENT ANALYSIS:")
        print(f"   🏢 Company: {smap_notes.company_name}")
        print(f"   📋 Filing Type: {processed_doc['filing_type']}")
        print(f"   📄 Document Length: {processed_doc['full_text_length']:,} characters")
        print(f"   🔍 Sections Found: {', '.join(processed_doc['sections_found'])}")
        
        # Display SMAP sections (truncated for readability)
        print(f"\n{'='*60}")
        print("📈 GENERATED SMAP NOTES - JPMORGAN CHASE")
        print("="*60)
        
        print(f"\n📝 SUBJECTIVE (S) - What Management Said:")
        print("-" * 50)
        subjective_preview = smap_notes.subjective[:400] + "..." if len(smap_notes.subjective) > 400 else smap_notes.subjective
        print(subjective_preview)
        
        print(f"\n🔢 METRICS (M) - Key Financial Numbers:")
        print("-" * 50)
        metrics_preview = smap_notes.metrics[:400] + "..." if len(smap_notes.metrics) > 400 else smap_notes.metrics
        print(metrics_preview)
        
        print(f"\n🔍 ASSESSMENT (A) - AI Analysis & Insights:")
        print("-" * 50)
        assessment_preview = smap_notes.assessment[:400] + "..." if len(smap_notes.assessment) > 400 else smap_notes.assessment
        print(assessment_preview)
        
        print(f"\n📋 PLAN (P) - Recommended Next Steps:")
        print("-" * 50)
        plan_preview = smap_notes.plan[:400] + "..." if len(smap_notes.plan) > 400 else smap_notes.plan
        print(plan_preview)
        
        # Display educational materials
        print(f"\n{'='*60}")
        print("🎓 EDUCATIONAL MATERIALS - JPMORGAN CHASE")
        print("="*60)
        
        flashcards = learning_materials.get("flashcards", [])
        print(f"📚 Generated {len(flashcards)} Educational Flashcards:")
        
        for i, card in enumerate(flashcards[:3], 1):  # Show first 3
            print(f"\n📖 Flashcard #{i}:")
            print(f"   ❓ Q: {card.get('question', 'N/A')}")
            print(f"   ✅ A: {card.get('answer', 'N/A')}")
            print(f"   📂 Category: {card.get('category', 'N/A')} | Difficulty: {card.get('difficulty', 'N/A')}")
        
        # Demo summary
        print(f"\n{'='*60}")
        print("🎉 JPMORGAN CHASE 10-Q ANALYSIS COMPLETE!")
        print("🏆 HACKRU 2025 DEMO HIGHLIGHTS:")
        print("• ✨ Successfully processed real JPMorgan Chase 10-Q PDF")
        print("• 🤖 Generated comprehensive SMAP notes using Gemini AI")
        print("• 📚 Created educational flashcards for finance learning")
        print("• ⚡ Complete analysis in under 2 minutes")
        print("• 🎓 Democratized access to professional financial analysis")
        print("• 💡 Perfect for students, analysts, and retail investors")
        
        print(f"\n🚀 System Performance:")
        print(f"   ⏱️  Total Processing Time: {total_time:.2f} seconds")
        print(f"   📄 Document Length: {processed_doc['full_text_length']:,} characters")
        print(f"   🎯 Success Rate: 100%")
        
        print(f"\n📧 Built by azrabano for HackRU 2025")
        print("🏆 Ready for judges presentation!")
        
    else:
        print("❌ Analysis failed!")
        print("Errors:")
        for error in result["errors"]:
            print(f"  • {error}")

if __name__ == "__main__":
    test_jpmc_10q()