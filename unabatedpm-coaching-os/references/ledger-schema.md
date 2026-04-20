# Assessment Ledger Schema

The assessment ledger (`assessments.jsonl`) is the single source of truth for all PM Assessment data. It's an append-only sequence of immutable events. The dashboard and versions.json are derived views that can be rebuilt from the ledger at any time.

## Entry Types

### Assessment Entry (type: "assessment")

Written by `/audit` for each document evaluated.

```json
{
  "id": "evt_{YYYYMMDD}_{HHMMSS}_{documentId}",
  "type": "assessment",
  "timestamp": "ISO 8601 timestamp",
  "documentId": "filename.ext (original filename, used as stable key)",
  "documentName": "Human-readable name extracted from document content",
  "contentHash": "sha256 hash of document text content",
  "classification": "One of: Strategy Document, PRD, Business Case, Pitch Deck, Demo Script, Customer Research, OKRs, Stakeholder Update, Competitive Analysis, GTM Plan, Resume, LinkedIn Profile, Portfolio, 30/60/90 Plan",
  "format": "docx|pptx|pdf|md|txt",
  "scores": {
    "total": 0-80,
    "pillars": {
      "strategy": {
        "total": 0-20,
        "categories": {
          "market_customer_intelligence": 0-5,
          "problem_discovery_prioritization": 0-5,
          "business_models_pitching": 0-5,
          "vision_storytelling": 0-5
        }
      },
      "delivery": {
        "total": 0-20,
        "categories": {
          "problem_solution_definition": 0-5,
          "stakeholder_alignment": 0-5,
          "team_throughput_quality": 0-5,
          "solution_validation": 0-5
        }
      },
      "cx": {
        "total": 0-20,
        "categories": {
          "journey_optimization": 0-5,
          "support_success_enablement": 0-5,
          "user_behavior_insights": 0-5,
          "messaging_communication": 0-5
        }
      },
      "growth": {
        "total": 0-20,
        "categories": {
          "market_segmentation": 0-5,
          "sales_enablement": 0-5,
          "product_evangelism": 0-5,
          "pricing_monetization": 0-5
        }
      }
    }
  },
  "gaps": [
    {
      "category": "category_key",
      "score": 1-5,
      "description": "What's missing or weak",
      "upgradeHint": "What framework or change would improve this"
    }
  ],
  "version": 0,
  "filePath": "relative path to original file",
  "annotationCount": null,
  "iterations": null,
  "pluginVersion": "2.0.0"
}
```

### Upgrade Entry (type: "upgrade")

Written by `/upgrade` after producing an upgraded document.

```json
{
  "id": "evt_{YYYYMMDD}_{HHMMSS}_{documentId}_upgrade",
  "type": "upgrade",
  "timestamp": "ISO 8601 timestamp",
  "documentId": "filename.ext (matches the original documentId)",
  "documentName": "Human-readable name",
  "contentHash": "sha256 hash of upgraded document content",
  "classification": "Same as original assessment",
  "format": "docx|pptx|md",
  "scores": {
    "total": 0-80,
    "pillars": { "...same structure as assessment..." }
  },
  "scoresBefore": "total score from the version being upgraded",
  "gaps": [],
  "version": "integer, incrementing from 1",
  "filePath": "relative path to latest upgraded file (e.g., strategy_upgraded.docx)",
  "archivePath": "relative path to archived copy (e.g., pm_assessment_data/archive/strategy_v1_20260327.docx)",
  "annotationCount": "integer, number of teaching annotations",
  "iterations": "integer, number of QA loop iterations",
  "iterationScores": [26, 41, 56],
  "patterns": [
    "Recurring pattern description 1",
    "Recurring pattern description 2"
  ],
  "pluginVersion": "2.0.0"
}
```

### Develop Entry (type: "develop")

Written by `/develop` when generating a growth plan.

```json
{
  "id": "evt_{YYYYMMDD}_{HHMMSS}_develop",
  "type": "develop",
  "timestamp": "ISO 8601 timestamp",
  "baselineScore": "integer, overall score at time of plan generation",
  "criticalGaps": ["category_key_1", "category_key_2"],
  "exerciseCount": "integer, total exercises across all phases",
  "pluginVersion": "2.0.0"
}
```

### Source tagging (all entry types)

Every entry written on or after 2026-04-17 includes a `source` field at the top level:

```json
{
  "source": "managed-agent" | "local-plugin"
}
```

- `"managed-agent"` — entry was written by the hosted Unabated PM Coach running on Anthropic's Managed Agents via the `mcp.unabatedpm.com` broker.
- `"local-plugin"` — entry was written by the open-source Claude plugin running directly in the user's Claude Code / Cowork session.

This lets migrated local-plugin ledgers coexist with hosted ledger rows in a single Postgres table once a free-tier user converts to paid. Entries written before 2026-04-17 are assumed to be `"local-plugin"` on read.

## Rules

1. **Append-only.** Never modify or delete existing entries. Corrections are new entries with updated data.
2. **Content hashing.** Before writing an assessment entry, compute the sha256 hash of the document text. If an entry with the same documentId and contentHash already exists, skip re-assessment (document hasn't changed). Report cached scores.
3. **Version numbering.** Version 0 is always the original document's first assessment. Upgrade versions start at 1 and increment.
4. **documentId stability.** The documentId is the original filename (e.g., "strategy.docx"). It never changes even when upgraded versions are created. All entries for the same document share the same documentId.
5. **Gap reporting.** Assessment entries include gaps for all categories scoring below 4. Upgrade entries include gaps only for categories that didn't improve (or new gaps discovered in the rewrite).
6. **Source required.** New writes must set `source`; reads must default missing values to `"local-plugin"`.

## Derived Views

### versions.json

Rebuilt from the ledger by:
1. Scan all entries, group by documentId
2. For each document: collect version history, determine latest score, latest file path
3. Compute portfolio aggregates (averages, weakest/strongest categories)

### Dashboard data

The dashboard template receives the full ledger contents as a JSON array. It computes all visualizations client-side (radar chart, heat map, document cards, score trajectories).

## File Location

- Plugin mode: `{user_folder}/pm_assessment_data/assessments.jsonl`
- Web LLM session: Compressed JSON stored in LLM persistent memory
- Hosted product: `assessment_events` Supabase table (same schema, rows instead of lines)
