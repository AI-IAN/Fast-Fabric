# Power BI Performance Optimization for <2 Second Load Times

## Overview
This document outlines performance optimization strategies to ensure all Fabric Fast-Track reports achieve <2 second visual load times on demo datasets with F2+ Direct Lake capacity.

## Performance Targets
- **Visual Load Time**: <2 seconds per visual
- **Dashboard Load Time**: <5 seconds total
- **Query Execution**: <1 second per DAX measure
- **Cross-filtering**: <500ms response time
- **Data Refresh**: Complete within refresh window

## Optimization Strategies

### 1. Data Model Optimization

#### Direct Lake Configuration
```json
{
  "connection_mode": "DirectLake",
  "storage_mode": "DirectLake",
  "fallback_mode": "DirectQuery"
}
```

#### Table-Level Optimizations
- **FactSales**: Partition by SaleDate (monthly partitions)
- **FactFinancial**: Partition by Date (quarterly partitions)
- **DimCustomers**: No partitioning (< 100K rows)
- **DimDate**: Calculated table (minimal overhead)

#### Column Optimizations
```dax
// Optimize data types for performance
SaleDate: DateTime (not Text)
CustomerID: Int64 (not Text)
TotalAmount: Currency (not Text)
Region: Text with encoding
```

### 2. Visual-Level Performance

#### Row Limitations per Visual Type
- **Cards**: 1 row (single aggregation)
- **Charts**: ≤1,000 data points maximum
- **Tables**: ≤100 rows displayed, ≤1,000 total
- **Maps**: ≤50 geographic points
- **Matrix**: ≤50 rows × 10 columns

#### Visual Interaction Settings
```json
{
  "cross_filter_limit": 3,
  "cross_highlight_enabled": true,
  "drill_through_enabled": true,
  "visual_interaction_timeout": 30000
}
```

#### Performance-Optimized Visual Configuration
```json
{
  "executive_dashboard": {
    "revenue_card": {
      "row_limit": 1,
      "cache_duration": "1 hour",
      "aggregation_pushdown": true
    },
    "revenue_trend": {
      "row_limit": 12,
      "aggregation_level": "month",
      "data_reduction": true
    }
  }
}
```

### 3. DAX Measure Optimization

#### Performance-Optimized Patterns
```dax
// ✅ GOOD: Use variables to reduce context transitions
[Optimized Revenue Growth] = 
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue)

// ❌ AVOID: Multiple context transitions
[Slow Revenue Growth] = 
DIVIDE(
    [Total Revenue] - CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date])),
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
)
```

#### Direct Lake Compatible Functions
```dax
// ✅ Optimized for Direct Lake
SUM()           // Fast aggregation
COUNT()         // Fast counting
AVERAGE()       // Direct aggregation
MIN() / MAX()   // Direct aggregation
DISTINCTCOUNT() // Optimized for indexed columns

// ⚠️ Use Carefully
CALCULATE()     // Keep filters simple
TOPN()          // Limit to small N values
SUMMARIZE()     // Avoid complex grouping

// ❌ Avoid in Direct Lake
FILTER()        // Use CALCULATE instead
CROSSFILTER()   // Use relationships
USERELATIONSHIP() // Single active relationship design
```

### 4. Report-Level Optimization

#### Page Load Optimization
```json
{
  "page_settings": {
    "background_refresh": true,
    "visual_lazy_loading": true,
    "interaction_throttling": 100,
    "cross_filter_direction": "single"
  }
}
```

#### Filter Optimization
- **Global filters**: Limit to 3 active filters
- **Page filters**: Limit to 5 per page
- **Visual filters**: Minimize complex filter expressions
- **Date filters**: Use relative date ranges when possible

### 5. Demo Dataset Optimization

#### Sample Data Volume Guidelines
```
FactSales:      10,000 rows (1 year of daily data)
FactFinancial:  1,200 rows (2 years of monthly data)
DimCustomers:   1,000 rows (typical mid-market client base)
DimDate:        1,095 rows (3 years of dates)
```

#### Data Distribution for Performance Testing
```sql
-- Balanced data distribution for realistic performance
-- 70% current year, 20% previous year, 10% older
-- Regional distribution: 40% North America, 30% Europe, 20% APAC, 10% Other
-- Customer size: 60% Small, 25% Medium, 10% Large, 5% Enterprise
```

### 6. F2 Capacity Optimization

#### Memory Management
```json
{
  "f2_capacity_limits": {
    "total_memory": "4GB",
    "available_for_data": "3GB",
    "model_size_limit": "2.5GB",
    "concurrent_users": 15
  }
}
```

#### CPU Utilization
- **Target CPU**: <70% average, <85% peak
- **Query timeout**: 120 seconds maximum
- **Parallel processing**: Enable for aggregations
- **Cache utilization**: 70% hit rate minimum

### 7. Caching Strategy

#### Visual-Level Caching
```json
{
  "cache_settings": {
    "card_visuals": "1 hour",
    "trend_charts": "30 minutes", 
    "detail_tables": "15 minutes",
    "real_time_visuals": "5 minutes"
  }
}
```

#### Query Result Caching
- **Aggregated measures**: 1 hour cache
- **Detailed queries**: 15 minute cache
- **Cross-filter results**: 5 minute cache
- **Drill-through queries**: No cache (always fresh)

### 8. Monitoring and Alerting

#### Performance Metrics to Track
```json
{
  "key_metrics": {
    "visual_load_time": "< 2 seconds",
    "query_execution_time": "< 1 second",
    "dashboard_load_time": "< 5 seconds",
    "memory_usage": "< 3GB",
    "cpu_utilization": "< 70%",
    "concurrent_users": "< 15",
    "error_rate": "< 1%"
  }
}
```

#### Alerting Thresholds
- **Critical**: Visual load >5 seconds
- **Warning**: Visual load >2 seconds
- **Info**: Visual load >1 second

### 9. Testing Methodology

#### Performance Test Scripts
```javascript
// Example performance test for executive dashboard
const performanceTest = {
  dashboard: "executive_kpi",
  tests: [
    {
      name: "Revenue Card Load",
      target: "< 0.5 seconds",
      measure: "[Total Revenue]"
    },
    {
      name: "Trend Chart Load", 
      target: "< 1.5 seconds",
      rows: 12,
      measure: "[Total Revenue]"
    }
  ]
};
```

#### Load Testing Scenarios
1. **Single User**: All visuals load within target times
2. **5 Concurrent Users**: 90% of queries within target
3. **10 Concurrent Users**: 80% of queries within target
4. **15 Concurrent Users**: 70% of queries within target (limit)

### 10. Optimization Checklist

#### Pre-Deployment Checklist
- [ ] All measures use Direct Lake compatible functions
- [ ] Visual row limits configured and tested
- [ ] Cross-filtering limited to essential interactions
- [ ] Date table optimized with proper relationships
- [ ] Theme applied consistently across all reports
- [ ] Mobile layouts configured for responsive design
- [ ] Performance tested with demo dataset
- [ ] F2 capacity limits validated
- [ ] Caching strategy implemented
- [ ] Monitoring alerts configured

#### Post-Deployment Monitoring
- [ ] Visual load times monitored continuously
- [ ] User feedback collected on performance
- [ ] Resource utilization tracked
- [ ] Performance regression testing scheduled
- [ ] Capacity planning updated based on usage

### 11. Troubleshooting Common Issues

#### Slow Visual Performance
1. Check data volume (reduce if >1K rows)
2. Verify Direct Lake mode is active
3. Review DAX measure complexity
4. Check for unnecessary cross-filtering
5. Validate F2 capacity resource usage

#### Memory Pressure
1. Reduce model size by removing unused columns
2. Optimize string columns with better encoding
3. Review concurrent user count
4. Check for memory leaks in custom visuals
5. Consider upgrading to F4 capacity

#### Query Timeouts
1. Simplify complex DAX measures
2. Add appropriate filters to reduce data volume
3. Check relationship cardinality settings
4. Verify partition strategy effectiveness
5. Review aggregation pushdown behavior

---

*Performance optimization ensures <2 second visual load times on F2+ Direct Lake capacity*
EOF < /dev/null