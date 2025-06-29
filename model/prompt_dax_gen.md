# DAX Generation Prompt Guide for Fabric Fast-Track

## Overview
This guide provides AI-assisted DAX measure generation prompts for creating professional, optimized measures in the Fabric Fast-Track semantic model. All prompts are designed for Direct Lake compatibility at F2+ capacity.

## Core Prompt Templates

### 1. Basic Measure Generation

**Prompt Template:**
```
Generate a DAX measure for [BUSINESS REQUIREMENT] using the Fabric Fast-Track semantic model.

Context:
- Tables: FactSales, FactFinancial, DimCustomers, DimDate
- Mode: Direct Lake (F2+ optimized)
- Format: [CURRENCY/PERCENTAGE/NUMBER]
- Business Logic: [SPECIFIC CALCULATION LOGIC]

Requirements:
- Use composable patterns from dax_library.json
- Include proper error handling with DIVIDE()
- Add descriptive measure name and formatting
- Optimize for Direct Lake performance
- Follow naming conventions (Pascal Case)

Example Input:
Business Requirement: Calculate monthly sales growth rate
Expected Output: DAX measure with proper time intelligence
```

### 2. Time Intelligence Measures

**Prompt Template:**
```
Create a time intelligence DAX measure for [TIME PERIOD COMPARISON].

Specifications:
- Base Measure: [EXISTING_MEASURE_NAME]
- Time Comparison: [YTD/MTD/QTD/Previous Year/Rolling N periods]
- Date Table: DimDate[Date]
- Handle fiscal year if applicable (July start)

Requirements:
- Use TOTALYTD, SAMEPERIODLASTYEAR, or similar functions
- Include null handling for incomplete periods
- Maintain performance for F2+ capacity
- Follow Fabric Fast-Track naming patterns

Example:
Input: "Sales growth compared to last year"
Output: Optimized DAX with year-over-year calculation
```

### 3. Financial Ratio Measures

**Prompt Template:**
```
Generate a financial ratio DAX measure for [FINANCIAL_METRIC].

Financial Context:
- Numerator: [DESCRIPTION]
- Denominator: [DESCRIPTION]
- Business Rules: [SPECIAL CONDITIONS]
- Expected Range: [TYPICAL VALUES]

Technical Requirements:
- Use FactFinancial table with Account filtering
- Handle zero/null denominators properly
- Format as percentage or decimal as appropriate
- Include variance handling if applicable
- Optimize for Direct Lake mode

Example:
Input: "Gross margin percentage"
Output: Ratio measure with proper formatting and error handling
```

### 4. Customer Analytics Measures

**Prompt Template:**
```
Create a customer analytics DAX measure for [CUSTOMER_METRIC].

Customer Data Context:
- Fact Table: FactSales
- Dimension: DimCustomers
- Active Filter: DimCustomers[IsActive] = TRUE
- Business Logic: [SEGMENTATION/CALCULATION RULES]

Requirements:
- Use DISTINCTCOUNT for customer counting
- Apply proper customer filters
- Handle customer segmentation if needed
- Consider relationship performance
- Include descriptive formatting

Example:
Input: "Average revenue per active customer by region"
Output: Customer measure with regional context
```

### 5. Advanced Aggregation Measures

**Prompt Template:**
```
Develop an advanced DAX measure for [COMPLEX_CALCULATION].

Complexity Requirements:
- Use VAR statements for intermediate calculations
- Include multiple table references if needed
- Handle complex business logic: [DESCRIPTION]
- Performance target: <2 seconds on F2 capacity
- Error scenarios: [NULL/ZERO HANDLING]

Optimization Guidelines:
- Minimize context transitions
- Use efficient filter patterns
- Leverage relationships over lookups
- Include performance comments in DAX

Example:
Input: "Top 10% customers contribution to total sales"
Output: Advanced measure with TOPN and SUMX functions
```

## Specialized Prompt Categories

### A. Sales Performance Measures

**Category Prompt:**
```
Generate sales performance DAX measures for [SALES_SCENARIO].

Available Metrics:
- Total Sales, Quantity, Average Deal Size
- Win Rate, Sales Velocity, Pipeline Value
- Regional/Channel Performance
- Sales Rep Rankings

Use FactSales table with relationships to:
- DimDate for time analysis
- DimCustomers for segmentation
- Built-in Status and Channel columns

Requirements:
- Direct Lake compatible aggregations
- Proper null handling
- Business-friendly formatting
- Include YoY comparisons where relevant
```

### B. Financial Health Measures

**Category Prompt:**
```
Create financial health DAX measures for [FINANCIAL_AREA].

Financial Categories:
- Revenue/Expense Analysis
- Profitability Ratios
- Cash Flow Indicators
- Balance Sheet Ratios
- Working Capital Metrics

Use FactFinancial with Account-based filtering:
- Revenue, Expenses, Assets, Liabilities
- Department-level analysis available
- Multi-currency considerations (USD default)

Requirements:
- GAAP/IFRS compliant calculations
- Period-over-period analysis
- Variance to budget (if applicable)
- Executive dashboard ready
```

### C. Operational Efficiency Measures

**Category Prompt:**
```
Develop operational efficiency DAX measures for [OPERATIONAL_AREA].

Operational Focus Areas:
- Process Performance (cycle times, throughput)
- Resource Utilization (employee productivity)
- Quality Metrics (error rates, satisfaction)
- Capacity Planning (forecasting, trends)

Data Sources:
- FactSales for transaction efficiency
- FactFinancial for cost analysis
- DimCustomers for service metrics

Requirements:
- Real-time monitoring capability
- Threshold-based alerting values
- Benchmark comparisons
- Trend analysis over time
```

## AI Assistant Integration Prompts

### 1. Source Mapper Integration

**Prompt for AI Assistant:**
```
Using the Fabric Fast-Track DAX library, generate measures for the following business requirements:

Input: [BUSINESS_REQUIREMENT_LIST]
Expected Output:
- Measure name following naming conventions
- Complete DAX expression
- Format string specification
- Dependencies on other measures
- Performance optimization notes
- Business description

Validate against:
- Direct Lake compatibility
- F2+ capacity performance
- dax_library.json patterns
- Error handling best practices
```

### 2. Quality Validation Prompt

**Quality Check Prompt:**
```
Review this DAX measure for Fabric Fast-Track compliance:

DAX Code: [PASTE_DAX_HERE]

Check for:
1. Direct Lake function compatibility
2. F2+ performance optimization
3. Proper error handling (DIVIDE, BLANK())
4. Naming convention adherence
5. Format string appropriateness
6. Business logic accuracy
7. Relationship usage efficiency

Provide:
- Compliance score (1-10)
- Specific improvement recommendations
- Alternative implementations if needed
- Performance impact assessment
```

### 3. Measure Enhancement Prompt

**Enhancement Prompt:**
```
Enhance this existing DAX measure for better performance and functionality:

Current Measure: [EXISTING_DAX]
Enhancement Goals:
- [ ] Add time intelligence
- [ ] Include error handling
- [ ] Optimize for Direct Lake
- [ ] Add business context filters
- [ ] Improve readability with variables
- [ ] Add variance analysis

Output Requirements:
- Improved DAX expression
- Performance comparison notes
- Business value explanation
- Implementation recommendations
```

## Business Scenario Prompts

### Scenario 1: Executive Dashboard

**Executive Focus Prompt:**
```
Create executive-level DAX measures for C-suite dashboard:

KPIs Needed:
- Revenue Growth (YoY, QoQ)
- Profitability Trends
- Customer Acquisition/Retention
- Market Share Indicators
- Operational Efficiency Ratios

Characteristics:
- High-level aggregations
- Trend analysis focused
- Exception highlighting
- Benchmark comparisons
- Forecast integration ready

Format: Currency for financials, percentages for ratios, counts for volumes
```

### Scenario 2: Operational Dashboard

**Operations Focus Prompt:**
```
Develop operational DAX measures for department managers:

Operational Areas:
- Daily/Weekly performance tracking
- Resource utilization metrics
- Process efficiency indicators
- Quality and compliance measures
- Team productivity analysis

Characteristics:
- Granular time periods (daily/weekly)
- Department-level filtering
- Target vs. actual comparisons
- Drill-down capability
- Real-time refresh compatible

Format: Operational units, percentages, rates, counts
```

### Scenario 3: Financial Analysis

**Finance Focus Prompt:**
```
Generate financial analysis DAX measures for CFO reporting:

Financial Analysis:
- P&L variance analysis
- Cash flow projections
- Budget vs. actual tracking
- Financial ratio analysis
- Cost center performance

Characteristics:
- Account-level detail capability
- Multi-period comparisons
- Currency handling
- Allocation logic support
- Audit trail compatibility

Format: Financial statement ready, GAAP compliant
```

## Validation and Testing Prompts

### Performance Testing Prompt

```
Test this DAX measure for F2+ Direct Lake performance:

Measure: [DAX_EXPRESSION]

Testing Criteria:
- Execution time target: <2 seconds
- Memory usage: Minimal
- CPU efficiency: Optimized
- Concurrent user load: 50+ users
- Data volume: 1M+ rows

Provide:
- Performance assessment
- Bottleneck identification
- Optimization recommendations
- Alternative approaches
- Capacity planning notes
```

### Business Logic Validation Prompt

```
Validate business logic accuracy for this DAX measure:

Business Requirement: [DETAILED_REQUIREMENT]
DAX Implementation: [DAX_CODE]

Validation Points:
- Mathematical accuracy
- Business rule compliance
- Edge case handling
- Data relationship correctness
- Filter context appropriateness

Output:
- Logic verification (Pass/Fail)
- Test case recommendations
- Business user validation steps
- Documentation requirements
```

## Best Practices for Prompt Usage

### 1. Context Setting
- Always provide table structure context
- Specify Direct Lake mode and F2+ capacity
- Include business domain (finance, sales, operations)
- Define data volume and performance expectations

### 2. Requirements Specification
- Clear business logic description
- Expected output format and precision
- Error handling requirements
- Performance constraints
- Integration needs with existing measures

### 3. Quality Assurance
- Request validation steps
- Include test scenarios
- Specify documentation needs
- Ask for performance optimization notes
- Require business user review points

### 4. Iterative Improvement
- Use feedback loops for measure refinement
- Version control measure changes
- Document performance impact
- Maintain backward compatibility
- Plan for scale and growth

---

*Use these prompts with the Fabric Fast-Track AI Assistant for consistent, high-quality DAX measure generation that meets enterprise standards and Direct Lake optimization requirements.*
EOF < /dev/null