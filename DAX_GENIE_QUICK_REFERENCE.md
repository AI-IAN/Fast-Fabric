# DAX Genie - Quick Reference Card

## 🚀 Quick Start (30 seconds)

```bash
cd /home/user/Fast-Fabric/ai-assistant
export OPENAI_API_KEY="sk-your-key-here"
streamlit run streamlit_app.py
# Open browser: http://localhost:8501
```

---

## 📁 Key Files

| File | Purpose | Location |
|------|---------|----------|
| `streamlit_app.py` | Web UI (919 lines) | Main entry point |
| `router.py` | LLM routing & cost tracking | Core logic |
| `system_prompt.md` | AI instructions | `prompts/dax_genie/` |
| `user_prompt_templates.md` | Input templates | `prompts/dax_genie/` |
| `example_conversations.md` | 8 examples | `prompts/dax_genie/` |
| `dax_library.json` | Pattern library | `model/` |
| `cost_log.sqlite` | Usage tracking database | Root directory |

---

## 🔧 Core Components

```
User → Streamlit UI → LLM Router → {OpenAI|Claude|Local|Offline} → DAX Output → SQLite Log
```

**Supported Providers:**
- **OpenAI** (gpt-4o-mini) - Default, $0.00015/1K input tokens
- **Claude** (claude-3-haiku) - Alternative
- **Local** (Ollama) - On-premises
- **Offline** - Testing/fallback

---

## 🎯 5 Template Types

1. **Basic Measure** - Simple aggregations (SUM, COUNT, AVERAGE)
2. **Time Intelligence** - YoY, MTD, QTD, rolling periods
3. **Financial Ratio** - Margins, growth rates, variance
4. **Customer Analytics** - Segmentation, lifetime value
5. **Advanced Calculation** - TOPN, RANKX, complex patterns

---

## 📊 Context Parameters

**Data Sources:**
- FactSales (transaction data)
- FactFinancial (financial statements)
- Combined Tables (multi-table calculations)

**Measure Categories:**
- Sales, Financial, Customer, Operational, Time Intelligence

**Output Formats:**
- Currency ($#,##0.00)
- Percentage (0.0%)
- Number (#,##0)
- Integer (0)
- Custom

**Complexity Levels:**
- Simple (basic aggregations)
- Medium (filters, time intelligence)
- Complex (advanced calculations, multiple variables)

---

## ✅ DAX Best Practices (Embedded in System)

1. **Use DIVIDE()** instead of division operator (/)
2. **Handle nulls** with ISBLANK(), IF(), or BLANK()
3. **PascalCase naming** with units (e.g., `Sales YoY %`)
4. **VAR statements** for intermediate calculations
5. **Direct Lake optimization** (SUM, COUNT, MIN, MAX, AVG)
6. **Performance target** <2 seconds on F2+ capacity
7. **Error protection** with default values
8. **Leverage relationships** over complex CALCULATE

---

## 🧪 Quick Tests

### Test 1: Offline Mode
```bash
cd ai-assistant
export LLM_OFFLINE=True
python3 test_ai_modules.py
```

### Test 2: Database Check
```bash
sqlite3 cost_log.sqlite "SELECT COUNT(*) FROM llm_usage;"
```

### Test 3: Launch UI
```bash
streamlit run streamlit_app.py
```

### Test 4: Docker Run
```bash
docker build -f ai-assistant/Dockerfile -t fast-fabric-ai .
docker run -p 8501:8501 -e OPENAI_API_KEY="$OPENAI_API_KEY" fast-fabric-ai
```

---

## 📈 Cost Tracking

**Database Query:**
```sql
SELECT
    feature,
    COUNT(*) as requests,
    SUM(total_tokens) as tokens,
    ROUND(SUM(cost_usd), 4) as total_cost
FROM llm_usage
WHERE feature = 'dax_genie'
GROUP BY feature;
```

**Expected Daily Costs** (typical usage):
- 10 requests/day × $0.001 = **$0.01/day**
- 50 requests/day × $0.001 = **$0.05/day**
- 200 requests/day × $0.001 = **$0.20/day**

---

## 🎨 Example Requests

### Example 1: Basic Sales
```
Template: Basic Measure
Requirement: Calculate total sales revenue
Result: Total Sales Revenue $ = SUM(FactSales[SalesAmount])
```

### Example 2: Time Intelligence
```
Template: Time Intelligence
Requirement: Year-over-year sales growth percentage
Result: Sales Growth YoY % = DIVIDE([Current] - [PY], [PY])
```

### Example 3: Financial Ratio
```
Template: Financial Ratio
Requirement: Gross profit margin percentage
Result: Gross Profit Margin % = DIVIDE([Gross Profit], [Revenue])
```

### Example 4: Customer Analytics
```
Template: Customer Analytics
Requirement: Active customers in last 90 days
Result: Active Customers = DISTINCTCOUNT(filtered by date & status)
```

### Example 5: Advanced Calculation
```
Template: Advanced Calculation
Requirement: Top 10 products by sales with running total
Result: Uses TOPN, SUMX with VAR statements
```

---

## 🔍 Response Format

Every generated measure includes:

```
**Measure Name:** [PascalCase with units]
**Category:** [Sales/Financial/Customer/Operational/Time Intelligence]
**Complexity:** [Simple/Medium/Complex]

```dax
[Measure Name] =
    [DAX expression]
```

**Format String:** [Currency/Percentage/Number]
**Description:** [Business purpose]
**Dependencies:** [Required base measures]
**Performance Notes:** [Optimization details]
**Business Context:** [When/how to use]
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No module 'streamlit' | `pip install -r requirements.txt` |
| No API key found | `export OPENAI_API_KEY="sk-..."` |
| Port 8501 in use | `lsof -i :8501` then `kill -9 <PID>` |
| Database locked | Close SQLite connections, restart app |
| Slow response | Check API connectivity, try offline mode |
| Docker won't start | Check logs: `docker logs <container>` |

---

## 📚 Documentation Map

**System Architecture:**
- See `DAX_GENIE_TESTING_GUIDE.md` for complete flow diagrams

**Prompt Engineering:**
- `prompts/dax_genie/system_prompt.md` - AI role definition
- `prompts/dax_genie/example_conversations.md` - 8 detailed examples
- `prompts/dax_genie/prompt_dax_gen.md` - Comprehensive guide

**Code References:**
- DAX Genie UI: `streamlit_app.py:207-345`
- LLM Routing: `router.py:40-58`
- OpenAI Call: `router.py:60-81`
- Cost Logging: `router.py:128-146`

---

## 🎯 Validation Checklist (Quick)

**Functional:**
- [ ] Generates basic measures
- [ ] Generates time intelligence
- [ ] Uses DIVIDE() for all divisions
- [ ] Handles null values
- [ ] Follows naming conventions

**Technical:**
- [ ] Works with OpenAI
- [ ] Offline mode works
- [ ] Database logging works
- [ ] Cost calculation accurate
- [ ] Response time <15s

**Direct Lake:**
- [ ] Uses SUM/COUNT/MIN/MAX/AVG
- [ ] Uses VAR statements
- [ ] Target <2s execution

---

## 🚢 Deployment Options

### Local Development
```bash
streamlit run streamlit_app.py
```

### Docker Container
```bash
docker build -f ai-assistant/Dockerfile -t fast-fabric-ai .
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -v $(pwd)/cost_log.sqlite:/app/cost_log.sqlite \
  fast-fabric-ai
```

### Production (with docker-compose)
```yaml
services:
  ai-assistant:
    build:
      context: .
      dockerfile: ai-assistant/Dockerfile
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LLM_OFFLINE=False
    volumes:
      - ./ai-assistant/cost_log.sqlite:/app/cost_log.sqlite
    restart: unless-stopped
```

---

## 📞 Support & Resources

**Testing Guide:**
- `/home/user/Fast-Fabric/DAX_GENIE_TESTING_GUIDE.md`

**GitHub Issues:**
- https://github.com/AI-IAN/Fast-Fabric/issues

**OpenAI Pricing:**
- https://openai.com/api/pricing/

**Direct Lake Documentation:**
- https://learn.microsoft.com/fabric/

---

## 💡 Pro Tips

1. **Start with Basic templates** before moving to Advanced
2. **Enable error handling** for production measures
3. **Always optimize for Direct Lake** (checkbox enabled)
4. **Use the download button** to save generated measures
5. **Check conversation history** to reference previous measures
6. **Monitor costs** via the Cost Tracking dashboard
7. **Test in offline mode** before deploying with real API keys
8. **Customize system_prompt.md** for your specific data model

---

## 📊 Performance Expectations

| Metric | Expected Value |
|--------|----------------|
| Response Time | 5-15 seconds |
| Generated DAX Execution | <2 seconds (F2+) |
| Concurrent Users | 10+ supported |
| Database Operations | <100ms |
| API Cost per Request | $0.001-$0.002 |
| Token Efficiency | 60-70% |

---

## 🔐 Security Notes

**API Keys:**
- Never commit `.env` file to git
- Use environment variables in production
- Rotate keys regularly

**Database:**
- SQLite suitable for <100 concurrent users
- Consider PostgreSQL for high-volume production
- Back up cost_log.sqlite regularly

**Docker:**
- Use secrets management for API keys
- Don't expose port 8501 publicly without auth
- Run health checks in production

---

## 📖 Additional Reading

**DAX Patterns:**
- https://www.daxpatterns.com/

**Direct Lake Best Practices:**
- Microsoft Fabric documentation

**Prompt Engineering:**
- See `example_conversations.md` for real examples

**Cost Optimization:**
- Use offline mode for development
- Cache frequently used measures
- Monitor daily budget alerts

---

**Version:** 1.0
**Last Updated:** 2025-10-30
**Maintainer:** AI-IAN/Fast-Fabric Team

**Ready to use DAX Genie? Start with the Quick Start section above!**
