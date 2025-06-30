# Release Scribe User Prompt Templates

## Template Categories

### 1. Git Diff Analysis for Release Notes

```
Generate release notes from git changes: [RELEASE_IDENTIFIER]

Release Context:
- Version/Tag: [Release version or tag name]
- Release Type: [Major/Minor/Patch/Hotfix]
- Target Audience: [Developers/Business Users/Executives/All]
- Deployment Timeline: [Planned deployment date and window]
- Previous Version: [Last release version for comparison]

Git Information:
- Branch/Commit Range: [main..release-branch or commit1..commit2]
- Repository: [Repository name and context]
- Time Period: [Development period for this release]

Git Diff/Changes:
[Paste git diff output, commit messages, or file change list here]

Documentation Requirements:
- Release Notes Style: [Formal/Informal/Technical/Business-focused]
- Detail Level: [High-level summary/Detailed/Technical deep-dive]
- Breaking Changes: [Highlight any breaking changes]
- Migration Guide: [Include migration steps if needed]

Example:
"Generate release notes from git changes: Fabric Fast-Track v2.1.0
- Release Type: Minor release with new AI assistant features
- Target Audience: Business users and data analysts
- Deployment: Saturday maintenance window, January 20th
- Focus: New DAX generation capabilities and performance improvements"
```

### 2. Feature Release Documentation

```
Create feature release documentation for: [FEATURE_NAME]

Feature Context:
- Feature Description: [What the feature does and why it was built]
- Business Value: [How it helps users and organization]
- User Stories: [Key user scenarios the feature addresses]
- Development Team: [Team or individuals who built it]
- Integration Points: [How it connects with existing features]

Technical Details:
- Implementation Approach: [High-level technical approach]
- Dependencies: [New libraries, services, or infrastructure required]
- Configuration Changes: [Any settings users need to adjust]
- Database Changes: [Schema modifications or data migrations]
- API Changes: [New endpoints or modifications to existing ones]

Change Analysis:
[Include git diff, file changes, or commit history]

Documentation Needs:
- User Guide Updates: [What documentation needs to be created/updated]
- Training Materials: [Any training or onboarding requirements]
- Support Information: [How users can get help with the new feature]
- Success Metrics: [How to measure successful adoption]

Example:
"Create feature release documentation for: AI-Powered DAX Generation
- Feature: Natural language to DAX measure conversion
- Business Value: Reduces measure creation time from hours to minutes
- Users: Business analysts and data modelers
- Integration: Works with existing semantic model and Power BI reports"
```

### 3. Hotfix and Bug Fix Documentation

```
Document hotfix release for: [CRITICAL_ISSUE]

Hotfix Context:
- Issue Severity: [Critical/High/Medium - production impact level]
- Root Cause: [Brief explanation of what caused the issue]
- Business Impact: [How the issue affected users/business operations]
- Resolution Timeline: [How quickly fix needs to be deployed]
- Affected Systems: [Which components or features were impacted]

Technical Resolution:
- Fix Description: [What was changed to resolve the issue]
- Code Changes: [Specific files or components modified]
- Testing Performed: [Validation done before deployment]
- Risk Assessment: [Potential side effects of the fix]

Change Details:
[Include git diff, commit messages, or specific code changes]

Deployment Requirements:
- Deployment Priority: [Emergency/Urgent/Scheduled]
- Rollback Plan: [How to revert if fix causes issues]
- Monitoring: [What to watch after deployment]
- Communication: [Who needs to be notified and when]

Example:
"Document hotfix release for: Data pipeline failure causing missing revenue data
- Severity: Critical - Executive dashboard showing incorrect revenue
- Root Cause: Currency conversion API timeout handling
- Impact: 15% revenue reporting error affecting board presentation
- Timeline: Must be fixed within 4 hours"
```

### 4. Infrastructure and Deployment Changes

```
Create deployment documentation for: [INFRASTRUCTURE_CHANGE]

Infrastructure Context:
- Change Type: [New deployment/Configuration update/Capacity change/Security update]
- Environment: [Development/Test/Production/All environments]
- Business Justification: [Why this change is needed]
- Stakeholder Impact: [How changes affect different user groups]
- Compliance Requirements: [Any regulatory or security considerations]

Technical Changes:
- Infrastructure Components: [Fabric capacity/Storage/Networking/Security]
- Configuration Updates: [Settings or parameter changes]
- Resource Requirements: [CPU/Memory/Storage/Cost implications]
- Dependencies: [Other systems or services affected]

Change Documentation:
[Include infrastructure code, configuration files, or deployment scripts]

Operational Impact:
- Downtime Requirements: [Planned outage windows if needed]
- Performance Impact: [Expected performance changes]
- Monitoring Changes: [New metrics or alerts to implement]
- Support Procedures: [Updated troubleshooting or maintenance steps]

Example:
"Create deployment documentation for: F2 to F4 capacity upgrade
- Change Type: Fabric capacity scaling for performance improvement
- Environment: Production workspace
- Justification: Pipeline performance degradation due to data growth
- Impact: 2-hour maintenance window, improved user experience afterward"
```

### 5. Security and Compliance Updates

```
Document security release for: [SECURITY_UPDATE]

Security Context:
- Security Classification: [Low/Medium/High/Critical vulnerability or enhancement]
- Compliance Framework: [GDPR/SOX/HIPAA/Custom security requirements]
- Risk Assessment: [What risks are being mitigated]
- Regulatory Requirements: [Any mandatory compliance deadlines]
- Stakeholder Notification: [Who needs to be informed of security changes]

Security Changes:
- Vulnerability Details: [If fixing known issue - CVE numbers, impact]
- Security Enhancements: [New security controls or improvements]
- Access Control Changes: [Permission or authentication modifications]
- Data Protection Updates: [Encryption, masking, or privacy enhancements]

Technical Implementation:
[Include security-related code changes, configuration updates, or policy changes]

Compliance Documentation:
- Audit Trail: [How changes support audit and compliance requirements]
- Evidence Collection: [What documentation proves compliance]
- Testing Requirements: [Security testing needed before deployment]
- Training Impact: [User training needed for security changes]

Example:
"Document security release for: Enhanced multi-factor authentication
- Classification: High - Mandatory security enhancement
- Compliance: SOX compliance requirement for financial data access
- Risk: Mitigates account compromise and unauthorized data access
- Timeline: Must be deployed before quarter-end audit"
```

## Specialized Scenario Templates

### Data Platform Release

```
Generate data platform release notes for: [DATA_PLATFORM_UPDATE]

Data Platform Context:
- Platform Components: [Ingestion/Transformation/Storage/Analytics/Governance]
- Data Sources Affected: [Which source systems have changes]
- Analytics Impact: [How reports, dashboards, or models are affected]
- User Groups: [Data engineers/Data analysts/Business users]
- Data Quality: [Any data quality improvements or changes]

Platform Changes:
- Pipeline Updates: [New data sources, transformation logic, or scheduling]
- Model Changes: [Semantic model updates, new measures, or schema changes]
- Report Updates: [New visualizations, performance improvements, or bug fixes]
- Governance Changes: [Security, compliance, or data quality enhancements]

Technical Details:
[Include relevant code changes, configuration updates, or deployment scripts]

Business Impact:
- New Analytics Capabilities: [What new insights or reports are available]
- Performance Improvements: [Faster queries, more data, better user experience]
- Data Quality Enhancements: [More accurate, complete, or timely data]
- Cost Optimizations: [Resource efficiency or cost reduction benefits]

Example:
"Generate data platform release notes for: Customer 360 analytics enhancement
- Components: New Salesforce integration, enhanced customer segmentation
- Analytics Impact: 5 new executive dashboards, real-time customer scoring
- Users: Sales teams, marketing analysts, customer success managers
- Business Value: 360-degree customer view for better retention strategies"
```

### AI Assistant Feature Release

```
Document AI assistant release for: [AI_FEATURE_UPDATE]

AI Feature Context:
- AI Capability: [DAX Generation/Source Mapping/QA Analysis/Release Notes]
- Model Updates: [LLM model changes, prompt improvements, or new providers]
- User Experience: [Interface changes or new interaction patterns]
- Performance Improvements: [Response time, accuracy, or cost efficiency]
- Integration: [How AI features connect with existing workflows]

AI Implementation:
- Prompt Engineering: [New or improved prompt templates]
- Model Configuration: [LLM routing, fallback mechanisms, or cost controls]
- Training Data: [Any new training data or fine-tuning]
- Quality Assurance: [Testing and validation of AI outputs]

Technical Changes:
[Include AI-related code changes, configuration updates, or model deployments]

User Value:
- Productivity Gains: [Time savings or workflow improvements]
- Quality Improvements: [Better outputs or reduced errors]
- Cost Benefits: [Resource efficiency or cost optimization]
- Learning Curve: [Training or adoption requirements for users]

Example:
"Document AI assistant release for: Enhanced natural language DAX generation
- Capability: Business users can describe measures in plain English
- Model: Updated GPT-4 integration with improved DAX prompt templates
- Experience: New Streamlit interface with guided measure creation
- Value: 80% reduction in measure creation time for business analysts"
```

### Performance and Optimization Release

```
Create performance release documentation for: [PERFORMANCE_IMPROVEMENT]

Performance Context:
- Performance Area: [Query speed/Data processing/Report rendering/System responsiveness]
- Baseline Metrics: [Current performance measurements]
- Target Improvements: [Expected performance gains]
- User Impact: [How performance changes affect user experience]
- Business Value: [Cost savings, productivity gains, or user satisfaction]

Optimization Details:
- Technical Approach: [What was optimized and how]
- Infrastructure Changes: [Capacity, configuration, or resource adjustments]
- Code Optimizations: [Algorithm improvements, caching, or efficiency gains]
- Data Optimizations: [Indexing, partitioning, or storage improvements]

Performance Metrics:
[Include before/after performance measurements and benchmarks]

Implementation:
- Deployment Strategy: [How optimizations will be rolled out]
- Monitoring Plan: [How to track performance improvements]
- Rollback Considerations: [What to do if performance degrades]
- Future Optimizations: [Additional improvements planned]

Example:
"Create performance release documentation for: Direct Lake query optimization
- Area: Power BI semantic model query response time
- Baseline: 15-second average query time
- Target: Sub-3-second response for 95% of queries
- Impact: Dramatically improved dashboard interactivity for 200+ users"
```

## Integration and Deployment Templates

### Multi-System Integration Release

```
Document integration release for: [INTEGRATION_PROJECT]

Integration Context:
- Systems Involved: [List of systems being integrated]
- Integration Pattern: [API/Event-driven/Batch/Real-time]
- Business Process: [What business process is being enabled or improved]
- Data Flow: [How data moves between systems]
- Stakeholder Groups: [Teams or departments affected by integration]

Integration Changes:
- API Modifications: [New endpoints, authentication, or data formats]
- Data Mapping: [How data is transformed between systems]
- Error Handling: [How integration failures are managed]
- Monitoring: [How integration health is tracked]

Technical Implementation:
[Include integration code, configuration files, or deployment scripts]

Business Benefits:
- Process Automation: [Manual processes being automated]
- Data Consistency: [Improved data accuracy or synchronization]
- User Experience: [Workflow improvements or new capabilities]
- Operational Efficiency: [Resource savings or productivity gains]

Example:
"Document integration release for: Real-time Salesforce to Power BI sync
- Systems: Salesforce CRM, Azure Data Factory, Power BI
- Pattern: Real-time API integration with change data capture
- Process: Sales pipeline visibility for executive decision making
- Benefit: 4-hour delay reduced to 15-minute near real-time updates"
```

### Configuration and Settings Update

```
Create configuration update documentation for: [CONFIG_CHANGE]

Configuration Context:
- Configuration Scope: [Application/Infrastructure/Security/Performance settings]
- Change Reason: [Why configuration is being updated]
- Environment Impact: [Which environments are affected]
- User Impact: [How configuration changes affect user experience]
- Compliance Requirements: [Any regulatory or policy drivers]

Configuration Changes:
- Settings Modified: [Specific parameters or configurations changed]
- Default Values: [New default settings or behavior]
- Migration Requirements: [How existing configurations are handled]
- Validation Rules: [How to verify configuration is correct]

Change Details:
[Include configuration files, parameter lists, or setting documentation]

Implementation Guide:
- Pre-change Checklist: [What to verify before making changes]
- Change Procedure: [Step-by-step configuration update process]
- Validation Steps: [How to confirm changes are working correctly]
- Rollback Process: [How to revert if issues occur]

Example:
"Create configuration update documentation for: Enhanced data refresh scheduling
- Scope: Power BI semantic model refresh frequency and timing
- Reason: Optimize performance and reduce capacity conflicts
- Impact: Users see more current data with better system responsiveness
- Change: Refresh schedules optimized based on usage patterns"
```

## Quality and Testing Templates

### Testing and Validation Release

```
Document testing update for: [TESTING_ENHANCEMENT]

Testing Context:
- Testing Scope: [Unit/Integration/Performance/Security/User acceptance testing]
- Quality Goals: [What quality improvements are being implemented]
- Coverage Improvements: [Areas of increased test coverage]
- Automation Enhancements: [New automated testing capabilities]
- Risk Mitigation: [How testing reduces deployment and operational risks]

Testing Changes:
- New Test Cases: [Additional scenarios being validated]
- Test Automation: [Automated testing tools or frameworks added]
- Performance Testing: [Load, stress, or performance validation]
- Security Testing: [Security scanning or penetration testing]

Implementation Details:
[Include test code, configuration, or validation procedures]

Quality Benefits:
- Defect Reduction: [Expected reduction in production issues]
- Deployment Confidence: [Improved release confidence and speed]
- User Experience: [More reliable and predictable system behavior]
- Maintenance Efficiency: [Faster troubleshooting and issue resolution]

Example:
"Document testing update for: Automated data quality validation
- Scope: End-to-end data pipeline testing with business rule validation
- Goals: Catch data quality issues before they reach production reports
- Automation: Daily validation of data completeness, accuracy, and timeliness
- Benefit: 90% reduction in data quality issues reaching business users"
```

## Usage Instructions

1. **Select Template**: Choose the template that best matches your release scenario
2. **Gather Information**: Collect git diffs, commit messages, and change context
3. **Fill Context**: Replace bracketed placeholders with specific release details
4. **Add Technical Details**: Include relevant code changes or configuration updates
5. **Submit Request**: Send completed prompt to Release Scribe
6. **Review Output**: Validate generated documentation for accuracy and completeness
7. **Customize**: Adjust tone and detail level for target audience
8. **Distribute**: Share release notes with appropriate stakeholders

## Best Practices

- **Complete Git Information**: Provide comprehensive change details and context
- **Business Context**: Explain why changes were made and their business value
- **Audience Awareness**: Specify target audience for appropriate communication style
- **Risk Assessment**: Include potential impacts and mitigation strategies
- **Clear Timeline**: Specify deployment windows and important dates
- **Support Information**: Include how users can get help or report issues

---

*Use these templates to generate professional, comprehensive release documentation that enables confident deployment decisions and effective change communication.*