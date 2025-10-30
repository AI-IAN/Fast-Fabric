# Fast-Fabric 15-Minute Quick Start Test Run

**Purpose**: Get Fast-Fabric running locally in 15 minutes for immediate testing

---

## ⚡ Option 1: Ultra-Fast Local Test (5 minutes)

### Prerequisites
- Docker Desktop installed and running
- Git installed

### Steps

**1. Clone and Start (2 minutes)**
```bash
# Clone repository
git clone https://github.com/YOUR_ORG/Fast-Fabric.git
cd Fast-Fabric

# Start AI Assistant
docker-compose up -d

# Wait 30 seconds for startup
sleep 30
```

**2. Access AI Assistant (1 minute)**
```bash
# Open in browser
open http://localhost:8501

# Or visit manually:
# http://localhost:8501
```

**3. Test AI Modules (2 minutes)**

Navigate through each module in the sidebar:
- ✅ **Dashboard**: See overview and quick actions
- ✅ **DAX Genie**: Generate a sample DAX measure
- ✅ **Source Mapper**: Create a data source mapping
- ✅ **QA Buddy**: Analyze sample logs
- ✅ **Release Scribe**: Generate release notes
- ✅ **Cost Tracking**: View usage analytics

**You're done!** AI Assistant is running locally. ✅

---

## ⚡ Option 2: Full Test with Validation (15 minutes)

### Prerequisites
- Python 3.11+
- Azure CLI (optional for template validation)
- Docker Desktop

### Step 1: Environment Setup (3 minutes)

```bash
# Clone repo
git clone https://github.com/YOUR_ORG/Fast-Fabric.git
cd Fast-Fabric

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ai-assistant/requirements.txt
```

### Step 2: Run Tests (2 minutes)

```bash
# Run comprehensive test suite
cd tests
./run_all_tests.sh

# Expected output: 15/15 tests passing ✅
```

### Step 3: Start AI Assistant (2 minutes)

```bash
# Create environment file
cd ../ai-assistant
cp .env.template .env

# Edit .env - set to offline mode for quick test
echo "LLM_OFFLINE=True" >> .env
echo "OPENAI_API_KEY=test" >> .env
echo "ANTHROPIC_API_KEY=test" >> .env

# Start Streamlit
streamlit run streamlit_app.py

# Opens automatically in browser at http://localhost:8501
```

### Step 4: Test Core Features (5 minutes)

**Test 1: DAX Genie (1 minute)**
```
1. Click "📊 DAX Genie" in sidebar
2. Enter: "Calculate total sales"
3. Click "Generate DAX Measure"
4. ✅ Verify: DAX code appears (offline mode uses templates)
```

**Test 2: Source Mapper (1 minute)**
```
1. Click "🗺️ Source Mapper"
2. Select "SQL Database"
3. Enter database name: "DemoDB"
4. Click "Generate Source Mapping"
5. ✅ Verify: YAML configuration appears
```

**Test 3: Data Quality Check (1 minute)**
```bash
# In new terminal
cd governance
python run_data_quality_checks.py

# ✅ Verify: All checks pass (simulation mode)
```

**Test 4: Infrastructure Validation (2 minutes)**
```bash
# Validate Bicep template (requires Azure CLI)
cd ../infra

az deployment group validate \
  --resource-group "test-rg" \
  --template-file main.bicep \
  --parameters @parameters.dev.json \
  --no-prompt

# ✅ Verify: "provisioningState": "Succeeded"
```

### Step 5: Generate Mock Data (3 minutes)

```bash
# Generate realistic demo data
cd ../ingest
python mock_data_generator.py

# Check output
ls -lh mock_data/

# ✅ Verify files created:
# - customers.csv (1000 records)
# - sales.csv (5000 records)
# - financial.csv (multiple records)
# - api_customers_response.json
# - api_sales_response.json
```

**You're done!** Full environment tested. ✅

---

## ⚡ Option 3: Azure Quick Deploy (30-45 minutes)

### Prerequisites
- Azure subscription
- Azure CLI installed and authenticated
- Contributor access to subscription

### Step 1: Authenticate to Azure (1 minute)

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Verify
az account show
```

### Step 2: Create Resources (2 minutes)

```bash
# Create resource group
az group create \
  --name rg-fabric-quickstart \
  --location eastus

# Create Key Vault
KV_NAME="kv-fabric-$(date +%s)"
az keyvault create \
  --name $KV_NAME \
  --resource-group rg-fabric-quickstart \
  --location eastus

# Store SQL password
az keyvault secret set \
  --vault-name $KV_NAME \
  --name sql-admin-password \
  --value "QuickTest123!"
```

### Step 3: Update Parameters (2 minutes)

```bash
cd infra

# Edit parameters.dev.json
# Update the KeyVault reference with your KV name
cat > parameters.dev.json <<EOF
{
  "\$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environment": {"value": "dev"},
    "orgPrefix": {"value": "fft"},
    "fabricCapacitySku": {"value": "F2"},
    "fabricAdmins": {"value": "your-email@company.com"},
    "enableMonitoring": {"value": true},
    "logRetentionDays": {"value": 30},
    "sqlAdminPassword": {"value": "QuickTest123!"},
    "sqlAllowedIpAddresses": {"value": ""}
  }
}
EOF
```

### Step 4: Deploy Infrastructure (15-20 minutes)

```bash
# Run deployment
./deploy.sh \
  -e dev \
  -g rg-fabric-quickstart \
  -s YOUR_SUBSCRIPTION_ID

# Monitor progress
# Expected: 10-20 minutes deployment time
```

### Step 5: Verify Deployment (5 minutes)

```bash
# Check resources created
az resource list \
  --resource-group rg-fabric-quickstart \
  --output table

# Expected resources:
# - Fabric Capacity
# - Storage Account (with bronze/silver/gold containers)
# - SQL Server + Database
# - Key Vault
# - Log Analytics Workspace
# - Application Insights
# - Container Instance (AI Assistant)
```

### Step 6: Set Up Fabric Workspace (5 minutes)

```bash
# Manual steps:
# 1. Go to https://app.fabric.microsoft.com
# 2. Click "Workspaces" → "New workspace"
# 3. Name: "FastTrack-QuickStart"
# 4. Click "Advanced" → Assign to your deployed capacity
# 5. Click "Apply"

# Note workspace name for next steps
```

### Step 7: Test Deployment (5 minutes)

```bash
# Set environment variables
export FABRIC_TENANT_ID=$(az account show --query tenantId -o tsv)
export FABRIC_CLIENT_ID="YOUR_APP_CLIENT_ID"
export FABRIC_CLIENT_SECRET="YOUR_APP_SECRET"

# Test workspace access
cd ../tools
python deploy_pipelines.py \
  --workspace "FastTrack-QuickStart" \
  --dry-run

# ✅ Verify: Authentication succeeds, workspace found
```

**You're deployed to Azure!** ✅

---

## 🎯 Quick Test Validation Matrix

After running any option above, verify these work:

| Component | Test | Expected Result | Status |
|-----------|------|-----------------|--------|
| **AI Assistant** | Open http://localhost:8501 | Dashboard loads | ⬜ |
| **DAX Genie** | Generate sample measure | DAX code returned | ⬜ |
| **Source Mapper** | Create SQL mapping | YAML config returned | ⬜ |
| **QA Buddy** | Analyze sample logs | Analysis returned | ⬜ |
| **Release Scribe** | Generate notes | Markdown returned | ⬜ |
| **Cost Tracking** | View dashboard | Metrics displayed | ⬜ |
| **Tests** | Run test suite | 15/15 passing | ⬜ |
| **Mock Data** | Generate data | CSV files created | ⬜ |
| **Template** | Validate Bicep | No errors | ⬜ |

---

## 🔧 Troubleshooting

### AI Assistant won't start
```bash
# Check Docker is running
docker ps

# Restart Docker Desktop
# Then try again:
docker-compose down
docker-compose up -d
```

### Tests failing
```bash
# Ensure environment variables set
export FABRIC_TENANT_ID=test
export FABRIC_CLIENT_ID=test
export FABRIC_CLIENT_SECRET=test
export WORKSPACE_NAME=test

# Run again
cd tests && ./run_all_tests.sh
```

### Python dependencies issue
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall requirements
pip install -r ai-assistant/requirements.txt --force-reinstall
```

### Azure deployment fails
```bash
# Check quotas
az vm list-usage --location eastus --output table

# Verify permissions
az role assignment list --assignee YOUR_USER_EMAIL --output table

# Should see: "Contributor" or "Owner"
```

### Port 8501 already in use
```bash
# Kill existing Streamlit
pkill -f streamlit

# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

---

## 📊 Performance Benchmarks

Expected timings for each option:

| Option | Total Time | Complexity | Requirements |
|--------|------------|------------|--------------|
| **Option 1: Local Only** | 5 minutes | ⭐ Easy | Docker |
| **Option 2: Full Test** | 15 minutes | ⭐⭐ Moderate | Python, Docker |
| **Option 3: Azure Deploy** | 30-45 minutes | ⭐⭐⭐ Advanced | Azure subscription |

---

## ✅ Success Criteria

You've successfully completed the quick start when:

### Option 1 Success:
- ✅ AI Assistant UI loads at http://localhost:8501
- ✅ Can navigate all 5 modules
- ✅ No errors in Docker logs

### Option 2 Success:
- ✅ All 15 tests passing
- ✅ AI Assistant running locally
- ✅ Mock data generated
- ✅ Infrastructure template validates

### Option 3 Success:
- ✅ All Azure resources deployed
- ✅ Fabric workspace created
- ✅ Can authenticate to workspace
- ✅ Deployment scripts validate successfully

---

## 🚀 Next Steps

After successful quick start:

1. **Review**: Check `PRE_DEMO_CHECKLIST.md` for comprehensive validation
2. **Practice**: Use `DEMO_GUIDE.md` for client demonstration script
3. **Position**: Read `CLIENT_POSITIONING.md` for value proposition
4. **Deploy**: Follow full deployment guide for production

**You're ready to explore Fast-Fabric!** 🎉

---

*Estimated Time: 5-45 minutes depending on option*
*Difficulty: Easy to Advanced*
*Prerequisites: Minimal to Azure subscription*
