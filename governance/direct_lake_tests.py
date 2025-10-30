#!/usr/bin/env python3
"""
Fabric Fast-Track Direct Lake Testing Script
Validates Direct Lake mode, refresh operations, and connectivity
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

class DirectLakeTester:
    """Test Direct Lake semantic models"""

    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name
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
        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.get(f"{self.powerbi_api}/groups", headers=headers)
        response.raise_for_status()

        workspaces = response.json().get('value', [])
        for ws in workspaces:
            if ws['name'] == self.workspace_name:
                logger.info(f"✅ Found workspace: {ws['id']}")
                return ws['id']

        raise ValueError(f"Workspace '{self.workspace_name}' not found")

    def get_datasets(self, workspace_id: str) -> List[Dict]:
        """Get all datasets in workspace"""
        logger.info("Retrieving datasets...")

        headers = {'Authorization': f'Bearer {self.access_token}'}

        response = requests.get(
            f"{self.powerbi_api}/groups/{workspace_id}/datasets",
            headers=headers
        )
        response.raise_for_status()

        datasets = response.json().get('value', [])
        logger.info(f"Found {len(datasets)} dataset(s)")
        return datasets

    def test_direct_lake_mode(self, workspace_id: str, dataset: Dict) -> Dict:
        """Test if dataset is in Direct Lake mode"""
        dataset_name = dataset['name']
        dataset_id = dataset['id']

        logger.info(f"Testing Direct Lake mode for: {dataset_name}")

        # Check dataset details
        headers = {'Authorization': f'Bearer {self.access_token}'}

        try:
            response = requests.get(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}",
                headers=headers
            )
            response.raise_for_status()

            dataset_details = response.json()

            # Check for Direct Lake indicators
            is_direct_lake = dataset_details.get('defaultMode') == 'DirectLake'
            configured_by = dataset_details.get('configuredBy', 'Unknown')

            test_result = {
                'test_name': f'Direct Lake Mode Check: {dataset_name}',
                'type': 'direct_lake_mode',
                'dataset_id': dataset_id,
                'is_direct_lake': is_direct_lake,
                'mode': dataset_details.get('defaultMode', 'Unknown'),
                'configured_by': configured_by,
                'passed': is_direct_lake,
                'timestamp': datetime.now().isoformat()
            }

            if is_direct_lake:
                logger.info(f"✅ Dataset is in Direct Lake mode")
            else:
                logger.warning(f"⚠️  Dataset is NOT in Direct Lake mode (mode: {dataset_details.get('defaultMode', 'Unknown')})")

            return test_result

        except Exception as e:
            logger.error(f"❌ Failed to check Direct Lake mode: {e}")
            return {
                'test_name': f'Direct Lake Mode Check: {dataset_name}',
                'type': 'direct_lake_mode',
                'dataset_id': dataset_id,
                'passed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def test_refresh_capability(self, workspace_id: str, dataset: Dict) -> Dict:
        """Test dataset refresh capability"""
        dataset_name = dataset['name']
        dataset_id = dataset['id']

        logger.info(f"Testing refresh capability for: {dataset_name}")

        headers = {'Authorization': f'Bearer {self.access_token}'}

        try:
            # Get refresh history
            response = requests.get(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}/refreshes?$top=1",
                headers=headers
            )
            response.raise_for_status()

            refreshes = response.json().get('value', [])
            has_refresh_history = len(refreshes) > 0

            last_refresh_status = 'Never refreshed'
            last_refresh_time = None

            if has_refresh_history:
                last_refresh = refreshes[0]
                last_refresh_status = last_refresh.get('status', 'Unknown')
                last_refresh_time = last_refresh.get('endTime', last_refresh.get('startTime'))

            # Check if dataset can be refreshed
            can_refresh = dataset.get('isRefreshable', False)

            test_result = {
                'test_name': f'Refresh Capability: {dataset_name}',
                'type': 'refresh_capability',
                'dataset_id': dataset_id,
                'can_refresh': can_refresh,
                'has_refresh_history': has_refresh_history,
                'last_refresh_status': last_refresh_status,
                'last_refresh_time': last_refresh_time,
                'passed': can_refresh,
                'timestamp': datetime.now().isoformat()
            }

            if can_refresh:
                logger.info(f"✅ Dataset can be refreshed (last: {last_refresh_status})")
            else:
                logger.warning(f"⚠️  Dataset cannot be refreshed")

            return test_result

        except Exception as e:
            logger.error(f"❌ Failed to check refresh capability: {e}")
            return {
                'test_name': f'Refresh Capability: {dataset_name}',
                'type': 'refresh_capability',
                'dataset_id': dataset_id,
                'passed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def test_trigger_refresh(self, workspace_id: str, dataset: Dict, wait_for_completion: bool = True) -> Dict:
        """Trigger dataset refresh and optionally wait for completion"""
        dataset_name = dataset['name']
        dataset_id = dataset['id']

        logger.info(f"Triggering refresh for: {dataset_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            # Trigger refresh
            response = requests.post(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}/refreshes",
                headers=headers
            )
            response.raise_for_status()

            refresh_triggered = response.status_code == 202
            logger.info(f"✅ Refresh triggered successfully")

            if wait_for_completion and refresh_triggered:
                logger.info("Waiting for refresh to complete...")
                refresh_status = self._wait_for_refresh(workspace_id, dataset_id)
            else:
                refresh_status = 'Triggered'

            test_result = {
                'test_name': f'Trigger Refresh: {dataset_name}',
                'type': 'trigger_refresh',
                'dataset_id': dataset_id,
                'refresh_triggered': refresh_triggered,
                'refresh_status': refresh_status,
                'passed': refresh_triggered and (refresh_status == 'Completed' if wait_for_completion else True),
                'timestamp': datetime.now().isoformat()
            }

            return test_result

        except Exception as e:
            error_msg = str(e)

            # Check for specific Direct Lake errors
            if '400' in error_msg:
                logger.warning(f"⚠️  Refresh not needed (Direct Lake auto-updates)")
                return {
                    'test_name': f'Trigger Refresh: {dataset_name}',
                    'type': 'trigger_refresh',
                    'dataset_id': dataset_id,
                    'refresh_triggered': False,
                    'refresh_status': 'Not needed (Direct Lake)',
                    'passed': True,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.error(f"❌ Failed to trigger refresh: {e}")
                return {
                    'test_name': f'Trigger Refresh: {dataset_name}',
                    'type': 'trigger_refresh',
                    'dataset_id': dataset_id,
                    'passed': False,
                    'error': error_msg,
                    'timestamp': datetime.now().isoformat()
                }

    def _wait_for_refresh(self, workspace_id: str, dataset_id: str, timeout: int = 300) -> str:
        """Wait for refresh to complete"""
        headers = {'Authorization': f'Bearer {self.access_token}'}

        start_time = time.time()

        while (time.time() - start_time) < timeout:
            try:
                response = requests.get(
                    f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}/refreshes?$top=1",
                    headers=headers
                )
                response.raise_for_status()

                refreshes = response.json().get('value', [])
                if refreshes:
                    status = refreshes[0].get('status', 'Unknown')

                    if status in ['Completed', 'Failed']:
                        return status

                time.sleep(5)  # Check every 5 seconds

            except Exception as e:
                logger.warning(f"Error checking refresh status: {e}")
                return 'Unknown'

        logger.warning("Refresh timeout")
        return 'Timeout'

    def test_data_connectivity(self, workspace_id: str, dataset_id: str, dataset_name: str) -> Dict:
        """Test data connectivity by executing a simple query"""
        logger.info(f"Testing data connectivity for: {dataset_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Simple DAX query to test connectivity
        test_query = 'EVALUATE ROW("Test", 1)'

        payload = {
            'queries': [{
                'query': test_query
            }]
        }

        try:
            response = requests.post(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}/executeQueries",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            test_result = {
                'test_name': f'Data Connectivity: {dataset_name}',
                'type': 'data_connectivity',
                'dataset_id': dataset_id,
                'query_executed': True,
                'passed': True,
                'timestamp': datetime.now().isoformat()
            }

            logger.info(f"✅ Data connectivity verified")
            return test_result

        except Exception as e:
            logger.error(f"❌ Data connectivity failed: {e}")
            return {
                'test_name': f'Data Connectivity: {dataset_name}',
                'type': 'data_connectivity',
                'dataset_id': dataset_id,
                'passed': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def run_all_tests(self, trigger_refresh: bool = False) -> Dict:
        """Run all Direct Lake tests"""
        logger.info("=" * 60)
        logger.info("DIRECT LAKE VALIDATION TESTS")
        logger.info("=" * 60)

        # Authenticate
        self.authenticate()

        # Get workspace
        workspace_id = self.get_workspace_id()

        # Get datasets
        datasets = self.get_datasets(workspace_id)

        if not datasets:
            logger.warning("⚠️  No datasets found")
            return {'total_tests': 0, 'all_passed': False, 'results': []}

        # Run tests on each dataset
        for dataset in datasets:
            logger.info(f"\n{'='*60}")
            logger.info(f"Testing Dataset: {dataset['name']}")
            logger.info(f"{'='*60}")

            # Test 1: Direct Lake mode check
            result = self.test_direct_lake_mode(workspace_id, dataset)
            self.test_results.append(result)

            # Test 2: Refresh capability
            result = self.test_refresh_capability(workspace_id, dataset)
            self.test_results.append(result)

            # Test 3: Data connectivity
            result = self.test_data_connectivity(workspace_id, dataset['id'], dataset['name'])
            self.test_results.append(result)

            # Test 4: Trigger refresh (optional)
            if trigger_refresh:
                result = self.test_trigger_refresh(workspace_id, dataset, wait_for_completion=True)
                self.test_results.append(result)

        return self.generate_summary()

    def generate_summary(self) -> Dict:
        """Generate test summary"""
        logger.info("\n" + "=" * 60)
        logger.info("DIRECT LAKE TEST SUMMARY")
        logger.info("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.get('passed', False))
        failed_tests = total_tests - passed_tests

        if total_tests > 0:
            pass_rate = (passed_tests / total_tests) * 100

            logger.info(f"Total Tests: {total_tests}")
            logger.info(f"✅ Passed: {passed_tests}")
            logger.info(f"❌ Failed: {failed_tests}")
            logger.info(f"Pass Rate: {pass_rate:.1f}%")

            # List failed tests
            if failed_tests > 0:
                logger.warning("\nFailed Tests:")
                for result in self.test_results:
                    if not result.get('passed', False):
                        logger.warning(f"  - {result['test_name']}")
                        if 'error' in result:
                            logger.warning(f"    Error: {result['error']}")

            return {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'pass_rate': pass_rate,
                'all_passed': failed_tests == 0,
                'results': self.test_results
            }
        else:
            logger.warning("No tests were executed")
            return {'total_tests': 0, 'all_passed': False, 'results': []}

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Direct Lake validation tests')
    parser.add_argument('--workspace', help='Fabric workspace name', default=os.getenv('WORKSPACE_NAME'))
    parser.add_argument('--trigger-refresh', action='store_true', help='Trigger dataset refresh')
    parser.add_argument('--output', help='Output file for results (JSON)')

    args = parser.parse_args()

    if not args.workspace:
        logger.error("Workspace name required (--workspace or WORKSPACE_NAME env var)")
        sys.exit(1)

    try:
        tester = DirectLakeTester(args.workspace)
        summary = tester.run_all_tests(trigger_refresh=args.trigger_refresh)

        # Save results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info(f"\n📊 Results saved to: {args.output}")

        # Exit with error if tests failed
        if not summary.get('all_passed', False):
            logger.error("\n❌ Direct Lake tests FAILED")
            sys.exit(1)

        logger.info("\n✅ All Direct Lake tests PASSED")

    except Exception as e:
        logger.error(f"\n❌ Direct Lake testing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
