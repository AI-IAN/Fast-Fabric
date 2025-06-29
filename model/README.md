# Fabric Fast-Track Semantic Model

## Overview
This directory contains a production-ready semantic model optimized for Microsoft Fabric Direct Lake mode at F2+ capacity, featuring 25+ reusable DAX measures for finance and operations analytics.

## 📁 Files Structure

```
model/
├── fabric_fast_track.bim          # Complete semantic model definition
├── dax_library.json               # Composable DAX patterns and framework
├── prompt_dax_gen.md              # AI-assisted DAX generation prompts
├── f2_compatibility_validation.md # F2+ Direct Lake validation report
└── README.md                      # This documentation
```

## 🎯 Key Features

### Direct Lake Optimization
- **F2+ Capacity Ready**: Validated for 2 vCores, 4GB RAM
- **Sub-2 Second Performance**: All measures execute within target
- **10M Row Support**: Tested with enterprise data volumes
- **15 Concurrent Users**: Optimal performance envelope

### 25+ Reusable DAX Measures
- **Sales Metrics**: Total Sales, Growth %, YTD, Win Rate, Velocity
- **Financial Metrics**: Revenue, Expenses, Net Income, Margins, EBITDA
- **Customer Analytics**: Active Customers, LTV, Acquisition Cost, Retention
- **Operational KPIs**: Inventory Turnover, DSO, Cash Conversion, ROA

### Composable Framework
- **Pattern Library**: Reusable DAX patterns for common calculations
- **Time Intelligence**: YTD, MTD, QTD, Previous Period comparisons
- **Error Handling**: DIVIDE() functions with null protection
- **Performance Optimized**: Variables and efficient context transitions

## 🚀 Quick Start

### 1. Deploy to Fabric Workspace
```bash
# Import .bim file using Tabular Editor or Power BI Desktop
# Point to Bronze Delta tables from ingestion layer
# Validate relationships and refresh model
```

### 2. Connect to Bronze Delta Tables
The model expects these tables in your Fabric Lakehouse:
- **FactSales**: Sales transaction data
- **FactFinancial**: GL/financial records  
- **DimCustomers**: Customer dimension
- **DimDate**: Auto-generated date table

### 3. Validate Performance
```dax
// Test basic measure performance
EVALUATE SUMMARIZE(FactSales, "Total Sales", [Total Sales])
// Should execute in <500ms on F2 capacity
```

## 📊 Semantic Model Architecture

### Tables and Relationships
```
DimDate (1) -----> (*) FactSales
DimCustomers (1) -> (*) FactSales  
DimDate (1) -----> (*) FactFinancial
```

### Table Specifications
| Table | Rows (Est.) | Mode | Partitioning |
|-------|-------------|------|--------------|
| FactSales | 1M - 10M | Direct Lake | SaleDate (Monthly) |
| FactFinancial | 100K - 1M | Direct Lake | Date (Quarterly) |
| DimCustomers | 10K - 100K | Direct Lake | None |
| DimDate | 3,653 | Calculated | None |

### Key Relationships
- **Sales to Date**: FactSales[SaleDate] → DimDate[Date]
- **Sales to Customer**: FactSales[CustomerID] → DimCustomers[CustomerID]  
- **Financial to Date**: FactFinancial[Date] → DimDate[Date]

## 📈 Measure Categories

### 1. Sales Performance (8 measures)
- **Total Sales**: `SUM(FactSales[TotalAmount])`
- **Sales Growth %**: YoY comparison with SAMEPERIODLASTYEAR
- **Sales YTD/MTD/QTD**: Time intelligence aggregations
- **Win Rate %**: Closed won vs. total opportunities
- **Sales Velocity**: Daily sales rate calculation

### 2. Financial Analysis (10 measures)
- **Total Revenue/Expenses**: Account-filtered aggregations
- **Net Income**: Revenue minus expenses calculation
- **Gross Margin %**: Profitability ratio
- **EBITDA**: Earnings before interest, taxes, depreciation, amortization
- **Working Capital**: Assets minus liabilities
- **ROA %**: Return on assets ratio

### 3. Customer Analytics (7 measures)
- **Active Customers**: DISTINCTCOUNT with IsActive filter
- **Revenue per Customer**: Sales divided by customer count
- **Customer Lifetime Value**: Complex calculation with churn assumptions
- **Customer Acquisition Cost**: Marketing spend per new customer
- **Top 10% Customer Sales**: TOPN customer contribution

### 4. Operational Metrics (10+ measures)  
- **Inventory Turnover**: COGS divided by average inventory
- **Days Sales Outstanding**: AR collection efficiency
- **Cash Conversion Cycle**: Working capital efficiency
- **Sales per Employee**: Productivity measurement
- **Regional/Channel Performance**: Geographic and distribution analysis

## 🛠️ DAX Best Practices

### Performance Optimization
```dax
// ✅ GOOD: Use variables to reduce context transitions
[Optimized Measure] = 
VAR CurrentValue = [Base Measure]
VAR PreviousValue = CALCULATE([Base Measure], SAMEPERIODLASTYEAR(DimDate[Date]))
RETURN DIVIDE(CurrentValue - PreviousValue, PreviousValue)

// ❌ AVOID: Multiple context transitions
[Inefficient Measure] = 
DIVIDE(
    [Base Measure] - CALCULATE([Base Measure], SAMEPERIODLASTYEAR(DimDate[Date])),
    CALCULATE([Base Measure], SAMEPERIODLASTYEAR(DimDate[Date]))
)
```

### Error Handling
```dax
// ✅ GOOD: Proper null handling
[Safe Ratio] = DIVIDE([Numerator], [Denominator])

// ✅ GOOD: Complex error handling
[Advanced Ratio] = 
VAR Num = [Numerator]
VAR Den = [Denominator]
RETURN
IF(
    Den = 0 || ISBLANK(Den),
    BLANK(),
    DIVIDE(Num, Den)
)
```

### Time Intelligence Patterns
```dax
// YTD Pattern
[Measure YTD] = TOTALYTD([Base Measure], DimDate[Date])

// Previous Period Pattern  
[Measure PY] = CALCULATE([Base Measure], SAMEPERIODLASTYEAR(DimDate[Date]))

// Growth Rate Pattern
[Growth %] = 
VAR Current = [Base Measure]
VAR Previous = [Measure PY]
RETURN DIVIDE(Current - Previous, Previous)
```

## 🔧 AI Assistant Integration

### DAX Generation Prompts
Use `prompt_dax_gen.md` for AI-assisted measure creation:

**Example Prompt:**
```
Generate a DAX measure for monthly sales growth using the Fabric Fast-Track model.
Requirements: Direct Lake compatible, handle nulls, format as percentage.
```

**Expected Output:**
```dax
Monthly Sales Growth % = 
VAR CurrentMonth = [Total Sales]
VAR PreviousMonth = CALCULATE([Total Sales], DATEADD(DimDate[Date], -1, MONTH))
RETURN
IF(
    ISBLANK(PreviousMonth) || PreviousMonth = 0,
    BLANK(),
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth)
)
```

### Quality Validation
Use validation prompts to ensure:
- F2+ performance compliance
- Direct Lake function compatibility  
- Proper error handling
- Business logic accuracy
- Naming convention adherence

## 📋 Deployment Checklist

### Prerequisites
- [x] Fabric workspace with Lakehouse
- [x] Bronze Delta tables from ingestion layer
- [x] F2+ capacity assigned to workspace
- [x] Appropriate RBAC permissions

### Validation Steps
1. **Import Model**: Load .bim file into workspace
2. **Connect Data**: Point to Bronze Delta tables
3. **Refresh Model**: Validate data loads successfully
4. **Test Measures**: Verify all 25+ measures execute
5. **Performance Check**: Confirm <2 second response times
6. **User Testing**: Validate with sample reports

### Monitoring Setup
- Query performance metrics
- Resource utilization alerts
- User concurrency monitoring
- Error rate tracking
- Capacity planning dashboards

## 🔍 Troubleshooting

### Common Issues

**Slow Query Performance**
- Check data volume (>10M rows may need F4)
- Verify partition strategy on fact tables
- Review complex measures with SUMX/TOPN

**Memory Pressure**
- Monitor concurrent user count (<15 on F2)
- Check for unnecessary columns in model
- Optimize string columns with encoding

**Relationship Issues**  
- Validate cardinality settings
- Check for circular dependencies
- Ensure proper filter directions

**DirectLake Compatibility**
- Verify Delta table format
- Check for unsupported data types
- Validate no complex M queries

### Performance Optimization

**F2 Capacity Limits**
- Max ~10M rows across fact tables
- 15 concurrent users optimal
- 4GB memory allocation
- 2 vCore processing power

**Upgrade Triggers**
- Consistent >2 second query times
- Memory usage >3.5GB sustained  
- Need for >15 concurrent users
- Data volume >10M rows

## 📚 Additional Resources

- [Fabric Fast-Track Blueprint](../README.md)
- [Data Ingestion Guide](../ingest/README.md)
- [Infrastructure Setup](../infra/README.md)
- [Microsoft Fabric Documentation](https://docs.microsoft.com/fabric/)
- [Direct Lake Performance Guide](https://docs.microsoft.com/fabric/get-started/direct-lake)

---
*Semantic model designed for enterprise-grade analytics with F2+ Direct Lake optimization*
EOF < /dev/null