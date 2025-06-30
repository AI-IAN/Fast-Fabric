# DAX Genie User Prompt Templates

## Template Categories

### 1. Basic Measure Generation

```
Generate a DAX measure for: [BUSINESS_REQUIREMENT]

Context:
- Measure Type: [SUM/COUNT/AVERAGE/RATIO/PERCENTAGE]
- Data Source: [FactSales/FactFinancial/Combined]
- Business Logic: [Detailed calculation rules]
- Filters: [Any specific filter conditions]
- Format: [Currency/Percentage/Number/Integer]

Example:
"Generate a DAX measure for: Total quarterly sales excluding returns
- Measure Type: SUM
- Data Source: FactSales
- Business Logic: Sum sales amount where return flag is false
- Filters: Current quarter only
- Format: Currency"
```

### 2. Time Intelligence Measures

```
Create a time intelligence DAX measure for: [TIME_COMPARISON]

Specifications:
- Base Measure: [Existing measure name or calculation]
- Time Period: [YTD/MTD/QTD/Rolling/Previous Period]
- Comparison Type: [Growth %/Variance/Trend]
- Date Context: [Calendar/Fiscal year, specific period rules]
- Handle Blanks: [How to treat incomplete periods]

Example:
"Create a time intelligence DAX measure for: Sales growth year over year
- Base Measure: Total Sales
- Time Period: Previous Year comparison
- Comparison Type: Growth %
- Date Context: Calendar year
- Handle Blanks: Show 0% for new customers"
```

### 3. Financial Ratio Measures

```
Generate a financial ratio DAX measure for: [FINANCIAL_METRIC]

Financial Details:
- Numerator: [Description and calculation]
- Denominator: [Description and calculation]
- Business Rules: [Special conditions or exclusions]
- Industry Context: [Benchmarks or typical ranges]
- Validation: [Business logic validation rules]

Example:
"Generate a financial ratio DAX measure for: Gross Margin Percentage
- Numerator: Revenue minus Cost of Goods Sold
- Denominator: Total Revenue
- Business Rules: Exclude one-time charges
- Industry Context: Retail industry, expect 20-40%
- Validation: Should never exceed 100%"
```

### 4. Customer Analytics Measures

```
Create a customer analytics DAX measure for: [CUSTOMER_METRIC]

Customer Context:
- Metric Focus: [Acquisition/Retention/Value/Segmentation]
- Customer Filter: [Active/All/Specific segments]
- Time Frame: [Period for analysis]
- Calculation Method: [Count/Average/Sum/Ratio]
- Business Rules: [Customer qualification criteria]

Example:
"Create a customer analytics DAX measure for: Average Revenue Per Customer
- Metric Focus: Customer Value
- Customer Filter: Active customers only
- Time Frame: Last 12 months
- Calculation Method: Revenue divided by customer count
- Business Rules: Min 2 transactions to qualify as active"
```

### 5. Advanced Calculations

```
Develop an advanced DAX measure for: [COMPLEX_CALCULATION]

Requirements:
- Complexity Level: [Multiple tables/conditions/calculations]
- Performance Target: [Response time requirement]
- Business Logic: [Detailed step-by-step calculation]
- Variables Needed: [Intermediate calculations]
- Error Handling: [Specific scenarios to handle]

Example:
"Develop an advanced DAX measure for: Top 10% Customers Revenue Contribution
- Complexity Level: Multi-step ranking and percentage calculation
- Performance Target: Under 2 seconds
- Business Logic: Rank customers by revenue, sum top 10%, calculate % of total
- Variables Needed: Customer revenue, total revenue, ranking
- Error Handling: Handle ties in ranking, minimum customer count"
```

## Business Scenario Templates

### Executive Dashboard Measures

```
Generate executive-level DAX measures for: [KPI_CATEGORY]

Executive Requirements:
- Audience: [C-suite/Board/Senior Management]
- KPI Focus: [Growth/Profitability/Efficiency/Risk]
- Time Horizon: [Strategic/Tactical periods]
- Benchmark: [Industry/Historical/Target comparisons]
- Alert Thresholds: [When to highlight concerns]

Business Context: [Industry, company size, strategic priorities]
```

### Operational Dashboard Measures

```
Create operational DAX measures for: [OPERATIONAL_AREA]

Operational Context:
- Department: [Sales/Marketing/Finance/Operations/HR]
- Manager Level: [Director/Manager/Supervisor]
- Frequency: [Daily/Weekly/Monthly monitoring]
- Action Trigger: [Performance thresholds for action]
- Drill-down: [Required detail levels]

Process Context: [Specific business processes being measured]
```

### Financial Analysis Measures

```
Develop financial analysis DAX measures for: [FINANCIAL_ANALYSIS]

Financial Context:
- Statement Type: [P&L/Balance Sheet/Cash Flow]
- Analysis Purpose: [Variance/Trend/Ratio/Forecast]
- Accounting Standard: [GAAP/IFRS/Management reporting]
- Period Comparison: [Monthly/Quarterly/Annual]
- Materiality: [Significance thresholds]

Compliance: [Regulatory or audit requirements]
```

## Specialized Domain Templates

### Sales Performance

```
Generate sales performance DAX measures for: [SALES_SCENARIO]

Sales Context:
- Sales Process: [Lead/Opportunity/Deal/Customer lifecycle stage]
- Sales Team: [Individual/Team/Region/Channel performance]
- Product Focus: [Product line/Category/SKU level analysis]
- Time Dimension: [Sales cycle/Seasonal/Trend analysis]
- Performance Metric: [Revenue/Volume/Conversion/Efficiency]

Sales Strategy: [Growth/Retention/Penetration objectives]
```

### Marketing Analytics

```
Create marketing analytics DAX measures for: [MARKETING_METRIC]

Marketing Context:
- Campaign Type: [Digital/Traditional/Event/Content marketing]
- Funnel Stage: [Awareness/Interest/Conversion/Retention]
- Attribution: [First-touch/Last-touch/Multi-touch model]
- Channel: [Email/Social/Paid/Organic/Direct]
- ROI Focus: [Cost/Revenue/Lifetime value optimization]

Marketing Strategy: [Brand/Performance/Account-based marketing]
```

### Supply Chain Metrics

```
Develop supply chain DAX measures for: [SUPPLY_CHAIN_AREA]

Supply Chain Context:
- Process Area: [Procurement/Inventory/Logistics/Quality]
- Performance Dimension: [Cost/Speed/Quality/Flexibility]
- Stakeholder: [Supplier/Internal/Customer perspective]
- Time Sensitivity: [Real-time/Batch/Historical analysis]
- Risk Factor: [Disruption/Compliance/Efficiency risks]

Business Impact: [Cost reduction/Service improvement/Risk mitigation]
```

## Quality Validation Templates

### Performance Testing Request

```
Validate DAX measure performance for: [MEASURE_NAME]

Performance Context:
- Expected Data Volume: [Row counts, user concurrency]
- Response Time Target: [Specific SLA requirements]
- Capacity: [F2/F4/F8 Fabric capacity]
- Usage Pattern: [Dashboard refresh/Ad-hoc query/Scheduled report]
- Peak Load: [Maximum expected usage scenarios]

Testing Scope: [Development/Test/Production validation]
```

### Business Logic Validation

```
Verify business logic for DAX measure: [MEASURE_NAME]

Business Validation:
- Requirement Source: [Business user/Process documentation/Regulation]
- Calculation Method: [Manual calculation/System comparison/Industry standard]
- Edge Cases: [Known scenarios that need special handling]
- Stakeholder: [Who will validate the business accuracy]
- Test Data: [Specific data scenarios for validation]

Success Criteria: [How to determine if the logic is correct]
```

## Integration Templates

### Measure Dependencies

```
Create DAX measure with dependencies: [MEASURE_NAME]

Dependency Context:
- Base Measures: [List of existing measures to reference]
- Calculation Chain: [Order of calculation dependencies]
- Circular Reference Check: [Potential circular dependency risks]
- Performance Impact: [How dependencies affect performance]
- Maintenance: [Impact of changes to base measures]

Architecture: [How this fits into overall measure hierarchy]
```

### Multi-Model Integration

```
Develop cross-model DAX measure: [INTEGRATION_SCENARIO]

Integration Context:
- Source Models: [List of semantic models involved]
- Data Consistency: [How to handle model differences]
- Refresh Timing: [Synchronization requirements]
- Performance: [Cross-model query optimization]
- Governance: [Change management across models]

Technical Architecture: [How models connect and interact]
```

## Usage Instructions

1. **Select Template**: Choose the template that best matches your DAX requirement
2. **Fill Context**: Replace bracketed placeholders with specific details
3. **Add Details**: Include any additional business context or constraints
4. **Submit Request**: Send the completed prompt to DAX Genie
5. **Review Output**: Validate the generated DAX against your requirements
6. **Iterate**: Refine the prompt if the output needs adjustment

## Best Practices

- **Be Specific**: More context leads to better DAX measures
- **Include Examples**: Provide sample calculations or expected results
- **Set Constraints**: Specify performance, formatting, and business rule requirements
- **Validate Logic**: Always review generated measures against business requirements
- **Document Usage**: Keep track of generated measures for future reference

---

*Use these templates to get consistent, high-quality DAX measures from the DAX Genie AI assistant.*