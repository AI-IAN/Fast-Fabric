#\!/usr/bin/env python3
"""
Fabric Fast-Track Data Quality Validation Runner
Comprehensive data quality checks with detailed validation logic
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataQualityRunner:
    def __init__(self):
        self.workspace_name = os.getenv("WORKSPACE_NAME", "FastTrack-Test-Workspace")
        self.results = []
        self.failed_checks = []
        
    def validate_row_counts(self, table_name: str, min_rows: int = 1) -> Dict:
        # Mock row counts - replace with actual queries
        mock_counts = {
            "bronze_customers": 10000,
            "bronze_orders": 50000, 
            "silver_fact_sales": 48500
        }
        
        actual = mock_counts.get(table_name, 0)
        passed = actual >= min_rows
        
        result = {
            "check": "row_count",
            "table": table_name,
            "expected_min": min_rows,
            "actual": actual,
            "passed": passed,
            "timestamp": datetime.now().isoformat()
        }
        
        if passed:
            logger.info(f"✅ {table_name}: {actual} rows")
        else:
            logger.error(f"❌ {table_name}: {actual} rows < {min_rows}")
            self.failed_checks.append(result)
            
        return result
    
    def validate_data_freshness(self, table_name: str, max_hours: int = 24) -> Dict:
        # Mock freshness check
        now = datetime.now()
        last_update = now - timedelta(hours=2)  # 2 hours old
        age_hours = (now - last_update).total_seconds() / 3600
        passed = age_hours <= max_hours
        
        result = {
            "check": "freshness",
            "table": table_name,
            "age_hours": round(age_hours, 2),
            "max_hours": max_hours,
            "passed": passed,
            "timestamp": now.isoformat()
        }
        
        if passed:
            logger.info(f"✅ {table_name}: {age_hours:.1f} hours old")
        else:
            logger.error(f"❌ {table_name}: {age_hours:.1f} hours old")
            self.failed_checks.append(result)
            
        return result
    
    def run_bronze_validation(self):
        logger.info("=== BRONZE LAYER VALIDATION ===")
        
        tables = [
            ("bronze_customers", 1000),
            ("bronze_orders", 5000),
            ("bronze_products", 100)
        ]
        
        for table, min_rows in tables:
            result = self.validate_row_counts(table, min_rows)
            self.results.append(result)
            
            result = self.validate_data_freshness(table, 48)
            self.results.append(result)
    
    def run_silver_validation(self):
        logger.info("=== SILVER LAYER VALIDATION ===")
        
        tables = [("silver_fact_sales", 4000)]
        
        for table, min_rows in tables:
            result = self.validate_row_counts(table, min_rows)
            self.results.append(result)
            
            result = self.validate_data_freshness(table, 24)
            self.results.append(result)
    
    def generate_summary(self):
        total = len(self.results)
        failed = len(self.failed_checks)
        passed = total - failed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        status = "PASS" if failed == 0 else "FAIL"
        
        print("
" + "="*50)
        print("DATA QUALITY SUMMARY")
        print("="*50)
        print(f"Status: {status}")
        print(f"Total Checks: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        return status == "PASS"
    
    def export_results(self):
        os.makedirs("/tmp", exist_ok=True)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "workspace": self.workspace_name,
            "total_checks": len(self.results),
            "failed_checks": len(self.failed_checks),
            "overall_status": "PASS" if len(self.failed_checks) == 0 else "FAIL",
            "results": self.results
        }
        
        with open("/tmp/data_quality_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        # JUnit XML
        xml = f"<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="DataQuality" tests="{len(self.results)}" failures="{len(self.failed_checks)}">
"
        
        for result in self.results:
            name = f"{result["check"]}_{result["table"]}"
            if result["passed"]:
                xml += f"  <testcase name="{name}"/>\n"
            else:
                xml += f"  <testcase name="{name}">\n    <failure/>\n  </testcase>\n"
        
        xml += "</testsuite>"
        
        with open("/tmp/data_quality_results.xml", "w") as f:
            f.write(xml)
        
        logger.info("Results exported")
    
    def run_all(self):
        logger.info(f"Starting validation at {datetime.now()}")
        
        try:
            self.run_bronze_validation()
            self.run_silver_validation()
            
            success = self.generate_summary()
            self.export_results()
            
            return success
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

def main():
    runner = DataQualityRunner()
    
    try:
        success = runner.run_all()
        
        if success:
            print("
🎉 All validations PASSED\!")
            sys.exit(0)
        else:
            print("
💥 Validations FAILED\!")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
