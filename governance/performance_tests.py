#!/usr/bin/env python3
"""
Fabric Fast-Track Performance Testing Script
Validates report load times and query performance against <2 second target
"""

import os
import sys
import json
import argparse
import logging
import time
from typing import Dict, List
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PerformanceTester:
    """Test Power BI report and query performance"""

    def __init__(self, workspace_name: str, target_load_time: int = 2000):
        self.workspace_name = workspace_name
        self.target_load_time_ms = target_load_time  # milliseconds
        self.tenant_id = os.getenv('FABRIC_TENANT_ID')
        self.client_id = os.getenv('FABRIC_CLIENT_ID')
        self.client_secret = os.getenv('FABRIC_CLIENT_SECRET')
        self.powerbi_api = "https://api.powerbi.com/v1.0/myorg"
        self.access_token = None
        self.test_results = []

        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("Missing required environment variables")

    def authenticate(self) -> str:
        """Authenticate with Power BI API"""
        logger.info("Authenticating...")

        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default',
            'grant_type': 'client_credentials'
        }

        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            logger.info("✅ Authentication successful")
            return self.access_token
        except Exception as e:
            logger.error(f"❌ Authentication failed: {e}")
            raise

    def get_workspace_id(self) -> str:
        """Get workspace ID by name"""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.get(f"{self.powerbi_api}/groups", headers=headers)
        response.raise_for_status()

        workspaces = response.json().get('value', [])
        for ws in workspaces:
            if ws['name'] == self.workspace_name:
                return ws['id']

        raise ValueError(f"Workspace '{self.workspace_name}' not found")

    def get_reports(self, workspace_id: str) -> List[Dict]:
        """Get all reports in workspace"""
        logger.info(f"Retrieving reports from workspace...")

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.get(
            f"{self.powerbi_api}/groups/{workspace_id}/reports",
            headers=headers
        )
        response.raise_for_status()

        reports = response.json().get('value', [])
        logger.info(f"Found {len(reports)} report(s)")
        return reports

    def get_datasets(self, workspace_id: str) -> List[Dict]:
        """Get all datasets in workspace"""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.get(
            f"{self.powerbi_api}/groups/{workspace_id}/datasets",
            headers=headers
        )
        response.raise_for_status()

        datasets = response.json().get('value', [])
        logger.info(f"Found {len(datasets)} dataset(s)")
        return datasets

    def test_dax_query_performance(self, workspace_id: str, dataset_id: str, dax_query: str, test_name: str) -> Dict:
        """Execute DAX query and measure performance"""
        logger.info(f"Testing query: {test_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'queries': [{
                'query': dax_query
            }],
            'serializerSettings': {
                'includeNulls': True
            }
        }

        start_time = time.time()

        try:
            response = requests.post(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}/executeQueries",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            end_time = time.time()
            execution_time_ms = int((end_time - start_time) * 1000)

            result = response.json()
            row_count = len(result.get('results', [{}])[0].get('tables', [{}])[0].get('rows', []))

            passed = execution_time_ms < self.target_load_time_ms

            test_result = {
                'test_name': test_name,
                'type': 'dax_query',
                'execution_time_ms': execution_time_ms,
                'target_time_ms': self.target_load_time_ms,
                'row_count': row_count,
                'passed': passed,
                'timestamp': datetime.now().isoformat()
            }

            if passed:
                logger.info(f"✅ {test_name}: {execution_time_ms}ms (target: {self.target_load_time_ms}ms)")
            else:
                logger.warning(f"❌ {test_name}: {execution_time_ms}ms exceeds target of {self.target_load_time_ms}ms")

            return test_result

        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            return {
                'test_name': test_name,
                'type': 'dax_query',
                'execution_time_ms': -1,
                'target_time_ms': self.target_load_time_ms,
                'passed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def test_report_page_load(self, workspace_id: str, report_id: str, report_name: str) -> Dict:
        """Test report page load time (via API - limited capability)"""
        logger.info(f"Testing report: {report_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        start_time = time.time()

        try:
            # Get report pages
            response = requests.get(
                f"{self.powerbi_api}/groups/{workspace_id}/reports/{report_id}/pages",
                headers=headers
            )
            response.raise_for_status()

            end_time = time.time()
            load_time_ms = int((end_time - start_time) * 1000)

            pages = response.json().get('value', [])
            page_count = len(pages)

            passed = load_time_ms < self.target_load_time_ms

            test_result = {
                'test_name': f"Report: {report_name}",
                'type': 'report_load',
                'execution_time_ms': load_time_ms,
                'target_time_ms': self.target_load_time_ms,
                'page_count': page_count,
                'passed': passed,
                'timestamp': datetime.now().isoformat()
            }

            if passed:
                logger.info(f"✅ {report_name}: {load_time_ms}ms ({page_count} pages)")
            else:
                logger.warning(f"⚠️  {report_name}: {load_time_ms}ms (API metadata only)")

            return test_result

        except Exception as e:
            logger.error(f"❌ Report test failed: {e}")
            return {
                'test_name': f"Report: {report_name}",
                'type': 'report_load',
                'execution_time_ms': -1,
                'passed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def run_standard_performance_tests(self, workspace_id: str, dataset_id: str) -> List[Dict]:
        """Run standard set of performance tests"""
        logger.info("\n" + "=" * 60)
        logger.info("RUNNING STANDARD PERFORMANCE TESTS")
        logger.info("=" * 60)

        # Standard DAX queries to test
        test_queries = [
            {
                'name': 'Simple Aggregation',
                'query': 'EVALUATE ROW("TotalSales", SUM(FactSales[TotalAmount]))'
            },
            {
                'name': 'Time Intelligence - YTD',
                'query': 'EVALUATE SUMMARIZECOLUMNS(DimDate[Year], "YTD Sales", TOTALYTD(SUM(FactSales[TotalAmount]), DimDate[Date]))'
            },
            {
                'name': 'Count Distinct Customers',
                'query': 'EVALUATE ROW("ActiveCustomers", DISTINCTCOUNT(FactSales[CustomerID]))'
            },
            {
                'name': 'Top 10 Products',
                'query': 'EVALUATE TOPN(10, SUMMARIZE(FactSales, FactSales[ProductID], "Sales", SUM(FactSales[TotalAmount])), [Sales], DESC)'
            },
            {
                'name': 'Calculate with Filter',
                'query': 'EVALUATE ROW("FilteredSales", CALCULATE(SUM(FactSales[TotalAmount]), FactSales[Status] = "Closed Won"))'
            }
        ]

        results = []

        for test in test_queries:
            result = self.test_dax_query_performance(
                workspace_id,
                dataset_id,
                test['query'],
                test['name']
            )
            results.append(result)
            self.test_results.append(result)

            # Small delay between tests
            time.sleep(0.5)

        return results

    def run_all_tests(self) -> Dict:
        """Run all performance tests"""
        logger.info("=" * 60)
        logger.info("POWER BI PERFORMANCE TESTING")
        logger.info(f"Target Load Time: {self.target_load_time_ms}ms (<{self.target_load_time_ms/1000}s)")
        logger.info("=" * 60)

        # Authenticate
        self.authenticate()

        # Get workspace
        workspace_id = self.get_workspace_id()

        # Get reports and datasets
        reports = self.get_reports(workspace_id)
        datasets = self.get_datasets(workspace_id)

        if not datasets:
            logger.warning("⚠️  No datasets found - skipping DAX query tests")
        else:
            # Run query performance tests on first dataset
            dataset = datasets[0]
            logger.info(f"\nTesting dataset: {dataset['name']}")
            self.run_standard_performance_tests(workspace_id, dataset['id'])

        # Test report load times
        if reports:
            logger.info("\n" + "=" * 60)
            logger.info("TESTING REPORT LOAD TIMES")
            logger.info("=" * 60)

            for report in reports:
                result = self.test_report_page_load(workspace_id, report['id'], report['name'])
                self.test_results.append(result)
        else:
            logger.warning("⚠️  No reports found")

        # Generate summary
        return self.generate_summary()

    def generate_summary(self) -> Dict:
        """Generate test summary and statistics"""
        logger.info("\n" + "=" * 60)
        logger.info("PERFORMANCE TEST SUMMARY")
        logger.info("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.get('passed', False))
        failed_tests = total_tests - passed_tests

        if total_tests > 0:
            pass_rate = (passed_tests / total_tests) * 100

            # Calculate average execution time (excluding failed tests)
            valid_times = [r['execution_time_ms'] for r in self.test_results if r['execution_time_ms'] > 0]
            avg_time = sum(valid_times) / len(valid_times) if valid_times else 0

            logger.info(f"Total Tests: {total_tests}")
            logger.info(f"✅ Passed: {passed_tests}")
            logger.info(f"❌ Failed: {failed_tests}")
            logger.info(f"Pass Rate: {pass_rate:.1f}%")
            logger.info(f"Average Execution Time: {avg_time:.0f}ms")
            logger.info(f"Target: {self.target_load_time_ms}ms")

            # List failed tests
            if failed_tests > 0:
                logger.warning("\nFailed Tests:")
                for result in self.test_results:
                    if not result.get('passed', False):
                        logger.warning(f"  - {result['test_name']}: {result.get('execution_time_ms', 'N/A')}ms")

            summary = {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'pass_rate': pass_rate,
                'average_time_ms': avg_time,
                'target_time_ms': self.target_load_time_ms,
                'all_passed': failed_tests == 0,
                'results': self.test_results
            }

            return summary
        else:
            logger.warning("No tests were executed")
            return {'total_tests': 0, 'all_passed': False, 'results': []}

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Performance testing for Power BI reports')
    parser.add_argument('--workspace', help='Fabric workspace name', default=os.getenv('WORKSPACE_NAME'))
    parser.add_argument('--target-load-time', type=int, default=2000, help='Target load time in milliseconds')
    parser.add_argument('--output', help='Output file for results (JSON)')

    args = parser.parse_args()

    if not args.workspace:
        logger.error("Workspace name required (--workspace or WORKSPACE_NAME env var)")
        sys.exit(1)

    try:
        tester = PerformanceTester(args.workspace, args.target_load_time)
        summary = tester.run_all_tests()

        # Save results to file if specified
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info(f"\n📊 Results saved to: {args.output}")

        # Exit with error if tests failed
        if not summary.get('all_passed', False):
            logger.error("\n❌ Performance tests FAILED")
            sys.exit(1)

        logger.info("\n✅ All performance tests PASSED")

    except Exception as e:
        logger.error(f"\n❌ Performance testing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
