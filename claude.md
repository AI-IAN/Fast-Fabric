# Claude Code Instructions for Fabric Fast-Track Development

## Development Environment Configuration
**CRITICAL: Claude Code is configured for autonomous development in this environment**
- Working directory: /root/Fast-Fabric/
- All operations must be performed within this directory structure
- Follow Fabric Fast-Track blueprint specifications strictly
- Use TodoWrite/TodoRead tools for all task management

## Project Overview
This is the Fabric Fast-Track Accelerator - a reusable, end-to-end Microsoft Fabric & Power BI starter kit with private AI developer co-pilot. The goal is to enable standing up a modern data platform for mid-market clients in less than 1 day and ship first insights within the first week.

## Blueprint Compliance Requirements
**MANDATORY: All development must strictly adhere to Fabric Fast-Track blueprint specifications:**
- Follow architectural patterns defined in blueprint documentation
- Implement technical requirements as specified in blueprint
- Maintain consistency with blueprint guidelines for all components
- Validate deliverables against blueprint success criteria
- Reference blueprint specifications before implementing any feature

## Development Methodology
Follow the 6-Week Sprint Methodology with 25-45 minute focused sprints:

### Sprint Structure
- Week 1: Infrastructure setup (IaC, folder structure, deployment)
- Week 2: Ingest kit (Dataflow Gen2, Spark notebooks) 
- Week 3: Semantic model (DAX library, bim files)
- Week 4: Report pack (Power BI themes, screenshots)
- Week 5: Governance & DevOps (pipelines, data quality)
- Week 6: AI assistant MVP & sales collateral

### Sprint Rules
- Keep Doing column ≤ 3 cards to prevent context-switch overload
- Each sprint = 25-45 minutes focused work
- Update task status in real-time using TodoWrite/TodoRead tools
- Complete current tasks before starting new ones
- Mark tasks complete IMMEDIATELY after finishing

## Core Technical Requirements

### Mandatory Deliverables Success Criteria
- Deploy: Tenant deploys in less than 15 min with zero manual clicks
- Ingest: Pipeline runs on demo data and lands bronze Delta tables
- Model: Model validates and refreshes in Direct Lake at F2+
- Visuals: Reports render with less than 2 sec visual load
- Governance: Git push triggers Test workspace update plus data-quality pass
- AI Assistant: Generate DAX measure and draft release notes in one click

### AI Assistant Features Priority Order
1. Secrets vault - env file with per-provider keys
2. Provider router - chooses openai, claude, or local via prompt tag
3. Offline fallback - LLM_OFFLINE=True produces deterministic stubs
4. Token and cost tracker - logs to SQLite, surfaced in Power BI tile
5. Prompt versioning - prompts organized by feature with version control
6. Core Modules:
   - Source Mapper: YAML medallion spec generator
   - DAX Genie: validated measure with commentary
   - QA Buddy: scans logs for issues
   - Release Scribe: git diff to markdown notes

## Development Best Practices

### Code Standards
- Branch per feature (feat/ingest-sql-template)
- Commit format: type(scope): summary
- Docs first - update docs/ in same PR
- Keep secrets out of git - use env template files

### Testing and Validation
- Validate all Bicep templates deploy successfully
- Test AI assistant in both online and offline modes
- Verify Direct Lake refresh works at F2+ capacity
- Ensure reports load within 2-second target

### Task Management Requirements
- Use TodoWrite tool for ALL sprint planning and task tracking
- Break complex features into 25-45 minute tasks
- Mark tasks complete IMMEDIATELY after finishing
- Maintain single task in_progress at any time
- Update docs/Gotchas.md when issues are discovered

## File Structure Compliance
Ensure all development follows this exact structure:
- infra/: IaC Bicep/Terraform plus SKU estimator
- ingest/: Dataflow Gen2 JSON plus Spark notebooks  
- model/: bim file, DAX library, generator prompts
- reports/: Themed Power BI report pack plus screenshots
- governance/: Deployment pipeline, RLS shortcuts, data-quality
- ai-assistant/: LLM router, prompts, cost-tracker DB, Streamlit UI
- tools/: Gateway-health scripts, DR scripts, misc utilities
- docs/: Gotchas.md, Architecture.svg, ROI-calculator.pbit
- legal/: EULA.md, AI-tool-clause.md, SOW-templates

## Success Metrics
- Deploy: Fabric workspaces spin up in less than 15 minutes
- Ingest: Demo data flows through to bronze Delta tables
- Model: Semantic model refreshes successfully in Direct Lake
- Reports: All visuals load within 2-second performance target
- AI: Generate DAX measures and release notes autonomously
- Cost: AI assistant daily spend stays under 5 dollar budget

## Autonomous Development Guidelines
- **Blueprint First**: Always reference and follow Fabric Fast-Track blueprint specifications
- Proactively use TodoWrite for sprint planning and tracking
- Follow 6-week roadmap but adapt based on blockers and blueprint requirements
- Prioritize core deliverables over nice-to-have features
- Test offline modes before considering features complete
- Update documentation concurrently with code changes
- Commit frequently with meaningful messages following blueprint patterns
- Focus on momentum over perfection - ship working MVPs that meet blueprint standards
- Validate all implementations against blueprint architecture and requirements

## Key Reference Files
- Blueprint specifications: fabric_fast_track_blueprint.md
- Task backlog: fabric_fast_track_backlog.md 
- Working practices: fabric_fast_track_best_practices.md
- Issues log: docs/Gotchas.md

## Claude Code Tool Usage
- Use TodoWrite/TodoRead extensively for task management
- Leverage all available tools for autonomous development
- Prioritize blueprint compliance in all development decisions
- Maintain focus on deliverable outcomes per sprint methodology

---
Blueprint-driven autonomous development: Kick-off is one commit away—momentum beats perfection\!
