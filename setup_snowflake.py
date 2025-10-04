#!/usr/bin/env python3
"""
Snowflake Setup Script for HackRU 2025
Automatically creates warehouse, database, and tables
"""

import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def setup_snowflake():
    """Set up complete Snowflake environment for 10Q Notes AI"""
    
    print("🏗️ Setting up Snowflake Data Warehouse for HackRU 2025")
    print("=" * 60)
    
    # Connection parameters
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    user = os.getenv('SNOWFLAKE_USER')
    password = os.getenv('SNOWFLAKE_PASSWORD')
    
    print(f"🔗 Connecting to account: {account}")
    print(f"👤 User: {user}")
    
    try:
        # Connect to Snowflake (without specifying warehouse initially)
        connection = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            role='ACCOUNTADMIN'
        )
        
        cursor = connection.cursor()
        print("✅ Connected to Snowflake successfully!")
        
        # 1. Create Warehouse
        print("\n🏭 Creating compute warehouse...")
        cursor.execute("""
            CREATE WAREHOUSE IF NOT EXISTS HACKRU_COMPUTE_WH 
            WITH WAREHOUSE_SIZE = 'XSMALL' 
            AUTO_SUSPEND = 60 
            AUTO_RESUME = TRUE
            COMMENT = 'HackRU 2025 - 10Q Notes AI Compute Warehouse'
        """)
        print("✅ Warehouse HACKRU_COMPUTE_WH created!")
        
        # Use the warehouse
        cursor.execute("USE WAREHOUSE HACKRU_COMPUTE_WH")
        
        # 2. Create Database
        print("\n💾 Creating database...")
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS HACKRU_10Q_NOTES
            COMMENT = 'HackRU 2025 - 10Q Notes AI Financial Data'
        """)
        print("✅ Database HACKRU_10Q_NOTES created!")
        
        # Use the database
        cursor.execute("USE DATABASE HACKRU_10Q_NOTES")
        
        # 3. Create Schema
        print("\n📋 Creating schema...")
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS FINANCIAL_DATA
            COMMENT = 'Schema for SEC filing analysis and SMAP data'
        """)
        print("✅ Schema FINANCIAL_DATA created!")
        
        # Use the schema
        cursor.execute("USE SCHEMA FINANCIAL_DATA")
        
        # 4. Create Tables
        print("\n🗄️ Creating tables...")
        
        # Companies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id STRING PRIMARY KEY,
                company_name STRING,
                ticker_symbol STRING,
                industry STRING,
                market_cap_category STRING,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ Companies table created")
        
        # Filings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS filings (
                filing_id STRING PRIMARY KEY,
                company_id STRING,
                filing_type STRING,
                filing_period STRING,
                filing_date DATE,
                quarter STRING,
                year INTEGER,
                raw_text TEXT,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ Filings table created")
        
        # Financial metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_metrics (
                metric_id STRING PRIMARY KEY,
                filing_id STRING,
                total_revenue FLOAT,
                revenue_yoy_growth FLOAT,
                net_income FLOAT,
                net_income_yoy_growth FLOAT,
                net_interest_income FLOAT,
                noninterest_revenue FLOAT,
                net_interest_margin FLOAT,
                efficiency_ratio FLOAT,
                return_on_equity FLOAT,
                common_equity_tier1_ratio FLOAT,
                provision_credit_losses FLOAT,
                book_value_per_share FLOAT,
                debt_to_equity FLOAT,
                current_ratio FLOAT,
                gross_margin FLOAT,
                operating_margin FLOAT,
                earnings_per_share FLOAT,
                diluted_eps FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ Financial metrics table created")
        
        # SMAP notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS smap_notes (
                note_id STRING PRIMARY KEY,
                filing_id STRING,
                subjective TEXT,
                metrics TEXT,
                assessment TEXT,
                plan TEXT,
                generated_by STRING,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ SMAP notes table created")
        
        # Risk factors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_factors (
                risk_id STRING PRIMARY KEY,
                filing_id STRING,
                risk_category STRING,
                risk_description TEXT,
                severity_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ Risk factors table created")
        
        # Business segments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_segments (
                segment_id STRING PRIMARY KEY,
                filing_id STRING,
                segment_name STRING,
                segment_revenue FLOAT,
                segment_net_income FLOAT,
                segment_assets FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ Business segments table created")
        
        # Industry benchmarks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS industry_benchmarks (
                benchmark_id STRING PRIMARY KEY,
                industry STRING,
                metric_name STRING,
                benchmark_value FLOAT,
                percentile_25 FLOAT,
                percentile_50 FLOAT,
                percentile_75 FLOAT,
                period STRING,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        print("   ✅ Industry benchmarks table created")
        
        # 5. Insert sample data for demo
        print("\n📊 Inserting sample data for HackRU demo...")
        
        # Sample company
        cursor.execute("""
            INSERT INTO companies (company_id, company_name, ticker_symbol, industry, market_cap_category)
            VALUES ('JPM_JPMORGAN_CHASE', 'JPMorgan Chase & Co.', 'JPM', 'Banking', 'Large Cap')
        """)
        
        # Sample filing
        cursor.execute("""
            INSERT INTO filings (filing_id, company_id, filing_type, filing_period, filing_date, quarter, year, raw_text)
            VALUES ('JPM_Q1_2025_20250104', 'JPM_JPMORGAN_CHASE', '10-Q', 'Q1 2025', '2025-04-30', 'Q1', 2025, 'Sample 10-Q filing text...')
        """)
        
        # Sample financial metrics
        cursor.execute("""
            INSERT INTO financial_metrics (metric_id, filing_id, total_revenue, net_income, return_on_equity, efficiency_ratio, net_interest_margin, common_equity_tier1_ratio)
            VALUES ('JPM_Q1_2025_METRICS', 'JPM_Q1_2025_20250104', 42500, 13400, 17.8, 56.0, 2.74, 15.9)
        """)
        
        # Sample industry benchmarks
        cursor.execute("""
            INSERT INTO industry_benchmarks (benchmark_id, industry, metric_name, benchmark_value, percentile_25, percentile_50, percentile_75, period)
            VALUES 
            ('BANKING_ROE_2025', 'Banking', 'return_on_equity', 14.5, 11.2, 14.5, 18.1, 'Q1 2025'),
            ('BANKING_EFFICIENCY_2025', 'Banking', 'efficiency_ratio', 60.0, 55.0, 60.0, 68.0, 'Q1 2025')
        """)
        
        print("   ✅ Sample data inserted for demo")
        
        # 6. Test a query
        print("\n🧪 Testing data warehouse with sample query...")
        cursor.execute("""
            SELECT c.company_name, c.ticker_symbol, fm.total_revenue, fm.return_on_equity
            FROM companies c
            JOIN filings f ON c.company_id = f.company_id
            JOIN financial_metrics fm ON f.filing_id = fm.filing_id
            WHERE c.ticker_symbol = 'JPM'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"   📊 Query result: {result[0]} ({result[1]}) - Revenue: ${result[2]}M, ROE: {result[3]}%")
        
        # Close connection
        cursor.close()
        connection.close()
        
        print(f"\n🎉 SNOWFLAKE SETUP COMPLETE!")
        print(f"🏆 Ready for HackRU 2025 - Best Use of Snowflake API!")
        print(f"📊 Your enterprise data warehouse is live and ready!")
        print(f"🔗 Access via: https://app.snowflake.com")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print(f"🔧 Check your credentials and try again")
        return False

if __name__ == "__main__":
    setup_snowflake()