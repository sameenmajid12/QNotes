#!/usr/bin/env python3
"""
Quick test to verify Snowflake connection works
Run this after setting up your Snowflake account
"""

import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

def test_snowflake_connection():
    """Test basic Snowflake connection"""
    
    print("🧪 Testing Snowflake Connection...")
    print("=" * 50)
    
    # Get credentials from .env
    account = os.getenv('SNOWFLAKE_ACCOUNT')
    user = os.getenv('SNOWFLAKE_USER')
    password = os.getenv('SNOWFLAKE_PASSWORD')
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
    database = os.getenv('SNOWFLAKE_DATABASE')
    schema = os.getenv('SNOWFLAKE_SCHEMA')
    
    print(f"🔗 Account: {account}")
    print(f"👤 User: {user}")
    print(f"🏢 Warehouse: {warehouse}")
    print(f"💾 Database: {database}")
    print(f"📋 Schema: {schema}")
    
    try:
        # Attempt connection
        connection = snowflake.connector.connect(
            account=account,
            user=user,
            password=password,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        
        print("\n✅ CONNECTION SUCCESSFUL!")
        
        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        
        print(f"📊 Snowflake Version: {version}")
        print(f"🎉 Ready for HackRU demo with REAL Snowflake!")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ CONNECTION FAILED: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your account ID format (should be: ABC123.us-east-1)")
        print("   2. Verify username and password")
        print("   3. Make sure warehouse exists in Snowflake")
        print("   4. Check if you have the right permissions")
        
        return False

if __name__ == "__main__":
    test_snowflake_connection()