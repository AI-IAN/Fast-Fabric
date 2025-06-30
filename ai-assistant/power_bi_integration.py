#!/usr/bin/env python3
"""
Power BI Integration for AI Cost Tracking
Exports AI usage data for Power BI dashboards
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
import os

class PowerBIIntegration:
    def __init__(self, db_path="cost_log.sqlite"):
        self.db_path = db_path
        
    def export_cost_data_for_powerbi(self, output_path="power_bi_data", days=90):
        """Export AI cost data in Power BI-friendly format"""
        
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        
        # Daily cost summary
        daily_summary = pd.read_sql_query(f"""
            SELECT 
                DATE(timestamp) as date,
                provider,
                feature,
                COUNT(*) as request_count,
                SUM(prompt_tokens) as total_prompt_tokens,
                SUM(completion_tokens) as total_completion_tokens,
                SUM(total_tokens) as total_tokens,
                SUM(cost_usd) as total_cost_usd,
                AVG(cost_usd) as avg_cost_per_request
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY DATE(timestamp), provider, feature
            ORDER BY date DESC
        """, conn)
        
        # Monthly cost summary
        monthly_summary = pd.read_sql_query(f"""
            SELECT 
                strftime('%Y-%m', timestamp) as month,
                provider,
                feature,
                COUNT(*) as request_count,
                SUM(total_tokens) as total_tokens,
                SUM(cost_usd) as total_cost_usd,
                AVG(cost_usd) as avg_cost_per_request
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY strftime('%Y-%m', timestamp), provider, feature
            ORDER BY month DESC
        """, conn)
        
        # Provider performance metrics
        provider_metrics = pd.read_sql_query(f"""
            SELECT 
                provider,
                model,
                feature,
                COUNT(*) as request_count,
                SUM(cost_usd) as total_cost,
                AVG(cost_usd) as avg_cost_per_request,
                SUM(total_tokens) / COUNT(*) as avg_tokens_per_request,
                MIN(timestamp) as first_used,
                MAX(timestamp) as last_used
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY provider, model, feature
            ORDER BY total_cost DESC
        """, conn)
        
        # Feature usage trends
        feature_trends = pd.read_sql_query(f"""
            SELECT 
                DATE(timestamp) as date,
                feature,
                COUNT(*) as daily_requests,
                SUM(cost_usd) as daily_cost,
                SUM(total_tokens) as daily_tokens
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY DATE(timestamp), feature
            ORDER BY date, feature
        """, conn)
        
        # Cost efficiency analysis
        cost_efficiency = pd.read_sql_query(f"""
            SELECT 
                feature,
                provider,
                COUNT(*) as requests,
                SUM(cost_usd) as total_cost,
                SUM(total_tokens) as total_tokens,
                SUM(cost_usd) / SUM(total_tokens) * 1000 as cost_per_1k_tokens,
                AVG(prompt_tokens) as avg_prompt_tokens,
                AVG(completion_tokens) as avg_completion_tokens
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY feature, provider
            HAVING COUNT(*) > 5  -- Only include combinations with meaningful usage
            ORDER BY cost_per_1k_tokens
        """, conn)
        
        conn.close()
        
        # Export to CSV files
        daily_summary.to_csv(f"{output_path}/daily_cost_summary.csv", index=False)
        monthly_summary.to_csv(f"{output_path}/monthly_cost_summary.csv", index=False)
        provider_metrics.to_csv(f"{output_path}/provider_performance.csv", index=False)
        feature_trends.to_csv(f"{output_path}/feature_usage_trends.csv", index=False)
        cost_efficiency.to_csv(f"{output_path}/cost_efficiency_analysis.csv", index=False)
        
        # Create metadata file for Power BI
        metadata = {
            "export_date": datetime.now().isoformat(),
            "data_range_days": days,
            "files": [
                {
                    "name": "daily_cost_summary.csv",
                    "description": "Daily cost breakdown by provider and feature",
                    "key_columns": ["date", "provider", "feature", "total_cost_usd"]
                },
                {
                    "name": "monthly_cost_summary.csv", 
                    "description": "Monthly aggregated cost data",
                    "key_columns": ["month", "provider", "feature", "total_cost_usd"]
                },
                {
                    "name": "provider_performance.csv",
                    "description": "Provider and model performance metrics",
                    "key_columns": ["provider", "model", "avg_cost_per_request"]
                },
                {
                    "name": "feature_usage_trends.csv",
                    "description": "Daily usage trends by AI feature",
                    "key_columns": ["date", "feature", "daily_cost", "daily_requests"]
                },
                {
                    "name": "cost_efficiency_analysis.csv",
                    "description": "Cost efficiency metrics by feature and provider",
                    "key_columns": ["feature", "provider", "cost_per_1k_tokens"]
                }
            ]
        }
        
        with open(f"{output_path}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "export_path": output_path,
            "files_created": len(metadata["files"]),
            "total_records": len(daily_summary) + len(monthly_summary) + len(provider_metrics),
            "date_range": f"Last {days} days"
        }
    
    def create_powerbi_template_measures(self):
        """Generate DAX measures for Power BI cost tracking dashboard"""
        
        dax_measures = {
            "Total AI Cost": """
Total AI Cost = SUM(daily_cost_summary[total_cost_usd])
            """,
            
            "Total Requests": """
Total Requests = SUM(daily_cost_summary[request_count])
            """,
            
            "Average Cost per Request": """
Average Cost per Request = 
DIVIDE(
    [Total AI Cost],
    [Total Requests],
    0
)
            """,
            
            "Cost Growth MoM": """
Cost Growth MoM = 
VAR CurrentMonth = [Total AI Cost]
VAR PreviousMonth = 
    CALCULATE(
        [Total AI Cost],
        DATEADD(daily_cost_summary[date], -1, MONTH)
    )
RETURN
    DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)
            """,
            
            "Most Expensive Feature": """
Most Expensive Feature = 
VAR MaxCost = 
    MAXX(
        VALUES(daily_cost_summary[feature]),
        CALCULATE([Total AI Cost])
    )
RETURN
    MAXX(
        FILTER(
            VALUES(daily_cost_summary[feature]),
            CALCULATE([Total AI Cost]) = MaxCost
        ),
        daily_cost_summary[feature]
    )
            """,
            
            "Budget Utilization %": """
Budget Utilization % = 
VAR MonthlyBudget = 100  -- Adjust this value based on your budget
VAR CurrentMonthCost = 
    CALCULATE(
        [Total AI Cost],
        MONTH(daily_cost_summary[date]) = MONTH(TODAY()),
        YEAR(daily_cost_summary[date]) = YEAR(TODAY())
    )
RETURN
    DIVIDE(CurrentMonthCost, MonthlyBudget, 0)
            """,
            
            "Cost per 1K Tokens": """
Cost per 1K Tokens = 
VAR TotalCost = [Total AI Cost]
VAR TotalTokens = SUM(daily_cost_summary[total_tokens])
RETURN
    DIVIDE(TotalCost * 1000, TotalTokens, 0)
            """,
            
            "Provider Efficiency Score": """
Provider Efficiency Score = 
VAR ProviderCostPer1K = [Cost per 1K Tokens]
VAR BenchmarkCostPer1K = 
    CALCULATE(
        [Cost per 1K Tokens],
        ALL(daily_cost_summary[provider])
    )
RETURN
    DIVIDE(BenchmarkCostPer1K, ProviderCostPer1K, 1)
            """,
            
            "Forecast Monthly Cost": """
Forecast Monthly Cost = 
VAR DaysInMonth = DAY(EOMONTH(TODAY(), 0))
VAR DaysElapsed = DAY(TODAY())
VAR CostToDate = 
    CALCULATE(
        [Total AI Cost],
        MONTH(daily_cost_summary[date]) = MONTH(TODAY()),
        YEAR(daily_cost_summary[date]) = YEAR(TODAY())
    )
RETURN
    DIVIDE(CostToDate * DaysInMonth, DaysElapsed, 0)
            """,
            
            "Cost Trend (7-day avg)": """
Cost Trend (7-day avg) = 
AVERAGEX(
    DATESINPERIOD(
        daily_cost_summary[date],
        LASTDATE(daily_cost_summary[date]),
        -7,
        DAY
    ),
    [Total AI Cost]
)
            """
        }
        
        return dax_measures
    
    def create_powerbi_dashboard_spec(self):
        """Create Power BI dashboard specification"""
        
        dashboard_spec = {
            "dashboard_name": "AI Cost Tracking Dashboard",
            "description": "Comprehensive AI service cost monitoring and optimization",
            "data_sources": [
                {
                    "name": "AI Usage Data",
                    "connection_type": "CSV/Excel Import",
                    "files": [
                        "daily_cost_summary.csv",
                        "monthly_cost_summary.csv", 
                        "provider_performance.csv",
                        "feature_usage_trends.csv",
                        "cost_efficiency_analysis.csv"
                    ]
                }
            ],
            "pages": [
                {
                    "name": "Executive Summary",
                    "description": "High-level cost overview and KPIs",
                    "visuals": [
                        {
                            "type": "Card",
                            "title": "Total Monthly Cost",
                            "measure": "Total AI Cost",
                            "filter": "Current Month"
                        },
                        {
                            "type": "Card", 
                            "title": "Total Requests",
                            "measure": "Total Requests",
                            "filter": "Current Month"
                        },
                        {
                            "type": "Card",
                            "title": "Budget Utilization",
                            "measure": "Budget Utilization %",
                            "format": "Percentage"
                        },
                        {
                            "type": "Line Chart",
                            "title": "Daily Cost Trend (Last 30 Days)",
                            "x_axis": "date",
                            "y_axis": "Total AI Cost",
                            "filter": "Last 30 Days"
                        },
                        {
                            "type": "Pie Chart",
                            "title": "Cost by AI Module",
                            "category": "feature",
                            "value": "Total AI Cost"
                        },
                        {
                            "type": "Bar Chart",
                            "title": "Cost by Provider",
                            "category": "provider", 
                            "value": "Total AI Cost"
                        }
                    ]
                },
                {
                    "name": "Detailed Analysis",
                    "description": "Detailed cost breakdown and trends",
                    "visuals": [
                        {
                            "type": "Matrix",
                            "title": "Cost Breakdown by Feature and Provider",
                            "rows": "feature",
                            "columns": "provider",
                            "values": "Total AI Cost"
                        },
                        {
                            "type": "Line Chart",
                            "title": "Feature Usage Trends",
                            "x_axis": "date",
                            "y_axis": "daily_requests",
                            "legend": "feature"
                        },
                        {
                            "type": "Scatter Chart",
                            "title": "Cost vs Requests by Feature",
                            "x_axis": "request_count",
                            "y_axis": "total_cost_usd",
                            "category": "feature"
                        },
                        {
                            "type": "Table",
                            "title": "Top Cost Events",
                            "columns": ["date", "feature", "provider", "total_cost_usd"],
                            "sort": "total_cost_usd DESC",
                            "top_n": 20
                        }
                    ]
                },
                {
                    "name": "Cost Optimization",
                    "description": "Cost efficiency and optimization opportunities",
                    "visuals": [
                        {
                            "type": "Bar Chart",
                            "title": "Cost per 1K Tokens by Provider",
                            "category": "provider",
                            "value": "cost_per_1k_tokens",
                            "sort": "ASC"
                        },
                        {
                            "type": "Gauge",
                            "title": "Provider Efficiency Score",
                            "measure": "Provider Efficiency Score",
                            "min": 0,
                            "max": 2,
                            "target": 1
                        },
                        {
                            "type": "Waterfall Chart",
                            "title": "Monthly Cost Breakdown",
                            "category": "feature",
                            "value": "Total AI Cost",
                            "filter": "Current Month"
                        },
                        {
                            "type": "Line Chart",
                            "title": "7-Day Moving Average Cost",
                            "x_axis": "date",
                            "y_axis": "Cost Trend (7-day avg)"
                        }
                    ]
                }
            ],
            "filters": [
                {
                    "name": "Date Range",
                    "type": "Date Slicer",
                    "column": "date",
                    "default": "Last 30 Days"
                },
                {
                    "name": "AI Module",
                    "type": "Multi-select",
                    "column": "feature",
                    "default": "All"
                },
                {
                    "name": "Provider",
                    "type": "Multi-select", 
                    "column": "provider",
                    "default": "All"
                }
            ],
            "refresh_schedule": {
                "frequency": "Daily",
                "time": "06:00 AM",
                "timezone": "UTC"
            }
        }
        
        return dashboard_spec

def main():
    """Export data and create Power BI templates"""
    integration = PowerBIIntegration()
    
    # Export data
    print("Exporting AI cost data for Power BI...")
    export_result = integration.export_cost_data_for_powerbi()
    print(f"Exported {export_result['files_created']} files to {export_result['export_path']}")
    
    # Create DAX measures
    print("\nGenerating DAX measures...")
    measures = integration.create_powerbi_template_measures()
    with open("power_bi_data/dax_measures.txt", "w") as f:
        for name, dax in measures.items():
            f.write(f"// {name}\n{dax}\n\n")
    print(f"Created {len(measures)} DAX measures")
    
    # Create dashboard specification
    print("\nCreating dashboard specification...")
    spec = integration.create_powerbi_dashboard_spec()
    with open("power_bi_data/dashboard_specification.json", "w") as f:
        json.dump(spec, f, indent=2)
    print("Dashboard specification created")
    
    print("\nPower BI integration files ready!")
    print("Next steps:")
    print("1. Import CSV files into Power BI Desktop")
    print("2. Apply DAX measures from dax_measures.txt")
    print("3. Create visuals according to dashboard_specification.json")
    print("4. Set up automated data refresh")

if __name__ == "__main__":
    main()