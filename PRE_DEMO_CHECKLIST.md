# Fast-Fabric Pre-Demo Evaluation Checklist

**Purpose**: Validate your Fast-Fabric deployment before client demonstrations

---

## ✅ Phase 1: Local Environment Testing (15 minutes)

### 1.1 AI Assistant Local Test
```bash
# Start AI Assistant locally
cd /path/to/Fast-Fabric
docker-compose up

# Access at http://localhost:8501
# ✅ Verify: Streamlit UI loads
# ✅ Verify: All 5 modules visible in sidebar
# ✅ Verify: Dashboard shows usage analytics
```

**What to Check:**
- [ ] Streamlit UI loads without errors
- [ ] All 5 AI modules are accessible
- [ ] Cost tracking database initializes
- [ ] No Python import errors in logs

### 1.2 Deployment Scripts Validation
```bash
# Run tests to validate all scripts
cd tests
./run_all_tests.sh

# Expected: 15/15 tests passing
```

**What to Check:**
- [ ] All 15 tests pass
- [ ] No authentication errors (simulation mode works)
- [ ] Mock data validation works
- [ ] Script imports are clean

### 1.3 Infrastructure Template Validation
```bash
# Validate Bicep template without deploying
cd infra
az deployment group validate \
  --resource-group "test-rg" \
  --template-file main.bicep \
  --parameters @parameters.dev.json \
  --subscription YOUR_SUBSCRIPTION_ID
```

**What to Check:**
- [ ] Template validates successfully
- [ ] No syntax errors
- [ ] All parameters are defined
- [ ] Resource dependencies are correct

---

## ✅ Phase 2: Azure Test Deployment (30-45 minutes)

### 2.1 Create Test Environment
```bash
# Create a dedicated test resource group
az group create \
  --name rg-fabric-demo \
  --location eastus

# Create Key Vault for secrets
az keyvault create \
  --name kv-fabric-demo-$(date +%s) \
  --resource-group rg-fabric-demo \
  --location eastus

# Store SQL password
az keyvault secret set \
  --vault-name YOUR_KV_NAME \
  --name sql-admin-password \
  --value "YourSecureDemo123!"
```

### 2.2 Deploy Infrastructure
```bash
cd infra

# Update parameters.dev.json with your details
# Then deploy
./deploy.sh \
  -e dev \
  -g rg-fabric-demo \
  -s YOUR_SUBSCRIPTION_ID

# Monitor deployment time (target: <15 minutes)
```

**What to Check:**
- [ ] Deployment completes in <20 minutes
- [ ] Fabric capacity is created
- [ ] Storage account with bronze/silver/gold containers exists
- [ ] SQL Server is created (private network)
- [ ] Key Vault contains secrets
- [ ] No deployment errors

### 2.3 Set Up Fabric Workspace
```bash
# Manual steps in Fabric portal:
# 1. Go to https://app.fabric.microsoft.com
# 2. Create a new workspace: "FastTrack-Demo-Workspace"
# 3. Assign to the deployed Fabric capacity
# 4. Note the workspace name for deployment scripts
```

**What to Check:**
- [ ] Workspace is created
- [ ] Workspace is assigned to your capacity
- [ ] You have admin access
- [ ] Can create items in workspace

### 2.4 Generate Mock Data
```bash
cd ingest

# Generate sample data for demo
python mock_data_generator.py

# Verify output
ls -lh mock_data/
# Should see: customers.csv, sales.csv, financial.csv, etc.
```

**What to Check:**
- [ ] Mock data files generated
- [ ] Files contain realistic data
- [ ] File sizes are reasonable
- [ ] CSV files are well-formed

### 2.5 Deploy Data Platform Components
```bash
# Set environment variables
export FABRIC_TENANT_ID="your-tenant-id"
export FABRIC_CLIENT_ID="your-app-id"
export FABRIC_CLIENT_SECRET="your-secret"

cd tools

# Deploy pipelines (optional - templates only)
python deploy_pipelines.py \
  --workspace "FastTrack-Demo-Workspace" \
  --validate-only

# Deploy semantic model
python deploy_semantic_model.py \
  --workspace "FastTrack-Demo-Workspace" \
  --validate-only

# Deploy reports
python deploy_reports.py \
  --workspace "FastTrack-Demo-Workspace" \
  --validate-only
```

**What to Check:**
- [ ] Authentication succeeds
- [ ] Workspace is found
- [ ] Validation passes
- [ ] No permission errors

---

## ✅ Phase 3: Quality Validation (15 minutes)

### 3.1 Run Data Quality Checks
```bash
cd governance

# Run in simulation mode for demo prep
python run_data_quality_checks.py

# Expected: All checks pass with simulated data
```

**What to Check:**
- [ ] All Bronze layer checks pass
- [ ] All Silver layer checks pass
- [ ] Results exported to /tmp/data_quality_summary.json
- [ ] JUnit XML created

### 3.2 Run Performance Tests
```bash
# Run performance tests (simulation mode)
python performance_tests.py \
  --workspace "FastTrack-Demo-Workspace" \
  --target-load-time 2000

# Note: Will use simulation if no actual data exists
```

**What to Check:**
- [ ] Script runs without errors
- [ ] Target times are configured
- [ ] Test framework is functional

### 3.3 Run Direct Lake Tests
```bash
# Run Direct Lake validation
python direct_lake_tests.py \
  --workspace "FastTrack-Demo-Workspace"
```

**What to Check:**
- [ ] Script initializes correctly
- [ ] Authentication works
- [ ] Test framework is ready

---

## ✅ Phase 4: AI Assistant Demo Prep (10 minutes)

### 4.1 Test AI Modules Locally

**Set API Keys:**
```bash
# Create .env file
cd ai-assistant
cp .env.template .env

# Edit .env and add:
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_OFFLINE=False
```

**Test Each Module:**
```bash
# Start Streamlit
streamlit run streamlit_app.py

# Test each module:
# 1. DAX Genie: Generate a simple sales measure
# 2. Source Mapper: Create a SQL source mapping
# 3. QA Buddy: Analyze sample log data
# 4. Release Scribe: Create release notes from sample git diff
# 5. Cost Tracking: Verify usage is logged
```

**What to Check:**
- [ ] All 4 AI modules respond
- [ ] API calls work (or offline mode activates)
- [ ] Cost tracking logs requests
- [ ] UI is responsive and professional
- [ ] No error messages

### 4.2 Prepare Demo Data

**Create Sample Scenarios:**
```bash
# Save these for live demo:

# 1. DAX Genie Example:
"Calculate year-over-year revenue growth percentage with error handling for Direct Lake"

# 2. Source Mapper Example:
"Map SQL Server database 'SalesDB' with tables: Customers, Orders, OrderItems to medallion architecture"

# 3. QA Buddy Example:
Paste sample error logs from docs/Gotchas.md

# 4. Release Scribe Example:
Use your actual git log from recent commits
```

---

## ✅ Phase 5: Demo Environment Checklist

### Visual Checks
- [ ] Clean browser with no extensions showing
- [ ] Font size is readable (zoom to 125-150%)
- [ ] Dark mode or light mode (consistent)
- [ ] Close unnecessary browser tabs
- [ ] Bookmark key URLs for quick access

### Technical Checks
- [ ] Stable internet connection
- [ ] Power adapter connected
- [ ] External monitor tested (if using)
- [ ] Screen sharing tested
- [ ] Audio tested (if virtual demo)

### Content Prepared
- [ ] PowerPoint/slides ready (if using)
- [ ] Code examples copied to clipboard
- [ ] Demo script printed/accessible
- [ ] Talking points memorized
- [ ] Questions & answers prepared

### Backup Plans
- [ ] Offline mode tested (if APIs fail)
- [ ] Screenshots of working features
- [ ] Pre-recorded demo video (optional)
- [ ] PDF export of key visuals

---

## ✅ Phase 6: Final Pre-Demo Verification (5 minutes)

### Quick Smoke Test (5 minutes before demo)
```bash
# 1. Check AI Assistant is running
curl http://localhost:8501/_stcore/health
# Expected: 200 OK

# 2. Verify cost tracking database
sqlite3 ai-assistant/cost_log.sqlite "SELECT COUNT(*) FROM llm_usage;"
# Expected: Some number (shows DB is working)

# 3. Quick template validation
cd infra && az deployment group validate --template-file main.bicep --parameters @parameters.dev.json --resource-group rg-fabric-demo
# Expected: Validation succeeded
```

### Mental Checklist
- [ ] I know my opening statement
- [ ] I can navigate to all demo components
- [ ] I have a backup plan if something fails
- [ ] I know how to handle technical questions
- [ ] I'm ready to show value, not just features

---

## 🎯 Success Criteria

Before proceeding to client demo, you should have:

### Technical Validation
- ✅ All 15 tests passing
- ✅ AI Assistant running locally without errors
- ✅ Infrastructure template validates successfully
- ✅ All 5 AI modules are functional
- ✅ Cost tracking is working

### Demo Readiness
- ✅ Demo script prepared and practiced
- ✅ Sample scenarios tested
- ✅ Backup plan in place
- ✅ Environment is clean and professional
- ✅ Timing is under control (15-20 min demo)

### Business Readiness
- ✅ Value proposition is clear
- ✅ ROI story is prepared
- ✅ Differentiation from competitors understood
- ✅ Pricing/engagement model defined
- ✅ Next steps process is clear

---

## ⚠️ Common Issues & Fixes

### Issue: "Tests failing"
**Fix:**
```bash
# Ensure environment variables are set
export FABRIC_TENANT_ID="test"
export FABRIC_CLIENT_ID="test"
export FABRIC_CLIENT_SECRET="test"
export WORKSPACE_NAME="test"

# Run again
cd tests && ./run_all_tests.sh
```

### Issue: "Streamlit won't start"
**Fix:**
```bash
# Reinstall dependencies
cd ai-assistant
pip install -r requirements.txt

# Try again
streamlit run streamlit_app.py
```

### Issue: "Authentication fails"
**Fix:**
```bash
# Verify Azure AD app registration
az ad app list --display-name "Your-App-Name"

# Check API permissions
# Should have: Microsoft Graph, Power BI Service APIs

# Regenerate client secret if needed
```

### Issue: "Infrastructure deployment fails"
**Fix:**
```bash
# Check subscription and resource group
az account show
az group show --name rg-fabric-demo

# Verify quota limits
az vm list-usage --location eastus --output table

# Check parameters file for typos
cat infra/parameters.dev.json | jq
```

---

## 📊 Evaluation Metrics

Track these during your test run:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Infrastructure deployment time | <15 min | ___ min | ⬜ |
| Test pass rate | 100% | ___% | ⬜ |
| AI module response time | <5 sec | ___ sec | ⬜ |
| Template validation | Success | ___ | ⬜ |
| Mock data generation | <1 min | ___ sec | ⬜ |

---

## 🚀 Ready to Demo?

Once you've completed this checklist:
1. ✅ Proceed to **DEMO_GUIDE.md** for client demonstration script
2. ✅ Review **CLIENT_POSITIONING.md** for value proposition
3. ✅ Practice demo 2-3 times
4. ✅ Schedule your client presentation

**You're ready to show the power of Fast-Fabric!** 🎉

---

*Generated: 2025-10-30*
*Estimated Completion Time: 1-2 hours*
*Prerequisites: Azure subscription, Power BI Premium/Fabric capacity*
