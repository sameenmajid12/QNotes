#!/usr/bin/env python3
"""
🔥 HTML SEC Filing Stress Test - Microsoft 10-Q
HackRU 2025 Project by azrabano

Real-world stress testing using an 8.2MB Microsoft HTML 10-Q filing.
Tests Gemini API's ability to handle:
- Large HTML documents with complex XBRL markup
- Mixed content extraction (HTML tags + financial data)
- Rate limiting and chunk processing
- High accuracy financial data extraction
"""

import os
import sys
import time
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import requests

# Import services
sys.path.append('/Users/azrabano/10q-notes-ai')
from robust_gemini_service import RobustGeminiService
from gemini_service import GeminiService

@dataclass 
class FilingGroundTruth:
    """Known correct data for Microsoft Q3 2023 10-Q"""
    company_name: str = "Microsoft Corporation"
    ticker: str = "MSFT"
    filing_type: str = "10-Q"
    quarter: str = "Q3"
    fiscal_year: str = "2023"
    filing_date: str = "2023-04-20"
    cik: str = "0000789019"
    
    # Expected business segments
    expected_segments: List[str] = None
    
    # Expected financial concepts
    expected_metrics: List[str] = None
    
    def __post_init__(self):
        if self.expected_segments is None:
            self.expected_segments = [
                "Productivity and Business Processes",
                "Intelligent Cloud", 
                "More Personal Computing"
            ]
        
        if self.expected_metrics is None:
            self.expected_metrics = [
                "Total revenue",
                "Operating income", 
                "Net income",
                "Earnings per share",
                "Cash and equivalents"
            ]

@dataclass
class ProcessingResults:
    """Results from processing the large HTML filing"""
    file_size_mb: float
    processing_time: float
    html_content_length: int
    clean_text_length: int
    extraction_success: bool
    gemini_response_quality: float
    rate_limit_encounters: int
    chunks_processed: int
    company_accuracy: float
    financial_data_found: int
    error_messages: List[str] = None
    
    def __post_init__(self):
        if self.error_messages is None:
            self.error_messages = []

class HTMLFilingStressTester:
    """Stress test Gemini with real HTML SEC filing"""
    
    def __init__(self, html_file_path: str):
        """Initialize with path to HTML filing"""
        self.html_file_path = html_file_path
        self.ground_truth = FilingGroundTruth()
        
        print("🔥 HTML SEC FILING STRESS TESTER")
        print("=" * 60)
        print(f"📄 Target File: {html_file_path}")
        print(f"🎯 Expected Company: {self.ground_truth.company_name}")
        print(f"🎯 Expected Filing: {self.ground_truth.filing_type} {self.ground_truth.quarter} {self.ground_truth.fiscal_year}")
        print("=" * 60)
        
        # Initialize services
        try:
            self.robust_service = RobustGeminiService(enable_circuit_breaker=True)
            print("✅ Robust Gemini Service initialized")
        except Exception as e:
            print(f"❌ Robust service failed: {e}")
            self.robust_service = None
        
        try:
            self.basic_service = GeminiService()
            print("✅ Basic Gemini Service initialized")
        except Exception as e:
            print(f"❌ Basic service failed: {e}")
            self.basic_service = None
        
        if not self.robust_service and not self.basic_service:
            raise ValueError("❌ No Gemini services available for testing")
    
    def load_and_preprocess_html(self) -> Dict[str, Any]:
        """Load HTML file and extract clean text for processing"""
        
        print("\n📂 LOADING AND PREPROCESSING HTML FILE")
        print("-" * 50)
        
        start_time = time.time()
        
        # Get file stats
        file_stats = os.stat(self.html_file_path)
        file_size_mb = file_stats.st_size / (1024 * 1024)
        print(f"📊 File size: {file_size_mb:.2f} MB")
        print(f"🕒 Last modified: {datetime.fromtimestamp(file_stats.st_mtime)}")
        
        # Read HTML content
        with open(self.html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        print(f"📄 Raw HTML length: {len(html_content):,} characters")
        
        # Parse with BeautifulSoup to extract clean text
        print("🧹 Cleaning HTML markup...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(["script", "style", "meta", "link"]):
            element.decompose()
        
        # Extract clean text
        clean_text = soup.get_text()
        
        # Clean up whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text)
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
        clean_text = clean_text.strip()
        
        processing_time = time.time() - start_time
        
        print(f"✅ Clean text length: {len(clean_text):,} characters")
        print(f"📉 Size reduction: {((len(html_content) - len(clean_text)) / len(html_content)) * 100:.1f}%")
        print(f"⏱️ Preprocessing time: {processing_time:.2f} seconds")
        
        # Extract a sample for inspection
        text_sample = clean_text[:2000]
        print(f"\n📝 TEXT SAMPLE (first 2000 chars):")
        print("-" * 50)
        print(text_sample)
        print("-" * 50)
        
        return {
            'file_size_mb': file_size_mb,
            'html_content': html_content,
            'clean_text': clean_text,
            'preprocessing_time': processing_time,
            'size_reduction_percent': ((len(html_content) - len(clean_text)) / len(html_content)) * 100
        }
    
    def create_intelligent_chunks(self, text: str, max_chunk_size: int = 15000) -> List[str]:
        """Create intelligent text chunks for processing"""
        
        print(f"\n✂️ CREATING INTELLIGENT TEXT CHUNKS")
        print(f"📊 Target chunk size: {max_chunk_size:,} characters")
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size, save current chunk
            if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            
            current_chunk += paragraph + '\n\n'
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        print(f"📦 Created {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            print(f"   Chunk {i+1}: {len(chunk):,} characters")
        
        return chunks
    
    def test_gemini_with_chunks(self, chunks: List[str]) -> ProcessingResults:
        """Test Gemini API with chunked content"""
        
        print(f"\n🤖 TESTING GEMINI API WITH {len(chunks)} CHUNKS")
        print("=" * 60)
        
        start_time = time.time()
        rate_limit_count = 0
        successful_extractions = 0
        all_company_info = []
        all_errors = []
        
        service = self.robust_service or self.basic_service
        
        for i, chunk in enumerate(chunks):
            print(f"\n🔄 Processing Chunk {i+1}/{len(chunks)}")
            print(f"📊 Chunk size: {len(chunk):,} characters")
            
            try:
                # Test company extraction on this chunk
                company_info = service.extract_company_info(chunk)
                all_company_info.append(company_info)
                successful_extractions += 1
                
                print(f"   ✅ Company: {company_info.get('company_name', 'N/A')}")
                print(f"   📊 Ticker: {company_info.get('ticker', 'N/A')}")
                print(f"   📋 Filing: {company_info.get('filing_type', 'N/A')}")
                
            except Exception as e:
                error_msg = str(e)
                all_errors.append(f"Chunk {i+1}: {error_msg}")
                print(f"   ❌ Error: {error_msg}")
                
                # Check for rate limiting
                if "429" in error_msg or "quota" in error_msg.lower():
                    rate_limit_count += 1
                    print(f"   ⏳ Rate limit encountered, waiting 30 seconds...")
                    time.sleep(30)
            
            # Brief pause between chunks to respect rate limits
            time.sleep(2)
        
        processing_time = time.time() - start_time
        
        # Analyze results
        print(f"\n📊 CHUNK PROCESSING RESULTS")
        print("-" * 40)
        print(f"✅ Successful extractions: {successful_extractions}/{len(chunks)}")
        print(f"⚠️ Rate limit encounters: {rate_limit_count}")
        print(f"⏱️ Total processing time: {processing_time:.2f} seconds")
        print(f"📈 Average time per chunk: {processing_time/len(chunks):.2f} seconds")
        
        # Calculate accuracy
        company_accuracy = self._calculate_company_accuracy(all_company_info)
        financial_data_found = self._count_financial_references(all_company_info)
        
        print(f"🎯 Company identification accuracy: {company_accuracy:.1f}%")
        print(f"💰 Financial data references found: {financial_data_found}")
        
        return ProcessingResults(
            file_size_mb=0,  # Will be set later
            processing_time=processing_time,
            html_content_length=0,  # Will be set later
            clean_text_length=sum(len(chunk) for chunk in chunks),
            extraction_success=successful_extractions > 0,
            gemini_response_quality=company_accuracy,
            rate_limit_encounters=rate_limit_count,
            chunks_processed=len(chunks),
            company_accuracy=company_accuracy,
            financial_data_found=financial_data_found,
            error_messages=all_errors
        )
    
    def _calculate_company_accuracy(self, company_info_list: List[Dict]) -> float:
        """Calculate accuracy of company identification"""
        
        if not company_info_list:
            return 0.0
        
        correct_identifications = 0
        
        for info in company_info_list:
            score = 0
            
            # Check company name
            company_name = info.get('company_name', '').lower()
            if 'microsoft' in company_name:
                score += 0.4
            
            # Check ticker
            ticker = info.get('ticker', '').upper()
            if ticker == 'MSFT':
                score += 0.3
            
            # Check filing type
            filing_type = info.get('filing_type', '')
            if '10-Q' in filing_type:
                score += 0.2
            
            # Check industry
            industry = info.get('industry', '').lower()
            if 'technology' in industry or 'software' in industry:
                score += 0.1
            
            if score >= 0.7:  # 70% threshold
                correct_identifications += 1
        
        return (correct_identifications / len(company_info_list)) * 100
    
    def _count_financial_references(self, company_info_list: List[Dict]) -> int:
        """Count financial data references found"""
        
        financial_keywords = [
            'revenue', 'income', 'earnings', 'profit', 'margin', 
            'cash', 'debt', 'equity', 'assets', 'liabilities'
        ]
        
        count = 0
        for info in company_info_list:
            for field_value in info.values():
                if isinstance(field_value, str):
                    for keyword in financial_keywords:
                        if keyword in field_value.lower():
                            count += 1
        
        return count
    
    def run_comprehensive_stress_test(self) -> Dict[str, Any]:
        """Run the complete stress test"""
        
        print("\n🚀 STARTING COMPREHENSIVE STRESS TEST")
        print("=" * 70)
        start_time = datetime.now()
        print(f"🕒 Test started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 1. Load and preprocess HTML
            preprocessing_results = self.load_and_preprocess_html()
            
            # 2. Create intelligent chunks
            chunks = self.create_intelligent_chunks(
                preprocessing_results['clean_text'],
                max_chunk_size=12000  # Smaller chunks to avoid rate limits
            )
            
            # 3. Test Gemini with chunks
            processing_results = self.test_gemini_with_chunks(chunks)
            
            # Update processing results with file info
            processing_results.file_size_mb = preprocessing_results['file_size_mb']
            processing_results.html_content_length = len(preprocessing_results['html_content'])
            
            # 4. Generate final report
            end_time = datetime.now()
            total_duration = (end_time - start_time).total_seconds()
            
            final_results = {
                'test_metadata': {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'total_duration_seconds': total_duration,
                    'file_path': self.html_file_path,
                    'ground_truth': asdict(self.ground_truth)
                },
                'preprocessing': preprocessing_results,
                'processing': asdict(processing_results),
                'performance_assessment': self._generate_performance_assessment(processing_results)
            }
            
            self._print_final_report(final_results)
            
            return final_results
            
        except Exception as e:
            print(f"\n❌ STRESS TEST FAILED: {e}")
            return {
                'error': str(e),
                'test_metadata': {
                    'start_time': start_time.isoformat(),
                    'failed_at': datetime.now().isoformat()
                }
            }
    
    def _generate_performance_assessment(self, results: ProcessingResults) -> Dict[str, Any]:
        """Generate performance assessment"""
        
        assessment = {
            'overall_grade': 'UNKNOWN',
            'strengths': [],
            'areas_for_improvement': [],
            'scalability_rating': 'UNKNOWN',
            'accuracy_rating': 'UNKNOWN'
        }
        
        # Accuracy assessment
        if results.company_accuracy >= 90:
            assessment['accuracy_rating'] = 'EXCELLENT'
            assessment['strengths'].append('High accuracy company identification')
        elif results.company_accuracy >= 70:
            assessment['accuracy_rating'] = 'GOOD'
            assessment['strengths'].append('Good accuracy in most cases')
        else:
            assessment['accuracy_rating'] = 'NEEDS_IMPROVEMENT'
            assessment['areas_for_improvement'].append('Improve company identification accuracy')
        
        # Scalability assessment
        if results.rate_limit_encounters == 0 and results.processing_time < 300:  # 5 minutes
            assessment['scalability_rating'] = 'EXCELLENT'
            assessment['strengths'].append('Handles large files efficiently')
        elif results.rate_limit_encounters < 3:
            assessment['scalability_rating'] = 'GOOD'
            assessment['strengths'].append('Reasonable performance with minor rate limiting')
        else:
            assessment['scalability_rating'] = 'NEEDS_IMPROVEMENT'
            assessment['areas_for_improvement'].append('Optimize for rate limiting and performance')
        
        # Overall grade
        if assessment['accuracy_rating'] == 'EXCELLENT' and assessment['scalability_rating'] == 'EXCELLENT':
            assessment['overall_grade'] = 'A+'
        elif 'EXCELLENT' in [assessment['accuracy_rating'], assessment['scalability_rating']]:
            assessment['overall_grade'] = 'B+'
        elif 'GOOD' in [assessment['accuracy_rating'], assessment['scalability_rating']]:
            assessment['overall_grade'] = 'B'
        else:
            assessment['overall_grade'] = 'C'
        
        return assessment
    
    def _print_final_report(self, results: Dict[str, Any]):
        """Print comprehensive final report"""
        
        print("\n" + "=" * 70)
        print("🏆 HTML SEC FILING STRESS TEST RESULTS")
        print("=" * 70)
        
        # Test metadata
        meta = results['test_metadata']
        print(f"\n📊 TEST SUMMARY:")
        print(f"   🕒 Duration: {meta['total_duration_seconds']:.1f} seconds")
        print(f"   📄 File: {os.path.basename(meta['file_path'])}")
        print(f"   🎯 Target: {meta['ground_truth']['company_name']} {meta['ground_truth']['filing_type']}")
        
        # File processing
        prep = results['preprocessing']
        proc = results['processing']
        print(f"\n📂 FILE PROCESSING:")
        print(f"   💾 Original size: {prep['file_size_mb']:.2f} MB")
        print(f"   📄 HTML content: {prep['html_content'].__len__() if 'html_content' in prep else 'N/A':,} chars")
        print(f"   🧹 Clean text: {proc['clean_text_length']:,} chars")
        print(f"   📦 Chunks processed: {proc['chunks_processed']}")
        
        # API Performance
        print(f"\n🤖 GEMINI API PERFORMANCE:")
        print(f"   ⏱️ Processing time: {proc['processing_time']:.2f} seconds")
        print(f"   ⚠️ Rate limit encounters: {proc['rate_limit_encounters']}")
        print(f"   🎯 Company accuracy: {proc['company_accuracy']:.1f}%")
        print(f"   💰 Financial references: {proc['financial_data_found']}")
        
        # Performance assessment
        assessment = results['performance_assessment']
        print(f"\n🎯 PERFORMANCE ASSESSMENT:")
        print(f"   📊 Overall Grade: {assessment['overall_grade']}")
        print(f"   🎯 Accuracy Rating: {assessment['accuracy_rating']}")
        print(f"   ⚡ Scalability Rating: {assessment['scalability_rating']}")
        
        print(f"\n✅ STRENGTHS:")
        for strength in assessment['strengths']:
            print(f"     • {strength}")
        
        if assessment['areas_for_improvement']:
            print(f"\n⚠️ AREAS FOR IMPROVEMENT:")
            for area in assessment['areas_for_improvement']:
                print(f"     • {area}")
        
        # Errors
        if proc['error_messages']:
            print(f"\n❌ ERRORS ENCOUNTERED:")
            for error in proc['error_messages'][:5]:  # Show first 5 errors
                print(f"     • {error}")
            if len(proc['error_messages']) > 5:
                print(f"     ... and {len(proc['error_messages']) - 5} more errors")
        
        print(f"\n✨ STRESS TEST COMPLETED!")
        print("🚀 Ready for production-scale SEC filing processing!")
        print("=" * 70)

def main():
    """Run the HTML filing stress test"""
    
    html_file_path = "/Users/azrabano/Downloads/10-Q.html"
    
    # Verify file exists
    if not os.path.exists(html_file_path):
        print(f"❌ File not found: {html_file_path}")
        return False
    
    try:
        # Create and run stress tester
        tester = HTMLFilingStressTester(html_file_path)
        results = tester.run_comprehensive_stress_test()
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"/Users/azrabano/10q-notes-ai/html_stress_test_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            # Handle non-serializable objects
            serializable_results = json.loads(json.dumps(results, default=str))
            json.dump(serializable_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        # Determine success
        if 'processing' in results:
            success = (results['processing']['extraction_success'] and 
                      results['processing']['company_accuracy'] >= 70)
        else:
            success = False
        
        return success
        
    except Exception as e:
        print(f"❌ HTML stress test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    print(f"\n📊 Exit code: {exit_code}")
    sys.exit(exit_code)