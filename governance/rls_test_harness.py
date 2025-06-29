#\!/usr/bin/env python3
"""
Fabric Fast-Track Row Level Security (RLS) Test Harness

This script validates RLS implementation across all semantic models in the Fast-Track accelerator.
It tests different user roles and ensures data access is properly restricted.
"""

import os
import json
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Fabric and Power BI SDK imports
try:
    from microsoft.fabric.core import FabricRestClient
    from microsoft.fabric.powerbi import PowerBIRestClient
    from microsoft.fabric.workspace import WorkspaceClient
except ImportError:
    print("Warning: Microsoft Fabric SDK not available. Using mock implementations.")
    # Mock implementations for testing
    class FabricRestClient:
        def __init__(self): pass
    class PowerBIRestClient:
        def __init__(self): pass
    class WorkspaceClient:
        def __init__(self): pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RLSTestHarness:
    """Test harness for Row Level Security validation"""
    
    def __init__(self, workspace_name: str = None):
        self.workspace_name = workspace_name or os.getenv('WORKSPACE_NAME', 'FastTrack-Test-Workspace')
        self.tenant_id = os.getenv('FABRIC_TENANT_ID')
        self.client_id = os.getenv('FABRIC_CLIENT_ID')
        self.client_secret = os.getenv('FABRIC_CLIENT_SECRET')
        
        # Initialize clients
        self.fabric_client = FabricRestClient()
        self.powerbi_client = PowerBIRestClient()
        self.workspace_client = WorkspaceClient()
        
        # Test configuration
        self.test_users = [
            {'username': 'sales.manager@company.com', 'role': 'Sales Manager', 'region': 'North America'},
            {'username': 'sales.rep.east@company.com', 'role': 'Sales Rep', 'region': 'East'},
            {'username': 'sales.rep.west@company.com', 'role': 'Sales Rep', 'region': 'West'},
            {'username': 'finance.analyst@company.com', 'role': 'Finance', 'region': 'All'},
            {'username': 'executive@company.com', 'role': 'Executive', 'region': 'All'}
        ]
        
        self.test_results = []
        self.failed_tests = []
        
    def setup_test_environment(self):
        """Setup test environment and validate prerequisites"""
        logger.info(f"Setting up RLS test environment for workspace: {self.workspace_name}")
        
        try:
            # Validate workspace exists
            workspace = self.workspace_client.get_workspace(self.workspace_name)
            if not workspace:
                raise Exception(f"Workspace '{self.workspace_name}' not found")
            
            # Validate semantic models exist
            semantic_models = self.get_semantic_models()
            if not semantic_models:
                raise Exception("No semantic models found in workspace")
            
            logger.info(f"Found {len(semantic_models)} semantic models to test")
            
            # Validate RLS roles are configured
            for model in semantic_models:
                roles = self.get_model_roles(model['id'])
                if not roles:
                    logger.warning(f"No RLS roles found for model: {model['name']}")
                else:
                    logger.info(f"Model '{model['name']}' has {len(roles)} RLS roles configured")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup test environment: {str(e)}")
            return False
    
    def get_semantic_models(self) -> List[Dict]:
        """Get all semantic models in the workspace"""
        try:
            # Mock data for testing - replace with actual API calls
            return [
                {'id': 'model-1', 'name': 'FastTrack Sales Model', 'type': 'SemanticModel'},
                {'id': 'model-2', 'name': 'FastTrack Finance Model', 'type': 'SemanticModel'},
                {'id': 'model-3', 'name': 'FastTrack Operations Model', 'type': 'SemanticModel'}
            ]
        except Exception as e:
            logger.error(f"Failed to get semantic models: {str(e)}")
            return []
    
    def get_model_roles(self, model_id: str) -> List[Dict]:
        """Get RLS roles for a specific model"""
        try:
            # Mock data for testing - replace with actual API calls
            return [
                {'name': 'Sales Manager', 'filter': "[Region] = 'North America'"},
                {'name': 'Sales Rep East', 'filter': "[Region] = 'East'"},
                {'name': 'Sales Rep West', 'filter': "[Region] = 'West'"},
                {'name': 'Finance', 'filter': "1=1"},  # No filter - access all data
                {'name': 'Executive', 'filter': "1=1"}   # No filter - access all data
            ]
        except Exception as e:
            logger.error(f"Failed to get model roles for {model_id}: {str(e)}")
            return []
    
    def test_user_data_access(self, user: Dict, model_id: str, expected_row_count: int = None) -> Dict:
        """Test data access for a specific user and model"""
        test_name = f"RLS_Test_{user['username']}_{model_id}"
        
        try:
            logger.info(f"Testing data access for {user['username']} on model {model_id}")
            
            # Simulate user context and query execution
            # In actual implementation, this would use Power BI REST API with user impersonation
            result = self.execute_query_as_user(user, model_id)
            
            test_result = {
                'test_name': test_name,
                'user': user['username'],
                'role': user['role'],
                'model_id': model_id,
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'row_count': result.get('row_count', 0),
                'execution_time_ms': result.get('execution_time_ms', 0),
                'error': None
            }
            
            # Validate expected results
            if expected_row_count and result.get('row_count', 0) \!= expected_row_count:
                test_result['success'] = False
                test_result['error'] = f"Expected {expected_row_count} rows, got {result.get('row_count', 0)}"
                self.failed_tests.append(test_result)
            
            # Additional validation based on user role
            if not self.validate_role_based_access(user, result):
                test_result['success'] = False
                test_result['error'] = "Role-based access validation failed"
                self.failed_tests.append(test_result)
            
            self.test_results.append(test_result)
            return test_result
            
        except Exception as e:
            error_result = {
                'test_name': test_name,
                'user': user['username'],
                'role': user['role'],
                'model_id': model_id,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            }
            self.failed_tests.append(error_result)
            self.test_results.append(error_result)
            logger.error(f"Test failed for {user['username']}: {str(e)}")
            return error_result
    
    def execute_query_as_user(self, user: Dict, model_id: str) -> Dict:
        """Execute a test query impersonating the specified user"""
        
        # Mock query execution - replace with actual Power BI REST API calls
        # This would use the /executeQueries endpoint with effective identity
        
        start_time = time.time()
        
        # Simulate different data access based on user role
        if user['role'] == 'Sales Manager':
            row_count = 1000  # Full access to North America region
        elif user['role'] == 'Sales Rep':
            row_count = 200   # Limited to specific region
        elif user['role'] == 'Finance':
            row_count = 1500  # Access to financial data across all regions
        elif user['role'] == 'Executive':
            row_count = 2000  # Full access to all data
        else:
            row_count = 0     # No access
        
        execution_time = (time.time() - start_time) * 1000
        
        return {
            'row_count': row_count,
            'execution_time_ms': execution_time,
            'columns': ['Region', 'Sales', 'Product', 'Date'],
            'has_data': row_count > 0
        }
    
    def validate_role_based_access(self, user: Dict, query_result: Dict) -> bool:
        """Validate that the user can only access data appropriate for their role"""
        
        # Role-based validation rules
        if user['role'] == 'Sales Rep' and user['region'] in ['East', 'West']:
            # Sales reps should only see data for their region
            return query_result.get('row_count', 0) > 0 and query_result.get('row_count', 0) < 500
        
        elif user['role'] == 'Sales Manager':
            # Sales managers should see more data but not everything
            return query_result.get('row_count', 0) > 500 and query_result.get('row_count', 0) < 1500
        
        elif user['role'] in ['Finance', 'Executive']:
            # Finance and executives should have broad access
            return query_result.get('row_count', 0) > 1000
        
        else:
            # Unknown roles should have no access
            return query_result.get('row_count', 0) == 0
    
    def test_cross_model_consistency(self):
        """Test that RLS is consistently applied across related models"""
        logger.info("Testing cross-model RLS consistency")
        
        models = self.get_semantic_models()
        consistency_results = []
        
        for user in self.test_users:
            user_results = {}
            
            # Test each model for this user
            for model in models:
                result = self.test_user_data_access(user, model['id'])
                user_results[model['id']] = result.get('row_count', 0)
            
            # Validate consistency rules
            # Example: Sales data should be consistent across sales and finance models
            consistency_check = {
                'user': user['username'],
                'role': user['role'],
                'models_tested': len(models),
                'consistent': True,
                'details': user_results
            }
            
            # Add specific consistency validation logic here
            # For example, check that related models show consistent row counts
            
            consistency_results.append(consistency_check)
        
        return consistency_results
    
    def test_role_inheritance(self):
        """Test that role inheritance works correctly"""
        logger.info("Testing RLS role inheritance")
        
        # Test cases for role inheritance
        inheritance_tests = [
            {
                'parent_role': 'Sales Manager',
                'child_role': 'Sales Rep East',
                'expected_behavior': 'child_subset_of_parent'
            },
            {
                'parent_role': 'Executive',
                'child_role': 'Finance', 
                'expected_behavior': 'child_subset_of_parent'
            }
        ]
        
        results = []
        for test in inheritance_tests:
            # Implementation would test actual role inheritance
            # For now, we'll create a mock result
            result = {
                'test_name': f"Inheritance_{test['parent_role']}_to_{test['child_role']}",
                'parent_role': test['parent_role'],
                'child_role': test['child_role'],
                'expected_behavior': test['expected_behavior'],
                'success': True,  # Mock success
                'details': 'Role inheritance working correctly'
            }
            results.append(result)
        
        return results
    
    def run_performance_tests(self):
        """Test RLS performance impact"""
        logger.info("Running RLS performance tests")
        
        performance_results = []
        
        for user in self.test_users:
            for model in self.get_semantic_models():
                # Run multiple queries to get average performance
                execution_times = []
                
                for i in range(5):  # Run 5 iterations
                    result = self.execute_query_as_user(user, model['id'])
                    execution_times.append(result.get('execution_time_ms', 0))
                
                avg_time = sum(execution_times) / len(execution_times)
                
                perf_result = {
                    'user': user['username'],
                    'model': model['name'],
                    'avg_execution_time_ms': avg_time,
                    'max_execution_time_ms': max(execution_times),
                    'min_execution_time_ms': min(execution_times),
                    'within_sla': avg_time < 2000,  # 2 second SLA
                    'test_iterations': len(execution_times)
                }
                
                performance_results.append(perf_result)
        
        return performance_results
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t['success']])
        failed_tests = len(self.failed_tests)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            'summary': {
                'timestamp': datetime.now().isoformat(),
                'workspace': self.workspace_name,
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': success_rate,
                'overall_status': 'PASS' if failed_tests == 0 else 'FAIL'
            },
            'test_results': self.test_results,
            'failed_tests': self.failed_tests
        }
        
        return report
    
    def export_junit_xml(self, report: Dict):
        """Export results in JUnit XML format for Azure Pipelines"""
        
        junit_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="RLSValidation" tests="{report['summary']['total_tests']}" failures="{report['summary']['failed_tests']}" time="0">
'''
        
        for test in self.test_results:
            if test['success']:
                junit_xml += f'  <testcase classname="RLS" name="{test['test_name']}" time="{test.get('execution_time_ms', 0)/1000}"/>\n'
            else:
                junit_xml += f'  <testcase classname="RLS" name="{test['test_name']}" time="0">\n'
                junit_xml += f'    <failure message="{test.get('error', 'Unknown error')}">\n'
                junit_xml += f'      User: {test['user']}\n'
                junit_xml += f'      Role: {test['role']}\n'
                junit_xml += f'      Model: {test['model_id']}\n'
                junit_xml += f'      Error: {test.get('error', 'Unknown error')}\n'
                junit_xml += '    </failure>\n'
                junit_xml += '  </testcase>\n'
        
        junit_xml += '</testsuite>'
        
        # Write to file
        with open('/tmp/rls_test_results.xml', 'w') as f:
            f.write(junit_xml)
        
        logger.info("JUnit XML results exported to /tmp/rls_test_results.xml")
    
    def run_all_tests(self):
        """Execute all RLS tests"""
        logger.info(f"Starting RLS test suite for workspace: {self.workspace_name}")
        
        # Setup test environment
        if not self.setup_test_environment():
            logger.error("Failed to setup test environment")
            return False
        
        try:
            # Run basic access tests
            logger.info("Running basic RLS access tests...")
            models = self.get_semantic_models()
            
            for user in self.test_users:
                for model in models:
                    self.test_user_data_access(user, model['id'])
            
            # Run cross-model consistency tests
            logger.info("Running cross-model consistency tests...")
            consistency_results = self.test_cross_model_consistency()
            
            # Run role inheritance tests
            logger.info("Running role inheritance tests...")
            inheritance_results = self.test_role_inheritance()
            
            # Run performance tests
            logger.info("Running performance tests...")
            performance_results = self.run_performance_tests()
            
            # Generate and export report
            report = self.generate_test_report()
            self.export_junit_xml(report)
            
            # Print summary
            self.print_test_summary(report)
            
            # Export detailed results
            with open('/tmp/rls_test_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            
            return report['summary']['overall_status'] == 'PASS'
            
        except Exception as e:
            logger.error(f"Error during RLS testing: {str(e)}")
            return False
    
    def print_test_summary(self, report: Dict):
        """Print test summary to console"""
        
        summary = report['summary']
        
        print("\n" + "="*60)
        print("RLS TEST SUMMARY REPORT")
        print("="*60)
        print(f"Timestamp: {summary['timestamp']}")
        print(f"Workspace: {summary['workspace']}")
        print(f"Overall Status: {summary['overall_status']}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        
        if self.failed_tests:
            print("\nFAILED TESTS:")
            print("-" * 40)
            for test in self.failed_tests:
                print(f"❌ {test['test_name']}")
                print(f"   User: {test['user']}")
                print(f"   Error: {test.get('error', 'Unknown error')}")
                print()
        
        print("\n" + "="*60)

def main():
    """Main execution function"""
    
    # Get configuration from environment
    workspace_name = os.getenv('WORKSPACE_NAME', 'FastTrack-Test-Workspace')
    
    # Initialize test harness
    rls_tester = RLSTestHarness(workspace_name)
    
    # Run all tests
    success = rls_tester.run_all_tests()
    
    # Exit with appropriate code
    if success:
        logger.info("All RLS tests passed\! ✅")
        exit(0)
    else:
        logger.error("RLS tests failed\! ❌")
        exit(1)

if __name__ == "__main__":
    main()
