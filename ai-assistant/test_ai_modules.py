#!/usr/bin/env python3
"""
Test script for AI Assistant modules
"""

import os
import sys
from router import LLMRouter

def test_ai_modules():
    """Test all AI assistant modules"""
    
    # Set offline mode for testing
    os.environ['LLM_OFFLINE'] = 'True'
    
    try:
        # Initialize router
        router = LLMRouter()
        print("✅ AI Router initialized successfully")
        
        # Test each module
        modules = {
            'dax_genie': 'Generate DAX measure for total sales',
            'source_mapper': 'Map SQL Server database to medallion architecture', 
            'qa_buddy': 'Analyze pipeline performance logs',
            'release_scribe': 'Generate release notes for v2.1.0'
        }
        
        print("\n🧪 Testing AI Modules:")
        print("=" * 50)
        
        for module, test_prompt in modules.items():
            try:
                response = router.route_request(test_prompt, 'openai', module)
                print(f"✅ {module.upper()}: {response[:60]}...")
            except Exception as e:
                print(f"❌ {module.upper()}: Error - {e}")
        
        print("\n✅ All AI modules tested successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI modules: {e}")
        return False

def test_database():
    """Test database functionality"""
    try:
        router = LLMRouter()
        
        # Test database connection
        import sqlite3
        conn = sqlite3.connect(router.db_path)
        
        # Check if table exists
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        print(f"✅ Database tables: {[table[0] for table in tables]}")
        
        # Test inserting a record
        router._log_usage(
            provider='test',
            model='test-model',
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cost_usd=0.001,
            feature='test'
        )
        
        # Test reading records
        records = conn.execute("SELECT COUNT(*) FROM llm_usage").fetchone()
        print(f"✅ Database records: {records[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🤖 Fabric Fast-Track AI Assistant - Test Suite")
    print("=" * 60)
    
    # Test database
    print("\n📊 Testing Database Functionality:")
    db_test = test_database()
    
    # Test AI modules
    ai_test = test_ai_modules()
    
    # Summary
    print("\n📋 Test Summary:")
    print("=" * 30)
    print(f"Database Test: {'✅ PASS' if db_test else '❌ FAIL'}")
    print(f"AI Modules Test: {'✅ PASS' if ai_test else '❌ FAIL'}")
    
    if db_test and ai_test:
        print("\n🎉 All tests passed! AI Assistant is ready for use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())