#!/usr/bin/env python3
"""
🛡️ Robust Gemini Service with Enhanced Error Handling
HackRU 2025 Project by azrabano

High-reliability Gemini API service with:
- Comprehensive error handling and retries
- Input validation and sanitization  
- Response validation and fallback mechanisms
- Rate limiting and circuit breaker patterns
- Performance monitoring and metrics
"""

import os
import json
import time
import logging
import statistics
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from functools import wraps
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class APIMetrics:
    """Track API performance metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    retry_count: int = 0
    average_response_time: float = 0.0
    response_times: List[float] = None
    error_types: Dict[str, int] = None
    
    def __post_init__(self):
        if self.response_times is None:
            self.response_times = []
        if self.error_types is None:
            self.error_types = {}
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def error_rate(self) -> float:
        return 100 - self.success_rate

@dataclass
class ValidationResult:
    """Result of input/output validation"""
    is_valid: bool
    errors: List[str] = None
    warnings: List[str] = None
    sanitized_input: Optional[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open"""
    pass

class CircuitBreaker:
    """Circuit breaker pattern for API resilience"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return True
        return (datetime.now() - self.last_failure_time).seconds >= self.recovery_timeout
    
    def _on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

class InputValidator:
    """Validate and sanitize input data"""
    
    @staticmethod
    def validate_filing_text(text: str) -> ValidationResult:
        """Validate SEC filing text input"""
        errors = []
        warnings = []
        
        if not text or not isinstance(text, str):
            errors.append("Input text is required and must be a string")
            return ValidationResult(False, errors)
        
        # Length checks
        if len(text) < 100:
            warnings.append("Input text is very short, may affect extraction quality")
        elif len(text) > 200000:  # 200k character limit
            warnings.append("Input text is very long, may cause API timeouts")
            text = text[:200000]  # Truncate
        
        # Content validation
        if not re.search(r'\d+', text):
            warnings.append("No numbers found in text, financial data extraction may be limited")
        
        if not re.search(r'(revenue|income|profit|loss|margin|ratio)', text, re.IGNORECASE):
            warnings.append("No common financial terms found, may not be a financial document")
        
        # Sanitize text
        sanitized = InputValidator._sanitize_text(text)
        
        return ValidationResult(
            is_valid=True,
            errors=errors,
            warnings=warnings,
            sanitized_input=sanitized
        )
    
    @staticmethod
    def _sanitize_text(text: str) -> str:
        """Sanitize input text for API processing"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove or replace problematic characters that might break JSON
        text = text.replace('\x00', '')  # Remove null bytes
        text = text.replace('\r\n', '\n')  # Normalize line endings
        text = text.replace('\r', '\n')
        
        # Ensure UTF-8 compliance
        text = text.encode('utf-8', errors='ignore').decode('utf-8')
        
        return text.strip()

class ResponseValidator:
    """Validate API responses and extracted data"""
    
    @staticmethod
    def validate_json_response(response_text: str) -> ValidationResult:
        """Validate JSON response from API"""
        errors = []
        warnings = []
        
        if not response_text:
            errors.append("Empty response from API")
            return ValidationResult(False, errors)
        
        # Try to parse JSON
        try:
            # Clean common JSON formatting issues
            cleaned_text = ResponseValidator._clean_json_response(response_text)
            parsed_json = json.loads(cleaned_text)
            
            if not isinstance(parsed_json, dict):
                errors.append("Response is not a valid JSON object")
                return ValidationResult(False, errors)
            
            return ValidationResult(True, errors, warnings)
            
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON format: {str(e)}")
            return ValidationResult(False, errors)
    
    @staticmethod
    def validate_company_info(data: Dict) -> ValidationResult:
        """Validate extracted company information"""
        errors = []
        warnings = []
        
        required_fields = ['company_name', 'ticker', 'filing_type']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate ticker format (typically 1-5 uppercase letters)
        if 'ticker' in data and data['ticker']:
            ticker = data['ticker'].upper()
            if not re.match(r'^[A-Z]{1,5}$', ticker):
                warnings.append(f"Unusual ticker format: {ticker}")
        
        # Validate filing type
        valid_filings = ['10-Q', '10-K', '8-K', '10-Q/A', '10-K/A']
        if 'filing_type' in data and data['filing_type'] not in valid_filings:
            warnings.append(f"Uncommon filing type: {data['filing_type']}")
        
        return ValidationResult(len(errors) == 0, errors, warnings)
    
    @staticmethod
    def validate_financial_metrics(data: Dict) -> ValidationResult:
        """Validate extracted financial metrics"""
        errors = []
        warnings = []
        
        # Check for reasonable metric values
        numeric_fields = ['total_revenue', 'net_income', 'return_on_equity', 'net_interest_margin']
        
        for field in numeric_fields:
            if field in data and data[field] is not None:
                value = data[field]
                
                # Basic sanity checks
                if field in ['return_on_equity', 'net_interest_margin'] and (value < -1 or value > 1):
                    warnings.append(f"{field} seems unusually high/low: {value}")
                elif field in ['total_revenue', 'net_income'] and value < 0 and field == 'total_revenue':
                    warnings.append(f"Negative revenue detected: {value}")
        
        return ValidationResult(True, errors, warnings)
    
    @staticmethod
    def _clean_json_response(text: str) -> str:
        """Clean common JSON formatting issues from API responses"""
        # Remove markdown code block markers
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'\s*```', '', text)
        text = re.sub(r'^```\s*', '', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Fix common JSON issues
        text = re.sub(r',\s*}', '}', text)  # Remove trailing commas
        text = re.sub(r',\s*]', ']', text)  # Remove trailing commas in arrays
        
        return text

def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    result = func(self, *args, **kwargs)
                    if attempt > 0:
                        self.metrics.retry_count += 1
                        logger.info(f"Retry succeeded on attempt {attempt + 1}")
                    return result
                    
                except Exception as e:
                    last_exception = e
                    self.metrics.failed_requests += 1
                    
                    error_type = type(e).__name__
                    self.metrics.error_types[error_type] = self.metrics.error_types.get(error_type, 0) + 1
                    
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed. Last error: {str(e)}")
            
            raise last_exception
        return wrapper
    return decorator

def track_performance(func):
    """Decorator to track API performance metrics"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        self.metrics.total_requests += 1
        
        try:
            result = func(self, *args, **kwargs)
            self.metrics.successful_requests += 1
            
            # Track response time
            response_time = time.time() - start_time
            self.metrics.response_times.append(response_time)
            
            # Update average
            if self.metrics.response_times:
                self.metrics.average_response_time = statistics.mean(self.metrics.response_times)
            
            return result
            
        except Exception as e:
            # Error is tracked in retry decorator
            raise e
    
    return wrapper

class RobustGeminiService:
    """High-reliability Gemini API service with comprehensive error handling"""
    
    def __init__(self, enable_circuit_breaker: bool = True):
        """Initialize the robust Gemini service"""
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Initialize components
        self.metrics = APIMetrics()
        self.input_validator = InputValidator()
        self.response_validator = ResponseValidator()
        
        # Circuit breaker (optional)
        self.circuit_breaker = CircuitBreaker() if enable_circuit_breaker else None
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
        logger.info("✅ Robust Gemini Service initialized with enhanced error handling")
    
    def _rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    @track_performance
    @retry_on_failure(max_retries=3, delay=1.0, backoff=2.0)
    def _make_api_call(self, prompt: str) -> str:
        """Make a rate-limited API call with circuit breaker protection"""
        self._rate_limit()
        
        if self.circuit_breaker:
            return self.circuit_breaker.call(self._raw_api_call, prompt)
        else:
            return self._raw_api_call(prompt)
    
    def _raw_api_call(self, prompt: str) -> str:
        """Make raw API call to Gemini"""
        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            return response.text
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """Test API connectivity with comprehensive validation"""
        try:
            response = self._make_api_call("Hello, this is a connectivity test.")
            
            if response and len(response) > 5:
                logger.info("✅ Gemini API connection test successful")
                return True
            else:
                logger.error("❌ Gemini API returned invalid response")
                return False
                
        except Exception as e:
            logger.error(f"❌ Gemini API connection test failed: {str(e)}")
            return False
    
    def extract_company_info(self, filing_text: str) -> Dict[str, str]:
        """Extract company information with comprehensive validation"""
        
        # Validate input
        validation = self.input_validator.validate_filing_text(filing_text)
        if not validation.is_valid:
            logger.error(f"Input validation failed: {validation.errors}")
            raise ValueError(f"Invalid input: {'; '.join(validation.errors)}")
        
        if validation.warnings:
            logger.warning(f"Input warnings: {'; '.join(validation.warnings)}")
        
        # Use sanitized input
        text_to_process = validation.sanitized_input or filing_text
        
        prompt = f"""
        Extract key company information from this SEC filing excerpt:
        
        {text_to_process[:2000]}...
        
        Please return a JSON object with the following fields:
        - company_name: The company's name
        - ticker: Stock ticker symbol
        - filing_type: Type of filing (10-Q, 10-K, etc.)
        - quarter_year: Quarter and year if applicable
        - industry: Company's industry/sector
        
        Return only valid JSON, no additional text.
        """
        
        try:
            response_text = self._make_api_call(prompt)
            
            # Validate JSON response
            json_validation = self.response_validator.validate_json_response(response_text)
            if not json_validation.is_valid:
                logger.error(f"JSON validation failed: {json_validation.errors}")
                return self._fallback_company_info(text_to_process)
            
            # Parse and validate company info
            cleaned_response = self.response_validator._clean_json_response(response_text)
            company_info = json.loads(cleaned_response)
            
            data_validation = self.response_validator.validate_company_info(company_info)
            if data_validation.warnings:
                logger.warning(f"Data warnings: {'; '.join(data_validation.warnings)}")
            
            if not data_validation.is_valid:
                logger.error(f"Data validation failed: {data_validation.errors}")
                return self._fallback_company_info(text_to_process)
            
            logger.info(f"Successfully extracted company info for {company_info.get('company_name', 'Unknown')}")
            return company_info
            
        except Exception as e:
            logger.error(f"Company extraction failed: {str(e)}")
            return self._fallback_company_info(text_to_process)
    
    def _fallback_company_info(self, text: str) -> Dict[str, str]:
        """Provide fallback company information extraction using regex"""
        logger.info("Using fallback extraction method for company info")
        
        fallback_info = {
            "company_name": "Unknown Company",
            "ticker": "N/A",
            "filing_type": "SEC Filing",
            "quarter_year": "N/A",
            "industry": "N/A"
        }
        
        try:
            # Simple regex patterns for basic extraction
            
            # Try to find company name
            company_patterns = [
                r'([A-Z][A-Z\s&\.]+(?:INC\.?|CORP\.?|LLC|CO\.?))',
                r'(\w+(?:\s+\w+)*)\s+(?:INC\.?|CORP\.?|LLC|CO\.?)'
            ]
            
            for pattern in company_patterns:
                match = re.search(pattern, text[:1000], re.IGNORECASE)
                if match:
                    fallback_info["company_name"] = match.group(1).strip()
                    break
            
            # Try to find ticker
            ticker_match = re.search(r'\b([A-Z]{1,5})\b', text[:500])
            if ticker_match:
                fallback_info["ticker"] = ticker_match.group(1)
            
            # Try to find filing type
            filing_match = re.search(r'FORM\s+(10-[QK])', text[:500])
            if filing_match:
                fallback_info["filing_type"] = filing_match.group(1)
            
            # Try to find quarter/year
            quarter_match = re.search(r'(Q[1-4]\s+20\d{2})', text[:1000])
            if quarter_match:
                fallback_info["quarter_year"] = quarter_match.group(1)
        
        except Exception as e:
            logger.warning(f"Fallback extraction also failed: {str(e)}")
        
        return fallback_info
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        return {
            'api_metrics': asdict(self.metrics),
            'circuit_breaker_state': self.circuit_breaker.state if self.circuit_breaker else None,
            'recent_performance': {
                'success_rate': self.metrics.success_rate,
                'error_rate': self.metrics.error_rate,
                'average_response_time': self.metrics.average_response_time,
                'total_requests': self.metrics.total_requests
            },
            'error_breakdown': self.metrics.error_types,
            'timestamp': datetime.now().isoformat()
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.metrics = APIMetrics()
        logger.info("Performance metrics reset")
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health_status = {
            'service_status': 'unknown',
            'api_connectivity': False,
            'circuit_breaker_state': self.circuit_breaker.state if self.circuit_breaker else 'disabled',
            'performance_metrics': self.get_performance_metrics(),
            'recommendations': []
        }
        
        try:
            # Test API connectivity
            health_status['api_connectivity'] = self.test_connection()
            
            # Determine overall service status
            if health_status['api_connectivity']:
                if self.metrics.success_rate >= 95:
                    health_status['service_status'] = 'healthy'
                elif self.metrics.success_rate >= 80:
                    health_status['service_status'] = 'degraded'
                else:
                    health_status['service_status'] = 'unhealthy'
            else:
                health_status['service_status'] = 'down'
            
            # Generate recommendations
            recommendations = []
            if self.metrics.error_rate > 10:
                recommendations.append("High error rate detected - check API key and network connectivity")
            if self.metrics.average_response_time > 5.0:
                recommendations.append("Slow response times - consider optimizing prompts or checking network")
            if self.circuit_breaker and self.circuit_breaker.state == 'OPEN':
                recommendations.append("Circuit breaker is open - service is temporarily unavailable")
            
            health_status['recommendations'] = recommendations
            
        except Exception as e:
            health_status['service_status'] = 'error'
            health_status['error'] = str(e)
        
        return health_status

def main():
    """Test the robust Gemini service"""
    try:
        service = RobustGeminiService()
        
        # Test health check
        health = service.health_check()
        print("🏥 Health Check Results:")
        print(json.dumps(health, indent=2))
        
        # Test with sample data
        sample_text = """
        JPMORGAN CHASE & CO.
        FORM 10-Q
        For the quarterly period ended March 31, 2025
        Total net revenue: $42.5 billion
        Net income: $13.4 billion
        """
        
        result = service.extract_company_info(sample_text)
        print("\n📊 Extraction Results:")
        print(json.dumps(result, indent=2))
        
        # Print metrics
        metrics = service.get_performance_metrics()
        print("\n📈 Performance Metrics:")
        print(json.dumps(metrics, indent=2))
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()