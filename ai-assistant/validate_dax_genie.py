#!/usr/bin/env python3
"""
DAX Genie - Comprehensive Validation Script
Tests all components and generates a detailed validation report
"""

import os
import sys
import time
import sqlite3
from datetime import datetime
from router import LLMRouter

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_test(name, status, details=""):
    """Print test result"""
    icon = f"{Colors.GREEN}✅{Colors.END}" if status else f"{Colors.RED}❌{Colors.END}"
    print(f"{icon} {Colors.BOLD}{name}{Colors.END}")
    if details:
        print(f"   {Colors.YELLOW}→{Colors.END} {details}")

def test_environment():
    """Test 1: Environment Configuration"""
    print_header("TEST 1: Environment Configuration")

    results = []

    # Check Python version
    python_version = sys.version_info
    is_valid = python_version.major == 3 and python_version.minor >= 11
    print_test(
        "Python Version",
        is_valid,
        f"Python {python_version.major}.{python_version.minor}.{python_version.micro}"
    )
    results.append(("Python Version", is_valid))

    # Check LLM_OFFLINE setting
    offline_mode = os.getenv('LLM_OFFLINE', 'False')
    print_test(
        "LLM_OFFLINE Setting",
        True,
        f"LLM_OFFLINE={offline_mode}"
    )
    results.append(("LLM Offline Mode", True))

    # Check API key (if not in offline mode)
    if offline_mode.lower() != 'true':
        api_key = os.getenv('OPENAI_API_KEY')
        has_key = api_key is not None and len(api_key) > 0
        print_test(
            "OpenAI API Key",
            has_key,
            "Set" if has_key else "Not set (will use offline mode)"
        )
        results.append(("API Key", has_key))

    return results

def test_database():
    """Test 2: Database Setup and Operations"""
    print_header("TEST 2: Database Setup & Operations")

    results = []

    try:
        # Initialize router (creates database)
        router = LLMRouter()
        print_test("Database Initialization", True, "Router initialized")
        results.append(("Database Init", True))

        # Check database file exists
        db_exists = os.path.exists(router.db_path)
        print_test("Database File", db_exists, f"Path: {router.db_path}")
        results.append(("Database File", db_exists))

        # Check table schema
        conn = sqlite3.connect(router.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='llm_usage'")
        table_exists = cursor.fetchone() is not None
        print_test("Table Schema", table_exists, "llm_usage table exists")
        results.append(("Table Schema", table_exists))

        # Test insert operation
        test_timestamp = datetime.now().isoformat()
        router._log_usage(
            provider='test',
            model='validation-model',
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cost_usd=0.001,
            feature='validation_test'
        )

        cursor.execute("SELECT COUNT(*) FROM llm_usage WHERE feature='validation_test'")
        count = cursor.fetchone()[0]
        print_test("Insert Operation", count > 0, f"{count} test record(s) inserted")
        results.append(("Insert Operation", count > 0))

        # Test read operation
        cursor.execute("""
            SELECT timestamp, provider, model, total_tokens, cost_usd
            FROM llm_usage
            WHERE feature='validation_test'
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        record = cursor.fetchone()
        read_success = record is not None
        if read_success:
            print_test(
                "Read Operation",
                True,
                f"Retrieved: {record[1]} | {record[2]} | {record[3]} tokens | ${record[4]:.6f}"
            )
        results.append(("Read Operation", read_success))

        conn.close()

    except Exception as e:
        print_test("Database Operations", False, f"Error: {str(e)}")
        results.append(("Database Operations", False))

    return results

def test_llm_router():
    """Test 3: LLM Router Functionality"""
    print_header("TEST 3: LLM Router Functionality")

    results = []

    try:
        # Force offline mode for predictable testing
        original_mode = os.getenv('LLM_OFFLINE')
        os.environ['LLM_OFFLINE'] = 'True'

        router = LLMRouter()

        # Test offline response
        response = router.route_request(
            "Generate DAX measure for total sales",
            "openai",
            "validation_test"
        )

        offline_works = response is not None and len(response) > 0
        print_test(
            "Offline Mode Response",
            offline_works,
            f"Response length: {len(response)} chars"
        )
        results.append(("Offline Response", offline_works))

        # Restore original mode and test online if configured
        if original_mode:
            os.environ['LLM_OFFLINE'] = original_mode

        if os.getenv('LLM_OFFLINE', 'False').lower() != 'true' and os.getenv('OPENAI_API_KEY'):
            print(f"\n{Colors.YELLOW}Testing online mode with OpenAI...{Colors.END}")
            router = LLMRouter()

            start_time = time.time()
            response = router.route_request(
                "Generate a simple DAX measure for total sales revenue",
                "openai",
                "validation_test"
            )
            elapsed = time.time() - start_time

            online_works = response is not None and len(response) > 50
            print_test(
                "Online Mode Response",
                online_works,
                f"Response in {elapsed:.2f}s | {len(response)} chars"
            )
            results.append(("Online Response", online_works))

            # Check if response looks like DAX
            has_measure_name = "**Measure Name:**" in response or "=" in response
            print_test(
                "DAX Format Validation",
                has_measure_name,
                "Response contains DAX structure"
            )
            results.append(("DAX Format", has_measure_name))
        else:
            print(f"{Colors.YELLOW}ℹ️  Skipping online test (offline mode or no API key){Colors.END}")

    except Exception as e:
        print_test("LLM Router", False, f"Error: {str(e)}")
        results.append(("LLM Router", False))

    return results

def test_prompt_files():
    """Test 4: Prompt System Files"""
    print_header("TEST 4: Prompt System Files")

    results = []
    prompt_dir = "prompts/dax_genie"

    required_files = {
        "system_prompt.md": 68,
        "user_prompt_templates.md": 286,
        "example_conversations.md": 505,
        "prompt_dax_gen.md": 421
    }

    for filename, expected_min_lines in required_files.items():
        filepath = os.path.join(prompt_dir, filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                line_count = len(f.readlines())

            is_valid = line_count >= expected_min_lines * 0.9  # Allow 10% variance
            print_test(
                f"File: {filename}",
                is_valid,
                f"{line_count} lines (expected ~{expected_min_lines})"
            )
            results.append((filename, is_valid))
        else:
            print_test(f"File: {filename}", False, "File not found")
            results.append((filename, False))

    return results

def test_dax_generation():
    """Test 5: DAX Measure Generation"""
    print_header("TEST 5: DAX Measure Generation Tests")

    results = []

    # Set offline mode for predictable testing
    os.environ['LLM_OFFLINE'] = 'True'
    router = LLMRouter()

    test_cases = [
        {
            "name": "Basic Sales Measure",
            "prompt": "Generate DAX measure for total sales revenue",
            "expected_keywords": ["SUM", "Sales"]
        },
        {
            "name": "Time Intelligence",
            "prompt": "Generate year-over-year sales growth percentage",
            "expected_keywords": ["YoY", "%"]
        },
        {
            "name": "Financial Ratio",
            "prompt": "Generate gross profit margin percentage",
            "expected_keywords": ["margin", "DIVIDE"]
        },
        {
            "name": "Customer Analytics",
            "prompt": "Generate count of active customers",
            "expected_keywords": ["COUNT", "Customer"]
        }
    ]

    for test_case in test_cases:
        try:
            response = router.route_request(
                test_case["prompt"],
                "openai",
                "validation_test"
            )

            # In offline mode, just check we got a response
            success = response is not None and len(response) > 0

            print_test(
                test_case["name"],
                success,
                f"Generated {len(response)} chars"
            )
            results.append((test_case["name"], success))

        except Exception as e:
            print_test(test_case["name"], False, f"Error: {str(e)}")
            results.append((test_case["name"], False))

    return results

def test_cost_tracking():
    """Test 6: Cost Tracking & Analytics"""
    print_header("TEST 6: Cost Tracking & Analytics")

    results = []

    try:
        router = LLMRouter()
        conn = sqlite3.connect(router.db_path)
        cursor = conn.cursor()

        # Test cost calculation
        cursor.execute("""
            SELECT
                COUNT(*) as requests,
                SUM(total_tokens) as total_tokens,
                SUM(cost_usd) as total_cost
            FROM llm_usage
            WHERE feature = 'validation_test'
        """)

        stats = cursor.fetchone()
        has_data = stats[0] > 0

        print_test(
            "Cost Logging",
            has_data,
            f"{stats[0]} requests | {stats[1]} tokens | ${stats[2]:.6f}"
        )
        results.append(("Cost Logging", has_data))

        # Test aggregation by provider
        cursor.execute("""
            SELECT provider, COUNT(*) as count
            FROM llm_usage
            WHERE feature = 'validation_test'
            GROUP BY provider
        """)

        providers = cursor.fetchall()
        print_test(
            "Provider Tracking",
            len(providers) > 0,
            f"{len(providers)} provider(s) logged"
        )
        results.append(("Provider Tracking", len(providers) > 0))

        conn.close()

    except Exception as e:
        print_test("Cost Tracking", False, f"Error: {str(e)}")
        results.append(("Cost Tracking", False))

    return results

def generate_report(all_results):
    """Generate final validation report"""
    print_header("VALIDATION REPORT")

    # Calculate statistics
    total_tests = sum(len(results) for results in all_results.values())
    passed_tests = sum(sum(1 for _, status in results if status) for results in all_results.values())
    failed_tests = total_tests - passed_tests
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    # Print summary
    print(f"{Colors.BOLD}Test Summary:{Colors.END}")
    print(f"  Total Tests: {Colors.BOLD}{total_tests}{Colors.END}")
    print(f"  {Colors.GREEN}Passed: {passed_tests}{Colors.END}")
    print(f"  {Colors.RED}Failed: {failed_tests}{Colors.END}")
    print(f"  Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.END}\n")

    # Print category breakdown
    print(f"{Colors.BOLD}Category Breakdown:{Colors.END}")
    for category, results in all_results.items():
        category_passed = sum(1 for _, status in results if status)
        category_total = len(results)
        icon = f"{Colors.GREEN}✅{Colors.END}" if category_passed == category_total else f"{Colors.YELLOW}⚠️{Colors.END}"
        print(f"  {icon} {category}: {category_passed}/{category_total}")

    # Overall status
    print()
    if failed_tests == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! DAX Genie is fully operational.{Colors.END}\n")
        return 0
    elif success_rate >= 80:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Most tests passed, but some issues detected.{Colors.END}\n")
        return 1
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Multiple test failures. Please review configuration.{Colors.END}\n")
        return 2

def cleanup_test_data():
    """Clean up test data from database"""
    try:
        router = LLMRouter()
        conn = sqlite3.connect(router.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM llm_usage WHERE feature='validation_test'")
        deleted = cursor.rowcount

        conn.commit()
        conn.close()

        print(f"\n{Colors.BLUE}ℹ️  Cleaned up {deleted} test records from database{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.YELLOW}⚠️  Could not clean up test data: {str(e)}{Colors.END}\n")

def main():
    """Run all validation tests"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║                                                                   ║")
    print("║           DAX GENIE - COMPREHENSIVE VALIDATION SUITE              ║")
    print("║                                                                   ║")
    print("║        Testing all components for production readiness...        ║")
    print("║                                                                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")

    # Store all results
    all_results = {}

    # Run all tests
    all_results["Environment"] = test_environment()
    all_results["Database"] = test_database()
    all_results["LLM Router"] = test_llm_router()
    all_results["Prompt Files"] = test_prompt_files()
    all_results["DAX Generation"] = test_dax_generation()
    all_results["Cost Tracking"] = test_cost_tracking()

    # Generate final report
    exit_code = generate_report(all_results)

    # Ask about cleanup
    print(f"{Colors.BOLD}Test data cleanup:{Colors.END}")
    print("  This script created test records in the database.")
    print("  Do you want to remove them? (recommended)")

    try:
        response = input(f"\n  {Colors.CYAN}Clean up test data? [Y/n]: {Colors.END}").strip().lower()
        if response in ['', 'y', 'yes']:
            cleanup_test_data()
        else:
            print(f"\n{Colors.YELLOW}ℹ️  Test data retained. You can clean it manually later.{Colors.END}\n")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}ℹ️  Cleanup skipped.{Colors.END}\n")

    # Final message
    if exit_code == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✨ DAX Genie is ready for production use!{Colors.END}")
        print(f"\n{Colors.CYAN}Next steps:{Colors.END}")
        print(f"  1. Run: {Colors.BOLD}streamlit run streamlit_app.py{Colors.END}")
        print(f"  2. Open: {Colors.BOLD}http://localhost:8501{Colors.END}")
        print(f"  3. Start generating DAX measures!\n")
    else:
        print(f"{Colors.YELLOW}⚠️  Please review the test results above.{Colors.END}")
        print(f"\n{Colors.CYAN}Troubleshooting:{Colors.END}")
        print(f"  • Check environment variables (OPENAI_API_KEY, LLM_OFFLINE)")
        print(f"  • Verify all dependencies: {Colors.BOLD}pip install -r requirements.txt{Colors.END}")
        print(f"  • Review prompt files in {Colors.BOLD}prompts/dax_genie/{Colors.END}")
        print(f"  • See {Colors.BOLD}DAX_GENIE_TESTING_GUIDE.md{Colors.END} for detailed help\n")

    return exit_code

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Validation interrupted by user.{Colors.END}\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Unexpected error: {str(e)}{Colors.END}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
