#\!/usr/bin/env python3
"""
Standalone script to run Great Expectations data quality checks
This script is called by the Azure Pipeline to validate data quality
"""

import sys
import subprocess
import json
import os
from datetime import datetime

def run_notebook():
    """Execute the data quality notebook and capture results"""
    
    try:
        # Convert notebook to Python script and execute
        cmd = [
            'jupyter', 'nbconvert', 
            '--to', 'script', 
            '--execute', 
            'data_quality_expectations.ipynb',
            '--output', '/tmp/data_quality_execution'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode \!= 0:
            print(f"Data quality validation failed: {result.stderr}")
            return False
        
        print("Data quality validation completed successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("Data quality validation timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"Error running data quality checks: {str(e)}")
        return False

def main():
    """Main execution"""
    print(f"Starting data quality validation at {datetime.now()}")
    
    # Check if notebook exists
    if not os.path.exists('data_quality_expectations.ipynb'):
        print("Error: data_quality_expectations.ipynb not found")
        sys.exit(1)
    
    # Run the notebook
    success = run_notebook()
    
    if success:
        print("✅ Data quality validation passed")
        sys.exit(0)
    else:
        print("❌ Data quality validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
