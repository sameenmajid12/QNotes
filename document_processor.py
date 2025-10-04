"""
10Q Notes AI - Document Processing Module
HackRU 2025 Project by azrabano

This module handles document parsing and preprocessing:
- PDF upload and text extraction
- Text cleaning and preparation
- SEC filing format recognition
"""

import os
import re
from typing import Dict, Optional
import PyPDF2
import requests
from io import BytesIO

class DocumentProcessor:
    """Handles document processing and text extraction"""
    
    def __init__(self):
        """Initialize document processor"""
        print("📄 Document processor initialized")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text.strip()
                
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_url(self, url: str) -> str:
        """Extract text from a URL (for EDGAR filings)"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # For HTML content, we'd need more sophisticated parsing
            # For now, return raw text (this would need enhancement for production)
            return response.text
            
        except Exception as e:
            print(f"Error extracting text from URL: {e}")
            return ""
    
    def clean_sec_filing_text(self, raw_text: str) -> str:
        """Clean and prepare SEC filing text for analysis"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', raw_text)
        
        # Remove common SEC filing noise
        text = re.sub(r'Table of Contents.*?(?=PART|ITEM|\n\n)', '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'UNITED STATES\s+SECURITIES AND EXCHANGE COMMISSION.*?(?=PART|ITEM|\n\n)', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        # Keep only relevant sections (this is a basic implementation)
        # In production, you'd want more sophisticated section extraction
        
        return text.strip()
    
    def identify_filing_type(self, text: str) -> Dict[str, str]:
        """Identify the type of SEC filing"""
        text_upper = text.upper()
        
        filing_info = {
            "type": "Unknown",
            "form": "Unknown",
            "confidence": "Low"
        }
        
        if "FORM 10-Q" in text_upper or "10-Q" in text_upper:
            filing_info["type"] = "Quarterly Report"
            filing_info["form"] = "10-Q"
            filing_info["confidence"] = "High"
        elif "FORM 10-K" in text_upper or "10-K" in text_upper:
            filing_info["type"] = "Annual Report"
            filing_info["form"] = "10-K"
            filing_info["confidence"] = "High"
        elif "FORM 8-K" in text_upper or "8-K" in text_upper:
            filing_info["type"] = "Current Report"
            filing_info["form"] = "8-K"
            filing_info["confidence"] = "High"
        
        return filing_info
    
    def extract_financial_tables(self, text: str) -> Dict[str, str]:
        """Extract key financial statement sections"""
        sections = {}
        
        # Look for income statement
        income_match = re.search(r'(CONSOLIDATED STATEMENTS OF OPERATIONS|STATEMENTS OF INCOME|INCOME STATEMENT).*?(?=CONSOLIDATED BALANCE|BALANCE SHEET|STATEMENT OF CASH|$)', text, re.IGNORECASE | re.DOTALL)
        if income_match:
            sections["income_statement"] = income_match.group(0)
        
        # Look for balance sheet
        balance_match = re.search(r'(CONSOLIDATED BALANCE SHEETS|BALANCE SHEET).*?(?=STATEMENT OF CASH|CONSOLIDATED STATEMENTS OF CASH|$)', text, re.IGNORECASE | re.DOTALL)
        if balance_match:
            sections["balance_sheet"] = balance_match.group(0)
        
        # Look for management discussion
        md_match = re.search(r'(MANAGEMENT.?S DISCUSSION AND ANALYSIS|MD&A).*?(?=ITEM \d+|PART |$)', text, re.IGNORECASE | re.DOTALL)
        if md_match:
            sections["management_discussion"] = md_match.group(0)
        
        return sections
    
    def prepare_for_analysis(self, raw_text: str) -> Dict[str, str]:
        """Prepare document for SMAP analysis"""
        # Clean the text
        cleaned_text = self.clean_sec_filing_text(raw_text)
        
        # Identify filing type
        filing_info = self.identify_filing_type(cleaned_text)
        
        # Extract key sections
        sections = self.extract_financial_tables(cleaned_text)
        
        # Prepare final text for analysis (limit length for API)
        # Take first 15000 characters to stay within API limits
        analysis_text = cleaned_text[:15000]
        
        return {
            "analysis_text": analysis_text,
            "filing_type": filing_info["form"],
            "filing_description": filing_info["type"],
            "confidence": filing_info["confidence"],
            "sections_found": list(sections.keys()),
            "full_text_length": len(cleaned_text)
        }

# Test function
def test_document_processor():
    """Test the document processor functionality"""
    print("🧪 Testing Document Processor")
    
    processor = DocumentProcessor()
    
    # Test with sample text
    sample_text = """
    APPLE INC.
    FORM 10-Q
    CONSOLIDATED STATEMENTS OF OPERATIONS
    (Unaudited)
    
    Revenue: $100,000
    Cost of sales: $60,000
    Gross profit: $40,000
    
    MANAGEMENT'S DISCUSSION AND ANALYSIS
    Our performance this quarter was strong...
    """
    
    result = processor.prepare_for_analysis(sample_text)
    
    print(f"Filing Type: {result['filing_type']}")
    print(f"Description: {result['filing_description']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Sections Found: {result['sections_found']}")
    print(f"Text Length: {result['full_text_length']}")
    
    print("✅ Document processor test complete!")

if __name__ == "__main__":
    test_document_processor()