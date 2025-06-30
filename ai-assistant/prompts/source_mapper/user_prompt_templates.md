# Source Mapper User Prompt Templates

## Template Categories

### 1. SQL Database Source Mapping

```
Map SQL database source to medallion architecture: [DATABASE_DESCRIPTION]

Source Details:
- Database Type: [SQL Server/PostgreSQL/MySQL/Oracle]
- Database Name: [Database identifier]
- Key Tables: [List of important tables to map]
- Business Context: [What business process this data supports]
- Data Volume: [Approximate row counts and growth rate]
- Update Frequency: [Real-time/Hourly/Daily/Weekly]

Schema Information:
- Primary Keys: [List primary key columns]
- Foreign Keys: [Important relationships between tables]
- Incremental Columns: [Timestamp/ID columns for incremental loading]
- Business Keys: [Natural keys used by business users]

Requirements:
- Load Pattern: [Full/Incremental/Real-time]
- SLA: [Data freshness requirements]
- Transformations: [Any required data transformations]
- Quality Rules: [Data validation requirements]

Example:
"Map SQL database source: Production ERP system
- Database Type: SQL Server
- Database Name: ProductionERP_DB
- Key Tables: Customers, Orders, OrderItems, Products
- Business Context: Sales order processing and customer management
- Data Volume: 10M customers, 50M orders (growing 5% monthly)
- Update Frequency: Real-time for orders, daily for customers"
```

### 2. SaaS API Source Mapping

```
Create SaaS API source mapping for: [SAAS_PLATFORM]

API Details:
- Platform: [Salesforce/HubSpot/Stripe/Dynamics/Other]
- API Version: [Specific version if known]
- Authentication: [OAuth2/API Key/Service Principal]
- Rate Limits: [Requests per hour/day limitations]
- Data Objects: [List of objects/entities to extract]

Business Context:
- Use Case: [CRM/Marketing/Finance/Operations]
- Critical Data: [Most important data elements]
- Integration Frequency: [How often to sync data]
- Historical Data: [How much history to load initially]

Technical Requirements:
- Incremental Strategy: [API field for incremental loading]
- Error Handling: [How to handle API failures]
- Pagination: [Large dataset handling requirements]
- Webhook Support: [Real-time event processing needs]

Example:
"Create SaaS API source mapping for: Salesforce CRM
- Platform: Salesforce
- API Version: v57.0
- Authentication: OAuth2 with refresh tokens
- Rate Limits: 5000 requests/hour
- Data Objects: Accounts, Contacts, Opportunities, Leads, Cases"
```

### 3. File Source Mapping

```
Design file source mapping for: [FILE_SOURCE_DESCRIPTION]

File Details:
- File Type: [CSV/Excel/JSON/Parquet/Delta]
- Location: [Azure Blob/ADLS/SharePoint/FTP]
- File Pattern: [Naming convention and frequency]
- Size: [Typical file sizes and counts]
- Schema: [Known schema or sample structure]

Processing Requirements:
- Validation: [Schema validation and data quality checks]
- Archive: [File retention and archive policy]
- Error Handling: [Invalid file processing strategy]
- Transformation: [Required data transformations]
- Partitioning: [How to organize data in lakehouse]

Business Context:
- Source System: [Where files originate]
- Business Process: [What process generates these files]
- Consumers: [Who uses this data downstream]
- SLA: [Processing time requirements]

Example:
"Design file source mapping for: Daily sales export files
- File Type: CSV with headers
- Location: Azure Blob Storage /sales-exports/
- File Pattern: sales_YYYYMMDD.csv (daily at 6 AM)
- Size: 100MB files, ~500K rows each
- Schema: 15 columns including SaleDate, CustomerID, Amount"
```

### 4. Streaming Source Mapping

```
Configure streaming source mapping for: [STREAMING_SOURCE]

Streaming Details:
- Source Type: [Event Hubs/IoT Hub/Kafka/Service Bus]
- Event Format: [JSON/Avro/CSV/Binary]
- Event Rate: [Messages per second/minute]
- Retention: [How long events are available]
- Partitioning: [Event partitioning strategy]

Processing Requirements:
- Window Type: [Tumbling/Sliding/Session windows]
- Aggregation Level: [Real-time/Micro-batch/Batch]
- State Management: [Checkpointing and recovery]
- Late Data: [How to handle out-of-order events]
- Scaling: [Auto-scaling requirements]

Business Context:
- Use Case: [Real-time monitoring/Alerting/Analytics]
- Latency: [Processing latency requirements]
- Reliability: [Delivery guarantees needed]
- Integration: [How streaming connects to batch data]

Example:
"Configure streaming source mapping for: IoT sensor telemetry
- Source Type: IoT Hub with device-to-cloud messages
- Event Format: JSON with timestamp, deviceId, sensorData
- Event Rate: 10,000 messages per minute across 500 devices
- Retention: 7 days in IoT Hub
- Partitioning: By deviceId for parallel processing"
```

### 5. Multi-Source Integration Mapping

```
Design multi-source integration for: [INTEGRATION_SCENARIO]

Source Systems:
- Primary Source: [Main authoritative system]
- Secondary Sources: [Supporting systems with data]
- Integration Points: [How systems connect/overlap]
- Master Data: [Which system owns each data element]
- Conflict Resolution: [How to handle data conflicts]

Integration Strategy:
- Join Keys: [How to link data across sources]
- Timing: [Load sequence and dependencies]
- Validation: [Cross-system data validation]
- Lineage: [Track data flow across systems]
- Fallback: [Handling source system outages]

Business Requirements:
- Golden Record: [Single version of truth requirements]
- Data Governance: [Ownership and quality standards]
- Compliance: [Regulatory requirements across sources]
- Performance: [Integration processing SLA]

Example:
"Design multi-source integration for: Customer 360 view
- Primary Source: CRM system (Salesforce) for customer master
- Secondary Sources: ERP (orders), Support system (cases), Marketing (campaigns)
- Integration Points: CustomerID across all systems
- Master Data: CRM owns customer profile, ERP owns transaction history"
```

## Specialized Domain Templates

### E-commerce Data Integration

```
Create e-commerce data source mapping for: [E-COMMERCE_PLATFORM]

E-commerce Context:
- Platform: [Magento/Shopify/WooCommerce/Custom]
- Business Model: [B2B/B2C/Marketplace]
- Transaction Volume: [Orders per day/month]
- Product Catalog: [Number of SKUs and categories]
- Customer Base: [Active customer count]

Key Data Entities:
- Products: [Catalog, inventory, pricing]
- Customers: [Profiles, preferences, segmentation]
- Orders: [Transactions, line items, payments]
- Marketing: [Campaigns, promotions, attribution]
- Operations: [Shipping, returns, support]

Analytics Requirements:
- Real-time: [Inventory, fraud detection]
- Near real-time: [Recommendations, personalization]
- Batch: [Reporting, analytics, compliance]
- ML/AI: [Recommendation engines, demand forecasting]
```

### Financial Services Integration

```
Design financial services data mapping for: [FINANCIAL_SYSTEM]

Financial Context:
- System Type: [Core Banking/Trading/Risk/Compliance]
- Regulatory: [SOX/Basel III/GDPR/PCI compliance]
- Data Classification: [Public/Internal/Confidential/Restricted]
- Audit Requirements: [Transaction logging, immutable records]
- Real-time Needs: [Fraud detection, risk monitoring]

Key Data Categories:
- Transactional: [Payments, trades, positions]
- Customer: [KYC, profiles, relationships]
- Risk: [Credit scores, exposure, limits]
- Market: [Prices, rates, reference data]
- Regulatory: [Reporting, compliance, audit]

Security Requirements:
- Encryption: [Data masking, tokenization]
- Access Control: [Role-based, attribute-based]
- Monitoring: [Data access auditing]
- Retention: [Legal hold, archival policies]
```

### Healthcare Data Integration

```
Configure healthcare data source mapping for: [HEALTHCARE_SYSTEM]

Healthcare Context:
- System Type: [EMR/EHR/LIS/PACS/Claims]
- Compliance: [HIPAA/FDA/Clinical trial regulations]
- Data Types: [Clinical/Administrative/Financial/Research]
- Interoperability: [HL7 FHIR/CDA/DICOM standards]
- Patient Privacy: [PHI protection, consent management]

Clinical Data Categories:
- Patient Demographics: [Identity, insurance, contacts]
- Clinical Notes: [Encounters, procedures, diagnoses]
- Lab Results: [Tests, values, reference ranges]
- Medications: [Prescriptions, administration, reactions]
- Imaging: [Studies, reports, DICOM integration]

Analytics Use Cases:
- Population Health: [Outcomes, quality measures]
- Clinical Research: [Trial data, real-world evidence]
- Operations: [Resource utilization, efficiency]
- Financial: [Claims, reimbursement, costs]
```

## Quality and Validation Templates

### Data Quality Rule Definition

```
Define data quality rules for source mapping: [SOURCE_SYSTEM]

Quality Dimensions:
- Completeness: [Required fields, null value handling]
- Uniqueness: [Primary keys, duplicate detection]
- Validity: [Data types, format validation, ranges]
- Consistency: [Cross-field validation, referential integrity]
- Timeliness: [Data freshness, SLA monitoring]
- Accuracy: [Business rule validation, outlier detection]

Validation Rules:
- Field Level: [Individual column validations]
- Record Level: [Cross-field business rules]
- Table Level: [Aggregate validations, counts]
- Cross-System: [Referential integrity across sources]

Quality Actions:
- Accept: [Valid records proceed to silver layer]
- Quarantine: [Invalid records held for review]
- Reject: [Unrecoverable errors logged and discarded]
- Alert: [Quality threshold breaches trigger notifications]

Example:
"Define data quality rules for: Customer master data
- Completeness: CustomerID, Name, Email required (100%)
- Uniqueness: CustomerID must be unique across all records
- Validity: Email format regex, Phone number format
- Consistency: Country code matches address country"
```

### Performance Optimization Specification

```
Optimize source mapping performance for: [PERFORMANCE_SCENARIO]

Performance Context:
- Data Volume: [Current size and growth projections]
- Processing Window: [Available time for ETL processing]
- Concurrency: [Parallel processing requirements]
- Resource Constraints: [Compute, memory, network limits]
- SLA: [Processing time and data freshness requirements]

Optimization Strategies:
- Partitioning: [Date/hash/range partitioning strategy]
- Indexing: [Z-order, bloom filters, statistics]
- Compression: [Optimal compression for data types]
- Caching: [Hot data caching strategy]
- Parallelism: [Optimal degree of parallelism]

Monitoring Requirements:
- Metrics: [Processing time, throughput, error rates]
- Alerts: [Performance degradation thresholds]
- Dashboards: [Real-time monitoring views]
- Optimization: [Auto-scaling and tuning recommendations]

Example:
"Optimize source mapping performance for: High-volume transaction processing
- Data Volume: 50M transactions/day, growing 20% annually
- Processing Window: 4-hour batch window (2 AM - 6 AM)
- Concurrency: 16 parallel streams for optimal throughput
- SLA: All data available by 7 AM for business reporting"
```

## Integration Pattern Templates

### Master Data Management

```
Design master data mapping for: [MDM_SCENARIO]

Master Data Context:
- Data Domain: [Customer/Product/Location/Account/Employee]
- Source Systems: [List of systems contributing data]
- Golden Record Strategy: [Consolidation and survivorship rules]
- Data Governance: [Stewardship and quality ownership]
- Change Management: [How updates propagate across systems]

Mapping Strategy:
- Source Priority: [Ranking of authoritative sources]
- Matching Rules: [How to identify same entities across sources]
- Merge Logic: [Field-level survivorship rules]
- Hierarchy Management: [Parent-child relationships]
- Versioning: [Historical tracking of changes]

Quality Framework:
- Data Profiling: [Understanding source data quality]
- Standardization: [Name, address, phone normalization]
- Validation: [Business rule enforcement]
- Monitoring: [Quality score tracking and alerting]

Example:
"Design master data mapping for: Customer MDM across CRM and ERP
- Data Domain: Customer master data consolidation
- Source Systems: Salesforce (CRM), SAP (ERP), Support system
- Golden Record Strategy: CRM wins for contact info, ERP wins for financial
- Matching Rules: Email exact match, name + address fuzzy match"
```

### Real-time Integration

```
Configure real-time integration mapping for: [REAL_TIME_SCENARIO]

Real-time Context:
- Latency Requirement: [Sub-second/Seconds/Minutes]
- Event Volume: [Events per second/minute]
- Processing Type: [Simple routing/Transformation/Aggregation]
- Reliability: [At-least-once/Exactly-once delivery]
- State Management: [Stateless/Stateful processing]

Architecture Pattern:
- Event Streaming: [Event sourcing, CQRS, messaging]
- Micro-batching: [Small batch processing for efficiency]
- Lambda Architecture: [Speed + batch layer combination]
- Kappa Architecture: [Streaming-only processing]

Integration Points:
- Source Events: [Event schema and partitioning]
- Processing Logic: [Transformation and enrichment]
- Destination: [Real-time analytics, operational systems]
- Monitoring: [Latency, throughput, error tracking]

Example:
"Configure real-time integration for: Fraud detection pipeline
- Latency Requirement: <100ms for transaction scoring
- Event Volume: 50,000 transactions per minute
- Processing Type: Real-time enrichment with ML model scoring
- Reliability: Exactly-once processing for financial accuracy"
```

## Usage Instructions

1. **Select Template**: Choose the template matching your source system type
2. **Provide Context**: Fill in all bracketed placeholders with specific details
3. **Add Requirements**: Include any special business or technical requirements
4. **Specify Quality**: Define data quality and validation requirements
5. **Submit Request**: Send completed prompt to Source Mapper
6. **Review Output**: Validate the generated YAML configuration
7. **Iterate**: Refine based on technical review and testing

## Best Practices

- **Complete Information**: Provide comprehensive source system details
- **Business Context**: Explain how the data supports business processes
- **Quality Requirements**: Specify data validation and quality standards
- **Performance Needs**: Include volume, frequency, and SLA requirements
- **Security Considerations**: Mention compliance and security requirements
- **Integration Patterns**: Describe how this source relates to others

---

*Use these templates to generate comprehensive source mappings for your Fabric Fast-Track data integration projects.*