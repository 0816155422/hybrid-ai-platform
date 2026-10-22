# HAP Source Collection — Batch 01

- Project: Hybrid AI Platform — Offline-first (HAP)
- Project ID: `HAP-2026-OFFLINE-FIRST`
- Collection date: 2026-10-22
- Collection mode: read-only source acquisition; this branch contains only collection metadata and references.
- Source branch base: `main`
- Base commit observed: `55d011f304ee7f811db06158ba3eb4e79bc9bf8a`
- Collection state: `PARTIAL` — do not treat as complete, audited, or approved.
- No changes were made to `main`. This collection is on a new branch.
- No API tokens, credentials, or secret values are recorded here.

## Project guardrails observed

- Current project state recorded in prior project context: `PHASE_0_BLOCKED`
- Next phase: `PHASE_1_NOT_AUTHORIZED`
- `DATABASE_WRITE_POLICY: ZERO_DATABASE_WRITE`
- `REMOTE_MUTATION_POLICY: PROHIBITED` (this branch was created only after the user's explicit instruction to continue the collection in GitHub; no database or main-branch changes were made).
- `HUMAN_APPROVAL_REQUIRED: TRUE`
- Specification: `NOT_APPROVED_FOR_FREEZE` / `REVISION FINAL+ — PENDING INDEPENDENT REVIEW`

## Confirmed source artifacts available

| ID | Source | Artifact / location | Acquisition status | Notes |
|---|---|---|---|---|
| SRC-001 | ChatGPT Library | `HAP_Research_Completion_Pack_v1.0.0.zip` | Read/materialized | ZIP has 12 members. SHA-256: `2591ee167a2009234175488ccc16991940a4f9201994c0282f83a909644a263d`. ZIP integrity check returned no corrupt member. |
| SRC-002 | ChatGPT Library | `HAP_RESEARCH_BACKED_PHASE0_BASELINE.md` | Read/materialized | Baseline / research-backed Phase 0 material. |
| SRC-003 | ChatGPT Library | `evidence-record.schema.json` | Read/materialized | Evidence record schema. |
| SRC-004 | ChatGPT Library | `state-manifest.schema.json` | Read/materialized | State manifest schema. |
| SRC-005 | ChatGPT Library | `PACK_FILE_MANIFEST.json` | Read/materialized | Pack file manifest; the manifest excludes itself from its own hash list. |
| SRC-006 | GitHub | [hybrid-ai-platform](https://github.com/0816155422/hybrid-ai-platform) | Connected repository confirmed | Default branch `main`; observed base commit above; connector reports push/admin permissions. |
| SRC-007 | GitHub | [hybrid-ai-platform-blueprint](https://github.com/0816155422/hybrid-ai-platform-blueprint) | Connected repository confirmed | Secondary related repository; not modified. |
| SRC-008 | GitHub repo docs | `docs/PHASE0-3-SOURCE-COLLECTION.md` | Previously fetched | Source collection plan. |
| SRC-009 | GitHub repo docs | `docs/ARCHITECTURE.md` | Previously fetched | Architecture. |
| SRC-010 | GitHub repo docs | `docs/DATA-CONTRACTS.md` | Previously fetched | Data contracts. |
| SRC-011 | GitHub repo docs | `docs/DATABASE-STRUCTURE.md` | Previously fetched | Database structure. |
| SRC-012 | GitHub repo docs | `docs/WORKFLOW-SPEC.md` | Previously fetched | Workflow specification. |
| SRC-013 | GitHub repo docs | `docs/CENTRAL-DATA-COLLECTION-ADAPTER.md` | Previously fetched | Central data collection adapter. |
| SRC-014 | Notion | `Project Control & Checkpoints` | Discovered/read via connected source | Project controls and checkpoints. |
| SRC-015 | Notion | `Unified Master & Consolidation Map (Draft)` | Discovered/read via connected source | Consolidation map draft. |
| SRC-016 | Notion | `Research Completion Pack Intake & Verification` | Discovered/read via connected source | Intake/verification notes. |
| SRC-017 | Notion | `Checkpoint 2026-10-22 unified master reconciliation` | Discovered/read via connected source | Recent checkpoint record. |
| SRC-018 | Asana | `Hybrid AI Platform — Offline-first | Master Execution` | Project discovered | Task details and full history still need source-by-source export/collection. |
| SRC-019 | Hjarni Notes | `HAP canonical project control/recovery index` | Search result discovered | Full note body not yet captured in this batch. |
| SRC-020 | Hjarni Notes | `HAP missing evidence hunt` | Search result discovered | Full note body not yet captured in this batch. |
| SRC-021 | Hjarni Notes | `HAP master raw evidence vault report` | Search result discovered | Full note body not yet captured in this batch. |

## External normative/reference sources cited by project materials

| ID | Source | URL | Purpose stated in project context |
|---|---|---|---|
| EXT-001 | JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12/ | Schema validation format |
| EXT-002 | NIST FIPS 180-4 | https://csrc.nist.gov/pubs/fips/180-4/upd1/final | Secure hash standard |
| EXT-003 | W3C PROV-DM | https://www.w3.org/TR/prov-dm/ | Provenance model |
| EXT-004 | NIST SP 800-53 Rev. 5 | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | Security/privacy control catalog |
| EXT-005 | Android offline-first architecture | https://developer.android.com/topic/architecture/data-layer/offline-first | Offline-first data-layer guidance |
| EXT-006 | Obsidian Android help | https://obsidian.md/help/android | Android platform guidance |
| EXT-007 | CouchDB replication/conflicts | https://docs.couchdb.org/en/stable/replication/conflicts.html | Replication/conflict handling |
| EXT-008 | DCMI Metadata Terms | https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | Metadata vocabulary |
| EXT-009 | ISO/IEC 42001:2023 | https://www.iso.org/standard/42001 | AI management system standard |

## Collection limitations / outstanding source acquisition

1. The complete raw contents of all prior project conversations are not yet captured as a single export. This collection must not be represented as a verbatim archive of every chat.
2. The full bodies and attachments of the Notion pages listed above need to be captured with source identifiers, canonical URLs, timestamps, and version/history metadata where available.
3. Asana task descriptions, comments, attachments, dependencies, and activity history need source-by-source capture.
4. Hjarni Notes full note bodies and metadata need capture.
5. GitHub repository tree, all relevant branches/tags, issues, pull requests, Actions runs, commit history, and all project-relevant files need a complete inventory; the six docs above are not the whole repository.
6. Library source files and all 12 ZIP members need a durable source inventory with byte lengths and SHA-256 values. The ZIP hash is confirmed above; the individual member hashes should be copied from a fresh manifest-generation result, not retyped from memory.
7. Official external references need a record of URL, retrieval time, title/version, and any applicable publication/update date.
8. A complete portable bundle has not yet been produced in this branch. The earlier file-generation attempt was denied by a temporary tool limit; no new ZIP bundle is claimed here.
9. The repository clone attempt failed because DNS resolution for github.com was unavailable in that runtime. GitHub connector/API access works and should be used for source retrieval.
10. This batch is a source register and recovery index only. It is not an audit, test report, approval, phase transition, or evidence that the implementation has passed real-world validation.

## Required next collection batches

- Batch 02: Export/capture full Notion source pages and their metadata.
- Batch 03: Capture Asana project/task records, comments, dependencies, attachments, and history.
- Batch 04: Capture Hjarni Notes full bodies and metadata.
- Batch 05: Enumerate GitHub repository trees and collect relevant source/config/workflow/docs, issues, PRs, commit and Actions metadata.
- Batch 06: Inventory Library pack members, schema files, hashes, byte lengths, and exact provenance.
- Batch 07: Capture official external references with retrieval metadata.
- Batch 08: Collect available project chat history and explicitly record any unavailable or truncated conversation sources.
- After collection is complete: reconcile duplicates/conflicts, then perform completeness/correctness checks only as a separate phase.

## Integrity note

This document is a human-readable source register. Its own Git blob SHA and commit SHA are provided by the GitHub API result for the commit that adds it. A detached manifest with hashes for every collected raw artifact remains outstanding.
