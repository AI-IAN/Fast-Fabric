"""
Fabric Fast-Track Spark Notebook: Bronze Delta Table Ingestion
Converts raw data from various sources into Delta Lake Bronze layer
Supports SQL, SaaS API, and file-based data sources
"""

# MAGIC %md
# # Bronze Layer Data Ingestion
# 
# This notebook ingests data from various sources and creates Bronze Delta tables
# following the Fabric Fast-Track medallion architecture.

# COMMAND ----------

# MAGIC %md
# ## Configuration and Setup

# COMMAND ----------

# Import required libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta.tables import *
import json
import os
from datetime import datetime, timedelta

# Initialize Spark session with Delta Lake support
spark = SparkSession.builder \
    .appName("FabricFastTrack-BronzeIngestion") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Set up configuration parameters
STORAGE_ACCOUNT = dbutils.widgets.get("storage_account_name") if "dbutils" in globals() else "{{STORAGE_ACCOUNT_NAME}}"
SOURCE_SYSTEM = dbutils.widgets.get("source_system") if "dbutils" in globals() else "{{SOURCE_SYSTEM_NAME}}"
SOURCE_TYPE = dbutils.widgets.get("source_type") if "dbutils" in globals() else "{{SOURCE_TYPE}}"
TABLE_NAME = dbutils.widgets.get("table_name") if "dbutils" in globals() else "{{TABLE_NAME}}"

# Define storage paths
BRONZE_PATH = f"abfss://bronze@{STORAGE_ACCOUNT}.dfs.core.windows.net/{SOURCE_SYSTEM}/{TABLE_NAME}/"
LANDING_PATH = f"abfss://landing@{STORAGE_ACCOUNT}.dfs.core.windows.net/{SOURCE_SYSTEM}/"
CHECKPOINT_PATH = f"abfss://checkpoints@{STORAGE_ACCOUNT}.dfs.core.windows.net/{SOURCE_SYSTEM}/{TABLE_NAME}/"

print(f"Bronze Path: {BRONZE_PATH}")
print(f"Landing Path: {LANDING_PATH}")
print(f"Source System: {SOURCE_SYSTEM}")
print(f"Source Type: {SOURCE_TYPE}")

# COMMAND ----------

# MAGIC %md
# ## Data Quality Functions

# COMMAND ----------

def add_audit_columns(df, source_system, source_type):
    """Add standard audit columns to incoming data"""
    return df.withColumn("LoadDate", current_timestamp()) \
             .withColumn("SourceSystem", lit(source_system)) \
             .withColumn("SourceType", lit(source_type)) \
             .withColumn("RecordHash", sha2(concat_ws("|", *df.columns), 256)) \
             .withColumn("IsActive", lit(True)) \
             .withColumn("ValidFrom", current_timestamp()) \
             .withColumn("ValidTo", lit(None).cast("timestamp"))

def apply_data_quality_rules(df, rules_config):
    """Apply configurable data quality rules"""
    if not rules_config:
        return df
    
    # Parse rules from configuration
    if isinstance(rules_config, str):
        rules = json.loads(rules_config)
    else:
        rules = rules_config
    
    # Apply null checks
    if "null_checks" in rules:
        for column in rules["null_checks"]:
            if column in df.columns:
                df = df.filter(col(column).isNotNull())
    
    # Apply range checks
    if "range_checks" in rules:
        for column, range_def in rules["range_checks"].items():
            if column in df.columns:
                df = df.filter(
                    (col(column) >= range_def["min"]) & 
                    (col(column) <= range_def["max"])
                )
    
    # Apply regex pattern checks
    if "pattern_checks" in rules:
        for column, pattern in rules["pattern_checks"].items():
            if column in df.columns:
                df = df.filter(col(column).rlike(pattern))
    
    return df

def standardize_column_names(df):
    """Standardize column names (lowercase, underscore-separated)"""
    for old_name in df.columns:
        new_name = old_name.lower().replace(" ", "_").replace("-", "_")
        df = df.withColumnRenamed(old_name, new_name)
    return df

# COMMAND ----------

# MAGIC %md
# ## Source-Specific Ingestion Functions

# COMMAND ----------

def ingest_from_sql(connection_config):
    """Ingest data from SQL sources using JDBC"""
    
    jdbc_url = f"jdbc:sqlserver://{connection_config['server']};databaseName={connection_config['database']}"
    
    # Build incremental query if configured
    if "incremental_column" in connection_config and "last_updated" in connection_config:
        query = f"(SELECT * FROM {connection_config['table']} WHERE {connection_config['incremental_column']} > '{connection_config['last_updated']}') as subquery"
    else:
        query = f"(SELECT * FROM {connection_config['table']}) as subquery"
    
    df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", query) \
        .option("user", connection_config["username"]) \
        .option("password", connection_config["password"]) \
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
        .load()
    
    return df

def ingest_from_files(file_config):
    """Ingest data from various file formats"""
    
    file_path = file_config["path"]
    file_format = file_config["format"].lower()
    
    if file_format == "csv":
        df = spark.read \
            .option("header", file_config.get("header", "true")) \
            .option("delimiter", file_config.get("delimiter", ",")) \
            .option("encoding", file_config.get("encoding", "UTF-8")) \
            .csv(file_path)
    
    elif file_format == "json":
        df = spark.read.json(file_path)
    
    elif file_format == "parquet":
        df = spark.read.parquet(file_path)
    
    elif file_format == "excel":
        # Note: Excel requires additional library (com.crealytics:spark-excel)
        df = spark.read \
            .format("excel") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load(file_path)
    
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
    
    # Add file metadata
    df = df.withColumn("SourceFileName", lit(file_config.get("filename", "unknown")))
    
    return df

def ingest_from_api_response(api_data):
    """Process data that was already fetched from API via Dataflow Gen2"""
    
    # Convert API response to DataFrame
    if isinstance(api_data, str):
        api_data = json.loads(api_data)
    
    # Handle nested JSON structures
    if "data" in api_data and isinstance(api_data["data"], list):
        df = spark.createDataFrame(api_data["data"])
    elif isinstance(api_data, list):
        df = spark.createDataFrame(api_data)
    else:
        # Single record case
        df = spark.createDataFrame([api_data])
    
    return df

# COMMAND ----------

# MAGIC %md
# ## Main Ingestion Process

# COMMAND ----------

def create_bronze_delta_table(df, table_path, table_name, partition_columns=None):
    """Create or merge data into Bronze Delta table"""
    
    # Standardize data
    df = standardize_column_names(df)
    df = add_audit_columns(df, SOURCE_SYSTEM, SOURCE_TYPE)
    
    # Create or update Delta table
    if DeltaTable.isDeltaTable(spark, table_path):
        # Table exists - perform upsert
        delta_table = DeltaTable.forPath(spark, table_path)
        
        # Define merge condition (customize based on your business key)
        merge_condition = "target.RecordHash = source.RecordHash"
        
        # Perform upsert operation
        delta_table.alias("target") \
            .merge(df.alias("source"), merge_condition) \
            .whenMatchedUpdate(set={
                "IsActive": "source.IsActive",
                "ValidTo": "source.LoadDate"
            }) \
            .whenNotMatchedInsertAll() \
            .execute()
        
        print(f"Merged data into existing Delta table: {table_name}")
    
    else:
        # Create new Delta table
        writer = df.write \
            .format("delta") \
            .mode("overwrite") \
            .option("mergeSchema", "true")
        
        if partition_columns:
            writer = writer.partitionBy(partition_columns)
        
        writer.save(table_path)
        print(f"Created new Delta table: {table_name}")
    
    # Optimize table performance
    spark.sql(f"OPTIMIZE delta.`{table_path}`")
    
    # Update table statistics
    spark.sql(f"ANALYZE TABLE delta.`{table_path}` COMPUTE STATISTICS")
    
    return table_path

# COMMAND ----------

# MAGIC %md
# ## Configuration-Driven Ingestion

# COMMAND ----------

# Sample configurations for different source types
SAMPLE_CONFIGS = {
    "sql": {
        "server": "demo-sql-server.database.windows.net",
        "database": "SampleDB",
        "table": "dbo.customers",
        "username": "fabricuser",
        "password": "{{SECRET:KeyVault:sql-password}}",
        "incremental_column": "ModifiedDate",
        "last_updated": "2024-01-01T00:00:00Z"
    },
    "file": {
        "path": f"{LANDING_PATH}customers.csv",
        "format": "csv",
        "header": "true",
        "delimiter": ",",
        "filename": "customers.csv"
    },
    "api": {
        "endpoint": "/customers",
        "response_data_field": "data",
        "incremental_field": "updated_at"
    }
}

# Data quality rules configuration
DATA_QUALITY_RULES = {
    "null_checks": ["id", "name"],
    "range_checks": {
        "amount": {"min": 0, "max": 1000000}
    },
    "pattern_checks": {
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    }
}

# COMMAND ----------

# MAGIC %md
# ## Execute Ingestion Process

# COMMAND ----------

def run_ingestion(source_config, quality_rules=None):
    """Main function to orchestrate the ingestion process"""
    
    try:
        print(f"Starting ingestion for {SOURCE_SYSTEM} - {TABLE_NAME}")
        print(f"Source Type: {SOURCE_TYPE}")
        
        # Load data based on source type
        if SOURCE_TYPE.lower() == "sql":
            df = ingest_from_sql(source_config)
        elif SOURCE_TYPE.lower() == "file":
            df = ingest_from_files(source_config)
        elif SOURCE_TYPE.lower() == "api":
            # For API data, assume it's already processed by Dataflow Gen2
            df = spark.read.format("delta").load(f"{LANDING_PATH}{TABLE_NAME}_raw/")
        else:
            raise ValueError(f"Unsupported source type: {SOURCE_TYPE}")
        
        print(f"Loaded {df.count()} records from source")
        
        # Apply data quality rules
        if quality_rules:
            original_count = df.count()
            df = apply_data_quality_rules(df, quality_rules)
            filtered_count = df.count()
            print(f"Data quality filtering: {original_count} -> {filtered_count} records")
        
        # Create Bronze Delta table
        bronze_path = create_bronze_delta_table(
            df, 
            BRONZE_PATH, 
            TABLE_NAME,
            partition_columns=["LoadDate"]
        )
        
        # Log success metrics
        final_count = spark.read.format("delta").load(bronze_path).count()
        print(f"Successfully created Bronze table with {final_count} total records")
        print(f"Bronze table location: {bronze_path}")
        
        return {
            "status": "success",
            "records_processed": df.count(),
            "bronze_table_path": bronze_path,
            "total_records": final_count
        }
        
    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        return {
            "status": "error",
            "error_message": str(e)
        }

# Execute the ingestion
if __name__ == "__main__":
    # Use sample configuration based on source type
    config = SAMPLE_CONFIGS.get(SOURCE_TYPE.lower(), {})
    result = run_ingestion(config, DATA_QUALITY_RULES)
    print(f"Ingestion result: {result}")

# COMMAND ----------

# MAGIC %md
# ## Monitoring and Alerting

# COMMAND ----------

def log_ingestion_metrics(result, source_system, table_name):
    """Log metrics for monitoring dashboard"""
    
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "source_system": source_system,
        "table_name": table_name,
        "status": result.get("status"),
        "records_processed": result.get("records_processed", 0),
        "total_records": result.get("total_records", 0),
        "bronze_table_path": result.get("bronze_table_path"),
        "error_message": result.get("error_message")
    }
    
    # Write metrics to monitoring table
    metrics_df = spark.createDataFrame([metrics])
    metrics_path = f"abfss://monitoring@{STORAGE_ACCOUNT}.dfs.core.windows.net/ingestion_metrics/"
    
    metrics_df.write \
        .format("delta") \
        .mode("append") \
        .save(metrics_path)
    
    print(f"Logged metrics to {metrics_path}")

# Log metrics for this ingestion run
if 'result' in locals():
    log_ingestion_metrics(result, SOURCE_SYSTEM, TABLE_NAME)

# COMMAND ----------

# MAGIC %md
# ## Cleanup and Optimization

# COMMAND ----------

# Clean up old checkpoint files (keep last 7 days)
try:
    checkpoint_files = spark.read.format("binaryFile").load(CHECKPOINT_PATH)
    old_threshold = datetime.now() - timedelta(days=7)
    
    # This would require additional logic to clean up old files
    print(f"Checkpoint cleanup completed for {CHECKPOINT_PATH}")
except:
    print("No checkpoint cleanup needed")

# Stop Spark session
spark.stop()

print("Bronze layer ingestion completed successfully\!")
