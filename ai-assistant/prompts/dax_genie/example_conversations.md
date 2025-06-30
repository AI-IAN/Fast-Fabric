# DAX Genie Example Conversations

## Example 1: Basic Sales Measure

**User Request:**
```
Generate a DAX measure for: Total Sales excluding returns

Context:
- Measure Type: SUM
- Data Source: FactSales
- Business Logic: Sum sales amount where IsReturn = FALSE
- Filters: None
- Format: Currency
```

**DAX Genie Response:**
```
**Measure Name:** Total Sales $
**Category:** Sales
**Complexity:** Simple

```dax
Total Sales $ = 
    CALCULATE(
        SUM(FactSales[SalesAmount]),
        FactSales[IsReturn] = FALSE
    )
```

**Format String:** "$#,##0"
**Description:** Total sales revenue excluding returned items. Uses CALCULATE with simple filter for Direct Lake optimization.
**Dependencies:** None
**Performance Notes:** Direct Lake compatible using SUM aggregation with simple boolean filter
**Business Context:** Use for revenue reporting and KPI dashboards where returns should be excluded
```

---

## Example 2: Time Intelligence Measure

**User Request:**
```
Create a time intelligence DAX measure for: Sales growth year over year

Specifications:
- Base Measure: Total Sales $
- Time Period: Previous Year comparison
- Comparison Type: Growth %
- Date Context: Calendar year
- Handle Blanks: Show 0% for periods with no prior year data
```

**DAX Genie Response:**
```
**Measure Name:** Sales Growth YoY %
**Category:** Time Intelligence
**Complexity:** Medium

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

**Format String:** "0.0%"
**Description:** Year-over-year sales growth percentage with proper handling of periods without prior year data
**Dependencies:** Total Sales $
**Performance Notes:** Uses VAR statements for efficiency and SAMEPERIODLASTYEAR for Direct Lake compatibility
**Business Context:** Essential for trend analysis and executive dashboards to track business growth
```

---

## Example 3: Financial Ratio Measure

**User Request:**
```
Generate a financial ratio DAX measure for: Gross Margin Percentage

Financial Details:
- Numerator: Revenue minus Cost of Goods Sold
- Denominator: Total Revenue
- Business Rules: Exclude one-time charges
- Industry Context: Retail industry, expect 20-40%
- Validation: Should never exceed 100%
```

**DAX Genie Response:**
```
**Measure Name:** Gross Margin %
**Category:** Financial
**Complexity:** Medium

```dax
Gross Margin % = 
VAR Revenue = 
    CALCULATE(
        SUM(FactFinancial[Amount]),
        FactFinancial[Account] = "Revenue",
        FactFinancial[IsOneTime] = FALSE
    )
VAR COGS = 
    CALCULATE(
        SUM(FactFinancial[Amount]),
        FactFinancial[Account] = "Cost of Goods Sold",
        FactFinancial[IsOneTime] = FALSE
    )
VAR GrossProfit = Revenue - COGS
RETURN
    IF(
        Revenue = 0,
        BLANK(),
        MIN(DIVIDE(GrossProfit, Revenue), 1)
    )
```

**Format String:** "0.0%"
**Description:** Gross margin percentage excluding one-time charges, capped at 100% for data quality
**Dependencies:** None (uses FactFinancial directly)
**Performance Notes:** Uses VAR for intermediate calculations and MIN function to enforce business rule ceiling
**Business Context:** Key profitability metric for retail operations, typically ranges 20-40% for healthy businesses
```

---

## Example 4: Customer Analytics Measure

**User Request:**
```
Create a customer analytics DAX measure for: Average Revenue Per Customer

Customer Context:
- Metric Focus: Customer Value
- Customer Filter: Active customers only (min 2 transactions)
- Time Frame: Last 12 months
- Calculation Method: Revenue divided by qualified customer count
- Business Rules: Must have at least 2 transactions to qualify as active
```

**DAX Genie Response:**
```
**Measure Name:** Avg Revenue Per Customer $
**Category:** Customer
**Complexity:** Medium

```dax
Avg Revenue Per Customer $ = 
VAR ActiveCustomers = 
    CALCULATE(
        DISTINCTCOUNT(FactSales[CustomerID]),
        FactSales[IsReturn] = FALSE,
        DimDate[Date] >= TODAY() - 365,
        HAVING(
            COUNTROWS(FactSales) >= 2
        )
    )
VAR TotalRevenue = 
    CALCULATE(
        SUM(FactSales[SalesAmount]),
        FactSales[IsReturn] = FALSE,
        DimDate[Date] >= TODAY() - 365
    )
RETURN
    DIVIDE(TotalRevenue, ActiveCustomers)
```

**Format String:** "$#,##0"
**Description:** Average revenue per active customer (minimum 2 transactions) over the last 12 months
**Dependencies:** None
**Performance Notes:** Uses HAVING clause for transaction count filter and relative date filtering for performance
**Business Context:** Key customer value metric for segmentation and lifecycle analysis
```

---

## Example 5: Advanced Calculation

**User Request:**
```
Develop an advanced DAX measure for: Top 10% Customers Revenue Contribution

Requirements:
- Complexity Level: Multi-step ranking and percentage calculation
- Performance Target: Under 2 seconds
- Business Logic: Rank customers by revenue, identify top 10%, calculate their % of total revenue
- Variables Needed: Customer revenue, total revenue, ranking threshold
- Error Handling: Handle minimum customer count scenarios
```

**DAX Genie Response:**
```
**Measure Name:** Top 10% Customer Revenue %
**Category:** Advanced
**Complexity:** Complex

```dax
Top 10% Customer Revenue % = 
VAR TotalRevenue = [Total Sales $]
VAR CustomerCount = DISTINCTCOUNT(FactSales[CustomerID])
VAR Top10Threshold = MAX(CEILING(CustomerCount * 0.1, 1), 1)
VAR CustomerRevenue = 
    ADDCOLUMNS(
        SUMMARIZE(FactSales, FactSales[CustomerID]),
        "CustomerRevenue", [Total Sales $]
    )
VAR Top10Customers = 
    TOPN(
        Top10Threshold,
        CustomerRevenue,
        [CustomerRevenue],
        DESC
    )
VAR Top10Revenue = 
    SUMX(Top10Customers, [CustomerRevenue])
RETURN
    IF(
        CustomerCount < 10,
        BLANK(),
        DIVIDE(Top10Revenue, TotalRevenue)
    )
```

**Format String:** "0.0%"
**Description:** Percentage of total revenue contributed by top 10% of customers by revenue, with minimum customer count validation
**Dependencies:** Total Sales $
**Performance Notes:** Uses SUMMARIZE and TOPN for efficient ranking, includes minimum threshold logic
**Business Context:** Pareto analysis for customer segmentation and account management prioritization
```

---

## Example 6: Operational Efficiency Measure

**User Request:**
```
Generate operational DAX measures for: Sales conversion rate by channel

Operational Context:
- Department: Sales
- Manager Level: Sales Director
- Frequency: Weekly monitoring
- Action Trigger: Below 15% conversion rate
- Drill-down: Channel, Region, Sales Rep levels

Process Context: Lead-to-opportunity-to-customer conversion tracking
```

**DAX Genie Response:**
```
**Measure Name:** Sales Conversion Rate %
**Category:** Operational
**Complexity:** Medium

```dax
Sales Conversion Rate % = 
VAR TotalLeads = 
    CALCULATE(
        DISTINCTCOUNT(FactSales[LeadID]),
        FactSales[Stage] IN {"Lead", "Qualified", "Opportunity", "Closed Won"}
    )
VAR ClosedWonLeads = 
    CALCULATE(
        DISTINCTCOUNT(FactSales[LeadID]),
        FactSales[Stage] = "Closed Won"
    )
RETURN
    DIVIDE(ClosedWonLeads, TotalLeads)
```

**Format String:** "0.0%"
**Description:** Conversion rate from initial lead to closed won opportunity, filterable by channel and region
**Dependencies:** None
**Performance Notes:** Uses IN operator for stage filtering and DISTINCTCOUNT for lead-level analysis
**Business Context:** Monitor weekly to identify underperforming channels (threshold: 15% minimum). Supports drill-down by Channel, Region, and Sales Rep.
```

---

## Example 7: Multi-Table Complex Calculation

**User Request:**
```
Create a comprehensive customer lifetime value measure that combines sales history, average deal size, and retention probability.

Requirements:
- Use both FactSales and FactFinancial tables
- Include customer segmentation logic
- Calculate monthly retention rate
- Project 24-month customer value
- Handle new customers appropriately
```

**DAX Genie Response:**
```
**Measure Name:** Customer Lifetime Value $
**Category:** Advanced
**Complexity:** Complex

```dax
Customer Lifetime Value $ = 
VAR MonthlyRevenue = 
    DIVIDE([Total Sales $], 12)
VAR CustomerTenure = 
    CALCULATE(
        DATEDIFF(
            MIN(FactSales[Date]),
            MAX(FactSales[Date]),
            MONTH
        ) + 1
    )
VAR RetentionRate = 
    IF(
        CustomerTenure >= 12,
        0.85,  -- Established customers
        IF(
            CustomerTenure >= 6,
            0.75,  -- Growing customers
            0.60   -- New customers
        )
    )
VAR MonthlyChurnRate = 1 - RetentionRate
VAR ProjectedMonths = 
    IF(
        MonthlyChurnRate > 0,
        MIN(1 / MonthlyChurnRate, 24),
        24
    )
RETURN
    MonthlyRevenue * ProjectedMonths * RetentionRate
```

**Format String:** "$#,##0"
**Description:** 24-month projected customer lifetime value based on monthly revenue, tenure, and segment-based retention rates
**Dependencies:** Total Sales $
**Performance Notes:** Uses conditional logic for segmentation and mathematical projection with performance caps
**Business Context:** Strategic customer value assessment for acquisition cost justification and account prioritization
```

---

## Example 8: Financial Variance Analysis

**User Request:**
```
Develop financial analysis DAX measures for: Budget vs Actual variance analysis

Financial Context:
- Statement Type: P&L variance analysis
- Analysis Purpose: Monthly variance tracking with YTD accumulation
- Accounting Standard: Management reporting
- Period Comparison: Budget vs Actual with forecast integration
- Materiality: Flag variances >5% or >$10K
```

**DAX Genie Response:**
```
**Measure Name:** Budget Variance $
**Category:** Financial
**Complexity:** Medium

```dax
Budget Variance $ = 
VAR ActualAmount = 
    CALCULATE(
        SUM(FactFinancial[Amount]),
        FactFinancial[AmountType] = "Actual"
    )
VAR BudgetAmount = 
    CALCULATE(
        SUM(FactFinancial[Amount]),
        FactFinancial[AmountType] = "Budget"
    )
RETURN
    ActualAmount - BudgetAmount
```

**Measure Name:** Budget Variance %
**Category:** Financial
**Complexity:** Medium

```dax
Budget Variance % = 
VAR VarianceAmount = [Budget Variance $]
VAR BudgetAmount = 
    CALCULATE(
        SUM(FactFinancial[Amount]),
        FactFinancial[AmountType] = "Budget"
    )
RETURN
    DIVIDE(VarianceAmount, BudgetAmount)
```

**Measure Name:** Variance Alert
**Category:** Financial
**Complexity:** Medium

```dax
Variance Alert = 
VAR AbsVariance = ABS([Budget Variance $])
VAR VariancePercent = ABS([Budget Variance %])
VAR MaterialityThreshold = 
    OR(
        AbsVariance >= 10000,
        VariancePercent >= 0.05
    )
RETURN
    IF(
        MaterialityThreshold,
        "⚠️ Material Variance",
        "✅ Within Range"
    )
```

**Format String:** 
- Budget Variance $: "$#,##0;($#,##0)"
- Budget Variance %: "0.0%;(0.0%)"
- Variance Alert: General

**Description:** Comprehensive budget variance analysis with materiality flagging for management reporting
**Dependencies:** Budget Variance $ (for % and Alert measures)
**Performance Notes:** Uses consistent filter patterns and conditional formatting for efficient calculation
**Business Context:** Monthly P&L variance review with automated flagging of material variances (>5% or >$10K)
```

---

## Troubleshooting Examples

### Common Error: Division by Zero

**User Request:**
```
My conversion rate measure is showing errors. Help fix this DAX:
Conversion Rate = SUM(FactSales[Won]) / SUM(FactSales[Total])
```

**DAX Genie Response:**
```
**Issue:** Division by zero when no sales data exists
**Solution:** Use DIVIDE function with proper error handling

**Measure Name:** Conversion Rate %
**Category:** Sales
**Complexity:** Simple

```dax
Conversion Rate % = 
    DIVIDE(
        SUM(FactSales[Won]),
        SUM(FactSales[Total]),
        0  -- Return 0% when no data
    )
```

**Improvement Notes:**
- DIVIDE function handles null denominators automatically
- Added default value of 0 for clear business meaning
- Consider using BLANK() instead of 0 if "no data" should appear blank
```

### Performance Optimization

**User Request:**
```
This measure is too slow on our F2 capacity:
Customer Count = CALCULATE(DISTINCTCOUNT(FactSales[CustomerID]), FactSales[Status] = "Active")
```

**DAX Genie Response:**
```
**Issue:** Table scan performance on large FactSales table
**Solution:** Optimize filter context and leverage relationships

**Measure Name:** Active Customer Count
**Category:** Customer
**Complexity:** Simple

```dax
Active Customer Count = 
    CALCULATE(
        DISTINCTCOUNT(FactSales[CustomerID]),
        DimCustomers[IsActive] = TRUE
    )
```

**Performance Improvements:**
- Filter on dimension table (DimCustomers) instead of fact table
- Leverages existing relationship for better performance
- Reduces scan volume by filtering smaller dimension table first
- Direct Lake optimized using DISTINCTCOUNT with relationship filter
```

---

*These examples demonstrate the DAX Genie's ability to generate production-ready measures with proper error handling, performance optimization, and business context.*