# Fabric Fast-Track Manual Creation Guide

## Overview
This guide provides step-by-step manual deployment instructions for the Fabric Fast-Track accelerator when automated deployment is not available.

## Prerequisites
- Microsoft Fabric license (F2+ capacity required)
- Power BI Pro license  
- Azure subscription with appropriate permissions
- PowerShell 7+ or Azure CLI installed

## Part 1: Infrastructure Setup

### Step 1: Create Fabric Workspace
1. Navigate to Power BI Service (app.powerbi.com)
2. Click Workspaces → Create a workspace
3. Name: FastTrack-Production (or your preferred name)
4. Advanced settings:
   - License mode: Fabric
   - Default storage format: Delta
5. Click Save

### Step 2: Configure Capacity
1. In workspace settings, go to Premium tab
2. Assign to F2 capacity (minimum required)
3. Verify capacity assignment successful

### Step 3: Enable Required Features
1. In workspace settings:
   - Enable Lakehouse 
   - Enable Data Engineering
   - Enable Data Science
   - Enable Real-Time Analytics

## Part 2: Data Infrastructure

### Step 4: Create Lakehouse
1. In workspace, click + New → Lakehouse
2. Name: FastTrack_Lakehouse  
3. Wait for creation to complete
4. Note the Lakehouse endpoint URL

### Step 5: Create Delta Tables Structure
1. In Lakehouse, create folder structure for bronze, silver, gold tables
2. Upload sample data files to Files section
3. Run notebook to create initial Delta tables

## Part 3: Data Pipelines

### Step 6: Create Data Pipeline
1. Click + New → Data pipeline
2. Name: FastTrack_Ingest_Pipeline
3. Add Copy data activity
4. Configure source and destination connections
5. Set destination to Lakehouse bronze tables

### Step 7: Create Transformation Pipeline  
1. Create new Data pipeline: FastTrack_Transform_Pipeline
2. Add Dataflow Gen2 activity
3. Configure transformations from bronze to silver tables
4. Save and publish

## Part 4: Semantic Model

### Step 8: Create Semantic Model
1. In Lakehouse, click New semantic model
2. Name: FastTrack_Sales_Model
3. Select required tables from silver/gold layers

### Step 9: Configure Model Relationships
1. Open semantic model in Model view
2. Create relationships between fact and dimension tables
3. Verify relationship cardinality and cross-filter direction

### Step 10: Add DAX Measures
Create essential DAX measures for reporting:
- Total Sales = SUM(fact_sales[sales_amount])
- Total Orders = COUNTROWS(fact_sales)
- Average Order Value = DIVIDE([Total Sales], [Total Orders])

## Part 5: Row Level Security (RLS)

### Step 11: Configure RLS Roles
1. In semantic model, go to Security tab
2. Create roles with appropriate DAX filters:
   - Sales Manager: [Region] = "North America"
   - Sales Rep East: [Region] = "East"
   - Sales Rep West: [Region] = "West"
   - Finance: 1=1 (no filter)

### Step 12: Test RLS
1. Click View as roles to test security
2. Verify data filtering works correctly
3. Test with sample user accounts

## Part 6: Power BI Reports

### Step 13: Create Report
1. Click + New → Report
2. Connect to semantic model: FastTrack_Sales_Model
3. Add key visualizations:
   - Sales by Region (Bar chart)
   - Sales Trend (Line chart)  
   - Top Products (Table)
   - KPI Cards (Total Sales, Orders, AOV)

### Step 14: Apply Theme and Formatting
1. Import custom theme file if available
2. Apply consistent formatting across visuals
3. Configure page layouts and navigation

### Step 15: Configure Report Settings
1. Set refresh schedule (recommended: Daily at 6 AM)
2. Enable automatic page refresh for real-time visuals
3. Configure performance settings

## Part 7: Governance & Security

### Step 16: Configure Data Quality
1. Create Data Quality notebook with validation rules
2. Install Great Expectations library
3. Schedule notebook to run after data refresh
4. Set up alerting for data quality failures

### Step 17: Setup Monitoring
1. Enable Usage metrics in workspace settings
2. Create monitoring dashboard
3. Set up alerts for refresh failures and performance issues

## Part 8: Deployment Validation

### Step 18: Performance Testing
1. Test report load times (target: under 2 seconds)
2. Validate Direct Lake refresh functionality
3. Test concurrent user access scenarios
4. Verify RLS performance impact

### Step 19: End-to-End Testing
1. Run complete data pipeline from source to reports
2. Validate data accuracy across all layers
3. Test user access with different security roles
4. Verify all visualizations render correctly

## Part 9: Production Deployment

### Step 20: Production Workspace Setup
1. Create production workspace
2. Deploy using Deployment pipelines if available
3. Update connection strings for production data sources
4. Complete end-to-end testing in production

## Troubleshooting Common Issues

### Direct Lake Issues
- Ensure F2+ capacity is assigned
- Verify Delta table format compliance
- Check for unsupported data types

### RLS Problems
- Verify user email matches security filter
- Test role assignments in development first
- Check for complex DAX filter performance

### Performance Issues
- Use Aggregations for large datasets
- Implement Incremental refresh
- Optimize DAX measures
- Consider Composite models for hybrid scenarios

## Success Criteria Checklist
- [ ] Workspace deploys in under 15 minutes
- [ ] Pipeline creates bronze Delta tables successfully
- [ ] Semantic model validates and refreshes in Direct Lake
- [ ] Reports render with under 2 second visual load time
- [ ] RLS works correctly for all defined user roles
- [ ] Data quality checks pass validation
- [ ] End-to-end pipeline completes without errors

## Next Steps After Manual Setup
- Implement automated deployment using provided pipelines
- Configure AI assistant for enhanced DAX generation
- Set up advanced monitoring and alerting systems
- Establish comprehensive data governance policies
- Scale to additional data sources and use cases
