#!/usr/bin/env python3
"""
10Q Notes AI - Backend API Testing Script
HackRU 2025 Project by azrabano

Complete demonstration of all three learning features:
1. Learn Mode (Read & Hover) 
2. Practice Mode (Student Writes SMAP)
3. AI Feedback Mode (Gemini comparison to Gold Standard)

Tests all endpoints and demonstrates the full learning flow.
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TEST_STUDENT_EMAIL = "john.smith@rutgers.edu"
TEST_STUDENT_NAME = "John Smith"

# Sample SEC filing for testing
SAMPLE_10Q_FILING = """
JPMORGAN CHASE & CO.
FORM 10-Q - QUARTERLY REPORT
For the quarterly period ended March 31, 2025

MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS

We are pleased to report strong Q1 2025 results that demonstrate the resilience of our fortress balance sheet 
and the strength of our diversified business model. Our disciplined approach to risk management continues 
to serve us well in this dynamic operating environment.

FINANCIAL HIGHLIGHTS:
Total net revenue: $42.5 billion (+6.8% year-over-year)
Net income: $13.4 billion (+6.1% year-over-year)  
Return on equity (ROE): 17.8%
Common Equity Tier 1 (CET1) ratio: 15.9%
Net interest margin (NIM): 2.74%
Efficiency ratio: 56%

Our Consumer & Community Banking division delivered solid performance with revenue of $17.8 billion.
Investment Banking fees totaled $2.1 billion, reflecting continued market volatility.
Commercial Banking achieved strong results with revenue of $3.2 billion.
Asset & Wealth Management maintained steady growth with revenue of $4.1 billion.

OUTLOOK AND RISK FACTORS:
We remain cautiously optimistic about the economic environment while monitoring several key areas:
- Credit provisions increased to $1.4 billion as we maintain conservative reserving
- Interest rate sensitivity continues to impact net interest income
- Regulatory capital requirements remain elevated
- Geopolitical tensions may affect global markets
- Digital transformation investments continue at pace

We expect to maintain strong capital levels while supporting our clients and communities.
Our technology investments position us well for future growth opportunities.
"""

class BackendAPITester:
    """Test all backend API endpoints systematically"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.student_id = None
        self.session_id = None
        self.session = requests.Session()
    
    def test_health_check(self) -> bool:
        """Test backend health check"""
        print("\n🔍 Testing Backend Health Check...")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Backend is healthy")
                print(f"   Active sessions: {health_data.get('active_sessions', 0)}")
                print(f"   Services: {health_data.get('services', {})}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_student_authentication(self) -> bool:
        """Test student authentication with .edu email"""
        print("\n👨‍🎓 Testing Student Authentication...")
        
        try:
            auth_data = {
                "email": TEST_STUDENT_EMAIL,
                "name": TEST_STUDENT_NAME
            }
            
            response = self.session.post(f"{self.base_url}/api/auth/login", json=auth_data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.student_id = result["student"]["student_id"]
                    print(f"✅ Student authenticated successfully")
                    print(f"   Student ID: {self.student_id}")
                    print(f"   Name: {result['student']['name']}")
                    print(f"   University: {result['student']['university']}")
                    return True
            
            print(f"❌ Authentication failed: {response.status_code}")
            if response.content:
                print(f"   Error: {response.json()}")
            return False
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def test_file_upload_and_session_start(self) -> bool:
        """Test filing upload and session creation"""
        print("\n📄 Testing SEC Filing Upload & Session Creation...")
        
        try:
            # Simulate file upload with text content
            upload_data = {
                "student_id": self.student_id,
                "company_name": "JPMorgan Chase & Co.",
                "ticker": "JPM",
                "filing_type": "10-Q",
                "filing_period": "Q1 2025"
            }
            
            # Upload as text filing
            response = self.session.post(
                f"{self.base_url}/api/upload/text",
                data={**upload_data, "filing_text": SAMPLE_10Q_FILING}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.session_id = result["session"]["session_id"]
                    print(f"✅ Filing uploaded and session created")
                    print(f"   Session ID: {self.session_id}")
                    print(f"   Company: {result['session']['company_name']}")
                    print(f"   Status: {result['session']['status']}")
                    return True
            
            print(f"❌ Upload failed: {response.status_code}")
            if response.content:
                print(f"   Error: {response.json()}")
            return False
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
    
    def test_learn_mode(self) -> bool:
        """Test Learn Mode - Feature #1"""
        print("\n📖 TESTING LEARN MODE (Feature #1)")
        print("   Student sees extracted sections + simplified explanations")
        print("   Hover definitions and voice synthesis available")
        
        try:
            # Enter Learn Mode
            response = self.session.get(f"{self.base_url}/api/session/{self.session_id}/learn")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("mode") == "learn":
                    content = result["content"]
                    sections = content["sections"]
                    
                    print(f"✅ Learn Mode activated successfully")
                    print(f"   Company: {content['company_info']['name']}")
                    print(f"   Sections available: {len(sections)}")
                    print(f"   Features: {result['features']}")
                    
                    # Test individual section access
                    for section_name in ["subjective", "metrics"]:
                        section_response = self.session.get(
                            f"{self.base_url}/api/session/{self.session_id}/learn/section/{section_name}"
                        )
                        
                        if section_response.status_code == 200:
                            section_data = section_response.json()
                            print(f"   ✅ {section_name.title()} section: {len(section_data['data']['content'])} chars")
                            print(f"      Hover definitions: {len(section_data['interactive_features']['hover_definitions'])}")
                        else:
                            print(f"   ❌ Failed to get {section_name} section")
                    
                    # Test voice synthesis (will be simulated without API key)
                    voice_request = {
                        "session_id": self.session_id,
                        "text": "This is a test of voice synthesis for the subjective section",
                        "voice_type": "management"
                    }
                    
                    voice_response = self.session.post(
                        f"{self.base_url}/api/session/{self.session_id}/voice/synthesize",
                        json=voice_request
                    )
                    
                    if voice_response.status_code == 200:
                        print(f"   ✅ Voice synthesis tested (simulation mode)")
                    
                    return True
            
            print(f"❌ Learn Mode failed: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"❌ Learn Mode error: {e}")
            return False
    
    def test_practice_mode(self) -> bool:
        """Test Practice Mode - Feature #2"""
        print("\n✍️ TESTING PRACTICE MODE (Feature #2)")
        print("   Student fills in their own S, M, A, P boxes")
        
        try:
            # Enter Practice Mode
            response = self.session.get(f"{self.base_url}/api/session/{self.session_id}/practice")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and result.get("mode") == "practice":
                    content = result["content"]
                    
                    print(f"✅ Practice Mode activated successfully")
                    print(f"   Instructions provided: {len(content['instructions']['sections'])} sections")
                    print(f"   Features: {result['features']}")
                    
                    # Test draft saving
                    draft_smap = {
                        "session_id": self.session_id,
                        "subjective": "Management expressed strong confidence in Q1 results, emphasizing fortress balance sheet strategy and disciplined risk management approach.",
                        "metrics": "Revenue $42.5B (+6.8% YoY), Net income $13.4B (+6.1% YoY), ROE 17.8%, CET1 ratio 15.9%, NIM 2.74%, Efficiency ratio 56%",
                        "assessment": "JPMorgan demonstrates solid fundamental strength with diversified revenue growth. Strong capital position provides flexibility during economic uncertainty.",
                        "plan": "Monitor credit provisions for trend changes, track interest rate sensitivity impact, evaluate investment banking recovery timeline, assess digital transformation ROI."
                    }
                    
                    # Save draft
                    draft_response = self.session.put(
                        f"{self.base_url}/api/session/{self.session_id}/practice/save-draft",
                        json=draft_smap
                    )
                    
                    if draft_response.status_code == 200:
                        draft_result = draft_response.json()
                        print(f"   ✅ Draft saved: {draft_result['completion_percentage']:.0f}% complete")
                    
                    # Submit final SMAP for feedback
                    submit_response = self.session.post(
                        f"{self.base_url}/api/session/{self.session_id}/practice/submit",
                        json=draft_smap
                    )
                    
                    if submit_response.status_code == 200:
                        submit_result = submit_response.json()
                        if submit_result.get("success"):
                            print(f"   ✅ SMAP submitted for feedback")
                            print(f"      Overall Score: {submit_result.get('overall_score', 'N/A'):.1f}/100")
                            return True
                        else:
                            print(f"   ❌ Submission failed: {submit_result}")
                    
                    return False
            
            print(f"❌ Practice Mode failed: {response.status_code}")
            return False
            
        except Exception as e:
            print(f"❌ Practice Mode error: {e}")
            return False
    
    def test_feedback_mode(self) -> bool:
        """Test AI Feedback Mode - Feature #3"""
        print("\n🎯 TESTING AI FEEDBACK MODE (Feature #3)")
        print("   Gemini compares student notes to Gold Standard")
        print("   Provides scores, suggestions, and detailed analysis")
        
        try:
            # Get AI feedback
            response = self.session.get(f"{self.base_url}/api/session/{self.session_id}/feedback")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"✅ AI Feedback generated successfully")
                    print(f"   Overall Score: {result['overall_score']:.1f}/100")
                    
                    # Display score breakdown
                    scores = result["score_breakdown"]
                    print(f"   Score Breakdown:")
                    for category, score in scores.items():
                        print(f"      {category.replace('_', ' ').title()}: {score:.1f}/100")
                    
                    # Display feedback
                    feedback = result["feedback"]
                    print(f"   ✅ Strengths ({len(feedback['strengths'])}):")
                    for strength in feedback["strengths"][:2]:
                        print(f"      • {strength}")
                    
                    print(f"   ⚠️ Areas for Improvement ({len(feedback['improvements'])}):")
                    for improvement in feedback["improvements"][:2]:
                        print(f"      • {improvement}")
                    
                    # Test Gold Standard comparison
                    comparison_response = self.session.get(
                        f"{self.base_url}/api/session/{self.session_id}/gold-standard"
                    )
                    
                    if comparison_response.status_code == 200:
                        comparison = comparison_response.json()
                        if comparison.get("success"):
                            print(f"   ✅ Gold Standard comparison available")
                            gold = comparison["comparison"]["gold_standard"]
                            print(f"      AI Subjective length: {len(gold['subjective'])} chars")
                            print(f"      AI Metrics length: {len(gold['metrics'])} chars")
                    
                    return True
            
            print(f"❌ Feedback Mode failed: {response.status_code}")
            if response.content:
                print(f"   Error: {response.json()}")
            return False
            
        except Exception as e:
            print(f"❌ Feedback Mode error: {e}")
            return False
    
    def test_voice_agent_features(self) -> bool:
        """Test ElevenLabs Voice Agent features"""
        print("\n🎤 TESTING VOICE AGENT FEATURES")
        print("   ElevenLabs earnings call simulation")
        print("   SMAP audio briefings")
        
        try:
            # Test earnings call generation
            earnings_response = self.session.get(
                f"{self.base_url}/api/session/{self.session_id}/earnings-call"
            )
            
            if earnings_response.status_code == 200:
                earnings_result = earnings_response.json()
                if earnings_result.get("success"):
                    call_data = earnings_result["earnings_call"]
                    print(f"✅ Earnings call experience generated")
                    print(f"   Management script: {len(call_data['scripts']['management'])} chars")
                    print(f"   Analyst script: {len(call_data['scripts']['analyst'])} chars")
                    print(f"   Learning questions: {len(call_data['learning_activities']['comprehension_questions'])}")
            
            # Test audio briefing
            briefing_response = self.session.get(
                f"{self.base_url}/api/session/{self.session_id}/audio-briefing"
            )
            
            if briefing_response.status_code == 200:
                briefing_result = briefing_response.json()
                if briefing_result.get("success"):
                    briefing_data = briefing_result["briefing"]
                    print(f"   ✅ SMAP audio briefing generated")
                    print(f"      Duration: ~{briefing_data['duration_estimate']} seconds")
                    print(f"      Company: {briefing_data['company']}")
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Voice Agent error: {e}")
            return False
    
    def test_session_management(self) -> bool:
        """Test session status and management"""
        print("\n📊 TESTING SESSION MANAGEMENT")
        
        try:
            # Get session status
            status_response = self.session.get(
                f"{self.base_url}/api/session/{self.session_id}/status"
            )
            
            if status_response.status_code == 200:
                status_result = status_response.json()
                if status_result.get("success"):
                    session_data = status_result["session"]
                    print(f"✅ Session status retrieved")
                    print(f"   Status: {session_data['status']}")
                    print(f"   Mode: {session_data['current_mode']}")
                    print(f"   Score: {session_data['overall_score']:.1f}/100")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Session management error: {e}")
            return False
    
    def test_student_dashboard(self) -> bool:
        """Test student progress dashboard"""
        print("\n📈 TESTING STUDENT DASHBOARD")
        
        try:
            dashboard_response = self.session.get(
                f"{self.base_url}/api/student/{self.student_id}/dashboard"
            )
            
            if dashboard_response.status_code == 200:
                dashboard_result = dashboard_response.json()
                if dashboard_result.get("success"):
                    dashboard = dashboard_result["dashboard"]
                    progress = dashboard["progress_summary"]
                    
                    print(f"✅ Student dashboard retrieved")
                    print(f"   Total sessions: {progress['total_sessions']}")
                    print(f"   Average score: {progress['average_score']:.1f}")
                    print(f"   Learning streak: {progress['learning_streak']} days")
                    print(f"   Achievements: {len(dashboard['achievements'])}")
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
            return False
    
    def run_full_test_suite(self):
        """Run complete test suite for all three learning modes"""
        print("🧪 10Q NOTES AI - COMPLETE BACKEND API TEST SUITE")
        print("🎓 HackRU 2025 - Testing All Three Learning Modes")
        print("=" * 70)
        
        test_results = []
        
        # Test sequence
        tests = [
            ("Health Check", self.test_health_check),
            ("Student Authentication", self.test_student_authentication),
            ("File Upload & Session", self.test_file_upload_and_session_start),
            ("Learn Mode (Feature #1)", self.test_learn_mode),
            ("Practice Mode (Feature #2)", self.test_practice_mode),
            ("AI Feedback Mode (Feature #3)", self.test_feedback_mode),
            ("Voice Agent Features", self.test_voice_agent_features),
            ("Session Management", self.test_session_management),
            ("Student Dashboard", self.test_student_dashboard),
        ]
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name.upper()} {'='*20}")
            
            try:
                success = test_func()
                test_results.append((test_name, success))
                
                if success:
                    print(f"✅ {test_name} - PASSED")
                else:
                    print(f"❌ {test_name} - FAILED")
                    
            except Exception as e:
                print(f"💥 {test_name} - ERROR: {e}")
                test_results.append((test_name, False))
            
            time.sleep(1)  # Brief pause between tests
        
        # Summary
        print("\n" + "="*70)
        print("🏆 TEST SUITE SUMMARY")
        print("="*70)
        
        passed = sum(1 for _, success in test_results if success)
        total = len(test_results)
        
        for test_name, success in test_results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"   {test_name:25} {status}")
        
        print(f"\nOverall Result: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Backend is ready for HackRU judges!")
            print("🏆 Three Learning Modes fully operational:")
            print("   1. ✅ Learn Mode - Read & Hover with explanations")
            print("   2. ✅ Practice Mode - Student writes SMAP notes") 
            print("   3. ✅ AI Feedback Mode - Gemini comparison & scoring")
            print("   🎤 ✅ ElevenLabs Voice Integration")
        else:
            print(f"\n⚠️  {total-passed} tests failed. Check backend configuration.")
        
        print("\n🌟 10Q Notes AI Backend Testing Complete!")

def main():
    """Main testing function"""
    
    print("🚀 Starting 10Q Notes AI Backend API Tests")
    print("📝 Make sure the backend server is running on localhost:8000")
    print("   Run: python start_backend.py")
    
    # Quick connectivity check
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server not responding. Please start it first.")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to backend. Please start the server first.")
        print("   Command: python start_backend.py")
        return
    
    # Run tests
    tester = BackendAPITester()
    tester.run_full_test_suite()

if __name__ == "__main__":
    main()