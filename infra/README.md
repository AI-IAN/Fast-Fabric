# Fabric Fast-Track Infrastructure

This directory contains the Infrastructure as Code (IaC) for deploying Microsoft Fabric workspaces and supporting resources.

## What Gets Deployed

### Core Fabric Components
- **Microsoft Fabric Capacity** - F2+ SKU for Direct Lake support
- **Data Lake Storage** - Medallion architecture (Bronze/Silver/Gold containers)
- **Key Vault** - Secure storage for connection strings and API keys

### Supporting Infrastructure  
- **SQL Database** - AI Assistant cost tracking and metadata
- **Container Instance** - AI Assistant Streamlit UI hosting
- **Log Analytics** - Monitoring and alerting
- **Application Insights** - AI Assistant telemetry

### Security & Governance
- **RBAC** - Role-based access control
- **Monitoring Alerts** - Capacity utilization tracking
- **Secret Management** - Key Vault integration

## Quick Start

### Prerequisites
- Azure CLI installed and logged in
- Contributor access to Azure subscription
- Bicep CLI (comes with Azure CLI)

### Deploy Development Environment
```bash
./deploy.sh -g rg-fabric-dev -s YOUR_SUBSCRIPTION_ID
```

### Deploy Production Environment
```bash
./deploy.sh -e prod -g rg-fabric-prod -s YOUR_SUBSCRIPTION_ID
```

### Validate Template Only
```bash
./deploy.sh -v -g rg-fabric-dev -s YOUR_SUBSCRIPTION_ID
```

## Environment Configuration

### Development (dev)
- **Fabric SKU**: F2 (minimum for Direct Lake)
- **Monitoring**: Enabled with 30-day retention
- **Cost**: ~$200-300/month

### Test (test)  
- **Fabric SKU**: F4 (better performance)
- **Monitoring**: Enabled with 60-day retention
- **Cost**: ~$400-500/month

### Production (prod)
- **Fabric SKU**: F8 (production workloads)
- **Monitoring**: Enabled with 90-day retention
- **Cost**: ~$800-1000/month

## Target Metrics

✅ **Deployment Time**: < 15 minutes  
✅ **Zero Manual Clicks**: Fully automated  
✅ **Multi-Environment**: Dev/Test/Prod support  
✅ **Cost Monitoring**: Built-in alerting  

## Files

- `main.bicep` - Primary infrastructure template
- `parameters.*.json` - Environment-specific configuration  
- `deploy.sh` - Automated deployment script
- `README.md` - This documentation

---
*Infrastructure designed for < 15 minute deployment with zero manual intervention*
