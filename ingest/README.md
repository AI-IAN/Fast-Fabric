# Fabric Fast-Track Data Ingestion Kit

This directory contains production-ready templates for ingesting data from various sources into Microsoft Fabric Bronze Delta tables.

## 🚀 Quick Start

### 1. Generate Sample Data (Development)
```bash
python mock_data_generator.py
```
This creates realistic sample data in `./mock_data/` for testing without real data sources.

### 2. Deploy Dataflow Gen2 Templates
- Import JSON templates into Fabric workspace
- Configure parameters for your data sources
- Schedule dataflows for regular execution

### 3. Run Spark Notebook for Bronze Tables
- Upload `ingest_delta.py` to Fabric Lakehouse
- Configure parameters and execute
- Creates Delta tables in Bronze layer

## 📁 File Structure

```
ingest/
├── dataflow_sql_template.json      # SQL Server/ODBC ingestion template
├── dataflow_saas_template.json     # SaaS API ingestion template  
├── dataflow_file_template.json     # File-based ingestion template
├── ingest_delta.py                 # Spark notebook for Bronze Delta tables
├── mock_data_generator.py          # Sample data generator
├── config_sql_sources.json         # SQL database configurations
├── config_saas_sources.json        # SaaS API configurations
├── config_file_sources.json        # File source configurations
├── requirements.txt                # Python dependencies
└── README.md                       # This documentation
```

## 🔄 Data Source Types

### SQL Databases
**Supported**: SQL Server, PostgreSQL, MySQL, Oracle
**Template**: `dataflow_sql_template.json`
**Configuration**: `config_sql_sources.json`

**Features**:
- Incremental loading with timestamp columns
- SQL Server Change Tracking support
- Connection string templates
- Data quality rules
- Key Vault integration for credentials

**Example Configuration**:
```json
{
  "SQL_SERVER_NAME": "myserver.database.windows.net",
  "SQL_DATABASE_NAME": "MyDatabase", 
  "SOURCE_TABLE_NAME": "dbo.customers",
  "INCREMENTAL_COLUMN": "ModifiedDate"
}
```

### SaaS APIs
**Supported**: Salesforce, HubSpot, Stripe, Dynamics 365
**Template**: `dataflow_saas_template.json`
**Configuration**: `config_saas_sources.json`

**Features**:
- OAuth2 and API key authentication
- Rate limiting and retry logic
- Incremental API calls
- JSON response transformation
- Pagination handling

**Example Configuration**:
```json
{
  "API_BASE_URL": "https://api.salesforce.com/v1",
  "API_ENDPOINT": "/customers",
  "API_KEY": "{{SECRET:KeyVault:salesforce-key}}"
}
```

### File Sources
**Supported**: CSV, Excel, JSON, Parquet, XML
**Template**: `dataflow_file_template.json`
**Configuration**: `config_file_sources.json`

**Features**:
- Multiple file format support
- File pattern matching
- Schema inference
- Archive strategies
- Encoding detection

**Example Configuration**:
```json
{
  "FILE_PATH": "abfss://landing@storage.dfs.core.windows.net/crm/customers.csv",
  "FILE_TYPE": "CSV",
  "CSV_DELIMITER": ","
}
```

## 🏗️ Architecture

### Medallion Architecture
```
Landing Zone → Bronze Layer → Silver Layer → Gold Layer
     ↓              ↓             ↓            ↓
Raw Files    Delta Tables   Clean Data   Business KPIs
```

### Data Flow
1. **Dataflow Gen2**: Extracts data from sources
2. **Landing Zone**: Temporary storage for raw data  
3. **Spark Notebook**: Transforms and loads to Bronze Delta
4. **Bronze Tables**: Partitioned Delta tables with audit columns

### Key Features
- **Incremental Loading**: Only process new/changed data
- **Data Quality**: Built-in validation rules
- **Audit Trail**: LoadDate, SourceSystem, RecordHash columns
- **Schema Evolution**: Automatic schema merging
- **Error Handling**: Retry logic and dead letter queues

## 📊 Sample Data

The mock data generator creates realistic datasets:

### Customer Data (1,000 records)
- CustomerID, Name, Email, Phone, Address
- Industry, CompanySize, AnnualRevenue
- CreatedDate, ModifiedDate, IsActive

### Sales Data (5,000 records)  
- SaleID, CustomerID, ProductID, ProductName
- Quantity, UnitPrice, TotalAmount
- SaleDate, SalesRep, Region, Status

### Financial Data (24 months)
- RecordID, Date, Account, AccountCode
- Amount, Currency, Department
- CreatedBy, ModifiedDate

### API Response Formats
- Wrapped in standard API envelope
- Pagination metadata included
- Error handling examples

## 🔧 Configuration

### Environment Variables
Create `.env` file or use Key Vault:
```bash
# Storage Account
STORAGE_ACCOUNT_NAME=mystorageaccount

# SQL Connections
SQL_SERVER_NAME=myserver.database.windows.net
SQL_USERNAME=fabricuser
SQL_PASSWORD=secretpassword

# API Keys  
SALESFORCE_CLIENT_ID=your_client_id
HUBSPOT_ACCESS_TOKEN=your_token
```

### Dataflow Parameters
Each template supports parameterization:
- **Source Configuration**: Connection strings, endpoints
- **Transformation Rules**: Column mappings, data types
- **Quality Rules**: Validation, filtering, cleansing
- **Destination Settings**: Delta table paths, partitioning

### Spark Configuration
For `ingest_delta.py` notebook:
```python
# Widget parameters
dbutils.widgets.text("storage_account_name", "mystorageaccount")
dbutils.widgets.text("source_system", "CRM_System") 
dbutils.widgets.text("table_name", "customers")
```

## 🎯 Production Deployment

### Prerequisites
1. Microsoft Fabric workspace with Lakehouse
2. Storage account with containers: landing, bronze, silver, gold
3. Key Vault for sensitive credentials
4. Appropriate RBAC permissions

### Deployment Steps

1. **Create Storage Containers**:
   ```bash
   az storage container create --name landing --account-name mystorageaccount
   az storage container create --name bronze --account-name mystorageaccount  
   az storage container create --name silver --account-name mystorageaccount
   az storage container create --name gold --account-name mystorageaccount
   ```

2. **Store Secrets in Key Vault**:
   ```bash
   az keyvault secret set --vault-name myvault --name sql-password --value "mypassword"
   az keyvault secret set --vault-name myvault --name api-key --value "myapikey"
   ```

3. **Import Dataflow Templates**:
   - Open Fabric workspace
   - Create new Dataflow Gen2
   - Import JSON template
   - Configure parameters
   - Test and publish

4. **Deploy Spark Notebook**:
   - Upload `ingest_delta.py` to Lakehouse
   - Configure notebook parameters
   - Create scheduled job
   - Monitor execution

### Performance Tuning

**Dataflow Gen2**:
- Use incremental loading where possible
- Optimize API pagination size
- Configure parallel processing

**Spark Notebook**:
- Partition by date columns
- Use appropriate cluster size
- Enable adaptive query execution
- Optimize Delta table layout

### Monitoring

**Key Metrics**:
- Records processed per hour
- Data quality failure rate  
- Pipeline execution time
- Storage usage growth

**Alerting**:
- Pipeline failures
- Data quality thresholds
- API rate limit warnings
- Storage capacity alerts

## 🔍 Troubleshooting

### Common Issues

**Connection Failures**:
- Verify credentials in Key Vault
- Check network connectivity
- Validate connection strings

**Schema Conflicts**:
- Enable `mergeSchema` option
- Review column data types
- Check for reserved keywords

**Performance Issues**:
- Increase cluster resources
- Optimize partition strategy
- Review data quality rules

**API Rate Limits**:
- Implement exponential backoff
- Reduce request frequency
- Use bulk endpoints when available

### Debug Mode
Enable detailed logging:
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.logLevel", "INFO")
```

## 📚 Additional Resources

- [Fabric Dataflow Gen2 Documentation](https://docs.microsoft.com/fabric/dataflow-gen2)
- [Delta Lake Documentation](https://delta.io/)
- [Spark SQL Reference](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Data Quality Best Practices](../docs/data-quality-guide.md)

## 🤝 Support

For issues and questions:
1. Check [Gotchas & Lessons](../docs/Gotchas.md)
2. Review [Project Tracker](../PROJECT_TRACKER.md)
3. Submit issue to project repository

---
*Designed for zero-configuration data ingestion with production-grade quality*
EOF < /dev/null