#!/usr/bin/env python3
"""
Fabric Fast-Track Pipeline Deployment Script
Deploys data ingestion pipelines to Microsoft Fabric workspace
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, List
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FabricPipelineDeployer:
    """Deploy data pipelines to Microsoft Fabric workspace"""

    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name
        self.tenant_id = os.getenv('FABRIC_TENANT_ID')
        self.client_id = os.getenv('FABRIC_CLIENT_ID')
        self.client_secret = os.getenv('FABRIC_CLIENT_SECRET')
        self.api_base = "https://api.fabric.microsoft.com/v1"
        self.access_token = None

        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("Missing required environment variables: FABRIC_TENANT_ID, FABRIC_CLIENT_ID, FABRIC_CLIENT_SECRET")

    def authenticate(self) -> str:
        """Authenticate with Microsoft Fabric API"""
        logger.info("Authenticating with Microsoft Fabric API...")

        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://api.fabric.microsoft.com/.default',
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
                f"{self.api_base}/workspaces",
                headers=headers
            )
            response.raise_for_status()

            workspaces = response.json().get('value', [])
            for ws in workspaces:
                if ws['displayName'] == self.workspace_name:
                    workspace_id = ws['id']
                    logger.info(f"✅ Found workspace ID: {workspace_id}")
                    return workspace_id

            logger.error(f"❌ Workspace '{self.workspace_name}' not found")
            raise ValueError(f"Workspace '{self.workspace_name}' not found")
        except Exception as e:
            logger.error(f"❌ Failed to get workspace: {e}")
            raise

    def deploy_dataflow(self, workspace_id: str, dataflow_config: Dict) -> Dict:
        """Deploy a single dataflow to workspace"""
        dataflow_name = dataflow_config.get('name', 'Unnamed Dataflow')
        logger.info(f"Deploying dataflow: {dataflow_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            # Create dataflow
            response = requests.post(
                f"{self.api_base}/workspaces/{workspace_id}/dataflows",
                headers=headers,
                json=dataflow_config
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"✅ Deployed dataflow: {dataflow_name} (ID: {result.get('id', 'unknown')})")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to deploy dataflow '{dataflow_name}': {e}")
            return {'error': str(e), 'name': dataflow_name}

    def deploy_notebook(self, workspace_id: str, notebook_path: str) -> Dict:
        """Deploy a Spark notebook to workspace"""
        notebook_name = Path(notebook_path).stem
        logger.info(f"Deploying notebook: {notebook_name}")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        try:
            # Read notebook content
            with open(notebook_path, 'r') as f:
                notebook_content = f.read()

            payload = {
                'displayName': notebook_name,
                'definition': {
                    'format': 'ipynb',
                    'parts': [{
                        'path': f'{notebook_name}.ipynb',
                        'payload': notebook_content,
                        'payloadType': 'InlineBase64'
                    }]
                }
            }

            response = requests.post(
                f"{self.api_base}/workspaces/{workspace_id}/notebooks",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            result = response.json()
            logger.info(f"✅ Deployed notebook: {notebook_name}")
            return result
        except Exception as e:
            logger.error(f"❌ Failed to deploy notebook '{notebook_name}': {e}")
            return {'error': str(e), 'name': notebook_name}

    def deploy_all_pipelines(self) -> Dict:
        """Deploy all data pipelines from ingest directory"""
        logger.info("=" * 60)
        logger.info("FABRIC PIPELINE DEPLOYMENT")
        logger.info("=" * 60)

        # Authenticate
        self.authenticate()

        # Get workspace ID
        workspace_id = self.get_workspace_id()

        # Find pipeline configuration files
        ingest_dir = Path(__file__).parent.parent / 'ingest'
        results = {
            'dataflows': [],
            'notebooks': [],
            'errors': []
        }

        # Deploy dataflow templates
        dataflow_files = list(ingest_dir.glob('dataflow_*.json'))
        logger.info(f"\nFound {len(dataflow_files)} dataflow templates")

        for dataflow_file in dataflow_files:
            try:
                with open(dataflow_file, 'r') as f:
                    dataflow_config = json.load(f)
                result = self.deploy_dataflow(workspace_id, dataflow_config)

                if 'error' in result:
                    results['errors'].append(result)
                else:
                    results['dataflows'].append(result)
            except Exception as e:
                logger.error(f"❌ Failed to process {dataflow_file.name}: {e}")
                results['errors'].append({'file': dataflow_file.name, 'error': str(e)})

        # Deploy Spark notebooks
        notebook_files = list(ingest_dir.glob('*.py'))
        logger.info(f"\nFound {len(notebook_files)} notebook files")

        for notebook_file in notebook_files:
            result = self.deploy_notebook(workspace_id, str(notebook_file))

            if 'error' in result:
                results['errors'].append(result)
            else:
                results['notebooks'].append(result)

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("DEPLOYMENT SUMMARY")
        logger.info("=" * 60)
        logger.info(f"✅ Dataflows deployed: {len(results['dataflows'])}")
        logger.info(f"✅ Notebooks deployed: {len(results['notebooks'])}")
        logger.info(f"❌ Errors: {len(results['errors'])}")

        if results['errors']:
            logger.error("\nErrors encountered:")
            for error in results['errors']:
                logger.error(f"  - {error}")

        return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Deploy Fabric pipelines to workspace')
    parser.add_argument('--workspace', required=True, help='Fabric workspace name')
    parser.add_argument('--dry-run', action='store_true', help='Validate only, do not deploy')

    args = parser.parse_args()

    try:
        deployer = FabricPipelineDeployer(args.workspace)

        if args.dry_run:
            logger.info("DRY RUN MODE - Validation only")
            deployer.authenticate()
            deployer.get_workspace_id()
            logger.info("✅ Validation successful")
        else:
            results = deployer.deploy_all_pipelines()

            # Exit with error if any deployments failed
            if results['errors']:
                sys.exit(1)

        logger.info("\n✅ Pipeline deployment completed successfully")

    except Exception as e:
        logger.error(f"\n❌ Pipeline deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
