# Power BI Reports Manual Creation Guide

## 🎯 **Overview**
This guide provides step-by-step instructions for manually creating the three Power BI reports (.pbix files) from the JSON template specifications. The JSON templates serve as detailed blueprints - this guide shows exactly how to build the actual reports.

---

## 📋 **Prerequisites**
1. **Power BI Desktop** (latest version installed)
2. **Fabric workspace** with F2+ capacity
3. **Semantic model** deployed (from `/model/fabric_fast_track.bim`)
4. **Demo data** loaded in Bronze Delta tables
5. **Corporate theme file** (`fabric_fast_track_theme.json`)

---

## 🚀 **Report 1: Executive KPI Dashboard (exec_kpi.pbix)**

### **Initial Setup**
```powerbi
1. Open Power BI Desktop
2. File → Import → Theme → Select fabric_fast_track_theme.json
3. Get Data → Power Platform → Power BI semantic models
4. Select "Fabric Fast-Track Semantic Model"
5. Connect in DirectLake mode
6. File → Page Settings → Type: Custom, Width: 1280px, Height: 720px
```

### **Page Layout Reference** (1280x720)
```
+------------------+------------------+------------------+------------------+------------------+
| Total Revenue    | Revenue Growth % | Net Income       | Active Customers | Gross Margin %   |
| Card Visual      | Card Visual      | Card Visual      | Card Visual      | Card Visual      |
| (40,40,200,120)  | (260,40,200,120) | (480,40,200,120) | (700,40,200,120) | (920,40,200,120) |
+------------------+------------------+------------------+------------------+------------------+
| Revenue Trend (12 Months)           | Sales by Region  | Top 10 Customers                  |
| Line Chart                           | Donut Chart      | Bar Chart                         |
| (40,180,560,240)                     | (620,180,280,240)| (920,180,280,240)                 |
+-------------------------------------+------------------+-----------------------------------+
| Key Performance Indicators          | Financial Summary (Quarterly)                        |
| Table Visual                         | Clustered Column Chart                                |
| (40,440,560,200)                     | (620,440,580,200)                                     |
+-------------------------------------+---------------------------------------------------+
```

### **Step-by-Step Visual Creation**

#### **1. Total Revenue Card**
```powerbi
1. Insert → Visualizations → Card
2. Drag to position (40, 40) and resize to 200x120
3. Data: Drag [Total Revenue] to Fields
4. Format Visual → Callout value → Display units: Millions → Custom format: $#,0,,M
5. Format Visual → General → Title → Text: "Total Revenue"
6. Format Visual → Effects → Background: On, Color: White
7. Format Visual → Effects → Border: On, Color: #1f4e79, Weight: 1px
```

#### **2. Revenue Growth % Card**
```powerbi
1. Insert → Visualizations → Card
2. Position: (260, 40, 200, 120)
3. Data: [Revenue Growth %]
4. Format Visual → Callout value → Display units: None → Custom format: 0.0%
5. Format Visual → Conditional formatting → Background color:
   - If value > 0 then #70ad47 (green)
   - If value < 0 then #c5504b (red)
   - Else #ffc000 (amber)
6. Title: "Revenue Growth %"
```

#### **3. Net Income Card**
```powerbi
1. Insert → Visualizations → Card
2. Position: (480, 40, 200, 120)
3. Data: [Net Income]
4. Format: $#,0,,M
5. Conditional formatting: Green if positive, red if negative
6. Title: "Net Income"
```

#### **4. Active Customers Card**
```powerbi
1. Insert → Visualizations → Card
2. Position: (700, 40, 200, 120)
3. Data: [Active Customers]
4. Format: #,0
5. Title: "Active Customers"
```

#### **5. Gross Margin % Card**
```powerbi
1. Insert → Visualizations → Card
2. Position: (920, 40, 200, 120)
3. Data: [Gross Margin %]
4. Format: 0.0%
5. Title: "Gross Margin %"
```

#### **6. Revenue Trend Chart**
```powerbi
1. Insert → Visualizations → Line Chart
2. Position: (40, 180, 560, 240)
3. X-axis: DimDate[MonthName]
4. Y-axis: [Total Revenue]
5. Format Visual → X-axis → Type: Categorical
6. Format Visual → Y-axis → Display units: Millions
7. Format Visual → Data colors: #1f4e79
8. Filters → Add DimDate[Date] → Relative date filtering → Last 12 months
9. Title: "Revenue Trend (12 Months)"
```

#### **7. Sales by Region Donut Chart**
```powerbi
1. Insert → Visualizations → Donut Chart
2. Position: (620, 180, 280, 240)
3. Legend: FactSales[Region]
4. Values: [Total Sales]
5. Format Visual → Legend → Position: Right
6. Format Visual → Data colors: Use theme colors
7. Title: "Sales by Region"
```

#### **8. Top 10 Customers Bar Chart**
```powerbi
1. Insert → Visualizations → Clustered Bar Chart
2. Position: (920, 180, 280, 240)
3. Y-axis: DimCustomers[CustomerName]
4. X-axis: [Revenue per Customer]
5. Filters → Add DimCustomers[CustomerName] → Filter type: Top N → Top 10 by [Revenue per Customer]
6. Format Visual → Data colors: #2e75b6
7. Title: "Top 10 Customers"
```

#### **9. KPI Table**
```powerbi
1. Insert → Visualizations → Table
2. Position: (40, 440, 560, 200)
3. Columns:
   - Create calculated column: KPI_Name = "Revenue YTD" (repeat for each KPI)
   - Current: [Sales YTD] (use appropriate measure for each row)
   - Previous: [Sales Previous Year]
   - Variance: Create calculated column for variance %
4. Format Visual → Conditional formatting → Variance column: Data bars
5. Title: "Key Performance Indicators"
```

#### **10. Financial Summary Chart**
```powerbi
1. Insert → Visualizations → Clustered Column Chart
2. Position: (620, 440, 580, 200)
3. X-axis: DimDate[Quarter]
4. Y-axis: [Total Revenue], [Total Expenses], [Net Income]
5. Legend: Show → Position: Top
6. Format Visual → Data colors: #1f4e79, #c5504b, #70ad47
7. Filters → DimDate[Date] → Last 4 quarters
8. Title: "Financial Summary (Quarterly)"
```

### **Page Filters**
```powerbi
1. Insert → Slicer → Position: (40, 660, 150, 40)
   - Field: DimDate[Year]
   - Style: Dropdown
2. Insert → Slicer → Position: (210, 660, 150, 40)
   - Field: FactSales[Region]
   - Style: Dropdown
```

### **Mobile Layout**
```powerbi
1. View → Mobile Layout
2. Phone layout (360x640):
   - Revenue Card: Resize and position at top
   - Revenue Growth Card: Below revenue
   - Revenue Trend Chart: Main chart area
   - Region Donut: Bottom section
   - Other visuals: Remove from mobile view
3. Test scrolling and interactions
```

---

## 🏢 **Report 2: Operations Drill-Down (ops_drill.pbix)**

### **Page 1: Sales Operations**

#### **Performance Cards Row**
```powerbi
1. Sales Velocity Card: (40, 40, 180, 100)
   - Data: [Sales Velocity]
   - Format: $#,0/day
   
2. Win Rate Card: (240, 40, 180, 100)
   - Data: [Win Rate %]
   - Format: 0.0%
   
3. Sales Count Card: (440, 40, 180, 100)
   - Data: [Sales Count]
   - Format: #,0
   
4. Avg Deal Size Card: (640, 40, 180, 100)
   - Data: [Average Sale Value]
   - Format: $#,0
```

#### **Pipeline Health Gauge**
```powerbi
1. Insert → Visualizations → Gauge
2. Position: (840, 40, 200, 100)
3. Value: [Win Rate %]
4. Target: 0.25 (25%)
5. Format Visual → Data colors → Good: #70ad47, Satisfactory: #ffc000, Poor: #c5504b
6. Title: "Pipeline Health"
```

#### **Sales by Channel & Region Matrix**
```powerbi
1. Insert → Visualizations → Matrix
2. Position: (40, 160, 400, 200)
3. Rows: FactSales[Channel]
4. Columns: FactSales[Region]
5. Values: [Total Sales], [Sales Count]
6. Format Visual → Row subtotals: On → Column subtotals: On
7. Enable drill-through (Format → General → Drill through: On)
8. Title: "Sales by Channel & Region"
```

#### **Sales Trend by Status**
```powerbi
1. Insert → Visualizations → Line Chart
2. Position: (460, 160, 400, 200)
3. X-axis: DimDate[Date]
4. Y-axis: [Total Sales]
5. Legend: FactSales[Status]
6. Format Visual → Data colors: #70ad47 (Closed Won), #ffc000 (In Progress), #c5504b (Closed Lost), #5b9bd5 (Qualified)
7. Filters → Last 365 days
8. Title: "Sales Trend by Status"
```

#### **Sales Rep Performance**
```powerbi
1. Insert → Visualizations → Clustered Bar Chart
2. Position: (880, 160, 320, 200)
3. Y-axis: FactSales[SalesRep]
4. X-axis: [Total Sales]
5. Filters → Top 15 by [Total Sales]
6. Format Visual → Data colors: #1f4e79
7. Title: "Sales Rep Performance"
```

#### **Product Performance Table**
```powerbi
1. Insert → Visualizations → Table
2. Position: (40, 380, 580, 200)
3. Columns:
   - FactSales[ProductName] (width: 200px)
   - [Total Sales] (format: $#,0)
   - [Total Quantity] (format: #,0)
   - [Average Sale Value] (format: $#,0)
   - [Sales Growth %] (format: 0.0% with conditional formatting)
4. Sort by [Total Sales] descending
5. Show top 25 products
6. Title: "Product Performance Analysis"
```

#### **Customer Segments Donut**
```powerbi
1. Insert → Visualizations → Donut Chart
2. Position: (640, 380, 280, 200)
3. Legend: DimCustomers[CompanySize]
4. Values: [Total Sales]
5. Format Visual → Data colors: Theme colors
6. Title: "Sales by Customer Size"
```

#### **Conversion Funnel**
```powerbi
1. Insert → Visualizations → Funnel Chart
2. Position: (940, 380, 260, 200)
3. Group: Create calculated column for funnel stages
4. Values: [Sales Count] with appropriate filters for each stage
5. Format Visual → Data colors: #a5c8ec → #5b9bd5 → #1f4e79
6. Title: "Sales Conversion Funnel"
```

### **Page 2: Customer Operations**

#### **Customer Metric Cards**
```powerbi
1. Customer Acquisition Cost: (40, 40, 200, 100)
   - Data: [Customer Acquisition Cost]
   - Format: $#,0
   
2. Customer LTV: (260, 40, 200, 100)
   - Data: [Customer Lifetime Value]
   - Format: $#,0
   
3. Revenue per Customer: (480, 40, 200, 100)
   - Data: [Revenue per Customer]
   - Format: $#,0
   
4. Top 10% Contribution: (700, 40, 200, 100)
   - Data: [Top 10% Customers Sales]
   - Format: $#,0,,M
```

#### **Customer Geography Map**
```powerbi
1. Insert → Visualizations → Map
2. Position: (40, 160, 400, 240)
3. Location: DimCustomers[State]
4. Size: [Total Sales]
5. Format Visual → Bubble size: Min 10, Max 50
6. Title: "Customer Geography"
```

#### **Industry Breakdown Pie Chart**
```powerbi
1. Insert → Visualizations → Pie Chart
2. Position: (460, 160, 300, 240)
3. Legend: DimCustomers[Industry]
4. Values: [Active Customers]
5. Format Visual → Data colors: Theme color palette
6. Title: "Customers by Industry"
```

#### **Customer Size Analysis**
```powerbi
1. Insert → Visualizations → Clustered Bar Chart
2. Position: (780, 160, 420, 240)
3. Y-axis: DimCustomers[CompanySize]
4. X-axis: [Total Sales]
5. Legend: DimCustomers[Industry]
6. Format Visual → Data colors: Theme colors
7. Title: "Revenue by Customer Size"
```

#### **Customer Retention Trend**
```powerbi
1. Insert → Visualizations → Line Chart
2. Position: (40, 420, 560, 200)
3. X-axis: DimDate[MonthName]
4. Y-axis: [Active Customers] (primary), [Customer Lifetime Value] (secondary)
5. Format Visual → Y-axis (secondary): On
6. Data colors: #1f4e79, #70ad47
7. Filters → Last 24 months
8. Title: "Customer Retention Trend"
```

#### **Customer Segmentation Scatter**
```powerbi
1. Insert → Visualizations → Scatter Chart
2. Position: (620, 420, 580, 200)
3. X-axis: [Revenue per Customer]
4. Y-axis: [Customer Lifetime Value]
5. Legend: DimCustomers[CompanySize]
6. Size: [Total Sales]
7. Format Visual → Data colors: Theme colors
8. Filters → Top 100 customers by revenue
9. Title: "Customer Segmentation (RFM)"
```

### **Drill-Through Setup**
```powerbi
1. Create new page: "Customer Detail"
2. Add DimCustomers[CustomerID] to drill-through filters
3. Add customer-specific visuals:
   - Customer transaction history table
   - Customer trend analysis chart
4. Test drill-through from customer visuals
```

---

## 💰 **Report 3: Financial Variance (finance_variance.pbix)**

### **Page 1: P&L Variance Analysis**

#### **Financial Metric Cards**
```powerbi
1. Total Revenue: (40, 40, 180, 100)
   - Data: [Total Revenue]
   - Format: $#,0,,M
   
2. Total Expenses: (240, 40, 180, 100)
   - Data: [Total Expenses]
   - Format: $#,0,,M
   - Color: #c5504b
   
3. Net Income: (440, 40, 180, 100)
   - Data: [Net Income]
   - Format: $#,0,,M
   - Conditional formatting: Green if positive, red if negative
   
4. Gross Margin %: (640, 40, 180, 100)
   - Data: [Gross Margin %]
   - Format: 0.0%
   
5. EBITDA: (840, 40, 180, 100)
   - Data: [EBITDA]
   - Format: $#,0,,M
```

#### **Budget Variance Gauge**
```powerbi
1. Insert → Visualizations → Gauge
2. Position: (1040, 40, 180, 100)
3. Value: [Budget Variance %]
4. Target: 0 (0% variance)
5. Format Visual → Data colors: Green for positive, red for negative
6. Title: "Budget Variance"
```

#### **Revenue vs Budget Chart**
```powerbi
1. Insert → Visualizations → Clustered Column Chart
2. Position: (40, 160, 400, 200)
3. X-axis: DimDate[MonthName]
4. Y-axis: [Total Revenue], Budget calculation ([Total Revenue] * 1.1)
5. Format Visual → Data colors: #1f4e79, #ffc000
6. Filters → Last 12 months
7. Title: "Revenue vs Budget (Monthly)"
```

#### **Expense Breakdown Waterfall**
```powerbi
1. Insert → Visualizations → Waterfall Chart
2. Position: (460, 160, 400, 200)
3. Category: FactFinancial[Department]
4. Y-axis: [Total Expenses]
5. Format Visual → Data colors: Various shades of red/orange
6. Title: "Expense Breakdown"
```

#### **Profit Margin Trend**
```powerbi
1. Insert → Visualizations → Area Chart
2. Position: (880, 160, 340, 200)
3. X-axis: DimDate[Date]
4. Y-axis: [Gross Margin %]
5. Format Visual → Data colors: #70ad47
6. Filters → Last 365 days
7. Title: "Profit Margin Trend"
```

#### **Variance Analysis Table**
```powerbi
1. Insert → Visualizations → Table
2. Position: (40, 380, 600, 240)
3. Columns:
   - FactFinancial[Account] (150px)
   - [Total Revenue] (format: $#,0,K)
   - Budget Amount (calculated: [Total Revenue] * 1.1, format: $#,0,K)
   - [Budget Variance %] (format: 0.0% with conditional formatting)
   - Variance Amount (calculated, format: $#,0,K)
4. Sort by Account alphabetically
5. Conditional formatting on variance columns
6. Title: "Variance Analysis by Account"
```

#### **Department Performance Matrix**
```powerbi
1. Insert → Visualizations → Matrix
2. Position: (660, 380, 560, 240)
3. Rows: FactFinancial[Department]
4. Columns: FactFinancial[Account]
5. Values: [Total Revenue], [Budget Variance %]
6. Format Visual → Conditional formatting: On for variance values
7. Title: "Department Performance Matrix"
```

### **Page 2: Cash Flow Analysis**

#### **Cash Flow Metric Cards**
```powerbi
1. Operating Cash Flow: (40, 40, 200, 100)
   - Data: [Operating Cash Flow]
   - Format: $#,0,,M
   
2. Working Capital: (260, 40, 200, 100)
   - Data: [Working Capital]
   - Format: $#,0,,M
   
3. Days Sales Outstanding: (480, 40, 200, 100)
   - Data: [Days Sales Outstanding]
   - Format: #,0 days
   
4. Cash Conversion Cycle: (700, 40, 200, 100)
   - Data: [Cash Conversion Cycle]
   - Format: #,0 days
   
5. Return on Assets: (920, 40, 200, 100)
   - Data: [Return on Assets %]
   - Format: 0.0%
```

#### **Cash Flow Waterfall**
```powerbi
1. Insert → Visualizations → Waterfall Chart
2. Position: (40, 160, 500, 240)
3. Category: Cash flow components (create calculated column)
4. Y-axis: Cash flow amounts
5. Format Visual → Data colors: Blues and greens
6. Title: "Cash Flow Waterfall (Quarterly)"
```

#### **Working Capital Trend**
```powerbi
1. Insert → Visualizations → Line Chart
2. Position: (560, 160, 400, 240)
3. X-axis: DimDate[Date]
4. Y-axis: [Working Capital] (primary), [Days Sales Outstanding] (secondary)
5. Format Visual → Y-axis (secondary): On
6. Data colors: #1f4e79, #c5504b
7. Filters → Last 24 months
8. Title: "Working Capital Trend"
```

#### **Liquidity Ratios Multi-Row Card**
```powerbi
1. Insert → Visualizations → Multi-row Card
2. Position: (980, 160, 240, 240)
3. Fields:
   - [Return on Assets %] (format: 0.0%, label: "ROA")
   - [Debt to Equity Ratio] (format: 0.00, label: "Debt/Equity")
   - [Inventory Turnover] (format: 0.0x, label: "Inventory Turns")
4. Title: "Liquidity Ratios"
```

#### **Financial Health Radar Chart** (if available)
```powerbi
1. Insert → Visualizations → Radar Chart (custom visual)
2. Position: (40, 420, 400, 200)
3. Axis: Liquidity, Profitability, Efficiency, Leverage, Growth
4. Values: Corresponding financial ratios
5. Format Visual → Data colors: #1f4e79
6. Title: "Financial Health Radar"
```

#### **Monthly Financial Summary Table**
```powerbi
1. Insert → Visualizations → Table
2. Position: (460, 420, 760, 200)
3. Columns:
   - DimDate[MonthName] (100px)
   - [Total Revenue] (format: $#,0,K)
   - [Total Expenses] (format: $#,0,K)
   - [Net Income] (format: $#,0,K with conditional formatting)
   - [Operating Cash Flow] (format: $#,0,K)
   - [Budget Variance %] (format: 0.0% with conditional formatting)
   - [Gross Margin %] (format: 0.0%)
4. Filters → Last 12 months
5. Title: "Monthly Financial Summary"
```

---

## ⚡ **Performance Optimization for All Reports**

### **1. Performance Analyzer Setup**
```powerbi
1. View → Performance Analyzer → Start recording
2. Refresh all visuals
3. Check each visual's load time (<2 seconds target)
4. Optimize slow visuals:
   - Reduce data points
   - Simplify DAX measures
   - Add appropriate filters
```

### **2. Visual Interactions**
```powerbi
1. Format → Edit Interactions
2. Disable unnecessary cross-filtering
3. Keep maximum 3 active cross-filters
4. Test interaction responsiveness (<500ms target)
```

### **3. Data Reduction Settings**
```powerbi
1. File → Options and Settings → Options → Data Load
2. DirectQuery → Query timeout: 120 seconds
3. Data connectivity → Enable parallel loading of tables
4. Performance → Reduce data by limiting rows displayed
```

### **4. Filter Optimization**
```powerbi
1. Use relative date filters where possible
2. Set default filter values
3. Limit concurrent active filters
4. Test filter responsiveness
```

---

## 📱 **Mobile Layout for All Reports**

### **Phone Layout Configuration (360x640)**
```powerbi
1. View → Mobile Layout
2. For each report, select priority visuals only:
   - Executive: 4-5 key cards + main trend chart
   - Operations: Performance cards + key chart
   - Finance: Financial cards + variance chart
3. Resize and reposition for mobile screen
4. Test scrolling and touch interactions
5. Verify readability and usability
```

---

## 💾 **Saving and Publishing**

### **Save Reports**
```powerbi
1. File → Save As
2. Filename: exec_kpi.pbix, ops_drill.pbix, finance_variance.pbix
3. Location: Local reports folder
```

### **Publish to Fabric Workspace**
```powerbi
1. Home → Publish
2. Select Fabric workspace
3. Verify F2+ capacity assignment
4. Test live performance in browser
5. Share with stakeholders
```

---

## ✅ **Final Validation Checklist**

### **Before Publishing Each Report:**
- [ ] Corporate theme applied correctly
- [ ] All visuals load within 2 seconds (Performance Analyzer)
- [ ] Cross-filtering works as expected
- [ ] Mobile layout configured and tested
- [ ] All filters working properly
- [ ] Data connections verified (DirectLake mode)
- [ ] Error handling for null/blank values
- [ ] Conditional formatting applied where specified
- [ ] Visual interactions optimized
- [ ] Drill-through pages working (operations report)
- [ ] All measures displaying correct values
- [ ] Professional appearance and consistent branding

### **Performance Validation:**
- [ ] Executive dashboard: All visuals <1 second
- [ ] Operations dashboard: All visuals <1.5 seconds  
- [ ] Finance dashboard: All visuals <1.8 seconds
- [ ] Cross-filtering response: <500ms
- [ ] Memory usage: <3GB total
- [ ] No visual errors or timeouts

---

*This manual creation guide ensures production-ready Power BI reports that match template specifications and achieve <2 second performance targets on F2+ Direct Lake capacity.*
EOF < /dev/null