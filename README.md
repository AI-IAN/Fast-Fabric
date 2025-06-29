# Fabric Fast-Track Accelerator

A reusable, end-to-end Microsoft Fabric & Power BI starter kit + private AI developer co-pilot that lets you stand-up a modern data platform for any mid-market client in < 1 day and ship first insights inside the first week.

## Quick Start
1. Deploy infrastructure: cd infra && ./deploy.sh
2. Configure ingest: cd ingest && python setup_dataflows.py
3. Build semantic model: cd model && tabular-editor deploy
4. Launch reports: cd reports && power-bi-cli publish

## Project Structure
- infra/: IaC - Bicep/Terraform + SKU estimator sheet
- ingest/: Dataflow Gen2 JSON + Spark notebooks
- model/: .bim file, DAX library, generator prompts
- reports/: Themed Power BI report pack + screenshots
- governance/: Deployment pipeline, RLS shortcuts, data-quality
- ai-assistant/: LLM router, prompts, cost-tracker DB, Streamlit UI
- tools/: Gateway-health PS1, DR scripts, misc utilities
- docs/: Gotchas.md, Architecture.svg, ROI-calculator.pbit
- legal/: EULA.md, AI-tool-clause.md, SOW-templates

## Core Features
- Deploy: Fabric workspaces (Dev/Test/Prod) in < 15 min
- Ingest: Parameterised templates for SQL, SaaS API, flat-file
- Model: Composable semantic model with 25+ reusable DAX measures
- Visuals: Executive KPIs, operational drill-down, finance variance reports
- Governance: YAML deployment pipeline with data quality checks
- AI Assistant: Multi-provider LLM router with cost tracking

Kick-off is one commit away—momentum beats perfection\!
