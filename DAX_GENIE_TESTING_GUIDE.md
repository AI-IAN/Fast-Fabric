# DAX Genie - Complete Testing & Validation Guide

## Overview

This guide provides step-by-step instructions to test and validate every component of the DAX Genie AI assistant.

---

## Part 1: Setup & Prerequisites

### 1.1 Check Prerequisites

```bash
# Navigate to the AI assistant directory
cd /home/user/Fast-Fabric/ai-assistant

# Check Python version (requires 3.11+)
python3 --version

# Verify required files exist
ls -la streamlit_app.py router.py requirements.txt
ls -la prompts/dax_genie/
```

### 1.2 Environment Configuration

Create a `.env` file from the template:

```bash
# Copy template
cp .env.template .env

# Edit with your API keys
# Option 1: Use nano/vim
nano .env

# Option 2: Export directly
export OPENAI_API_KEY="sk-your-key-here"
export LLM_OFFLINE=False
```

**Required Environment Variables:**
```env
# LLM Provider API Keys (at least ONE required)
OPENAI_API_KEY=sk-...                    # OpenAI GPT-4o-mini (RECOMMENDED)
ANTHROPIC_API_KEY=sk-ant-...             # Claude 3 Haiku (OPTIONAL)

# Operation Mode
LLM_OFFLINE=False                        # Set to True for offline testing

# Cost Tracking (OPTIONAL)
DAILY_BUDGET_USD=5.00
ALERT_THRESHOLD_USD=4.00

# Local Ollama (OPTIONAL - for on-premises)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2:7b
```

### 1.3 Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Expected packages:
# - streamlit>=1.29.0
# - plotly>=5.17.0
# - pandas>=2.1.4
# - openai>=1.6.1
# - anthropic>=0.8.1
# - pyyaml>=6.0
# - python-dotenv>=1.0.0
# - requests>=2.31.0
```

---

## Part 2: Component-Level Testing

### 2.1 Test Database Setup

**Test Script:**
```bash
python3 test_ai_modules.py
```

**Expected Output:**
```
🤖 Fabric Fast-Track AI Assistant - Test Suite
============================================================

📊 Testing Database Functionality:
✅ Database tables: ['llm_usage']
✅ Database records: 1

🧪 Testing AI Modules:
==================================================
✅ DAX_GENIE: -- Generated DAX measure...
✅ SOURCE_MAPPER: -- Generated source mapping...
✅ QA_BUDDY: -- Analyzed pipeline logs...
✅ RELEASE_SCRIBE: -- Generated release notes...

✅ All AI modules tested successfully!

📋 Test Summary:
==============================
Database Test: ✅ PASS
AI Modules Test: ✅ PASS

🎉 All tests passed! AI Assistant is ready for use.
```

**What This Tests:**
- ✅ SQLite database initialization
- ✅ Table creation (llm_usage)
- ✅ Record insertion/retrieval
- ✅ LLMRouter initialization
- ✅ Offline mode fallback
- ✅ All 4 AI modules respond

### 2.2 Test Database Manually

```bash
# Connect to SQLite database
sqlite3 cost_log.sqlite

# Inside SQLite shell:
.schema llm_usage
SELECT * FROM llm_usage LIMIT 5;
SELECT COUNT(*) FROM llm_usage;
.exit
```

**Expected Schema:**
```sql
CREATE TABLE llm_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    provider TEXT,
    model TEXT,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    cost_usd REAL,
    feature TEXT
);
```

### 2.3 Test LLM Router (Offline Mode)

Create a test script:

```bash
cat > test_router_offline.py << 'EOF'
import os
os.environ['LLM_OFFLINE'] = 'True'

from router import LLMRouter

router = LLMRouter()
response = router.route_request(
    "Generate DAX measure for total sales",
    "openai",
    "dax_genie"
)
print("OFFLINE RESPONSE:")
print(response)
print("\n✅ Offline mode works!")
EOF

python3 test_router_offline.py
```

**Expected Output:**
```
OFFLINE RESPONSE:
-- Generated DAX measure based on your requirements
Sample Measure = SUM(Table[Column])

✅ Offline mode works!
```

### 2.4 Test LLM Router (Online Mode with OpenAI)

```bash
cat > test_router_online.py << 'EOF'
import os
os.environ['LLM_OFFLINE'] = 'False'
# Make sure OPENAI_API_KEY is set

from router import LLMRouter

router = LLMRouter()
response = router.route_request(
    "Generate a simple DAX measure for total sales revenue",
    "openai",
    "dax_genie"
)
print("ONLINE RESPONSE FROM GPT-4o-mini:")
print(response)
print("\n✅ Online mode with OpenAI works!")
EOF

python3 test_router_online.py
```

**Expected Output:**
Should return a properly formatted DAX measure like:
```
**Measure Name:** Total Sales Revenue $
**Category:** Sales
**Complexity:** Simple

```dax
Total Sales Revenue $ = SUM(FactSales[SalesAmount])
```

**Format String:** "$#,##0.00"
...
✅ Online mode with OpenAI works!
```

### 2.5 Test Prompt System

```bash
# Verify all prompt files exist
ls -la prompts/dax_genie/

# Expected files:
# - system_prompt.md          (68 lines)
# - user_prompt_templates.md  (286 lines)
# - example_conversations.md  (505 lines)
# - prompt_dax_gen.md         (421 lines)

# Read system prompt
cat prompts/dax_genie/system_prompt.md | head -20

# Count example conversations
grep -c "Example [0-9]" prompts/dax_genie/example_conversations.md
# Expected: 8
```

---

## Part 3: Full Application Testing

### 3.1 Launch Streamlit Application

```bash
# Make sure you're in the ai-assistant directory
cd /home/user/Fast-Fabric/ai-assistant

# Launch Streamlit
streamlit run streamlit_app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.0.0.x:8501
```

### 3.2 Access Web Interface

Open your browser to: **http://localhost:8501**

**Expected UI Elements:**
```
┌─────────────────────────────────────────────────────┐
│  🚀 Fabric Fast-Track AI Assistant                  │
│  [Home] [DAX Genie] [Source Mapper] ...            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Select Template Type:                              │
│  ○ Basic Measure                                    │
│  ○ Time Intelligence                                │
│  ○ Financial Ratio                                  │
│  ○ Customer Analytics                               │
│  ○ Advanced Calculation                             │
│                                                     │
│  Business Requirement:                              │
│  ┌─────────────────────────────────────────────┐   │
│  │ [Text area to describe requirement]         │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Context:                                           │
│  [Primary Data Source] [Measure Category] [Format] │
│                                                     │
│  [✓] Include robust error handling                 │
│  [✓] Optimize for Direct Lake                      │
│  [✓] Include explanatory comments                  │
│                                                     │
│  [✨ Generate DAX Measure]                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3.3 Test Cases

#### Test Case 1: Basic Sales Measure

**Input:**
- Template Type: Basic Measure
- Business Requirement: "Calculate total sales revenue"
- Data Source: FactSales
- Category: Sales
- Format: Currency
- Complexity: Simple
- Click "Generate DAX Measure"

**Expected Output:**
```dax
Total Sales Revenue $ =
    SUM(FactSales[SalesAmount])
```

**Validation Checklist:**
- ✅ Measure name uses PascalCase with unit ($)
- ✅ Uses SUM aggregation (Direct Lake compatible)
- ✅ References FactSales table
- ✅ Format string is currency
- ✅ Response time < 15 seconds

#### Test Case 2: Time Intelligence (YoY Growth)

**Input:**
- Template Type: Time Intelligence
- Business Requirement: "Calculate year-over-year sales growth percentage"
- Data Source: FactSales
- Category: Sales
- Format: Percentage
- Complexity: Medium
- Enable error handling
- Click "Generate DAX Measure"

**Expected Output:**
```dax
Sales Growth YoY % =
VAR CurrentSales = [Total Sales $]
VAR PreviousYearSales =
    CALCULATE(
        [Total Sales $],
        SAMEPERIODLASTYEAR(DimDate[Date])
    )
RETURN
    IF(
        ISBLANK(PreviousYearSales),
        0,
        DIVIDE(CurrentSales - PreviousYearSales, PreviousYearSales)
    )
```

**Validation Checklist:**
- ✅ Uses VAR statements for efficiency
- ✅ Uses SAMEPERIODLASTYEAR (time intelligence)
- ✅ Uses DIVIDE() not division operator
- ✅ Handles null values with IF(ISBLANK())
- ✅ Format is percentage

#### Test Case 3: Financial Ratio

**Input:**
- Template Type: Financial Ratio
- Business Requirement: "Calculate gross profit margin as percentage of revenue"
- Data Source: FactFinancial
- Category: Financial
- Format: Percentage
- Complexity: Medium
- Enable error handling and Direct Lake optimization
- Click "Generate DAX Measure"

**Expected Output:**
```dax
Gross Profit Margin % =
DIVIDE(
    [Gross Profit $],
    [Total Revenue $],
    0
)
```

**Validation Checklist:**
- ✅ Uses DIVIDE() with default value (0)
- ✅ References base measures
- ✅ Lists dependencies
- ✅ Performance optimized

#### Test Case 4: Customer Analytics

**Input:**
- Template Type: Customer Analytics
- Business Requirement: "Count of active customers who purchased in last 90 days"
- Data Source: FactSales
- Category: Customer
- Format: Integer
- Complexity: Medium

**Expected Output:**
```dax
Active Customers Count =
CALCULATE(
    DISTINCTCOUNT(FactSales[CustomerID]),
    FactSales[TransactionDate] >= TODAY() - 90,
    DimCustomers[Status] = "Active"
)
```

**Validation Checklist:**
- ✅ Uses DISTINCTCOUNT for customer count
- ✅ Applies date filter (last 90 days)
- ✅ Filters by customer status
- ✅ Format is integer/number

#### Test Case 5: Advanced Calculation

**Input:**
- Template Type: Advanced Calculation
- Business Requirement: "Calculate top 10 products by sales with running total"
- Data Source: Combined Tables
- Category: Sales
- Format: Currency
- Complexity: Complex
- Performance Target: <2 seconds

**Expected Output:**
Should include TOPN, SUMX, or similar complex patterns with VAR statements.

**Validation Checklist:**
- ✅ Uses advanced DAX functions (TOPN/RANKX)
- ✅ Multiple VAR statements
- ✅ Performance optimized
- ✅ Error handling included

### 3.4 Test Download Functionality

After generating a measure:
1. Click "Download DAX Measure" button
2. Verify file downloads: `dax_measure_YYYYMMDD_HHMMSS.txt`
3. Open file and verify contents match displayed measure

### 3.5 Test Conversation History

1. Generate multiple measures
2. Check that each request is logged
3. Verify timestamp, module name, request, and response are saved

---

## Part 4: Cost Tracking Validation

### 4.1 Test Cost Logging

After generating measures, check the database:

```bash
sqlite3 cost_log.sqlite << EOF
SELECT
    timestamp,
    provider,
    model,
    prompt_tokens,
    completion_tokens,
    total_tokens,
    ROUND(cost_usd, 6) as cost_usd,
    feature
FROM llm_usage
WHERE feature = 'dax_genie'
ORDER BY timestamp DESC
LIMIT 10;
EOF
```

**Expected Output:**
```
2025-10-30T14:32:15|openai|gpt-4o-mini|2145|387|2532|0.001480|dax_genie
2025-10-30T14:28:42|openai|gpt-4o-mini|1892|425|2317|0.001539|dax_genie
...
```

### 4.2 Verify Cost Calculations

**OpenAI GPT-4o-mini Pricing (as of 2024):**
- Input: $0.00015 per 1K tokens
- Output: $0.0006 per 1K tokens

**Manual Calculation Example:**
```
Prompt tokens: 2145
Completion tokens: 387

Input cost:  2145 * 0.00015 / 1000 = $0.00032175
Output cost:  387 * 0.0006  / 1000 = $0.0002322
Total cost:                         = $0.00055395

Rounded: $0.000554
```

Compare with database value to verify accuracy.

### 4.3 Test Cost Tracking Dashboard

In Streamlit UI:
1. Navigate to "Cost Tracking" tab
2. Verify charts display:
   - Daily cost trends (line chart)
   - Cost by provider (pie chart)
   - Cost by feature (bar chart)
   - Usage log table (last 100 records)
3. Check budget alerts if configured

---

## Part 5: Performance & Load Testing

### 5.1 Response Time Test

```bash
cat > test_performance.py << 'EOF'
import time
import os
os.environ['LLM_OFFLINE'] = 'False'

from router import LLMRouter

router = LLMRouter()

# Test 5 requests
for i in range(5):
    start = time.time()
    response = router.route_request(
        f"Generate DAX measure for metric #{i}",
        "openai",
        "dax_genie"
    )
    elapsed = time.time() - start
    print(f"Request {i+1}: {elapsed:.2f} seconds")

print("\n✅ Performance test complete!")
EOF

python3 test_performance.py
```

**Expected Results:**
- Average response time: 3-15 seconds (depends on API latency)
- All requests should complete successfully

### 5.2 Concurrent Request Test

```bash
cat > test_concurrent.py << 'EOF'
import concurrent.futures
import time
import os
os.environ['LLM_OFFLINE'] = 'False'

from router import LLMRouter

def generate_measure(num):
    router = LLMRouter()
    start = time.time()
    response = router.route_request(
        f"Generate DAX measure #{num}",
        "openai",
        "dax_genie"
    )
    elapsed = time.time() - start
    return f"Request {num}: {elapsed:.2f}s"

# Run 3 concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(generate_measure, i) for i in range(3)]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

print("\n✅ Concurrent request test complete!")
EOF

python3 test_concurrent.py
```

**Expected Results:**
- All 3 requests complete successfully
- No database locking errors
- Each request logged separately

---

## Part 6: Integration Testing

### 6.1 Test with Real Business Scenarios

**Scenario 1: E-commerce Dashboard**
```
Requirement: "Calculate average order value for premium customers in Q4 2024"
Expected: Measure using AVERAGE, customer filter, date range
```

**Scenario 2: Financial Reporting**
```
Requirement: "Calculate EBITDA margin with proper error handling"
Expected: Complex financial ratio with DIVIDE and dependencies
```

**Scenario 3: Inventory Analytics**
```
Requirement: "Calculate days of inventory on hand"
Expected: Ratio of current inventory to average daily usage
```

### 6.2 Test Error Handling

**Test Invalid Inputs:**
1. Empty business requirement → Should show validation error
2. Extremely long requirement (>10,000 chars) → Should handle gracefully
3. Special characters in requirement → Should process correctly

**Test API Failures:**
```bash
# Temporarily set invalid API key
export OPENAI_API_KEY="invalid-key"

# Try to generate measure
# Expected: Falls back to offline mode with deterministic response
```

---

## Part 7: Docker Deployment Testing

### 7.1 Build Docker Image

```bash
cd /home/user/Fast-Fabric

# Build image
docker build -f ai-assistant/Dockerfile -t fast-fabric-ai:test .

# Verify image built successfully
docker images | grep fast-fabric-ai
```

**Expected Output:**
```
fast-fabric-ai   test   abc123def456   Just now   500MB
```

### 7.2 Run Container

```bash
# Run with environment variables
docker run -d \
  --name fast-fabric-test \
  -p 8501:8501 \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -e LLM_OFFLINE=False \
  -v $(pwd)/ai-assistant/cost_log.sqlite:/app/cost_log.sqlite \
  fast-fabric-ai:test

# Check container is running
docker ps | grep fast-fabric-test
```

### 7.3 Test Container Health

```bash
# Check health endpoint
curl -f http://localhost:8501/_stcore/health

# Expected: HTTP 200 OK

# View logs
docker logs fast-fabric-test

# Expected: Streamlit startup messages
```

### 7.4 Test Application in Container

1. Access http://localhost:8501
2. Run all test cases from Part 3
3. Verify functionality matches local deployment

### 7.5 Cleanup

```bash
# Stop container
docker stop fast-fabric-test

# Remove container
docker rm fast-fabric-test

# Remove image (optional)
docker rmi fast-fabric-ai:test
```

---

## Part 8: Validation Checklist

### 8.1 Functional Requirements

- [ ] Generates basic DAX measures (SUM, COUNT, AVERAGE)
- [ ] Generates time intelligence measures (YoY, MTD, QTD)
- [ ] Generates financial ratios with error handling
- [ ] Generates customer analytics measures
- [ ] Generates advanced calculations (TOPN, RANKX)
- [ ] Uses DIVIDE() for all divisions
- [ ] Handles null values appropriately
- [ ] Follows PascalCase naming with units
- [ ] Includes format strings
- [ ] Lists dependencies
- [ ] Provides performance notes
- [ ] Includes business context

### 8.2 Technical Requirements

- [ ] Works with OpenAI provider
- [ ] Works with Claude provider (if configured)
- [ ] Works with local Ollama (if configured)
- [ ] Offline mode functions correctly
- [ ] Database logging works
- [ ] Cost calculation is accurate
- [ ] Response time < 15 seconds
- [ ] Handles concurrent requests
- [ ] No database locking errors
- [ ] Download functionality works
- [ ] Conversation history saved

### 8.3 Direct Lake Optimization

- [ ] Uses supported aggregations (SUM, COUNT, MIN, MAX, AVG)
- [ ] Avoids complex iterators when possible
- [ ] Leverages relationships over complex filters
- [ ] Uses VAR statements for efficiency
- [ ] Target execution time <2 seconds on F2+

### 8.4 Error Handling

- [ ] DIVIDE() instead of division operator
- [ ] ISBLANK() checks for null values
- [ ] Default values for edge cases
- [ ] Data type validation
- [ ] Graceful API failure handling

### 8.5 User Experience

- [ ] UI loads without errors
- [ ] All template types available
- [ ] Context inputs work correctly
- [ ] Advanced options toggle properly
- [ ] Generated code syntax highlighted
- [ ] Download button functions
- [ ] Conversation history displays
- [ ] Cost dashboard shows data

### 8.6 Deployment

- [ ] Docker image builds successfully
- [ ] Container runs without errors
- [ ] Health check passes
- [ ] Port 8501 accessible
- [ ] Environment variables work
- [ ] Volume mounts persist data

---

## Part 9: Known Limitations & Troubleshooting

### 9.1 Known Limitations

1. **Response Time**: API calls take 5-15 seconds (network dependent)
2. **Token Limits**: Max 1000 completion tokens per request
3. **Offline Mode**: Returns deterministic samples, not real AI generation
4. **Data Model**: Examples assume specific tables (FactSales, FactFinancial)
5. **Cost Tracking**: Calculations based on 2024 pricing (may change)

### 9.2 Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'streamlit'"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: "No API key found"**
```bash
# Solution: Set environment variable
export OPENAI_API_KEY="your-key-here"
# OR create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

**Issue: "Database is locked"**
```bash
# Solution: Close all SQLite connections
# Restart Streamlit app
```

**Issue: "Streamlit not accessible"**
```bash
# Check if port 8501 is in use
lsof -i :8501

# Kill existing process
kill -9 <PID>

# Restart Streamlit
streamlit run streamlit_app.py
```

**Issue: Docker container not starting**
```bash
# Check logs
docker logs fast-fabric-test

# Verify environment variables
docker inspect fast-fabric-test | grep -A 10 Env

# Check health
docker exec fast-fabric-test curl http://localhost:8501/_stcore/health
```

---

## Part 10: Next Steps & Advanced Testing

### 10.1 Custom Data Model Testing

1. Modify `system_prompt.md` with your actual table schema
2. Test with real business requirements
3. Validate generated measures in Power BI Desktop

### 10.2 Power BI Integration

```python
# Use power_bi_integration.py to:
# - Export measures to .pbit template
# - Validate measures in semantic model
# - Test Direct Lake compatibility
```

### 10.3 Performance Benchmarking

1. Generate 100 measures
2. Track average response time
3. Calculate total cost
4. Measure token efficiency (output tokens / input tokens ratio)

### 10.4 Custom Pattern Library

1. Add your organization's DAX patterns to `dax_library.json`
2. Update `example_conversations.md` with real examples
3. Test that AI learns from new examples

---

## Summary

This guide covers:

✅ **Setup**: Environment configuration and dependency installation
✅ **Component Testing**: Database, router, prompts, offline/online modes
✅ **Application Testing**: Full UI testing with 5 test cases
✅ **Cost Tracking**: Database validation and calculation verification
✅ **Performance**: Response time and concurrent request testing
✅ **Integration**: Real business scenarios and error handling
✅ **Deployment**: Docker build, run, and health checks
✅ **Validation**: Comprehensive 40+ item checklist

**Total Testing Time**: 2-4 hours for complete validation

**Recommended Testing Order**:
1. Part 1: Setup (15 min)
2. Part 2: Component tests (30 min)
3. Part 3: Application tests (45 min)
4. Part 4: Cost tracking (15 min)
5. Part 7: Docker deployment (30 min)
6. Part 8: Final validation checklist (15 min)

**Ready to start testing? Begin with Part 1!**
