# Source Mapper Example Configurations

## Example 1: SQL Server E-commerce Database

**User Request:**
```
Map SQL database source to medallion architecture: E-commerce production database

Source Details:
- Database Type: SQL Server
- Database Name: ECommerceDB
- Key Tables: Customers, Orders, OrderItems, Products, Categories
- Business Context: Online retail order processing and customer management
- Data Volume: 2M customers, 10M orders, 25M order items
- Update Frequency: Real-time for orders, daily for customers and products

Schema Information:
- Primary Keys: CustomerID, OrderID, ProductID, CategoryID
- Foreign Keys: Orders.CustomerID → Customers.CustomerID, OrderItems.OrderID → Orders.OrderID
- Incremental Columns: ModifiedDate on all tables
- Business Keys: CustomerEmail, OrderNumber, ProductSKU

Requirements:
- Load Pattern: Incremental (last 7 days full refresh)
- SLA: Data available within 2 hours of source update
- Transformations: PII masking, currency standardization
- Quality Rules: Email validation, order total validation
```

**Source Mapper Response:**
```yaml
# E-commerce SQL Server Source Mapping
source_name: ecommerce_sqlserver
source_type: sql
source_system: "SQL Server - ECommerceDB"
business_domain: "E-commerce Operations"

# Connection Configuration
connection_details:
  server: "{{SQL_SERVER_NAME}}"
  database: "ECommerceDB"
  authentication:
    type: "sql_auth"
    username: "{{SQL_USERNAME}}"
    password: "{{SECRET:KeyVault:sql-password}}"
  connection_string: "Server={{SQL_SERVER_NAME}};Database=ECommerceDB;User Id={{SQL_USERNAME}};Password={{SQL_PASSWORD}};Encrypt=true;TrustServerCertificate=false;"

# Medallion Architecture Mapping
destination_layers:
  bronze:
    schema: "bronze_ecommerce"
    load_strategy: "incremental"
    incremental_column: "ModifiedDate"
    full_refresh_days: 7
    
    tables:
      customers:
        source_table: "dbo.Customers"
        destination_table: "bronze_ecommerce.customers"
        business_key: "CustomerID"
        incremental_column: "ModifiedDate"
        schema_mapping:
          CustomerID: "customer_id:bigint:not_null"
          FirstName: "first_name:string:nullable"
          LastName: "last_name:string:nullable"
          Email: "email:string:not_null"
          Phone: "phone:string:nullable"
          CreatedDate: "created_date:timestamp:not_null"
          ModifiedDate: "modified_date:timestamp:not_null"
        audit_columns:
          _bronze_load_timestamp: "current_timestamp()"
          _bronze_source_file: "'sqlserver_ecommerce'"
          _bronze_load_id: "uuid()"
      
      orders:
        source_table: "dbo.Orders"
        destination_table: "bronze_ecommerce.orders"
        business_key: "OrderID"
        incremental_column: "ModifiedDate"
        schema_mapping:
          OrderID: "order_id:bigint:not_null"
          CustomerID: "customer_id:bigint:not_null"
          OrderNumber: "order_number:string:not_null"
          OrderDate: "order_date:date:not_null"
          TotalAmount: "total_amount:decimal(10,2):not_null"
          Status: "status:string:not_null"
          CreatedDate: "created_date:timestamp:not_null"
          ModifiedDate: "modified_date:timestamp:not_null"
        partitioning:
          partition_by: "order_date"
          partition_type: "date_monthly"
          
      order_items:
        source_table: "dbo.OrderItems"
        destination_table: "bronze_ecommerce.order_items"
        business_key: "OrderItemID"
        incremental_column: "ModifiedDate"
        schema_mapping:
          OrderItemID: "order_item_id:bigint:not_null"
          OrderID: "order_id:bigint:not_null"
          ProductID: "product_id:bigint:not_null"
          Quantity: "quantity:int:not_null"
          UnitPrice: "unit_price:decimal(10,2):not_null"
          LineTotal: "line_total:decimal(10,2):not_null"
          ModifiedDate: "modified_date:timestamp:not_null"
          
      products:
        source_table: "dbo.Products"
        destination_table: "bronze_ecommerce.products"
        business_key: "ProductID"
        incremental_column: "ModifiedDate"
        schema_mapping:
          ProductID: "product_id:bigint:not_null"
          ProductSKU: "product_sku:string:not_null"
          ProductName: "product_name:string:not_null"
          CategoryID: "category_id:bigint:not_null"
          Price: "price:decimal(10,2):not_null"
          IsActive: "is_active:boolean:not_null"
          ModifiedDate: "modified_date:timestamp:not_null"

  silver:
    schema: "silver_ecommerce"
    
    tables:
      dim_customers:
        source_table: "bronze_ecommerce.customers"
        destination_table: "silver_ecommerce.dim_customers"
        transformation_rules:
          - "Clean and standardize customer names"
          - "Validate email format using regex"
          - "Mask PII for non-production environments"
          - "Standardize phone number format"
        schema_mapping:
          customer_id: "customer_id:bigint:not_null"
          customer_name: "CONCAT(TRIM(first_name), ' ', TRIM(last_name)):string"
          email_address: "LOWER(TRIM(email)):string:not_null"
          phone_number: "standardize_phone(phone):string"
          customer_since: "created_date:date:not_null"
          last_modified: "modified_date:timestamp:not_null"
          is_active: "CASE WHEN modified_date >= CURRENT_DATE - INTERVAL '365' DAYS THEN TRUE ELSE FALSE END"
        data_quality_rules:
          - field: "email_address"
            rule: "email_format_validation"
            action: "quarantine"
          - field: "customer_name"
            rule: "not_null_and_not_empty"
            action: "quarantine"
            
      fact_orders:
        source_tables: 
          - "bronze_ecommerce.orders"
          - "bronze_ecommerce.order_items"
        destination_table: "silver_ecommerce.fact_orders"
        join_logic: "orders o JOIN order_items oi ON o.order_id = oi.order_id"
        transformation_rules:
          - "Calculate order metrics and aggregations"
          - "Validate order totals against line item sums"
          - "Standardize currency to USD"
        schema_mapping:
          order_id: "o.order_id:bigint:not_null"
          customer_id: "o.customer_id:bigint:not_null"
          order_number: "o.order_number:string:not_null"
          order_date: "o.order_date:date:not_null"
          order_total: "o.total_amount:decimal(10,2):not_null"
          item_count: "COUNT(oi.order_item_id):int"
          calculated_total: "SUM(oi.line_total):decimal(10,2)"
          order_status: "o.status:string:not_null"
        data_quality_rules:
          - field: "order_total"
            rule: "order_total = calculated_total"
            tolerance: "0.01"
            action: "quarantine"
          - field: "order_total"
            rule: "greater_than_zero"
            action: "quarantine"

  gold:
    schema: "gold_ecommerce"
    
    tables:
      customer_metrics:
        source_table: "silver_ecommerce.fact_orders"
        destination_table: "gold_ecommerce.customer_metrics"
        aggregation_level: "customer_id, order_date_month"
        business_metrics:
          total_orders: "COUNT(DISTINCT order_id)"
          total_revenue: "SUM(order_total)"
          avg_order_value: "AVG(order_total)"
          first_order_date: "MIN(order_date)"
          last_order_date: "MAX(order_date)"
          customer_lifetime_months: "DATEDIFF(MONTH, MIN(order_date), MAX(order_date)) + 1"
        partitioning:
          partition_by: "order_date_month"
          partition_type: "date_monthly"
          
      daily_sales_summary:
        source_table: "silver_ecommerce.fact_orders"
        destination_table: "gold_ecommerce.daily_sales_summary"
        aggregation_level: "order_date"
        business_metrics:
          total_orders: "COUNT(DISTINCT order_id)"
          total_revenue: "SUM(order_total)"
          avg_order_value: "AVG(order_total)"
          unique_customers: "COUNT(DISTINCT customer_id)"
          new_customers: "COUNT(DISTINCT CASE WHEN is_first_order = TRUE THEN customer_id END)"
        refresh_frequency: "daily"
        optimization:
          z_order_by: ["order_date"]
          table_properties:
            delta.autoOptimize.optimizeWrite: "true"
            delta.autoOptimize.autoCompact: "true"

# Processing Configuration
processing_config:
  incremental_strategy: "timestamp_watermark"
  watermark_column: "ModifiedDate"
  watermark_delay: "2 hours"
  batch_size: 100000
  max_parallel_connections: 8
  timeout_minutes: 60
  retry_attempts: 3
  
# Data Quality Framework
data_quality_checks:
  bronze_layer:
    row_count_validation:
      min_rows: 1000
      max_variance: 0.1
    freshness_check:
      max_age_hours: 6
    schema_validation:
      enforce_schema: true
      allow_nullable_changes: false
      
  silver_layer:
    referential_integrity:
      - child_table: "fact_orders"
        parent_table: "dim_customers"
        foreign_key: "customer_id"
        parent_key: "customer_id"
    business_rules:
      - rule: "order_total_positive"
        sql: "order_total > 0"
        severity: "error"
      - rule: "valid_order_date"
        sql: "order_date >= '2020-01-01' AND order_date <= CURRENT_DATE"
        severity: "warning"
        
  gold_layer:
    aggregation_validation:
      - metric: "total_revenue"
        comparison: "sum(silver_layer.order_total)"
        tolerance: 0.01
    business_kpi_checks:
      - kpi: "daily_revenue_growth"
        rule: "revenue_growth_rate BETWEEN -0.5 AND 2.0"
        alert_threshold: "revenue_growth_rate < -0.2"

# Performance Optimization
performance_optimization:
  bronze_layer:
    partitioning: "PARTITIONED BY (DATE(modified_date))"
    z_order: ["customer_id", "order_date"]
    optimize_write: true
    auto_compact: true
    
  silver_layer:
    partitioning: "PARTITIONED BY (DATE(order_date))"
    z_order: ["customer_id", "order_date"]
    bloom_filters: ["customer_id", "order_number"]
    
  gold_layer:
    partitioning: "PARTITIONED BY (order_date_month)"
    z_order: ["customer_id"]
    liquid_clustering: ["customer_id", "order_date_month"]

# Monitoring and Alerting
monitoring:
  data_freshness:
    alert_after_hours: 4
    critical_after_hours: 8
  processing_time:
    expected_duration_minutes: 30
    alert_after_minutes: 45
  data_quality:
    quarantine_threshold: 0.05
    alert_on_quality_degradation: true
  
# Security and Compliance
security:
  pii_fields:
    - "customers.email"
    - "customers.phone"
    - "customers.first_name"
    - "customers.last_name"
  masking_rules:
    non_production:
      email: "hash_email(email)"
      phone: "mask_phone(phone)"
      names: "anonymize_name(first_name, last_name)"
  access_control:
    bronze_layer: "data_engineers"
    silver_layer: "data_analysts, data_engineers"
    gold_layer: "business_users, data_analysts, data_engineers"
  retention_policy:
    bronze: "3 years"
    silver: "7 years"
    gold: "10 years"

# Deployment Configuration
deployment:
  environment_promotion:
    dev:
      full_refresh: true
      row_limit: 100000
    test:
      full_refresh: false
      data_mask: true
    prod:
      full_refresh: false
      data_mask: false
  rollback_strategy:
    backup_retention_days: 7
    rollback_validation: true
```

---

## Example 2: Salesforce CRM API Integration

**User Request:**
```
Create SaaS API source mapping for: Salesforce CRM integration

API Details:
- Platform: Salesforce
- API Version: v57.0
- Authentication: OAuth2 with refresh tokens
- Rate Limits: 5000 requests per hour
- Data Objects: Accounts, Contacts, Opportunities, Leads, Cases

Business Context:
- Use Case: Sales and customer service analytics
- Critical Data: Account hierarchy, opportunity pipeline, case resolution
- Integration Frequency: Every 2 hours for critical objects
- Historical Data: 5 years of historical data for initial load

Technical Requirements:
- Incremental Strategy: LastModifiedDate field
- Error Handling: Retry with exponential backoff
- Pagination: Handle large result sets with cursor-based pagination
- Webhook Support: Real-time alerts for high-value opportunities
```

**Source Mapper Response:**
```yaml
# Salesforce CRM API Source Mapping
source_name: salesforce_crm
source_type: saas_api
source_system: "Salesforce CRM - Production Org"
business_domain: "Sales and Customer Service"

# API Connection Configuration
connection_details:
  base_url: "https://{{SALESFORCE_INSTANCE}}.salesforce.com/services/data/v57.0"
  authentication:
    type: "oauth2"
    grant_type: "password"
    token_url: "https://{{SALESFORCE_INSTANCE}}.salesforce.com/services/oauth2/token"
    client_id: "{{SALESFORCE_CLIENT_ID}}"
    client_secret: "{{SECRET:KeyVault:salesforce-client-secret}}"
    username: "{{SALESFORCE_USERNAME}}"
    password: "{{SECRET:KeyVault:salesforce-password}}"
    security_token: "{{SECRET:KeyVault:salesforce-security-token}}"
    refresh_token_handling: true
    token_refresh_buffer_minutes: 10
  
  rate_limiting:
    requests_per_hour: 5000
    burst_limit: 100
    retry_strategy: "exponential_backoff"
    max_retries: 3
    backoff_multiplier: 2
    
  pagination:
    method: "cursor_based"
    page_size: 2000
    max_pages: 1000

# Medallion Architecture Mapping
destination_layers:
  bronze:
    schema: "bronze_salesforce"
    load_strategy: "incremental_api"
    
    api_endpoints:
      accounts:
        endpoint: "/sobjects/Account"
        method: "GET"
        destination_table: "bronze_salesforce.accounts"
        incremental_field: "LastModifiedDate"
        soql_query: >
          SELECT Id, Name, Type, Industry, AnnualRevenue, NumberOfEmployees,
                 BillingStreet, BillingCity, BillingState, BillingPostalCode, BillingCountry,
                 Phone, Website, Description, OwnerId, CreatedDate, LastModifiedDate,
                 ParentId, AccountSource, Rating
          FROM Account
          WHERE LastModifiedDate >= {watermark}
          ORDER BY LastModifiedDate
        schema_mapping:
          Id: "account_id:string:not_null"
          Name: "account_name:string:not_null"
          Type: "account_type:string:nullable"
          Industry: "industry:string:nullable"
          AnnualRevenue: "annual_revenue:decimal(15,2):nullable"
          NumberOfEmployees: "employee_count:int:nullable"
          BillingStreet: "billing_street:string:nullable"
          BillingCity: "billing_city:string:nullable"
          BillingState: "billing_state:string:nullable"
          BillingPostalCode: "billing_postal_code:string:nullable"
          BillingCountry: "billing_country:string:nullable"
          Phone: "phone:string:nullable"
          Website: "website:string:nullable"
          Description: "description:string:nullable"
          OwnerId: "owner_id:string:nullable"
          CreatedDate: "created_date:timestamp:not_null"
          LastModifiedDate: "last_modified_date:timestamp:not_null"
          ParentId: "parent_account_id:string:nullable"
          AccountSource: "account_source:string:nullable"
          Rating: "account_rating:string:nullable"
        audit_columns:
          _bronze_load_timestamp: "current_timestamp()"
          _bronze_api_call_id: "uuid()"
          _bronze_source_system: "'salesforce_crm'"
          
      contacts:
        endpoint: "/sobjects/Contact"
        method: "GET"
        destination_table: "bronze_salesforce.contacts"
        incremental_field: "LastModifiedDate"
        soql_query: >
          SELECT Id, AccountId, FirstName, LastName, Email, Phone, MobilePhone,
                 Title, Department, MailingStreet, MailingCity, MailingState,
                 MailingPostalCode, MailingCountry, LeadSource, OwnerId,
                 CreatedDate, LastModifiedDate, HasOptedOutOfEmail
          FROM Contact
          WHERE LastModifiedDate >= {watermark}
          ORDER BY LastModifiedDate
        schema_mapping:
          Id: "contact_id:string:not_null"
          AccountId: "account_id:string:nullable"
          FirstName: "first_name:string:nullable"
          LastName: "last_name:string:not_null"
          Email: "email:string:nullable"
          Phone: "phone:string:nullable"
          MobilePhone: "mobile_phone:string:nullable"
          Title: "title:string:nullable"
          Department: "department:string:nullable"
          MailingStreet: "mailing_street:string:nullable"
          MailingCity: "mailing_city:string:nullable"
          MailingState: "mailing_state:string:nullable"
          MailingPostalCode: "mailing_postal_code:string:nullable"
          MailingCountry: "mailing_country:string:nullable"
          LeadSource: "lead_source:string:nullable"
          OwnerId: "owner_id:string:nullable"
          CreatedDate: "created_date:timestamp:not_null"
          LastModifiedDate: "last_modified_date:timestamp:not_null"
          HasOptedOutOfEmail: "email_opt_out:boolean:nullable"
          
      opportunities:
        endpoint: "/sobjects/Opportunity"
        method: "GET"
        destination_table: "bronze_salesforce.opportunities"
        incremental_field: "LastModifiedDate"
        high_value_threshold: 50000
        soql_query: >
          SELECT Id, AccountId, Name, StageName, Amount, Probability, CloseDate,
                 Type, NextStep, LeadSource, ForecastCategory, OwnerId,
                 CreatedDate, LastModifiedDate, IsClosed, IsWon, Description,
                 CampaignId, HasOpportunityLineItems
          FROM Opportunity
          WHERE LastModifiedDate >= {watermark}
          ORDER BY LastModifiedDate
        schema_mapping:
          Id: "opportunity_id:string:not_null"
          AccountId: "account_id:string:nullable"
          Name: "opportunity_name:string:not_null"
          StageName: "stage_name:string:not_null"
          Amount: "amount:decimal(15,2):nullable"
          Probability: "probability:decimal(5,2):nullable"
          CloseDate: "close_date:date:nullable"
          Type: "opportunity_type:string:nullable"
          NextStep: "next_step:string:nullable"
          LeadSource: "lead_source:string:nullable"
          ForecastCategory: "forecast_category:string:nullable"
          OwnerId: "owner_id:string:nullable"
          CreatedDate: "created_date:timestamp:not_null"
          LastModifiedDate: "last_modified_date:timestamp:not_null"
          IsClosed: "is_closed:boolean:not_null"
          IsWon: "is_won:boolean:not_null"
          Description: "description:string:nullable"
          CampaignId: "campaign_id:string:nullable"
          HasOpportunityLineItems: "has_line_items:boolean:nullable"
        real_time_alerts:
          - condition: "Amount > 50000 AND StageName = 'Closed Won'"
            alert_type: "high_value_win"
            webhook_url: "{{WEBHOOK_URL_HIGH_VALUE}}"
          - condition: "Amount > 100000 AND StageName = 'Proposal/Price Quote'"
            alert_type: "large_deal_at_risk"
            webhook_url: "{{WEBHOOK_URL_LARGE_DEALS}}"

  silver:
    schema: "silver_salesforce"
    
    tables:
      dim_accounts:
        source_table: "bronze_salesforce.accounts"
        destination_table: "silver_salesforce.dim_accounts"
        scd_type: "SCD2"
        scd_columns: ["account_name", "account_type", "industry", "annual_revenue"]
        transformation_rules:
          - "Standardize industry classification"
          - "Clean and validate address components"
          - "Create account hierarchy relationships"
          - "Derive account size segments"
        schema_mapping:
          account_id: "account_id:string:not_null"
          account_name: "TRIM(account_name):string:not_null"
          account_type: "CASE WHEN account_type IS NULL THEN 'Unknown' ELSE account_type END:string"
          industry_standardized: "standardize_industry(industry):string"
          annual_revenue: "annual_revenue:decimal(15,2):nullable"
          employee_count: "employee_count:int:nullable"
          account_size_segment: >
            CASE 
              WHEN annual_revenue >= 1000000000 THEN 'Enterprise'
              WHEN annual_revenue >= 100000000 THEN 'Large'
              WHEN annual_revenue >= 10000000 THEN 'Mid-Market'
              WHEN annual_revenue >= 1000000 THEN 'Small'
              ELSE 'Unknown'
            END:string
          billing_address: "CONCAT_WS(', ', billing_street, billing_city, billing_state, billing_postal_code):string"
          billing_country: "UPPER(TRIM(billing_country)):string"
          phone_standardized: "standardize_phone(phone):string"
          website_clean: "clean_website_url(website):string"
          parent_account_id: "parent_account_id:string:nullable"
          account_source: "account_source:string:nullable"
          account_rating: "account_rating:string:nullable"
          created_date: "created_date:timestamp:not_null"
          last_modified_date: "last_modified_date:timestamp:not_null"
          effective_start_date: "current_timestamp():timestamp"
          effective_end_date: "null:timestamp"
          is_current: "true:boolean"
        data_quality_rules:
          - field: "account_name"
            rule: "not_null_and_not_empty"
            action: "quarantine"
          - field: "annual_revenue"
            rule: "greater_than_or_equal_to_zero"
            action: "alert"
          - field: "employee_count"
            rule: "greater_than_zero"
            action: "alert"
            
      fact_opportunities:
        source_tables:
          - "bronze_salesforce.opportunities"
          - "bronze_salesforce.accounts"
        destination_table: "silver_salesforce.fact_opportunities"
        join_logic: "opportunities o LEFT JOIN accounts a ON o.account_id = a.account_id"
        transformation_rules:
          - "Calculate opportunity metrics and age"
          - "Derive sales stage progression"
          - "Create opportunity scoring"
        schema_mapping:
          opportunity_id: "o.opportunity_id:string:not_null"
          account_id: "o.account_id:string:nullable"
          opportunity_name: "TRIM(o.opportunity_name):string:not_null"
          stage_name: "o.stage_name:string:not_null"
          amount: "o.amount:decimal(15,2):nullable"
          probability: "o.probability:decimal(5,2):nullable"
          close_date: "o.close_date:date:nullable"
          opportunity_type: "COALESCE(o.opportunity_type, 'Unknown'):string"
          lead_source: "o.lead_source:string:nullable"
          forecast_category: "o.forecast_category:string:nullable"
          is_closed: "o.is_closed:boolean:not_null"
          is_won: "o.is_won:boolean:not_null"
          created_date: "o.created_date:timestamp:not_null"
          last_modified_date: "o.last_modified_date:timestamp:not_null"
          opportunity_age_days: "DATEDIFF(CURRENT_DATE, DATE(o.created_date)):int"
          days_to_close: "CASE WHEN o.is_closed THEN DATEDIFF(DATE(o.last_modified_date), DATE(o.created_date)) ELSE NULL END:int"
          weighted_amount: "COALESCE(o.amount * o.probability / 100, 0):decimal(15,2)"
          account_annual_revenue: "a.annual_revenue:decimal(15,2):nullable"
          deal_size_category: >
            CASE 
              WHEN o.amount >= 1000000 THEN 'Large'
              WHEN o.amount >= 100000 THEN 'Medium'
              WHEN o.amount >= 10000 THEN 'Small'
              ELSE 'Micro'
            END:string

  gold:
    schema: "gold_salesforce"
    
    tables:
      sales_pipeline_summary:
        source_table: "silver_salesforce.fact_opportunities"
        destination_table: "gold_salesforce.sales_pipeline_summary"
        aggregation_level: "stage_name, close_date_month"
        business_metrics:
          opportunity_count: "COUNT(opportunity_id)"
          total_pipeline_value: "SUM(amount)"
          weighted_pipeline_value: "SUM(weighted_amount)"
          avg_deal_size: "AVG(amount)"
          avg_probability: "AVG(probability)"
          avg_opportunity_age: "AVG(opportunity_age_days)"
          closed_won_count: "SUM(CASE WHEN is_won = true THEN 1 ELSE 0 END)"
          closed_lost_count: "SUM(CASE WHEN is_closed = true AND is_won = false THEN 1 ELSE 0 END)"
          win_rate: "CASE WHEN SUM(CASE WHEN is_closed = true THEN 1 ELSE 0 END) > 0 THEN SUM(CASE WHEN is_won = true THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN is_closed = true THEN 1 ELSE 0 END) ELSE 0 END"
        refresh_frequency: "every_2_hours"
        
      account_health_metrics:
        source_tables:
          - "silver_salesforce.dim_accounts"
          - "silver_salesforce.fact_opportunities"
        destination_table: "gold_salesforce.account_health_metrics"
        aggregation_level: "account_id"
        business_metrics:
          total_opportunities: "COUNT(opportunity_id)"
          total_opportunity_value: "SUM(amount)"
          open_opportunities: "SUM(CASE WHEN is_closed = false THEN 1 ELSE 0 END)"
          closed_won_opportunities: "SUM(CASE WHEN is_won = true THEN 1 ELSE 0 END)"
          last_opportunity_date: "MAX(created_date)"
          avg_deal_size: "AVG(amount)"
          account_win_rate: "CASE WHEN SUM(CASE WHEN is_closed = true THEN 1 ELSE 0 END) > 0 THEN SUM(CASE WHEN is_won = true THEN 1 ELSE 0 END) * 100.0 / SUM(CASE WHEN is_closed = true THEN 1 ELSE 0 END) ELSE 0 END"
          days_since_last_activity: "DATEDIFF(CURRENT_DATE, MAX(last_modified_date))"
        health_scoring:
          engagement_score: >
            CASE 
              WHEN days_since_last_activity <= 30 THEN 100
              WHEN days_since_last_activity <= 60 THEN 75
              WHEN days_since_last_activity <= 90 THEN 50
              WHEN days_since_last_activity <= 180 THEN 25
              ELSE 0
            END
          opportunity_score: >
            CASE 
              WHEN open_opportunities >= 3 THEN 100
              WHEN open_opportunities = 2 THEN 75
              WHEN open_opportunities = 1 THEN 50
              ELSE 25
            END
          overall_health_score: "(engagement_score + opportunity_score) / 2"

# Processing Configuration
processing_config:
  schedule: "every_2_hours"
  initial_load:
    historical_months: 60
    batch_size: 1000
    parallel_objects: 5
  incremental_load:
    watermark_strategy: "last_modified_date"
    overlap_minutes: 60
    batch_size: 2000
    max_concurrent_requests: 10
  error_handling:
    retry_strategy: "exponential_backoff"
    max_retries: 3
    backoff_multiplier: 2
    dead_letter_queue: true
    
# Real-time Processing
real_time_processing:
  webhook_endpoints:
    high_value_opportunities:
      url: "/webhooks/salesforce/high-value-opps"
      authentication: "bearer_token"
      processing_logic: "immediate_alert_to_sales_team"
    large_deals:
      url: "/webhooks/salesforce/large-deals"
      authentication: "bearer_token"
      processing_logic: "executive_notification"
  streaming_integration:
    change_data_capture: true
    platform_events: true
    buffer_size: 1000
    flush_interval_seconds: 30

# Data Quality Framework
data_quality_checks:
  api_response_validation:
    - check: "http_status_success"
      expected: [200, 201]
      action: "retry"
    - check: "json_schema_validation"
      schema_file: "salesforce_api_schemas.json"
      action: "quarantine"
  
  bronze_layer:
    duplicate_detection:
      - table: "accounts"
        key_columns: ["account_id"]
        action: "deduplicate_keep_latest"
    referential_integrity:
      - child_table: "contacts"
        parent_table: "accounts"
        foreign_key: "account_id"
        action: "quarantine_orphans"
    
  silver_layer:
    business_rules:
      - rule: "opportunity_amount_validation"
        sql: "amount IS NULL OR amount >= 0"
        severity: "error"
      - rule: "close_date_future_validation"
        sql: "close_date IS NULL OR close_date >= created_date"
        severity: "warning"
      - rule: "probability_range_validation"
        sql: "probability IS NULL OR (probability >= 0 AND probability <= 100)"
        severity: "error"

# Security and Compliance
security:
  field_level_security:
    sensitive_fields:
      - "accounts.annual_revenue"
      - "contacts.email"
      - "contacts.phone"
      - "contacts.mobile_phone"
  access_control:
    bronze_layer: "salesforce_integration_service"
    silver_layer: "data_analysts, sales_ops"
    gold_layer: "business_users, executives"
  audit_logging:
    api_calls: true
    data_access: true
    transformations: true
  compliance:
    gdpr_compliance: true
    data_retention_policy: "7_years"
    right_to_be_forgotten: true

# Monitoring and Alerting
monitoring:
  api_health:
    rate_limit_monitoring: true
    response_time_threshold_ms: 5000
    error_rate_threshold: 0.05
  data_freshness:
    expected_delay_minutes: 120
    alert_threshold_minutes: 180
    critical_threshold_minutes: 360
  processing_metrics:
    throughput_monitoring: true
    queue_depth_alerts: true
    transformation_success_rate: true
  business_metrics:
    opportunity_creation_rate: true
    large_deal_alerts: true
    pipeline_velocity_tracking: true
```

---

*These examples demonstrate comprehensive source mapping configurations for both SQL and SaaS API sources, showing the full medallion architecture implementation with data quality, security, and monitoring considerations.*