# Hybrid AI Platform — Offline-first (HAP)

> Project ID: `HAP-2026-OFFLINE-FIRST`  
> Repository: https://github.com/0816155422/hybrid-ai-platform  
> Evidence policy: evidence over assumptions; do not report a check as passed without execution evidence.

## Current verified repository facts

- Repository exists and its default branch is `main`.
- Repository visibility was observed as `private` through the GitHub connector on 2026-10-21. This verifies the visibility field only; collaborator/app access and prior public exposure were not audited.
- The repository now contains documentation, an evidence validator, a fixed-command test orchestrator, unit-test definitions, and a GitHub Actions workflow. Presence of these files does **not** prove the tests passed, the extension is installed, or a security sandbox exists.

## Governance and current phase

- Current phase: `PHASE_0_BLOCKED`
- Phase label: `PHASE_0_DOCUMENTATION_AND_GOVERNANCE_REVIEW`
- Phase 1 authorization: `PHASE_1_NOT_AUTHORIZED`
- Specification status: `NOT_APPROVED_FOR_FREEZE` / `REVISION FINAL+ — PENDING INDEPENDENT REVIEW`
- Database write policy recorded for the project: `ZERO_DATABASE_WRITE`
- Remote mutation policy recorded for the project: `PROHIBITED`
- Human approval required: `TRUE`

This repository commit is an explicitly user-requested documentation action. It does not authorize database writes, deployment, external service mutations, or progression to Phase 1. If project governance is changed later, record the change and its evidence explicitly.

## Non-negotiable verification rules

1. Separate verified facts, user-provided requirements, proposals, assumptions, and unknowns.
2. Do not mark a gate `PASS` based on documentation alone. A gate requires the evidence specified by its acceptance criteria.
3. Preserve append-only history; do not silently overwrite checkpoints or execution history.
4. If a check fails, record the failure, cause if known, affected requirement, recovery action, and the re-validation result.
5. Keep authorization, permission, waiting, and not-found states distinct.
6. Automated skills and scripts must not write directly to a central database or vault unless a separately approved and evidenced write path permits it.
7. Do not store API keys, passwords, tokens, raw secrets, or private personal information in this repository.
8. Use SHA-256 to identify captured source artifacts where bytes are available. A hash proves byte identity, not authenticity or completeness.

## Planned documentation inventory

The following are collection targets, not claims that the artifacts already exist or are complete:

- Project overview, scope, requirements, and decision history
- Architecture and data-flow descriptions
- Database/schema proposal and migration plan
- Tool and connector inventory with actual permission boundaries
- Gate register G1–G10 and requirements BR-001–BR-007
- Gap register G-01–G-11
- Baseline document set DOC-A01 through DOC-G03
- Evidence register with source URL/path, source version or commit, capture time, SHA-256, verification method, and status
- Append-only execution ledger / checkpoint history
- Independent verification plan and adversarial test matrix
- Handoff package index and unresolved-items register

Each artifact must be labeled as one of: `VERIFIED`, `USER_PROVIDED_UNVERIFIED`, `PROPOSED`, `NOT_FOUND`, `NOT_RUN`, or `BLOCKED`. Do not imply that placeholder datasets or proposed schemas are real deployed data.

## Evidence register format

For every captured artifact, record:

| Field | Meaning |
|---|---|
| Evidence ID | Stable unique identifier |
| Artifact name | Human-readable title |
| Source | URL, repository path, or source system |
| Source version | Commit SHA, release, revision, or `UNKNOWN` |
| Captured at | Timestamp with timezone |
| SHA-256 | Hash of the exact captured bytes, or `NOT_COMPUTED` |
| Verification method | Reproducible procedure |
| Status | One of the defined evidence statuses |
| Limitations | Missing context, unavailable bytes, or other caveats |

Never invent a source version, capture time, hash, test result, or approval.

## Immediate blockers and next steps

1. Change repository visibility to Private before adding any confidential history. Verify the resulting visibility from GitHub.
2. Collect the original Phase 0–3 documents and source artifacts. Preserve exact originals separately from normalized summaries.
3. Compute SHA-256 from the exact bytes of each captured file and independently re-check the hashes.
4. Populate the evidence register and database/schema/tool inventories using evidence, not inference.
5. Run an independent consistency review against the requirements and gate register.
6. Keep Phase 1 blocked until the defined gates are reviewed and explicitly authorized.

## Change log

### Initial index

- Added this README as the initial repository index following the user's explicit request to begin writing to this repository.
- No existing repository files were overwritten.
- No database, deployment, connector, or external service state was changed by this documentation commit.
- This index is not a complete transcript archive and does not establish that the listed future artifacts have been collected.


## Repository map

- [Architecture baseline](docs/ARCHITECTURE.md)
- [Data and evidence contracts](docs/DATA-CONTRACTS.md)
- [Evidence-first workflow](docs/WORKFLOW-SPEC.md)
- [Verification matrix](docs/VERIFICATION-MATRIX.md)
- [Append-only decision log](docs/DECISION-LOG.md)
- [Evidence store rules](evidence/README.md)
- [Artifact register](evidence/register/ARTIFACT_REGISTER.csv)
- [SHA-256 manifest template](evidence/manifests/SHA256_MANIFEST.json)
- [External source audit and collection status](docs/HAP_EXTERNAL_SOURCE_AUDIT_2026-10-20.md)
- [Tool, skill, and connector inventory](docs/TOOL-INVENTORY.md)
- [Proposed database structure and write boundaries](docs/DATABASE-STRUCTURE.md)
- [Phase 0–3 source collection plan](docs/PHASE0-3-SOURCE-COLLECTION.md)
- [Execution evidence contract](evidence/execution/README.md)
- [Current Phase 0 checkpoint snapshot](evidence/checkpoints/CURRENT_STATE.json)
- [Evidence validator](scripts/validate_evidence.py)
- [Validator unit tests](tests/test_validate_evidence.py)
- [GitHub Actions validation workflow](.github/workflows/hap-evidence-validation.yml)

## Repository operating note

This repository is the designated versioned project store. Only files actually collected and verified may be marked complete. The repository was most recently reported as **Public** by the connected GitHub listing; do not commit confidential history, credentials, or sensitive personal data until Private visibility is independently confirmed. The user requested a “4D” format, but the exact four-D definition is not present in the reviewed project context; its mapping remains blocked rather than guessed.
