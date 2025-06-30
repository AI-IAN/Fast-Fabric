# QA Buddy User Prompt Templates

## Template Categories

### 1. General Log Analysis

```
Analyze these system logs for issues and provide recommendations: [LOG_SOURCE]

Log Context:
- Time Range: [Start time - End time]
- System/Component: [Fabric workspace/Spark job/Pipeline/Report]
- Log Level: [ERROR/WARN/INFO/DEBUG/ALL]
- Expected Behavior: [What should be happening normally]
- Recent Changes: [Any recent deployments or configuration changes]

Log Data:
[Paste log entries here - can be multiple lines]

Analysis Request:
- Issue Detection: [Look for specific types of issues]
- Performance Analysis: [Focus on performance metrics]
- Root Cause: [Investigate specific error or anomaly]
- Trends: [Identify patterns over time]

Example:
"Analyze these Fabric workspace logs for performance issues:
- Time Range: 2024-01-15 08:00 - 12:00
- System: Dataflow Gen2 pipeline execution
- Log Level: WARN and ERROR
- Expected Behavior: Daily data refresh should complete in 30 minutes
- Recent Changes: Upgraded to F4 capacity yesterday"
```

### 2. Performance Issue Investigation

```
Investigate performance degradation in: [SYSTEM_COMPONENT]

Performance Context:
- Component: [Specific system experiencing issues]
- Symptoms: [Slow queries/timeouts/high resource usage/etc.]
- Baseline Performance: [Normal performance metrics]
- Current Performance: [Current degraded metrics]
- Business Impact: [Effect on users/reports/processes]

System Details:
- Fabric Capacity: [F2/F4/F8 and utilization]
- Data Volume: [Size of datasets being processed]
- Concurrent Users: [Number of active users]
- Recent Growth: [Data or usage growth patterns]

Investigation Focus:
- [ ] Query performance analysis
- [ ] Resource utilization review
- [ ] Data model optimization
- [ ] Capacity planning assessment
- [ ] Bottleneck identification

Example:
"Investigate performance degradation in: Power BI semantic model
- Symptoms: DAX queries taking 10+ seconds (normally <2 seconds)
- Baseline: F2 capacity, 2-second response times
- Current: Same F2 capacity, 10-15 second response times
- Business Impact: Executive dashboard unusable during morning meetings"
```

### 3. Data Pipeline Failure Analysis

```
Analyze data pipeline failure for: [PIPELINE_NAME]

Pipeline Context:
- Pipeline Type: [Dataflow Gen2/Spark notebook/Copy activity]
- Data Source: [SQL Server/Salesforce/Files/etc.]
- Destination: [Bronze/Silver/Gold layer table]
- Schedule: [Frequency and expected duration]
- Failure Pattern: [Intermittent/Consistent/New issue]

Failure Details:
- Error Messages: [Specific error text from logs]
- Failure Point: [Where in pipeline it's failing]
- Data Volume: [Amount of data being processed]
- Success History: [When it last worked successfully]

Log Data:
[Include relevant pipeline execution logs]

Analysis Needed:
- Root cause identification
- Data quality issues
- Infrastructure problems
- Configuration errors
- Retry strategy effectiveness

Example:
"Analyze data pipeline failure for: Daily Customer Data Sync
- Pipeline Type: Dataflow Gen2 from SQL Server
- Data Source: Production CRM database
- Destination: Bronze layer customer table
- Failure Pattern: Started failing 3 days ago, was working fine before"
```

### 4. Data Quality Issue Detection

```
Investigate data quality issues in: [DATA_DOMAIN]

Data Quality Context:
- Affected Dataset: [Table/report/dashboard name]
- Quality Dimension: [Completeness/Accuracy/Consistency/Timeliness]
- Business Rules: [Specific validation rules that should apply]
- Discovery Method: [How the issue was discovered]
- Stakeholder Impact: [Who is affected by the quality issue]

Quality Issues Observed:
- Symptoms: [Missing data/wrong values/inconsistencies/etc.]
- Scope: [How much data is affected]
- Pattern: [When/where the issues occur]
- Source Systems: [Which source systems are involved]

Investigation Request:
- Validate business rules compliance
- Check data lineage and transformations
- Identify systematic vs. isolated issues
- Recommend remediation steps
- Suggest prevention measures

Example:
"Investigate data quality issues in: Sales reporting data
- Quality Dimension: Accuracy - Revenue totals don't match source system
- Business Rules: Daily sales total should equal sum of individual transactions
- Discovery: CFO noticed 15% variance in monthly revenue report
- Scope: Last 2 weeks of data shows discrepancies"
```

### 5. Capacity and Resource Analysis

```
Analyze capacity and resource utilization for: [FABRIC_ENVIRONMENT]

Capacity Context:
- Current Capacity: [F2/F4/F8 SKU and utilization levels]
- Workload Types: [Data engineering/BI/ML/etc.]
- Peak Usage Times: [When system is under highest load]
- Growth Trajectory: [Data and user growth patterns]
- Performance Targets: [SLA requirements and expectations]

Resource Metrics:
- CPU Utilization: [Average and peak levels]
- Memory Usage: [Memory consumption patterns]
- Storage Growth: [Data growth rates and projections]
- Network I/O: [Data transfer patterns and bottlenecks]
- Concurrent Operations: [Parallel job execution]

Analysis Request:
- Current capacity adequacy
- Performance bottleneck identification
- Growth planning recommendations
- Cost optimization opportunities
- Scaling strategy suggestions

Example:
"Analyze capacity utilization for: Production Fabric workspace
- Current Capacity: F4 with 70% average utilization
- Workload: 50 daily ETL jobs + 200 concurrent report users
- Peak Times: 8-10 AM (ETL) and 2-4 PM (reporting)
- Growth: 25% data growth and 40% user growth expected this year"
```

## Specialized Domain Templates

### Power BI Performance Analysis

```
Analyze Power BI performance issues for: [REPORT_OR_DATASET]

Power BI Context:
- Component Type: [Semantic model/Report/Dashboard]
- Direct Lake Status: [Enabled/Disabled/Fallback mode]
- User Load: [Number of concurrent users]
- Data Size: [Dataset size and row counts]
- Query Complexity: [Simple aggregations/Complex DAX/Cross-filtering]

Performance Symptoms:
- Report Load Time: [Current vs. expected times]
- Query Response: [DAX query execution times]
- Refresh Duration: [Data refresh performance]
- User Experience: [Specific user complaints or issues]

Technical Details:
- Capacity SKU: [F2/F4/F8 and current utilization]
- Memory Usage: [Semantic model memory consumption]
- CPU Patterns: [Processing load during queries/refresh]
- Cache Hit Rates: [Query result caching effectiveness]

Analysis Focus:
- DAX optimization opportunities
- Data model efficiency review
- Direct Lake compatibility check
- Capacity right-sizing assessment
- User access pattern analysis

Example:
"Analyze Power BI performance for: Executive Sales Dashboard
- Component: Semantic model with 15 tables, 50M rows
- Direct Lake: Enabled but frequently falling back to DirectQuery
- User Load: 25 executives accessing during morning meetings
- Symptoms: Dashboard takes 30+ seconds to load, should be <5 seconds"
```

### Data Engineering Pipeline Monitoring

```
Monitor data engineering pipeline health for: [PIPELINE_ECOSYSTEM]

Pipeline Ecosystem:
- Pipeline Count: [Number of pipelines in scope]
- Data Sources: [List of source systems]
- Processing Layers: [Bronze/Silver/Gold architecture]
- Orchestration: [Data Factory/Synapse/Custom scheduling]
- Dependencies: [Inter-pipeline dependencies and schedules]

Health Monitoring Focus:
- Success/Failure Rates: [Pipeline execution statistics]
- Performance Trends: [Execution time patterns]
- Data Quality Metrics: [Validation rule compliance]
- Resource Utilization: [Compute and storage consumption]
- SLA Compliance: [Meeting data freshness requirements]

Alert Conditions:
- Pipeline failures or timeouts
- Data quality rule violations
- Performance degradation patterns
- Resource threshold breaches
- Dependency chain failures

Reporting Requirements:
- Daily pipeline health summary
- Weekly performance trend analysis
- Monthly capacity planning review
- Real-time critical failure alerts

Example:
"Monitor data engineering pipeline health for: Customer 360 data platform
- Pipeline Count: 25 pipelines across 8 source systems
- Processing: Bronze layer (raw) → Silver (cleansed) → Gold (aggregated)
- Dependencies: CRM pipeline must complete before Customer Analytics
- SLA: All customer data must be available by 8 AM daily"
```

### Security and Compliance Monitoring

```
Analyze security and compliance logs for: [SECURITY_DOMAIN]

Security Context:
- Compliance Framework: [GDPR/SOX/HIPAA/PCI/Custom]
- Audit Scope: [Workspace access/Data access/Administrative actions]
- Time Period: [Audit period for analysis]
- Risk Level: [High/Medium/Low risk focus areas]
- Stakeholders: [Compliance team/Security team/Auditors]

Security Events:
- Authentication Events: [Login patterns/failures/anomalies]
- Authorization Events: [Permission changes/access violations]
- Data Access Events: [Sensitive data access/export activities]
- Administrative Events: [Configuration changes/user management]

Compliance Requirements:
- Access Control Validation: [Role-based access compliance]
- Data Handling Validation: [PII processing compliance]
- Audit Trail Completeness: [Required logging coverage]
- Retention Policy Compliance: [Data retention adherence]

Analysis Request:
- Identify security anomalies or violations
- Validate compliance control effectiveness
- Generate audit reports and evidence
- Recommend security improvements
- Track remediation of identified issues

Example:
"Analyze security logs for: GDPR compliance audit
- Compliance Framework: GDPR Article 32 (security measures)
- Audit Scope: All customer PII access in last 6 months
- Focus: Data export activities and admin privilege usage
- Requirement: Generate evidence for annual compliance review"
```

### Cost Optimization Analysis

```
Analyze cost patterns and optimization opportunities for: [COST_DOMAIN]

Cost Context:
- Scope: [Fabric capacity/Storage/Compute/Networking/AI services]
- Time Period: [Cost analysis timeframe]
- Budget: [Current budget and variance]
- Growth Pattern: [Cost trend analysis]
- Business Value: [ROI and value realization metrics]

Cost Breakdown:
- Fabric Capacity Costs: [F-SKU usage and efficiency]
- Storage Costs: [Data lake storage consumption]
- Compute Costs: [Spark job execution costs]
- AI Service Costs: [LLM API usage and optimization]
- Data Transfer Costs: [Egress and cross-region transfers]

Optimization Focus:
- Capacity right-sizing opportunities
- Storage lifecycle management
- Compute job optimization
- AI service usage efficiency
- Reserved capacity planning

Business Alignment:
- Cost per business metric (cost per report, per user, per GB)
- Value realization tracking
- Budget variance analysis
- Forecasting and planning

Example:
"Analyze cost optimization for: Monthly Fabric workspace spend
- Scope: F4 capacity + storage + AI assistant costs
- Current: $8,500/month, budget $7,000/month
- Growth: 30% increase over last 3 months
- Focus: Right-size capacity and optimize AI usage"
```

## Issue-Specific Templates

### Intermittent Failure Investigation

```
Investigate intermittent failure pattern in: [SYSTEM_COMPONENT]

Failure Pattern:
- Frequency: [How often failures occur]
- Timing Pattern: [Time-based patterns observed]
- Success Rate: [Percentage of successful executions]
- Duration: [How long this pattern has been occurring]
- Consistency: [Are failures consistent in nature]

Environmental Factors:
- Load Conditions: [System load during failures vs successes]
- External Dependencies: [Third-party services/network conditions]
- Resource Availability: [Memory/CPU/storage during failures]
- Concurrent Activities: [Other processes running during failures]

Diagnostic Information:
- Error Messages: [Specific errors when they occur]
- System State: [Resource utilization during failures]
- Recovery Behavior: [How system recovers after failure]
- Workarounds: [Any manual interventions that resolve issues]

Investigation Strategy:
- Pattern correlation analysis
- Resource monitoring during failures
- Dependency health checking
- Timing and load correlation
- Environmental factor analysis

Example:
"Investigate intermittent failures in: Salesforce data sync pipeline
- Pattern: Fails 2-3 times per week, random times
- Success Rate: 85% (was 98% last month)
- Error: API timeout errors, but Salesforce reports no issues
- Recovery: Manual restart always succeeds"
```

### Performance Regression Analysis

```
Analyze performance regression for: [PERFORMANCE_DOMAIN]

Regression Context:
- Baseline Performance: [Previous good performance metrics]
- Current Performance: [Current degraded metrics]
- Change Timeline: [When regression started]
- Regression Scope: [What specific operations are affected]
- Business Impact: [Effect on users and business processes]

Potential Causes:
- Code Changes: [Recent deployments or updates]
- Data Changes: [Data volume or pattern changes]
- Infrastructure Changes: [Capacity/configuration changes]
- Load Changes: [User or system load increases]
- External Changes: [Third-party service changes]

Performance Metrics:
- Response Times: [Query/operation execution times]
- Throughput: [Records/requests processed per unit time]
- Resource Usage: [CPU/memory/storage utilization]
- Concurrency: [Parallel operation performance]
- Error Rates: [Increase in timeouts or failures]

Analysis Approach:
- Before/after performance comparison
- Change correlation analysis
- Resource utilization pattern analysis
- System component performance isolation
- Load testing and capacity verification

Example:
"Analyze performance regression for: Customer analytics dashboard
- Baseline: 3-second load time last month
- Current: 15-second load time this week
- Timeline: Started degrading after F2→F4 capacity upgrade
- Impact: Executives can't use dashboard for daily standup meetings"
```

### Data Consistency Validation

```
Validate data consistency across: [DATA_ECOSYSTEM]

Consistency Scope:
- Data Sources: [Source systems being compared]
- Target Systems: [Destination systems/reports]
- Data Elements: [Specific fields/metrics to validate]
- Time Period: [Timeframe for consistency check]
- Tolerance: [Acceptable variance thresholds]

Validation Rules:
- Reconciliation Logic: [How to match records across systems]
- Business Rules: [Domain-specific validation requirements]
- Timing Considerations: [Data refresh timing differences]
- Aggregation Levels: [Detail vs summary consistency]

Consistency Checks:
- Record Count Validation: [Source vs destination counts]
- Sum/Total Validation: [Aggregate value reconciliation]
- Key Field Validation: [Critical business field consistency]
- Referential Integrity: [Cross-table relationship validation]
- Temporal Consistency: [Time-based data alignment]

Discrepancy Analysis:
- Systematic vs random differences
- Pattern identification in inconsistencies
- Root cause determination
- Impact assessment and prioritization
- Remediation planning

Example:
"Validate data consistency across: Sales reporting ecosystem
- Sources: Salesforce CRM + ERP system + Spreadsheet uploads
- Target: Executive sales dashboard
- Elements: Revenue totals, deal counts, win rates
- Issue: Monthly sales number differs by 12% across systems"
```

## Quality Assurance Templates

### Automated Testing Validation

```
Validate automated testing results for: [TESTING_DOMAIN]

Testing Context:
- Test Suite: [Data pipeline tests/Report tests/Integration tests]
- Test Coverage: [Percentage of code/logic covered]
- Test Environment: [Dev/Test/Staging environment details]
- Execution Frequency: [How often tests run]
- Success Criteria: [What constitutes passing tests]

Test Results Analysis:
- Pass/Fail Rates: [Overall test success statistics]
- Failing Tests: [Specific tests that are failing]
- Performance Tests: [Response time and load test results]
- Regression Tests: [Tests that started failing recently]
- Coverage Gaps: [Areas not covered by automated testing]

Quality Metrics:
- Code Quality: [Static analysis results]
- Data Quality: [Validation rule compliance]
- Performance Quality: [SLA compliance]
- Security Quality: [Security test results]

Recommendations:
- Test coverage improvements
- Test automation enhancements
- Quality gate adjustments
- Performance benchmark updates

Example:
"Validate automated testing for: Customer data pipeline
- Test Suite: 150 data validation tests + 25 performance tests
- Coverage: 85% pipeline logic, 90% business rules
- Issue: 12 tests started failing after latest deployment
- Focus: Determine if failures indicate real issues or test updates needed"
```

### Production Readiness Assessment

```
Assess production readiness for: [SYSTEM_OR_FEATURE]

Readiness Criteria:
- Functional Requirements: [Business functionality completion]
- Non-Functional Requirements: [Performance/security/reliability]
- Quality Gates: [Testing completion and quality metrics]
- Documentation: [User/technical documentation completeness]
- Training: [User training and knowledge transfer]

Technical Readiness:
- Performance Validation: [Load testing and capacity verification]
- Security Review: [Security controls and compliance validation]
- Disaster Recovery: [Backup and recovery procedures]
- Monitoring: [Observability and alerting setup]
- Support Procedures: [Incident response and maintenance plans]

Risk Assessment:
- Technical Risks: [Known issues and mitigation plans]
- Business Risks: [Impact of potential failures]
- Operational Risks: [Support and maintenance considerations]
- Compliance Risks: [Regulatory and audit requirements]

Go/No-Go Decision:
- Critical issues that must be resolved
- Nice-to-have improvements that can wait
- Production deployment timeline
- Rollback procedures and criteria

Example:
"Assess production readiness for: New customer 360 analytics platform
- Functional: All 25 user stories complete
- Performance: Load tested with 500 concurrent users
- Concern: 3 minor data quality issues found in testing
- Timeline: Scheduled go-live in 2 weeks"
```

## Usage Instructions

1. **Select Template**: Choose the template that best matches your QA analysis need
2. **Provide Context**: Fill in all bracketed placeholders with specific details
3. **Include Log Data**: Paste relevant log entries or error messages
4. **Specify Focus**: Indicate what type of analysis or investigation you need
5. **Submit Request**: Send completed prompt to QA Buddy
6. **Review Analysis**: Validate the findings and recommendations
7. **Take Action**: Implement suggested remediation steps
8. **Follow Up**: Monitor improvements and track resolution

## Best Practices

- **Complete Information**: Provide comprehensive context and recent changes
- **Specific Examples**: Include exact error messages and log entries
- **Business Impact**: Explain how issues affect users and business processes
- **Timeline Context**: Specify when issues started and any correlating events
- **Expected Behavior**: Describe what normal operations should look like
- **Priority Level**: Indicate urgency and business criticality

---

*Use these templates to get thorough, actionable analysis from the QA Buddy AI assistant for maintaining healthy data platform operations.*