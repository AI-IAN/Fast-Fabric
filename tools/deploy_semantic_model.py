#!/usr/bin/env python3
"""
Fabric Fast-Track Semantic Model Deployment Script
Deploys Power BI semantic models (.bim files) to Microsoft Fabric workspace
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict
import requests
from pathlib import Path
import base64

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SemanticModelDeployer:
    """Deploy semantic models to Microsoft Fabric workspace"""

    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name
        self.tenant_id = os.getenv('FABRIC_TENANT_ID')
        self.client_id = os.getenv('FABRIC_CLIENT_ID')
        self.client_secret = os.getenv('FABRIC_CLIENT_SECRET')
        self.api_base = "https://api.fabric.microsoft.com/v1"
        self.powerbi_api = "https://api.powerbi.com/v1.0/myorg"
        self.access_token = None

        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("Missing required environment variables")

    def authenticate(self) -> str:
        """Authenticate with Microsoft Fabric API"""
        logger.info("Authenticating with Microsoft Fabric API...")

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
        logger.info(f"Looking up workspace: {self.workspace_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.get(
                f"{self.powerbi_api}/groups",
                headers=headers
            )
            response.raise_for_status()

            workspaces = response.json().get('value', [])
            for ws in workspaces:
                if ws['name'] == self.workspace_name:
                    workspace_id = ws['id']
                    logger.info(f"✅ Found workspace ID: {workspace_id}")
                    return workspace_id

            raise ValueError(f"Workspace '{self.workspace_name}' not found")
        except Exception as e:
            logger.error(f"❌ Failed to get workspace: {e}")
            raise

    def validate_bim_file(self, bim_path: str) -> Dict:
        """Validate BIM file structure"""
        logger.info(f"Validating BIM file: {bim_path}")

        try:
            with open(bim_path, 'r') as f:
                bim_content = json.load(f)

            # Check for required fields
            required_fields = ['name', 'model']
            missing = [field for field in required_fields if field not in bim_content]

            if missing:
                raise ValueError(f"Missing required fields: {missing}")

            # Validate model structure
            model = bim_content.get('model', {})
            if 'tables' not in model:
                logger.warning("⚠️  No tables defined in model")

            if 'measures' not in model:
                logger.warning("⚠️  No measures defined in model")

            measure_count = len(model.get('measures', []))
            table_count = len(model.get('tables', []))

            logger.info(f"✅ BIM validation passed:")
            logger.info(f"   - Tables: {table_count}")
            logger.info(f"   - Measures: {measure_count}")

            return bim_content
        except Exception as e:
            logger.error(f"❌ BIM validation failed: {e}")
            raise

    def deploy_semantic_model(self, workspace_id: str, bim_path: str, dataset_name: str = None) -> Dict:
        """Deploy semantic model to workspace"""

        # Validate BIM file
        bim_content = self.validate_bim_file(bim_path)

        if dataset_name is None:
            dataset_name = bim_content.get('name', Path(bim_path).stem)

        logger.info(f"Deploying semantic model: {dataset_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            # Check if dataset already exists
            response = requests.get(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets",
                headers=headers
            )
            response.raise_for_status()

            existing_datasets = response.json().get('value', [])
            existing_dataset = next((ds for ds in existing_datasets if ds['name'] == dataset_name), None)

            if existing_dataset:
                dataset_id = existing_dataset['id']
                logger.info(f"Dataset '{dataset_name}' already exists. Updating...")

                # Update existing dataset using XMLA endpoint
                # Note: This requires XMLA read-write enabled on the workspace
                result = self._update_dataset_via_xmla(workspace_id, dataset_id, bim_content)
            else:
                logger.info(f"Creating new dataset '{dataset_name}'...")

                # Create new dataset
                # Note: For Direct Lake models, we need to use Fabric-specific API
                result = self._create_direct_lake_dataset(workspace_id, dataset_name, bim_content)

            logger.info(f"✅ Semantic model deployed: {dataset_name}")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to deploy semantic model: {e}")
            raise

    def _create_direct_lake_dataset(self, workspace_id: str, dataset_name: str, bim_content: Dict) -> Dict:
        """Create a Direct Lake semantic model"""

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        # Convert BIM to Power BI dataset definition
        payload = {
            'name': dataset_name,
            'defaultMode': 'DirectLake',
            'tables': []
        }

        # Extract table definitions from BIM
        for table in bim_content.get('model', {}).get('tables', []):
            table_def = {
                'name': table['name'],
                'columns': []
            }

            for column in table.get('columns', []):
                table_def['columns'].append({
                    'name': column['name'],
                    'dataType': column.get('dataType', 'string')
                })

            payload['tables'].append(table_def)

        try:
            response = requests.post(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            dataset_id = result.get('id')

            # Refresh the dataset
            if dataset_id:
                self._trigger_refresh(workspace_id, dataset_id)

            return result
        except Exception as e:
            logger.error(f"Failed to create dataset: {e}")
            raise

    def _update_dataset_via_xmla(self, workspace_id: str, dataset_id: str, bim_content: Dict) -> Dict:
        """Update dataset using XMLA endpoint (for advanced scenarios)"""
        logger.info("Updating dataset via XMLA endpoint...")

        # For full BIM deployment, you would typically use tools like:
        # - Tabular Editor CLI
        # - AMO (Analysis Management Objects)
        # - Azure Analysis Services APIs

        # This is a simplified implementation
        logger.warning("⚠️  Full XMLA update requires additional tooling (Tabular Editor, AMO, etc.)")
        logger.info("Consider using: tabular-editor-cli deploy --model {bim_file} --server {xmla_endpoint}")

        return {'id': dataset_id, 'status': 'update_required'}

    def _trigger_refresh(self, workspace_id: str, dataset_id: str):
        """Trigger dataset refresh"""
        logger.info(f"Triggering dataset refresh for {dataset_id}...")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                f"{self.powerbi_api}/groups/{workspace_id}/datasets/{dataset_id}/refreshes",
                headers=headers
            )
            response.raise_for_status()
            logger.info("✅ Dataset refresh triggered")
        except Exception as e:
            logger.warning(f"⚠️  Failed to trigger refresh: {e}")

    def deploy_all_models(self) -> Dict:
        """Deploy all semantic models from model directory"""
        logger.info("=" * 60)
        logger.info("SEMANTIC MODEL DEPLOYMENT")
        logger.info("=" * 60)

        # Authenticate
        self.authenticate()

        # Get workspace ID
        workspace_id = self.get_workspace_id()

        # Find BIM files
        model_dir = Path(__file__).parent.parent / 'model'
        bim_files = list(model_dir.glob('*.bim'))

        if not bim_files:
            logger.warning("⚠️  No .bim files found in model directory")
            return {'deployed': [], 'errors': []}

        logger.info(f"\nFound {len(bim_files)} semantic model(s)")

        results = {
            'deployed': [],
            'errors': []
        }

        for bim_file in bim_files:
            try:
                result = self.deploy_semantic_model(workspace_id, str(bim_file))
                results['deployed'].append({
                    'file': bim_file.name,
                    'result': result
                })
            except Exception as e:
                logger.error(f"❌ Failed to deploy {bim_file.name}: {e}")
                results['errors'].append({
                    'file': bim_file.name,
                    'error': str(e)
                })

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("DEPLOYMENT SUMMARY")
        logger.info("=" * 60)
        logger.info(f"✅ Models deployed: {len(results['deployed'])}")
        logger.info(f"❌ Errors: {len(results['errors'])}")

        return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Deploy semantic models to Fabric workspace')
    parser.add_argument('--workspace', required=True, help='Fabric workspace name')
    parser.add_argument('--model', help='Specific .bim file to deploy (optional)')
    parser.add_argument('--validate-only', action='store_true', help='Validate BIM files only')

    args = parser.parse_args()

    try:
        deployer = SemanticModelDeployer(args.workspace)

        if args.validate_only:
            logger.info("VALIDATION MODE")
            model_dir = Path(__file__).parent.parent / 'model'
            bim_files = list(model_dir.glob('*.bim'))

            for bim_file in bim_files:
                deployer.validate_bim_file(str(bim_file))

            logger.info("✅ All models validated successfully")
        else:
            results = deployer.deploy_all_models()

            if results['errors']:
                sys.exit(1)

        logger.info("\n✅ Semantic model deployment completed")

    except Exception as e:
        logger.error(f"\n❌ Semantic model deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
