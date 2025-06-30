#!/usr/bin/env python3
"""
Fabric Fast-Track AI Assistant - Streamlit Interface
Multi-module AI assistance for data platform development
"""

import streamlit as st
import pandas as pd
import sqlite3
import json
import os
from datetime import datetime, timedelta
from router import LLMRouter
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Fabric Fast-Track AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'router' not in st.session_state:
    st.session_state.router = LLMRouter()
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Sidebar for navigation and settings
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("**Fabric Fast-Track Platform**")
    
    # Module selection
    selected_module = st.selectbox(
        "Select AI Module",
        ["🏠 Dashboard", "📊 DAX Genie", "🗺️ Source Mapper", "🔍 QA Buddy", "📝 Release Scribe", "💰 Cost Tracking"],
        index=0
    )
    
    # Provider selection
    st.subheader("AI Provider Settings")
    provider = st.selectbox(
        "LLM Provider",
        ["openai", "claude", "local"],
        index=0,
        help="Choose your preferred AI provider"
    )
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        offline_mode = st.checkbox("Offline Mode", help="Use deterministic responses when APIs unavailable")
        max_tokens = st.slider("Max Response Tokens", 500, 4000, 1000)
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.7)
    
    # Quick stats
    st.subheader("Quick Stats")
    try:
        conn = sqlite3.connect(st.session_state.router.db_path)
        today_usage = conn.execute(
            "SELECT COUNT(*), SUM(cost_usd) FROM llm_usage WHERE DATE(timestamp) = DATE('now')"
        ).fetchone()
        total_usage = conn.execute(
            "SELECT COUNT(*), SUM(cost_usd) FROM llm_usage"
        ).fetchone()
        conn.close()
        
        st.metric("Today's Requests", today_usage[0] or 0)
        st.metric("Today's Cost", f"${today_usage[1]:.3f}" if today_usage[1] else "$0.000")
        st.metric("Total Requests", total_usage[0] or 0)
        st.metric("Total Cost", f"${total_usage[1]:.2f}" if total_usage[1] else "$0.00")
    except Exception as e:
        st.error(f"Error loading stats: {e}")

# Main content area
def render_dashboard():
    """Main dashboard with overview and recent activity"""
    st.title("🏠 Fabric Fast-Track AI Assistant Dashboard")
    st.markdown("Welcome to your comprehensive AI-powered data platform assistant!")
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info("""
        **📊 DAX Genie**
        
        Transform business requirements into optimized DAX measures
        
        • Natural language to DAX
        • F2+ optimization
        • Error handling
        • Performance tuning
        """)
    
    with col2:
        st.info("""
        **🗺️ Source Mapper**
        
        Generate data source mappings and medallion architecture
        
        • SQL/SaaS/File sources
        • Bronze→Silver→Gold
        • Data quality rules
        • YAML configurations
        """)
    
    with col3:
        st.info("""
        **🔍 QA Buddy**
        
        Analyze logs and detect issues proactively
        
        • Log analysis
        • Performance monitoring
        • Root cause analysis
        • Troubleshooting guides
        """)
    
    with col4:
        st.info("""
        **📝 Release Scribe**
        
        Generate professional release notes from git changes
        
        • Git diff analysis
        • Business impact assessment
        • Deployment documentation
        • Stakeholder communication
        """)
    
    # Recent activity and usage trends
    st.subheader("📈 Usage Analytics")
    
    try:
        conn = sqlite3.connect(st.session_state.router.db_path)
        
        # Daily usage over last 30 days
        daily_data = pd.read_sql_query("""
            SELECT 
                DATE(timestamp) as date,
                feature,
                COUNT(*) as requests,
                SUM(cost_usd) as cost
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-30 days')
            GROUP BY DATE(timestamp), feature
            ORDER BY date
        """, conn)
        
        if not daily_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_requests = px.line(
                    daily_data.groupby('date')['requests'].sum().reset_index(),
                    x='date', y='requests',
                    title="Daily AI Requests (Last 30 Days)"
                )
                st.plotly_chart(fig_requests, use_container_width=True)
            
            with col2:
                fig_cost = px.line(
                    daily_data.groupby('date')['cost'].sum().reset_index(),
                    x='date', y='cost',
                    title="Daily AI Cost (Last 30 Days)"
                )
                st.plotly_chart(fig_cost, use_container_width=True)
            
            # Feature usage breakdown
            feature_usage = daily_data.groupby('feature')['requests'].sum().reset_index()
            if not feature_usage.empty:
                fig_features = px.pie(
                    feature_usage,
                    values='requests', names='feature',
                    title="AI Module Usage Distribution"
                )
                st.plotly_chart(fig_features, use_container_width=True)
        
        conn.close()
        
    except Exception as e:
        st.warning(f"Could not load usage analytics: {e}")
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Generate Sample DAX", use_container_width=True):
            st.session_state.quick_action = "sample_dax"
    
    with col2:
        if st.button("Map Data Source", use_container_width=True):
            st.session_state.quick_action = "map_source"
    
    with col3:
        if st.button("Analyze Logs", use_container_width=True):
            st.session_state.quick_action = "analyze_logs"
    
    with col4:
        if st.button("Create Release Notes", use_container_width=True):
            st.session_state.quick_action = "release_notes"

def render_dax_genie():
    """DAX Genie interface for business logic to DAX conversion"""
    st.title("📊 DAX Genie")
    st.markdown("Transform business requirements into optimized DAX measures")
    
    # Template selection
    template_type = st.selectbox(
        "Select DAX Template Type",
        ["Basic Measure", "Time Intelligence", "Financial Ratio", "Customer Analytics", "Advanced Calculation"],
        help="Choose the type of DAX measure you want to create"
    )
    
    # Business requirement input
    st.subheader("Business Requirement")
    business_req = st.text_area(
        "Describe what you want to calculate:",
        placeholder="Example: Calculate year-over-year sales growth percentage for the current quarter",
        height=100
    )
    
    # Additional context
    col1, col2 = st.columns(2)
    
    with col1:
        data_source = st.selectbox(
            "Primary Data Source",
            ["FactSales", "FactFinancial", "FactCustomers", "Combined Tables"]
        )
        
        measure_category = st.selectbox(
            "Measure Category",
            ["Sales", "Financial", "Customer", "Operational", "Time Intelligence"]
        )
    
    with col2:
        format_type = st.selectbox(
            "Output Format",
            ["Currency", "Percentage", "Number", "Integer", "Custom"]
        )
        
        complexity = st.selectbox(
            "Complexity Level",
            ["Simple", "Medium", "Complex"]
        )
    
    # Advanced options
    with st.expander("Advanced Options"):
        include_error_handling = st.checkbox("Include robust error handling", value=True)
        optimize_for_direct_lake = st.checkbox("Optimize for Direct Lake", value=True)
        include_comments = st.checkbox("Include explanatory comments", value=True)
        performance_target = st.selectbox(
            "Performance Target",
            ["<1 second", "<2 seconds", "<5 seconds", "No specific target"]
        )
    
    # Generate DAX
    if st.button("✨ Generate DAX Measure", type="primary", use_container_width=True):
        if business_req:
            with st.spinner("Generating optimized DAX measure..."):
                prompt = f"""
                Generate a DAX measure for: {business_req}
                
                Context:
                - Measure Type: {template_type}
                - Data Source: {data_source}
                - Category: {measure_category}
                - Format: {format_type}
                - Complexity: {complexity}
                - Error Handling: {include_error_handling}
                - Direct Lake Optimization: {optimize_for_direct_lake}
                - Performance Target: {performance_target}
                
                Please provide a complete DAX measure with proper formatting, error handling, and performance optimization.
                """
                
                try:
                    response = st.session_state.router.route_request(
                        prompt, provider, "dax_genie"
                    )
                    
                    st.subheader("Generated DAX Measure")
                    st.code(response, language="dax")
                    
                    # Save to conversation history
                    st.session_state.conversation_history.append({
                        "module": "DAX Genie",
                        "timestamp": datetime.now(),
                        "request": business_req,
                        "response": response
                    })
                    
                    # Download button
                    st.download_button(
                        "Download DAX Measure",
                        response,
                        file_name=f"dax_measure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating DAX: {e}")
        else:
            st.warning("Please enter a business requirement first.")
    
    # Example gallery
    st.subheader("💡 Example DAX Measures")
    example_tab1, example_tab2, example_tab3 = st.tabs(["Sales Metrics", "Financial Ratios", "Time Intelligence"])
    
    with example_tab1:
        st.code("""
Total Sales $ = 
    CALCULATE(
        SUM(FactSales[SalesAmount]),
        FactSales[IsReturn] = FALSE
    )
        """, language="dax")
    
    with example_tab2:
        st.code("""
Gross Margin % = 
VAR Revenue = [Total Sales $]
VAR COGS = [Total Cost of Goods Sold $]
RETURN
    DIVIDE(Revenue - COGS, Revenue)
        """, language="dax")
    
    with example_tab3:
        st.code("""
Sales Growth YoY % = 
VAR CurrentSales = [Total Sales $]
VAR PreviousYearSales = 
    CALCULATE(
        [Total Sales $],
        SAMEPERIODLASTYEAR(DimDate[Date])
    )
RETURN
    DIVIDE(CurrentSales - PreviousYearSales, PreviousYearSales)
        """, language="dax")

def render_source_mapper():
    """Source Mapper interface for data source mapping"""
    st.title("🗺️ Source Mapper")
    st.markdown("Generate data source mappings and medallion architecture specifications")
    
    # Source type selection
    source_type = st.selectbox(
        "Select Source Type",
        ["SQL Database", "SaaS API", "File Source", "Streaming Source", "Multi-Source Integration"]
    )
    
    # Dynamic form based on source type
    if source_type == "SQL Database":
        st.subheader("SQL Database Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            db_type = st.selectbox("Database Type", ["SQL Server", "PostgreSQL", "MySQL", "Oracle"])
            db_name = st.text_input("Database Name", placeholder="ProductionDB")
            
        with col2:
            data_volume = st.text_input("Data Volume", placeholder="10M customers, 50M orders")
            update_frequency = st.selectbox("Update Frequency", ["Real-time", "Hourly", "Daily", "Weekly"])
        
        key_tables = st.text_area(
            "Key Tables (comma-separated)",
            placeholder="Customers, Orders, OrderItems, Products",
            height=60
        )
        
        business_context = st.text_area(
            "Business Context",
            placeholder="Describe what business process this data supports...",
            height=80
        )
    
    elif source_type == "SaaS API":
        st.subheader("SaaS API Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            platform = st.selectbox("Platform", ["Salesforce", "HubSpot", "Stripe", "Dynamics 365", "Other"])
            api_version = st.text_input("API Version", placeholder="v57.0")
            
        with col2:
            auth_type = st.selectbox("Authentication", ["OAuth2", "API Key", "Service Principal"])
            rate_limits = st.text_input("Rate Limits", placeholder="5000 requests/hour")
        
        data_objects = st.text_area(
            "Data Objects",
            placeholder="Accounts, Contacts, Opportunities, Leads",
            height=60
        )
        
        business_context = st.text_area(
            "Business Context",
            placeholder="How this API data supports business processes...",
            height=80
        )
    
    # Common fields for all source types
    st.subheader("Medallion Architecture Requirements")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        bronze_requirements = st.text_area("Bronze Layer", placeholder="Raw data requirements...", height=80)
    with col2:
        silver_requirements = st.text_area("Silver Layer", placeholder="Cleansed data requirements...", height=80)
    with col3:
        gold_requirements = st.text_area("Gold Layer", placeholder="Business-ready data requirements...", height=80)
    
    # Generate mapping
    if st.button("🗺️ Generate Source Mapping", type="primary", use_container_width=True):
        with st.spinner("Generating comprehensive source mapping..."):
            prompt = f"""
            Create {source_type.lower()} source mapping for data platform integration.
            
            Source Details:
            - Type: {source_type}
            - Business Context: {business_context}
            - Data Requirements: Bronze: {bronze_requirements}, Silver: {silver_requirements}, Gold: {gold_requirements}
            
            Please generate a complete YAML configuration with medallion architecture mapping.
            """
            
            try:
                response = st.session_state.router.route_request(
                    prompt, provider, "source_mapper"
                )
                
                st.subheader("Generated Source Mapping")
                st.code(response, language="yaml")
                
                # Save to conversation history
                st.session_state.conversation_history.append({
                    "module": "Source Mapper",
                    "timestamp": datetime.now(),
                    "request": f"{source_type} mapping",
                    "response": response
                })
                
                # Download button
                st.download_button(
                    "Download YAML Configuration",
                    response,
                    file_name=f"source_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml",
                    mime="text/yaml"
                )
                
            except Exception as e:
                st.error(f"Error generating source mapping: {e}")

def render_qa_buddy():
    """QA Buddy interface for log analysis and issue detection"""
    st.title("🔍 QA Buddy")
    st.markdown("Analyze logs, detect issues, and get actionable troubleshooting guidance")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["General Log Analysis", "Performance Investigation", "Data Pipeline Failure", 
         "Data Quality Issues", "Security Audit", "Capacity Analysis"]
    )
    
    # Log input methods
    input_method = st.radio("Log Input Method", ["Paste Logs", "Upload File", "System Integration"])
    
    if input_method == "Paste Logs":
        log_data = st.text_area(
            "Paste Log Data",
            placeholder="Paste your log entries here...",
            height=200
        )
    elif input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload Log File", type=['txt', 'log', 'csv'])
        log_data = ""
        if uploaded_file:
            log_data = str(uploaded_file.read(), "utf-8")
            st.text_area("Log Preview", log_data[:1000] + "..." if len(log_data) > 1000 else log_data, height=100)
    else:
        st.info("System integration for live log analysis coming soon!")
        log_data = ""
    
    # Context information
    st.subheader("Analysis Context")
    col1, col2 = st.columns(2)
    
    with col1:
        time_range = st.text_input("Time Range", placeholder="2024-01-15 08:00 - 12:00")
        system_component = st.selectbox(
            "System Component",
            ["Fabric Workspace", "Data Pipeline", "Power BI Reports", "AI Assistant", "Infrastructure"]
        )
    
    with col2:
        expected_behavior = st.text_input("Expected Behavior", placeholder="What should normally happen?")
        recent_changes = st.text_input("Recent Changes", placeholder="Any recent deployments or changes?")
    
    issue_symptoms = st.text_area(
        "Issue Symptoms",
        placeholder="Describe what issues you're experiencing...",
        height=80
    )
    
    # Analysis focus
    st.subheader("Analysis Focus")
    focus_areas = st.multiselect(
        "What should we focus on?",
        ["Performance Issues", "Error Detection", "Security Concerns", "Data Quality", 
         "Resource Utilization", "Trend Analysis", "Root Cause Investigation"]
    )
    
    # Analyze logs
    if st.button("🔍 Analyze Logs", type="primary", use_container_width=True):
        if log_data or issue_symptoms:
            with st.spinner("Analyzing logs and detecting issues..."):
                prompt = f"""
                Analyze these system logs for issues: {analysis_type}
                
                Log Context:
                - Time Range: {time_range}
                - System Component: {system_component}
                - Expected Behavior: {expected_behavior}
                - Recent Changes: {recent_changes}
                - Issue Symptoms: {issue_symptoms}
                - Focus Areas: {', '.join(focus_areas)}
                
                Log Data:
                {log_data[:2000]}  # Truncate for API limits
                
                Please provide comprehensive analysis with actionable recommendations.
                """
                
                try:
                    response = st.session_state.router.route_request(
                        prompt, provider, "qa_buddy"
                    )
                    
                    st.subheader("🔍 Analysis Results")
                    st.markdown(response)
                    
                    # Save to conversation history
                    st.session_state.conversation_history.append({
                        "module": "QA Buddy",
                        "timestamp": datetime.now(),
                        "request": f"{analysis_type} - {issue_symptoms}",
                        "response": response
                    })
                    
                    # Download button
                    st.download_button(
                        "Download Analysis Report",
                        response,
                        file_name=f"qa_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Error analyzing logs: {e}")
        else:
            st.warning("Please provide log data or describe the issue symptoms.")
    
    # Quick analysis templates
    st.subheader("🚀 Quick Analysis Templates")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Pipeline Performance", use_container_width=True):
            st.session_state.qa_template = "pipeline_performance"
    
    with col2:
        if st.button("Data Quality Check", use_container_width=True):
            st.session_state.qa_template = "data_quality"
    
    with col3:
        if st.button("Security Audit", use_container_width=True):
            st.session_state.qa_template = "security_audit"

def render_release_scribe():
    """Release Scribe interface for git diff to release notes"""
    st.title("📝 Release Scribe")
    st.markdown("Generate professional release notes and deployment documentation")
    
    # Release information
    st.subheader("Release Information")
    col1, col2 = st.columns(2)
    
    with col1:
        release_version = st.text_input("Release Version/Tag", placeholder="v2.1.0")
        release_type = st.selectbox("Release Type", ["Major", "Minor", "Patch", "Hotfix"])
        
    with col2:
        target_audience = st.multiselect(
            "Target Audience",
            ["Developers", "Business Users", "IT Operations", "Executives", "All Users"]
        )
        deployment_date = st.date_input("Planned Deployment Date")
    
    # Git information
    st.subheader("Git Changes")
    git_input_method = st.radio("Git Input Method", ["Paste Git Diff", "Commit Messages", "Manual Description"])
    
    if git_input_method == "Paste Git Diff":
        git_data = st.text_area(
            "Git Diff Output",
            placeholder="Paste git diff output here...",
            height=200
        )
    elif git_input_method == "Commit Messages":
        git_data = st.text_area(
            "Commit Messages",
            placeholder="Paste recent commit messages...",
            height=200
        )
    else:
        git_data = st.text_area(
            "Manual Change Description",
            placeholder="Describe the changes made in this release...",
            height=200
        )
    
    # Additional context
    st.subheader("Release Context")
    col1, col2 = st.columns(2)
    
    with col1:
        breaking_changes = st.checkbox("Contains Breaking Changes")
        security_updates = st.checkbox("Contains Security Updates")
        
    with col2:
        performance_improvements = st.checkbox("Performance Improvements")
        new_features = st.checkbox("New Features")
    
    business_value = st.text_area(
        "Business Value & Impact",
        placeholder="Describe the business value and impact of these changes...",
        height=80
    )
    
    # Documentation requirements
    with st.expander("Documentation Requirements"):
        doc_style = st.selectbox("Documentation Style", ["Formal", "Informal", "Technical", "Business-Focused"])
        detail_level = st.selectbox("Detail Level", ["High-Level Summary", "Detailed", "Technical Deep-Dive"])
        include_migration = st.checkbox("Include Migration Guide")
        include_rollback = st.checkbox("Include Rollback Plan")
    
    # Generate release notes
    if st.button("📝 Generate Release Notes", type="primary", use_container_width=True):
        if git_data:
            with st.spinner("Generating professional release documentation..."):
                prompt = f"""
                Generate release notes from git changes: {release_version}
                
                Release Context:
                - Version: {release_version}
                - Release Type: {release_type}
                - Target Audience: {', '.join(target_audience)}
                - Deployment Date: {deployment_date}
                - Breaking Changes: {breaking_changes}
                - Security Updates: {security_updates}
                - Performance Improvements: {performance_improvements}
                - New Features: {new_features}
                - Business Value: {business_value}
                
                Git Changes:
                {git_data}
                
                Documentation Style: {doc_style}
                Detail Level: {detail_level}
                
                Please generate comprehensive release notes with deployment guidance.
                """
                
                try:
                    response = st.session_state.router.route_request(
                        prompt, provider, "release_scribe"
                    )
                    
                    st.subheader("📝 Generated Release Notes")
                    st.markdown(response)
                    
                    # Save to conversation history
                    st.session_state.conversation_history.append({
                        "module": "Release Scribe",
                        "timestamp": datetime.now(),
                        "request": f"Release {release_version}",
                        "response": response
                    })
                    
                    # Download button
                    st.download_button(
                        "Download Release Notes",
                        response,
                        file_name=f"release_notes_{release_version}_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating release notes: {e}")
        else:
            st.warning("Please provide git changes or change description.")

def render_cost_tracking():
    """Cost tracking dashboard with detailed analytics"""
    st.title("💰 AI Cost Tracking Dashboard")
    st.markdown("Monitor and optimize AI service usage and costs")
    
    try:
        conn = sqlite3.connect(st.session_state.router.db_path)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Today's metrics
        today_data = conn.execute("""
            SELECT 
                COUNT(*) as requests,
                SUM(cost_usd) as cost,
                SUM(total_tokens) as tokens
            FROM llm_usage 
            WHERE DATE(timestamp) = DATE('now')
        """).fetchone()
        
        # This month's metrics
        month_data = conn.execute("""
            SELECT 
                COUNT(*) as requests,
                SUM(cost_usd) as cost,
                SUM(total_tokens) as tokens
            FROM llm_usage 
            WHERE strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        """).fetchone()
        
        with col1:
            st.metric("Today's Requests", today_data[0] or 0)
        with col2:
            st.metric("Today's Cost", f"${today_data[1]:.3f}" if today_data[1] else "$0.000")
        with col3:
            st.metric("Month Requests", month_data[0] or 0)
        with col4:
            st.metric("Month Cost", f"${month_data[1]:.2f}" if month_data[1] else "$0.00")
        
        # Time period selection
        st.subheader("📊 Usage Analytics")
        time_period = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"])
        
        days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90, "All Time": 3650}
        days = days_map[time_period]
        
        # Usage over time
        usage_data = pd.read_sql_query(f"""
            SELECT 
                DATE(timestamp) as date,
                provider,
                feature,
                COUNT(*) as requests,
                SUM(cost_usd) as cost,
                SUM(total_tokens) as tokens
            FROM llm_usage 
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY DATE(timestamp), provider, feature
            ORDER BY date
        """, conn)
        
        if not usage_data.empty:
            # Daily cost trend
            daily_cost = usage_data.groupby('date')['cost'].sum().reset_index()
            fig_cost_trend = px.line(daily_cost, x='date', y='cost', 
                                   title=f"Daily AI Cost Trend ({time_period})")
            st.plotly_chart(fig_cost_trend, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Provider breakdown
                provider_data = usage_data.groupby('provider').agg({
                    'requests': 'sum',
                    'cost': 'sum'
                }).reset_index()
                
                fig_provider = px.pie(provider_data, values='cost', names='provider',
                                    title="Cost by Provider")
                st.plotly_chart(fig_provider, use_container_width=True)
            
            with col2:
                # Feature breakdown
                feature_data = usage_data.groupby('feature').agg({
                    'requests': 'sum',
                    'cost': 'sum'
                }).reset_index()
                
                fig_feature = px.bar(feature_data, x='feature', y='cost',
                                   title="Cost by AI Module")
                st.plotly_chart(fig_feature, use_container_width=True)
            
            # Detailed usage table
            st.subheader("📋 Detailed Usage Log")
            
            detailed_data = pd.read_sql_query(f"""
                SELECT 
                    timestamp,
                    provider,
                    model,
                    feature,
                    prompt_tokens,
                    completion_tokens,
                    total_tokens,
                    cost_usd
                FROM llm_usage 
                WHERE timestamp >= datetime('now', '-{days} days')
                ORDER BY timestamp DESC
                LIMIT 100
            """, conn)
            
            if not detailed_data.empty:
                st.dataframe(detailed_data, use_container_width=True)
            
            # Cost optimization recommendations
            st.subheader("💡 Cost Optimization Recommendations")
            
            # Analyze usage patterns for recommendations
            avg_daily_cost = usage_data.groupby('date')['cost'].sum().mean()
            high_cost_features = feature_data.nlargest(3, 'cost')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"""
                **📈 Usage Insights**
                
                • Average daily cost: ${avg_daily_cost:.3f}
                • Projected monthly cost: ${avg_daily_cost * 30:.2f}
                • Most expensive module: {high_cost_features.iloc[0]['feature'] if not high_cost_features.empty else 'N/A'}
                """)
            
            with col2:
                st.success("""
                **💰 Optimization Tips**
                
                • Use cached responses for repeated queries
                • Prefer local models for simple tasks
                • Monitor token usage and optimize prompts
                • Set daily/monthly budget alerts
                """)
        
        else:
            st.info("No usage data available for the selected time period.")
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error loading cost tracking data: {e}")
    
    # Budget settings
    st.subheader("⚙️ Budget Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        daily_budget = st.number_input("Daily Budget ($)", min_value=0.0, value=5.0, step=0.1)
        monthly_budget = st.number_input("Monthly Budget ($)", min_value=0.0, value=100.0, step=1.0)
    
    with col2:
        alert_threshold = st.slider("Alert Threshold (%)", 50, 100, 80)
        if st.button("Save Budget Settings"):
            st.success("Budget settings saved!")

# Main app routing
def main():
    """Main application with module routing"""
    
    # Handle quick actions from dashboard
    if hasattr(st.session_state, 'quick_action'):
        quick_action = st.session_state.quick_action
        if quick_action == "sample_dax":
            selected_module = "📊 DAX Genie"
        elif quick_action == "map_source":
            selected_module = "🗺️ Source Mapper"
        elif quick_action == "analyze_logs":
            selected_module = "🔍 QA Buddy"
        elif quick_action == "release_notes":
            selected_module = "📝 Release Scribe"
        delattr(st.session_state, 'quick_action')
    else:
        selected_module = st.sidebar.selectbox(
            "Select AI Module",
            ["🏠 Dashboard", "📊 DAX Genie", "🗺️ Source Mapper", "🔍 QA Buddy", "📝 Release Scribe", "💰 Cost Tracking"],
            index=0
        )
    
    # Route to appropriate module
    if selected_module == "🏠 Dashboard":
        render_dashboard()
    elif selected_module == "📊 DAX Genie":
        render_dax_genie()
    elif selected_module == "🗺️ Source Mapper":
        render_source_mapper()
    elif selected_module == "🔍 QA Buddy":
        render_qa_buddy()
    elif selected_module == "📝 Release Scribe":
        render_release_scribe()
    elif selected_module == "💰 Cost Tracking":
        render_cost_tracking()
    
    # Conversation history sidebar
    if st.session_state.conversation_history:
        st.sidebar.subheader("📝 Recent Activity")
        for i, conv in enumerate(st.session_state.conversation_history[-3:]):
            with st.sidebar.expander(f"{conv['module']} - {conv['timestamp'].strftime('%H:%M')}"):
                st.write(f"**Request:** {conv['request'][:100]}...")
                if st.button(f"View Full Response", key=f"view_{i}"):
                    st.session_state.show_history = i

if __name__ == "__main__":
    main()