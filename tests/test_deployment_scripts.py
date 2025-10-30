#!/usr/bin/env python3
"""
Integration Tests for Fabric Fast-Track Deployment Scripts
Tests deployment automation, validation, and error handling
"""

import os
import sys
import unittest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'governance'))

class TestDeploymentScripts(unittest.TestCase):
    """Test suite for deployment automation scripts"""

    def setUp(self):
        """Set up test environment"""
        self.test_workspace = "Test-Workspace"
        self.test_env_vars = {
            'FABRIC_TENANT_ID': 'test-tenant-id',
            'FABRIC_CLIENT_ID': 'test-client-id',
            'FABRIC_CLIENT_SECRET': 'test-secret',
            'WORKSPACE_NAME': self.test_workspace
        }

        # Set environment variables for tests
        for key, value in self.test_env_vars.items():
            os.environ[key] = value

    def tearDown(self):
        """Clean up after tests"""
        for key in self.test_env_vars.keys():
            if key in os.environ:
                del os.environ[key]

    def test_pipeline_deployer_initialization(self):
        """Test FabricPipelineDeployer initialization"""
        from deploy_pipelines import FabricPipelineDeployer

        deployer = FabricPipelineDeployer(self.test_workspace)

        self.assertEqual(deployer.workspace_name, self.test_workspace)
        self.assertEqual(deployer.tenant_id, 'test-tenant-id')
        self.assertEqual(deployer.client_id, 'test-client-id')
        self.assertEqual(deployer.client_secret, 'test-secret')
        self.assertIsNotNone(deployer.api_base)

    def test_pipeline_deployer_missing_credentials(self):
        """Test error handling for missing credentials"""
        from deploy_pipelines import FabricPipelineDeployer

        # Remove required env var
        del os.environ['FABRIC_CLIENT_SECRET']

        with self.assertRaises(ValueError) as context:
            deployer = FabricPipelineDeployer(self.test_workspace)

        self.assertIn("Missing required environment variables", str(context.exception))

    @patch('deploy_pipelines.requests.post')
    def test_pipeline_deployer_authentication(self, mock_post):
        """Test authentication flow"""
        from deploy_pipelines import FabricPipelineDeployer

        # Mock successful auth response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test-token-123'}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        deployer = FabricPipelineDeployer(self.test_workspace)
        token = deployer.authenticate()

        self.assertEqual(token, 'test-token-123')
        self.assertEqual(deployer.access_token, 'test-token-123')
        mock_post.assert_called_once()

    def test_semantic_model_deployer_initialization(self):
        """Test SemanticModelDeployer initialization"""
        from deploy_semantic_model import SemanticModelDeployer

        deployer = SemanticModelDeployer(self.test_workspace)

        self.assertEqual(deployer.workspace_name, self.test_workspace)
        self.assertIsNotNone(deployer.powerbi_api)

    def test_semantic_model_bim_validation(self):
        """Test BIM file validation"""
        from deploy_semantic_model import SemanticModelDeployer

        deployer = SemanticModelDeployer(self.test_workspace)

        # Create temporary test BIM file
        test_bim_path = Path(__file__).parent / 'test_model.bim'
        test_bim_content = {
            'name': 'TestModel',
            'model': {
                'tables': [
                    {'name': 'TestTable', 'columns': []}
                ],
                'measures': [
                    {'name': 'TestMeasure', 'expression': 'SUM(TestTable[Amount])'}
                ]
            }
        }

        with open(test_bim_path, 'w') as f:
            json.dump(test_bim_content, f)

        try:
            result = deployer.validate_bim_file(str(test_bim_path))

            self.assertEqual(result['name'], 'TestModel')
            self.assertIn('tables', result['model'])
            self.assertIn('measures', result['model'])
            self.assertEqual(len(result['model']['tables']), 1)
            self.assertEqual(len(result['model']['measures']), 1)

        finally:
            test_bim_path.unlink()

    def test_report_deployer_initialization(self):
        """Test ReportDeployer initialization"""
        from deploy_reports import ReportDeployer

        deployer = ReportDeployer(self.test_workspace)

        self.assertEqual(deployer.workspace_name, self.test_workspace)
        self.assertIsNotNone(deployer.powerbi_api)

    def test_report_template_validation(self):
        """Test report template validation"""
        from deploy_reports import ReportDeployer

        deployer = ReportDeployer(self.test_workspace)

        # Create temporary test template
        test_template_path = Path(__file__).parent / 'test_report.json'
        test_template = {
            'name': 'Test Report',
            'pages': [
                {
                    'name': 'Page1',
                    'displayName': 'Overview',
                    'visualContainers': []
                }
            ]
        }

        with open(test_template_path, 'w') as f:
            json.dump(test_template, f)

        try:
            result = deployer.validate_report_template(str(test_template_path))

            self.assertEqual(result['name'], 'Test Report')
            self.assertEqual(len(result['pages']), 1)

        finally:
            test_template_path.unlink()

    def test_performance_tester_initialization(self):
        """Test PerformanceTester initialization"""
        from performance_tests import PerformanceTester

        tester = PerformanceTester(self.test_workspace, target_load_time=2000)

        self.assertEqual(tester.workspace_name, self.test_workspace)
        self.assertEqual(tester.target_load_time_ms, 2000)
        self.assertIsNotNone(tester.test_results)

    def test_direct_lake_tester_initialization(self):
        """Test DirectLakeTester initialization"""
        from direct_lake_tests import DirectLakeTester

        tester = DirectLakeTester(self.test_workspace)

        self.assertEqual(tester.workspace_name, self.test_workspace)
        self.assertIsNotNone(tester.test_results)

    def test_data_quality_runner_initialization(self):
        """Test DataQualityRunner initialization"""
        from run_data_quality_checks import DataQualityRunner

        runner = DataQualityRunner()

        self.assertEqual(runner.workspace_name, self.test_workspace)
        self.assertIsNotNone(runner.results)
        self.assertIsNotNone(runner.failed_checks)

    def test_data_quality_runner_simulation_mode(self):
        """Test DataQualityRunner in simulation mode"""
        from run_data_quality_checks import DataQualityRunner

        # Remove credentials to force simulation mode
        del os.environ['FABRIC_CLIENT_SECRET']

        runner = DataQualityRunner()

        # Test simulated row count
        count = runner.query_table_count('bronze_customers')
        self.assertEqual(count, 10000)  # Simulated count

        # Test simulated update time
        update_time = runner.query_last_update_time('bronze_customers')
        self.assertIsNotNone(update_time)

    def test_data_quality_validation_pass(self):
        """Test data quality validation passing"""
        from run_data_quality_checks import DataQualityRunner

        del os.environ['FABRIC_CLIENT_SECRET']
        runner = DataQualityRunner()

        # Test row count validation (should pass with simulated data)
        result = runner.validate_row_counts('bronze_customers', min_rows=100)

        self.assertTrue(result['passed'])
        self.assertEqual(result['check'], 'row_count')
        self.assertEqual(result['table'], 'bronze_customers')
        self.assertGreaterEqual(result['actual'], result['expected_min'])

    def test_data_quality_validation_fail(self):
        """Test data quality validation failing"""
        from run_data_quality_checks import DataQualityRunner

        del os.environ['FABRIC_CLIENT_SECRET']
        runner = DataQualityRunner()

        # Test row count validation with impossible requirement
        result = runner.validate_row_counts('bronze_customers', min_rows=1000000)

        self.assertFalse(result['passed'])
        self.assertEqual(result['check'], 'row_count')
        self.assertIn(result, runner.failed_checks)


class TestIntegrationScenarios(unittest.TestCase):
    """End-to-end integration test scenarios"""

    def setUp(self):
        """Set up integration test environment"""
        self.test_env = {
            'FABRIC_TENANT_ID': 'integration-test-tenant',
            'FABRIC_CLIENT_ID': 'integration-test-client',
            'FABRIC_CLIENT_SECRET': 'integration-test-secret',
            'WORKSPACE_NAME': 'Integration-Test-Workspace'
        }

        for key, value in self.test_env.items():
            os.environ[key] = value

    def tearDown(self):
        """Clean up integration test environment"""
        for key in self.test_env.keys():
            if key in os.environ:
                del os.environ[key]

    def test_full_deployment_workflow(self):
        """Test complete deployment workflow"""
        # This test simulates the full deployment pipeline
        # In a real environment, this would deploy to a test workspace

        from deploy_pipelines import FabricPipelineDeployer
        from deploy_semantic_model import SemanticModelDeployer
        from deploy_reports import ReportDeployer

        # Initialize deployers
        pipeline_deployer = FabricPipelineDeployer('Integration-Test-Workspace')
        model_deployer = SemanticModelDeployer('Integration-Test-Workspace')
        report_deployer = ReportDeployer('Integration-Test-Workspace')

        # Verify all deployers initialized correctly
        self.assertIsNotNone(pipeline_deployer)
        self.assertIsNotNone(model_deployer)
        self.assertIsNotNone(report_deployer)

        # In a real test, we would call:
        # pipeline_deployer.deploy_all_pipelines()
        # model_deployer.deploy_all_models()
        # report_deployer.deploy_all_reports()

    def test_validation_pipeline(self):
        """Test validation pipeline workflow"""
        from performance_tests import PerformanceTester
        from direct_lake_tests import DirectLakeTester
        from run_data_quality_checks import DataQualityRunner

        # Initialize all testers
        performance_tester = PerformanceTester('Integration-Test-Workspace')
        direct_lake_tester = DirectLakeTester('Integration-Test-Workspace')

        # Remove credentials to use simulation mode
        del os.environ['FABRIC_CLIENT_SECRET']
        data_quality_runner = DataQualityRunner()

        # Verify all validators initialized correctly
        self.assertIsNotNone(performance_tester)
        self.assertIsNotNone(direct_lake_tester)
        self.assertIsNotNone(data_quality_runner)


def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDeploymentScripts))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
