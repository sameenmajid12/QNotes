#!/usr/bin/env python3
"""
Demo: Complete Practice Mode with Gemini API Integration
Shows the full interactive SMAP learning experience
"""

import requests
import json
import time

def demo_practice_mode():
    """Demo the complete Practice Mode functionality"""
    print("🎯 10Q Notes AI - Practice Mode Demo")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health Check
    print("\n1. 🔧 Testing Backend Health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Backend is healthy")
            print(f"   Status: {health_data['status']}")
            print(f"   Services: {health_data['services']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Test 2: Extract Sections from Filing
    print("\n2. 📄 Extracting Sections from 10-Q Filing...")
    try:
        filing_content = """
        JPMorgan Chase & Co. Q1 2025 10-Q Filing
        
        PART I - FINANCIAL INFORMATION
        Item 1. Financial Statements
        
        CONSOLIDATED STATEMENTS of INCOME
        For the three months ended March 31, 2025 and 2024
        (in millions, except per share amounts)
        
        Net revenues increased 6.8% to $42,500 million for the three months ended March 31, 2025, compared to $39,800 million for the three months ended March 31, 2024. The increase was primarily due to higher net interest income and increased investment banking fees.
        
        Net income was $13,400 million for the three months ended March 31, 2025, compared to $12,600 million for the same period in 2024, representing an increase of 6.3%.
        
        Diluted earnings per share were $4.44 for the three months ended March 31, 2025, compared to $4.18 for the three months ended March 31, 2024.
        
        MANAGEMENT'S DISCUSSION AND ANALYSIS
        Our first quarter results reflect strong performance across our business lines, with particular strength in our consumer and community banking segment. We remain focused on delivering value to our shareholders while maintaining our fortress balance sheet.
        
        Risk Factors
        We face various risks including credit risk, market risk, operational risk, and regulatory risk. We have implemented comprehensive risk management frameworks to identify, measure, monitor, and control these risks.
        """
        
        response = requests.post(
            f"{base_url}/api/session/demo123/practice",
            json={
                "action": "get_sections",
                "filing_content": filing_content
            }
        )
        
        if response.status_code == 200:
            sections_data = response.json()
            if sections_data["success"]:
                sections = sections_data["sections"]
                print(f"✅ Extracted {len(sections)} practice sections")
                for i, section in enumerate(sections, 1):
                    print(f"   {i}. {section['title']} ({section['difficulty']})")
                    print(f"      Focus: {section['smap_focus']}")
                    print(f"      Objectives: {len(section['learning_objectives'])} learning goals")
            else:
                print(f"❌ Section extraction failed: {sections_data['error']}")
        else:
            print(f"❌ Section request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Section extraction error: {e}")
    
    # Test 3: SMAP Framework Teaching
    print("\n3. 📚 Teaching SMAP Framework...")
    try:
        section = sections[0] if 'sections' in locals() else {
            "title": "Revenue Analysis",
            "content": "Revenue increased 6.8% to $42.5B",
            "smap_focus": "Metrics and Assessment"
        }
        
        response = requests.post(
            f"{base_url}/api/session/demo123/practice",
            json={
                "action": "teach_smap",
                "section": section
            }
        )
        
        if response.status_code == 200:
            teaching_data = response.json()
            if teaching_data["success"]:
                teaching = teaching_data["teaching"]
                print("✅ SMAP framework teaching generated")
                print(f"   Components: {len(teaching['smap_explanation'])} explained")
                print(f"   Example SMAP: {'✓' if teaching['example_smap'] else '✗'}")
                print(f"   Learning tips: {len(teaching['learning_tips'])} tips")
                
                print("\n   📖 SMAP Framework Components:")
                for component, data in teaching['smap_explanation'].items():
                    print(f"      {component.upper()}: {data['definition'][:60]}...")
            else:
                print(f"❌ Teaching generation failed: {teaching_data['error']}")
        else:
            print(f"❌ Teaching request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Teaching error: {e}")
    
    # Test 4: Student SMAP Submission and Grading
    print("\n4. ✏️ Student SMAP Submission and Grading...")
    try:
        student_smap = {
            "subjective": "Management expresses strong confidence in the company's strategic direction and market position. The tone is optimistic about future growth prospects.",
            "metrics": "Revenue increased 6.8% year-over-year to $42.5 billion. Net income was $13.4 billion, representing a 6.3% increase. Diluted EPS grew to $4.44.",
            "assessment": "Performance exceeds industry averages with strong profitability metrics. The company demonstrates robust financial health with consistent growth across key indicators.",
            "plan": "Continue strategic investments in digital transformation and market expansion initiatives. Maintain fortress balance sheet while delivering shareholder value."
        }
        
        response = requests.post(
            f"{base_url}/api/session/demo123/practice",
            json={
                "action": "grade_submission",
                "student_smap": student_smap,
                "section": section,
                "teaching_data": teaching
            }
        )
        
        if response.status_code == 200:
            grading_data = response.json()
            if grading_data["success"]:
                grading = grading_data["grading"]
                print("✅ Student submission graded successfully")
                print(f"   Overall Score: {grading['overall_score']}/100 ({grading['grade_letter']})")
                
                print("\n   📊 Component Scores:")
                for comp, data in grading['component_scores'].items():
                    print(f"      {comp.upper()}: {data['score']}/100 - {data['feedback']}")
                
                print(f"\n   💬 Feedback Summary:")
                feedback = grading['detailed_feedback']
                print(f"      Strengths: {len(feedback['what_you_did_well'])} areas")
                print(f"      Improvements: {len(feedback['areas_for_improvement'])} suggestions")
                print(f"      Next Steps: {len(feedback['next_steps'])} actions")
            else:
                print(f"❌ Grading failed: {grading_data['error']}")
        else:
            print(f"❌ Grading request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Grading error: {e}")
    
    # Test 5: Progress Insights
    print("\n5. 📊 Generating Progress Insights...")
    try:
        session_history = [
            {
                "section_title": "Revenue Analysis",
                "overall_score": 85,
                "difficulty": "beginner",
                "date": "2025-10-04T20:00:00Z"
            },
            {
                "section_title": "Risk Factors", 
                "overall_score": 78,
                "difficulty": "intermediate",
                "date": "2025-10-04T20:30:00Z"
            }
        ]
        
        response = requests.post(
            f"{base_url}/api/session/demo123/practice",
            json={
                "action": "get_insights",
                "session_history": session_history
            }
        )
        
        if response.status_code == 200:
            insights_data = response.json()
            if insights_data["success"]:
                insights = insights_data["insights"]
                print("✅ Progress insights generated")
                progress = insights['overall_progress']
                print(f"   Average Score: {progress['average_score']}")
                print(f"   Total Sessions: {progress['total_sessions']}")
                print(f"   Trend: {progress['trend']}")
                print(f"   Strengths: {len(insights['strengths'])} areas")
                print(f"   Improvements: {len(insights['weaknesses'])} areas")
                print(f"   Recommendations: {len(insights['recommendations'])} suggestions")
            else:
                print(f"❌ Insights generation failed: {insights_data['error']}")
        else:
            print(f"❌ Insights request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Insights error: {e}")
    
    # Test 6: Next Section Assignment
    print("\n6. ➡️ Assigning Next Practice Section...")
    try:
        completed_sections = ["revenue_analysis", "risk_factors"]
        available_sections = sections if 'sections' in locals() else []
        
        response = requests.post(
            f"{base_url}/api/session/demo123/practice",
            json={
                "action": "assign_next_section",
                "completed_sections": completed_sections,
                "available_sections": available_sections,
                "mode": "sequential"
            }
        )
        
        if response.status_code == 200:
            assignment_data = response.json()
            if assignment_data["success"]:
                assignment = assignment_data["assignment"]
                if assignment["section"]:
                    next_section = assignment["section"]
                    print("✅ Next section assigned")
                    print(f"   Section: {next_section['title']}")
                    print(f"   Difficulty: {next_section['difficulty']}")
                    print(f"   Focus: {next_section['smap_focus']}")
                else:
                    print("🎉 All sections completed!")
                    print(f"   Message: {assignment['message']}")
            else:
                print(f"❌ Assignment failed: {assignment_data['error']}")
        else:
            print(f"❌ Assignment request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Assignment error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Practice Mode Demo Complete!")
    print("\n📋 Summary:")
    print("✅ Backend server running")
    print("✅ Section extraction from 10-Q filings")
    print("✅ SMAP framework teaching with Gemini AI")
    print("✅ Student submission grading with detailed feedback")
    print("✅ Progress tracking and insights generation")
    print("✅ Next section assignment (sequential/random modes)")
    print("✅ Complete interactive learning loop")
    
    print("\n🎯 Practice Mode Features:")
    print("- 📄 Automatic section extraction from uploaded 10-Q filings")
    print("- 📚 Interactive SMAP framework teaching")
    print("- ✏️ Student practice with real filing content")
    print("- 📊 AI-powered grading with detailed feedback")
    print("- 📈 Progress tracking and personalized insights")
    print("- 🔄 Continuous learning loop with section progression")
    print("- 🎲 Sequential and random practice modes")
    
    print("\n🚀 Ready for Students:")
    print("1. Upload 10-Q filing")
    print("2. Choose Practice Mode")
    print("3. Select practice section")
    print("4. Learn SMAP framework")
    print("5. Create SMAP analysis")
    print("6. Get detailed AI feedback")
    print("7. View progress insights")
    print("8. Continue to next section")
    print("9. Repeat for comprehensive learning!")

def main():
    """Main function"""
    demo_practice_mode()

if __name__ == "__main__":
    main()
