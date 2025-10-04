#!/usr/bin/env python3
"""
🧪 Gemini API Stress Testing & Accuracy Validation Suite
HackRU 2025 Project by azrabano

Comprehensive testing framework for Gemini API:
- Accuracy testing against ground truth data
- Performance benchmarking and load testing
- Error handling and edge case validation
- Response quality and consistency metrics
"""

import asyncio
import time
import json
import statistics
import concurrent.futures
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import sys
import os

# Import your Gemini services
sys.path.append('/Users/azrabano/10q-notes-ai')
from gemini_service import GeminiService
from enhanced_gemini_service import EnhancedGeminiService

@dataclass
class GroundTruthData:
    """Known correct data for accuracy testing"""
    company_name: str
    ticker: str
    filing_type: str
    quarter_year: str
    industry: str
    
    # Financial metrics
    total_revenue: float
    net_income: float
    return_on_equity: float
    net_interest_margin: Optional[float] = None
    common_equity_tier1_ratio: Optional[float] = None
    
    # Expected SMAP characteristics
    expected_subjective_keywords: List[str] = None
    expected_metrics_count: int = 5
    expected_risk_categories: int = 3

@dataclass
class TestResult:
    """Individual test result"""
    test_name: str
    success: bool
    accuracy_score: float  # 0-100
    response_time: float
    error_message: Optional[str] = None
    extracted_data: Optional[Dict] = None

@dataclass
class StressTestMetrics:
    """Overall stress test metrics"""
    total_tests: int
    passed_tests: int
    failed_tests: int
    average_accuracy: float
    average_response_time: float
    max_response_time: float
    min_response_time: float
    error_rate: float
    concurrent_performance: Dict[str, float]

class GeminiStressTester:
    """Comprehensive Gemini API testing framework"""
    
    def __init__(self):
        """Initialize the stress tester"""
        print("🧪 Initializing Gemini Stress Testing Framework")
        print("=" * 60)
        
        try:
            self.basic_service = GeminiService()
            print("✅ Basic Gemini Service initialized")
        except Exception as e:
            print(f"❌ Basic Gemini Service failed: {e}")
            self.basic_service = None
        
        try:
            self.enhanced_service = EnhancedGeminiService()
            print("✅ Enhanced Gemini Service initialized")
        except Exception as e:
            print(f"❌ Enhanced Gemini Service failed: {e}")
            self.enhanced_service = None
        
        if not self.basic_service and not self.enhanced_service:
            raise ValueError("❌ No Gemini services available for testing")
        
        self.test_results = []
        
        # Ground truth test data
        self.ground_truth_data = self._create_ground_truth_datasets()
        print(f"📊 Created {len(self.ground_truth_data)} ground truth test datasets")
    
    def _create_ground_truth_datasets(self) -> Dict[str, Tuple[str, GroundTruthData]]:
        """Create test datasets with known correct answers"""
        
        datasets = {}
        
        # JPMorgan Chase 10-Q Q1 2025 (Sample)
        jpmc_filing = """
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
        
        jpmc_truth = GroundTruthData(
            company_name="JPMorgan Chase & Co.",
            ticker="JPM",
            filing_type="10-Q",
            quarter_year="Q1 2025",
            industry="Banking",
            total_revenue=42.5,
            net_income=13.4,
            return_on_equity=0.178,
            net_interest_margin=0.0274,
            common_equity_tier1_ratio=0.159,
            expected_subjective_keywords=["fortress", "resilience", "diversified", "disciplined", "cautiously optimistic"],
            expected_metrics_count=6,
            expected_risk_categories=4
        )
        
        datasets["jpmc_q1_2025"] = (jpmc_filing, jpmc_truth)
        
        # Apple 10-Q Q2 2024 (Sample)
        apple_filing = """
        APPLE INC.
        FORM 10-Q - QUARTERLY REPORT
        For the quarterly period ended March 31, 2024
        
        Three Months Ended March 31, 2024 and 2023
        
        Net sales for the second quarter of fiscal 2024 were $90.8 billion, a decrease of 4% 
        compared to the same quarter of fiscal 2023. This decline was primarily due to lower 
        iPhone sales in certain international markets, partially offset by strong services growth.
        
        Products revenue was $69.7 billion, down 1% year-over-year, while Services revenue 
        reached a new all-time high of $23.9 billion, up 14% year-over-year.
        
        Net income was $23.6 billion, representing earnings per diluted share of $1.53, 
        compared to $24.2 billion and $1.52 per share in the prior year.
        
        Gross margin was 46.6%, compared to 44.3% in the year-ago quarter, reflecting 
        favorable product mix and improved Services margins.
        
        We returned $27 billion to shareholders during the quarter through dividends and 
        share repurchases, maintaining our commitment to capital return.
        
        Looking ahead, we remain focused on innovation across our product portfolio and 
        expanding our services ecosystem. Key risks include supply chain disruptions, 
        foreign exchange volatility, and competitive pressures in key markets.
        """
        
        apple_truth = GroundTruthData(
            company_name="Apple Inc.",
            ticker="AAPL",
            filing_type="10-Q",
            quarter_year="Q2 2024",
            industry="Technology",
            total_revenue=90.8,
            net_income=23.6,
            return_on_equity=None,  # Not provided
            expected_subjective_keywords=["innovation", "ecosystem", "commitment", "focused"],
            expected_metrics_count=7,
            expected_risk_categories=3
        )
        
        datasets["apple_q2_2024"] = (apple_filing, apple_truth)
        
        # Edge case: Short, incomplete filing
        short_filing = """
        TESTCORP INC.
        FORM 10-Q
        
        Revenue: $100 million
        Net income: $10 million
        We face competitive pressures.
        """
        
        short_truth = GroundTruthData(
            company_name="TestCorp Inc.",
            ticker="TEST",
            filing_type="10-Q",
            quarter_year="Unknown",
            industry="Unknown",
            total_revenue=100,
            net_income=10,
            return_on_equity=None,
            expected_metrics_count=2,
            expected_risk_categories=1
        )
        
        datasets["short_filing"] = (short_filing, short_truth)
        
        return datasets
    
    def test_basic_api_connectivity(self) -> TestResult:
        """Test basic API connectivity and response"""
        print("\n🔗 Testing Basic API Connectivity...")
        
        start_time = time.time()
        
        try:
            if self.basic_service:
                success = self.basic_service.test_connection()
                response_time = time.time() - start_time
                
                return TestResult(
                    test_name="Basic API Connectivity",
                    success=success,
                    accuracy_score=100.0 if success else 0.0,
                    response_time=response_time
                )
            else:
                return TestResult(
                    test_name="Basic API Connectivity",
                    success=False,
                    accuracy_score=0.0,
                    response_time=0.0,
                    error_message="Basic service not available"
                )
                
        except Exception as e:
            return TestResult(
                test_name="Basic API Connectivity",
                success=False,
                accuracy_score=0.0,
                response_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def test_company_extraction_accuracy(self, filing_text: str, ground_truth: GroundTruthData) -> TestResult:
        """Test accuracy of company information extraction"""
        print(f"📊 Testing company extraction for {ground_truth.company_name}...")
        
        start_time = time.time()
        
        try:
            if self.basic_service:
                extracted_info = self.basic_service.extract_company_info(filing_text)
                response_time = time.time() - start_time
                
                # Calculate accuracy score
                accuracy_score = self._calculate_company_extraction_accuracy(extracted_info, ground_truth)
                
                return TestResult(
                    test_name=f"Company Extraction - {ground_truth.company_name}",
                    success=accuracy_score > 70,  # 70% threshold
                    accuracy_score=accuracy_score,
                    response_time=response_time,
                    extracted_data=extracted_info
                )
            else:
                return TestResult(
                    test_name=f"Company Extraction - {ground_truth.company_name}",
                    success=False,
                    accuracy_score=0.0,
                    response_time=0.0,
                    error_message="Service not available"
                )
                
        except Exception as e:
            return TestResult(
                test_name=f"Company Extraction - {ground_truth.company_name}",
                success=False,
                accuracy_score=0.0,
                response_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def test_financial_metrics_accuracy(self, filing_text: str, ground_truth: GroundTruthData) -> TestResult:
        """Test accuracy of financial metrics extraction"""
        print(f"💰 Testing financial metrics for {ground_truth.company_name}...")
        
        start_time = time.time()
        
        try:
            if self.enhanced_service:
                extracted_metrics = self.enhanced_service.extract_structured_metrics(filing_text)
                response_time = time.time() - start_time
                
                # Calculate accuracy score
                accuracy_score = self._calculate_metrics_accuracy(extracted_metrics, ground_truth)
                
                return TestResult(
                    test_name=f"Financial Metrics - {ground_truth.company_name}",
                    success=accuracy_score > 70,
                    accuracy_score=accuracy_score,
                    response_time=response_time,
                    extracted_data=asdict(extracted_metrics)
                )
            else:
                return TestResult(
                    test_name=f"Financial Metrics - {ground_truth.company_name}",
                    success=False,
                    accuracy_score=0.0,
                    response_time=0.0,
                    error_message="Enhanced service not available"
                )
                
        except Exception as e:
            return TestResult(
                test_name=f"Financial Metrics - {ground_truth.company_name}",
                success=False,
                accuracy_score=0.0,
                response_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def test_smap_generation_quality(self, filing_text: str, ground_truth: GroundTruthData) -> TestResult:
        """Test quality of SMAP note generation"""
        print(f"📝 Testing SMAP generation for {ground_truth.company_name}...")
        
        start_time = time.time()
        
        try:
            if self.basic_service:
                smap_notes = self.basic_service.generate_smap_notes(filing_text)
                response_time = time.time() - start_time
                
                # Calculate quality score
                quality_score = self._calculate_smap_quality(smap_notes, ground_truth)
                
                return TestResult(
                    test_name=f"SMAP Generation - {ground_truth.company_name}",
                    success=quality_score > 70,
                    accuracy_score=quality_score,
                    response_time=response_time,
                    extracted_data={
                        'subjective_length': len(smap_notes.subjective),
                        'metrics_length': len(smap_notes.metrics),
                        'assessment_length': len(smap_notes.assessment),
                        'plan_length': len(smap_notes.plan)
                    }
                )
            else:
                return TestResult(
                    test_name=f"SMAP Generation - {ground_truth.company_name}",
                    success=False,
                    accuracy_score=0.0,
                    response_time=0.0,
                    error_message="Service not available"
                )
                
        except Exception as e:
            return TestResult(
                test_name=f"SMAP Generation - {ground_truth.company_name}",
                success=False,
                accuracy_score=0.0,
                response_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def test_concurrent_load(self, num_concurrent: int = 5) -> TestResult:
        """Test concurrent API calls performance"""
        print(f"⚡ Testing concurrent load with {num_concurrent} requests...")
        
        start_time = time.time()
        
        try:
            # Use first dataset for load testing
            filing_text, ground_truth = list(self.ground_truth_data.values())[0]
            
            def single_request():
                if self.basic_service:
                    return self.basic_service.extract_company_info(filing_text)
                return None
            
            # Execute concurrent requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
                futures = [executor.submit(single_request) for _ in range(num_concurrent)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            response_time = time.time() - start_time
            
            # Check if all requests succeeded
            successful_requests = sum(1 for result in results if result is not None and result.get('company_name'))
            success_rate = successful_requests / num_concurrent
            
            return TestResult(
                test_name=f"Concurrent Load ({num_concurrent} requests)",
                success=success_rate > 0.8,  # 80% success rate threshold
                accuracy_score=success_rate * 100,
                response_time=response_time,
                extracted_data={
                    'successful_requests': successful_requests,
                    'total_requests': num_concurrent,
                    'success_rate': success_rate,
                    'avg_time_per_request': response_time / num_concurrent
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name=f"Concurrent Load ({num_concurrent} requests)",
                success=False,
                accuracy_score=0.0,
                response_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def test_edge_cases(self) -> List[TestResult]:
        """Test various edge cases and error handling"""
        print("🔍 Testing edge cases and error handling...")
        
        edge_cases = [
            ("Empty text", ""),
            ("Very short text", "Apple revenue $1M"),
            ("Malformed text", "}{invalid json malformed$$$"),
            ("Very long text", "A" * 50000),  # 50k characters
            ("Non-English text", "这是中文测试文本"),
            ("Special characters", "Revenue: $1.5M @#$%^&*()"),
            ("HTML-like text", "<html><body>Revenue: $100M</body></html>"),
            ("Numbers only", "123456789 987654321 100.50"),
        ]
        
        results = []
        
        for case_name, test_text in edge_cases:
            start_time = time.time()
            
            try:
                if self.basic_service:
                    result = self.basic_service.extract_company_info(test_text)
                    response_time = time.time() - start_time
                    
                    # For edge cases, success is handling gracefully without crashing
                    success = isinstance(result, dict) and 'company_name' in result
                    
                    results.append(TestResult(
                        test_name=f"Edge Case - {case_name}",
                        success=success,
                        accuracy_score=100.0 if success else 0.0,
                        response_time=response_time,
                        extracted_data=result if success else None
                    ))
                else:
                    results.append(TestResult(
                        test_name=f"Edge Case - {case_name}",
                        success=False,
                        accuracy_score=0.0,
                        response_time=0.0,
                        error_message="Service not available"
                    ))
                    
            except Exception as e:
                results.append(TestResult(
                    test_name=f"Edge Case - {case_name}",
                    success=False,
                    accuracy_score=0.0,
                    response_time=time.time() - start_time,
                    error_message=str(e)
                ))
        
        return results
    
    def _calculate_company_extraction_accuracy(self, extracted: Dict, truth: GroundTruthData) -> float:
        """Calculate accuracy score for company extraction"""
        score = 0.0
        max_score = 5.0
        
        # Company name similarity (case-insensitive partial match)
        if extracted.get('company_name', '').lower() in truth.company_name.lower() or \
           truth.company_name.lower() in extracted.get('company_name', '').lower():
            score += 1.5
        
        # Ticker exact match
        if extracted.get('ticker', '').upper() == truth.ticker.upper():
            score += 1.0
        
        # Filing type match
        if extracted.get('filing_type', '') == truth.filing_type:
            score += 1.0
        
        # Quarter/year match
        if extracted.get('quarter_year', '') == truth.quarter_year:
            score += 1.0
        
        # Industry match (partial)
        extracted_industry = extracted.get('industry', '').lower()
        truth_industry = truth.industry.lower()
        if truth_industry in extracted_industry or extracted_industry in truth_industry:
            score += 0.5
        
        return (score / max_score) * 100
    
    def _calculate_metrics_accuracy(self, extracted_metrics, truth: GroundTruthData) -> float:
        """Calculate accuracy score for financial metrics"""
        score = 0.0
        max_score = 0.0
        
        # Check each metric with tolerance
        tolerance = 0.05  # 5% tolerance
        
        metrics_to_check = [
            ('total_revenue', truth.total_revenue),
            ('net_income', truth.net_income),
            ('return_on_equity', truth.return_on_equity),
            ('net_interest_margin', truth.net_interest_margin),
            ('common_equity_tier1_ratio', truth.common_equity_tier1_ratio),
        ]
        
        for metric_name, truth_value in metrics_to_check:
            if truth_value is not None:
                max_score += 1.0
                extracted_value = getattr(extracted_metrics, metric_name)
                
                if extracted_value is not None:
                    # Calculate relative error
                    if truth_value != 0:
                        relative_error = abs(extracted_value - truth_value) / abs(truth_value)
                        if relative_error <= tolerance:
                            score += 1.0
                        elif relative_error <= tolerance * 2:  # Partial credit
                            score += 0.5
        
        return (score / max_score * 100) if max_score > 0 else 0.0
    
    def _calculate_smap_quality(self, smap_notes, truth: GroundTruthData) -> float:
        """Calculate quality score for SMAP notes"""
        score = 0.0
        max_score = 4.0
        
        # Check section lengths (should be substantial)
        min_length = 50
        
        if len(smap_notes.subjective) >= min_length:
            score += 1.0
        if len(smap_notes.metrics) >= min_length:
            score += 1.0
        if len(smap_notes.assessment) >= min_length:
            score += 1.0
        if len(smap_notes.plan) >= min_length:
            score += 1.0
        
        # Check for expected keywords in subjective section (if provided)
        if truth.expected_subjective_keywords:
            subjective_lower = smap_notes.subjective.lower()
            keyword_matches = sum(1 for keyword in truth.expected_subjective_keywords 
                                if keyword.lower() in subjective_lower)
            keyword_score = keyword_matches / len(truth.expected_subjective_keywords)
            # Add bonus for keyword presence (up to 20 points)
            score += keyword_score * 0.8
            max_score += 0.8
        
        return (score / max_score) * 100
    
    def run_comprehensive_stress_test(self) -> StressTestMetrics:
        """Run the complete stress testing suite"""
        print("\n🧪 RUNNING COMPREHENSIVE GEMINI STRESS TEST SUITE")
        print("=" * 70)
        print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        all_results = []
        
        # 1. Basic connectivity test
        connectivity_result = self.test_basic_api_connectivity()
        all_results.append(connectivity_result)
        
        if not connectivity_result.success:
            print("❌ Basic connectivity failed. Aborting stress test.")
            return self._generate_stress_metrics(all_results)
        
        # 2. Accuracy tests for each dataset
        for dataset_name, (filing_text, ground_truth) in self.ground_truth_data.items():
            print(f"\n📊 Testing dataset: {dataset_name}")
            
            # Company extraction test
            company_result = self.test_company_extraction_accuracy(filing_text, ground_truth)
            all_results.append(company_result)
            
            # Financial metrics test (if enhanced service available)
            if self.enhanced_service:
                metrics_result = self.test_financial_metrics_accuracy(filing_text, ground_truth)
                all_results.append(metrics_result)
            
            # SMAP generation test
            smap_result = self.test_smap_generation_quality(filing_text, ground_truth)
            all_results.append(smap_result)
            
            # Brief pause between datasets
            time.sleep(1)
        
        # 3. Concurrent load tests
        for num_concurrent in [3, 5, 8]:
            concurrent_result = self.test_concurrent_load(num_concurrent)
            all_results.append(concurrent_result)
            time.sleep(2)  # Cool down between load tests
        
        # 4. Edge case tests
        edge_results = self.test_edge_cases()
        all_results.extend(edge_results)
        
        # Store results
        self.test_results = all_results
        
        # Generate metrics
        return self._generate_stress_metrics(all_results)
    
    def _generate_stress_metrics(self, results: List[TestResult]) -> StressTestMetrics:
        """Generate comprehensive metrics from test results"""
        
        if not results:
            return StressTestMetrics(0, 0, 0, 0.0, 0.0, 0.0, 0.0, 100.0, {})
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.success)
        failed_tests = total_tests - passed_tests
        
        # Calculate accuracy and timing metrics
        accuracy_scores = [r.accuracy_score for r in results if r.accuracy_score is not None]
        response_times = [r.response_time for r in results if r.response_time is not None and r.response_time > 0]
        
        average_accuracy = statistics.mean(accuracy_scores) if accuracy_scores else 0.0
        average_response_time = statistics.mean(response_times) if response_times else 0.0
        max_response_time = max(response_times) if response_times else 0.0
        min_response_time = min(response_times) if response_times else 0.0
        error_rate = (failed_tests / total_tests) * 100
        
        # Concurrent performance analysis
        concurrent_results = [r for r in results if 'Concurrent Load' in r.test_name]
        concurrent_performance = {}
        for result in concurrent_results:
            if result.extracted_data:
                num_requests = result.extracted_data.get('total_requests', 0)
                concurrent_performance[f'{num_requests}_requests'] = result.accuracy_score
        
        return StressTestMetrics(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            average_accuracy=average_accuracy,
            average_response_time=average_response_time,
            max_response_time=max_response_time,
            min_response_time=min_response_time,
            error_rate=error_rate,
            concurrent_performance=concurrent_performance
        )
    
    def print_detailed_results(self, metrics: StressTestMetrics):
        """Print comprehensive test results"""
        print("\n" + "=" * 70)
        print("🏆 GEMINI STRESS TEST RESULTS")
        print("=" * 70)
        
        print(f"\n📊 OVERALL PERFORMANCE:")
        print(f"   Total Tests: {metrics.total_tests}")
        print(f"   ✅ Passed: {metrics.passed_tests} ({(metrics.passed_tests/metrics.total_tests)*100:.1f}%)")
        print(f"   ❌ Failed: {metrics.failed_tests} ({(metrics.failed_tests/metrics.total_tests)*100:.1f}%)")
        print(f"   📈 Average Accuracy: {metrics.average_accuracy:.1f}%")
        print(f"   ⚠️ Error Rate: {metrics.error_rate:.1f}%")
        
        print(f"\n⏱️ TIMING PERFORMANCE:")
        print(f"   Average Response: {metrics.average_response_time:.2f}s")
        print(f"   Fastest Response: {metrics.min_response_time:.2f}s")
        print(f"   Slowest Response: {metrics.max_response_time:.2f}s")
        
        if metrics.concurrent_performance:
            print(f"\n⚡ CONCURRENT PERFORMANCE:")
            for load_test, success_rate in metrics.concurrent_performance.items():
                print(f"   {load_test}: {success_rate:.1f}% success rate")
        
        print(f"\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result.success else "❌"
            print(f"   {status} {result.test_name:40} Acc: {result.accuracy_score:.1f}% Time: {result.response_time:.2f}s")
            if result.error_message:
                print(f"      Error: {result.error_message}")
        
        # Performance assessment
        print(f"\n🎯 PERFORMANCE ASSESSMENT:")
        
        if metrics.average_accuracy >= 90:
            accuracy_grade = "🟢 EXCELLENT"
        elif metrics.average_accuracy >= 80:
            accuracy_grade = "🟡 GOOD"
        elif metrics.average_accuracy >= 70:
            accuracy_grade = "🟠 ACCEPTABLE"
        else:
            accuracy_grade = "🔴 NEEDS IMPROVEMENT"
        
        if metrics.average_response_time <= 2.0:
            speed_grade = "🟢 FAST"
        elif metrics.average_response_time <= 5.0:
            speed_grade = "🟡 MODERATE"
        else:
            speed_grade = "🔴 SLOW"
        
        if metrics.error_rate <= 5:
            reliability_grade = "🟢 HIGHLY RELIABLE"
        elif metrics.error_rate <= 15:
            reliability_grade = "🟡 RELIABLE"
        else:
            reliability_grade = "🔴 UNRELIABLE"
        
        print(f"   Accuracy: {accuracy_grade} ({metrics.average_accuracy:.1f}%)")
        print(f"   Speed: {speed_grade} ({metrics.average_response_time:.2f}s avg)")
        print(f"   Reliability: {reliability_grade} ({metrics.error_rate:.1f}% error rate)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if metrics.average_accuracy < 80:
            print("   • Improve prompt engineering for better accuracy")
            print("   • Add more context to extraction prompts")
        if metrics.average_response_time > 3:
            print("   • Consider optimizing prompt length")
            print("   • Implement request batching for concurrent calls")
        if metrics.error_rate > 10:
            print("   • Strengthen error handling and retries")
            print("   • Add input validation before API calls")
        
        print(f"\n✨ TEST COMPLETED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

def main():
    """Main function to run stress tests"""
    try:
        tester = GeminiStressTester()
        metrics = tester.run_comprehensive_stress_test()
        tester.print_detailed_results(metrics)
        
        # Save results to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"/Users/azrabano/10q-notes-ai/stress_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump({
                'metrics': asdict(metrics),
                'detailed_results': [asdict(r) for r in tester.test_results],
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        return metrics.average_accuracy >= 80 and metrics.error_rate <= 10
        
    except Exception as e:
        print(f"❌ Stress test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)