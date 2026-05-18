# Agent: Prospect Research

**Category:** Prospect Intelligence  
**Version:** 1.0  
**Workflow:** Prospect Intake + Dedupe Workflow  
**Skills used:** B2B Persona Classification Skill

---

## Purpose
Builds a raw target account and contact list from approved data sources, scoped to ICP-matching companies and decision-maker contacts within each account.

---

## Trigger
Campaign approved with ICP definition confirmed. User initiates prospect build from the control tower.

---

## Input schema
| Field | Type | Required |
|-------|------|----------|
| campaign_id | uuid | yes |
| icp_definition | object | yes |
| persona_map | list | yes |
| approved_sources | list[string] | yes |
| max_prospects | int | no (default 500) |

---

## Reasoning logic
1. Parse ICP definition into source query parameters (industry, region, company size, seniority)
2. Query each approved source for matching companies (accounts)
3. For each account, identify contacts matching the target persona seniority and function
4. Return raw, undeduped, unenriched prospect list for handoff to Data Quality agent
5. Log source, query params, and count per source in agent run record

---

## Output schema
| Field | Type | Description |
|-------|------|-------------|
| raw_prospects | list | Undeduped contact records from all sources |
| accounts_found | int | Total matching companies |
| contacts_found | int | Total raw contacts returned |
| source_breakdown | object | Count per approved source |
| query_params_used | object | ICP parameters applied to each source |

---

## Rules
- Only query sources in the `approved_sources` list
- Do not enrich or clean data — pass raw to Data Quality agent
- Do not classify personas — pass raw designations for Persona Classifier agent
- Log all queries in AuditLog

---

## Failure modes
| Failure | Handling |
|---------|----------|
| Source API unavailable | Skip source, log failure, continue with remaining sources |
| Zero results from all sources | Return empty list with flag for human review |
| Source returns >2000 records | Cap at 2000, flag for review, recommend ICP refinement |

---

## Open dependency
Specific data source tools (Apollo, Clay, ZoomInfo, Sales Navigator, etc.) must be defined before this agent is implemented. The agent is source-agnostic by design.
