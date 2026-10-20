# Phase 0–3 Source Collection and Provenance Plan

- Project: `HAP-2026-OFFLINE-FIRST`
- Status: `IN_PROGRESS — COLLECTION TARGETS, NOT COMPLETION CLAIMS`
- Current phase: `PHASE_0_BLOCKED`
- Phase 1: `NOT_AUTHORIZED`

## 1. Scope

Collect and organize the original source artifacts, specifications, code, package records, and verification evidence needed for Phase 0–3 documentation/design review. Phase 0–3 do not require evidence of real-world use unless an approved requirement explicitly says so. Do not add that requirement by assumption.

The GitHub repository linked by the user represents the intended initial project conversation/history period. Do not label that repository as missing later Extension-era history; later project periods are separate source collections.

## 2. Source periods

| Period | Working description | Evidence rule |
|---|---|---|
| Period A | Initial HAP design and Gemini consultation before Extension work | The linked repository is an intended source for this period; preserve its current scope and provenance |
| Period B | Extension V1 onward | Collect the original extension packages, source files, test reports, manifests, and release notes as separate artifacts |
| Period C | Governance, evidence, controls, and recovery design | Collect the actual versions of the documents and records; do not infer a date boundary unless a source proves it |

These labels are an organizing convention, not verified exact date ranges. Record actual dates from commit metadata or source timestamps where available.

## 3. Collection sequence

1. Inventory the current repository at a specific commit.
2. Record branch, commit SHA, path, Git blob SHA, byte size, and source URL for each file.
3. Retrieve original packages/files from their actual source systems where available and authorized.
4. Preserve originals unchanged under a suitable source archive path; derived summaries must be separate.
5. Compute SHA-256 over exact bytes, recording the command/tool version and result.
6. Independently recompute each hash and compare.
7. Map each artifact to requirements, gates, and the verification matrix.
8. Mark absent sources `NOT_FOUND` only after a defined search scope is documented; mark inaccessible sources `BLOCKED` or `UNVERIFIED`.
9. Record every collection failure, missing dependency, and retry as an append-only event.
10. Review the inventory independently before declaring the collection baseline complete.

## 4. Required artifact metadata

Each record in `evidence/register/ARTIFACT_REGISTER.csv` should include:

- Stable artifact ID and project ID
- Title, type, original filename, and origin/source URI
- Version/release/commit SHA, or `UNKNOWN`
- Capture timestamp in UTC with timezone
- Exact byte size, if the bytes are available
- SHA-256 of exact bytes, or `PENDING` with a reason
- Git blob SHA as a separate field
- Evidence status and limitations
- Related requirement/gate IDs where the register schema is extended to include them

Do not fill byte size or SHA-256 from a Git blob SHA. Do not hash a rendered preview and describe it as the original file hash.

## 5. Collection targets

| ID | Collection target | Current state | Completion evidence |
|---|---|---|---|
| SRC-01 | Initial-period repository history | Repository is reachable; current file-level inventory still requires a reproducible export | Commit/path inventory, exact content retrieval, hash report |
| SRC-02 | Original Extension V1+ source and packages | Not fully collected in this repository based on current verified evidence | Original files, source references, SHA-256 manifest |
| SRC-03 | Extension test/install evidence | Historical reports exist in prior context, but full fresh rerun is not established | Raw logs, environment details, exact artifact digest, rerun results |
| SRC-04 | ChatGPT export archive | Not yet collected in this repository | Original export, file inventory, SHA-256, coverage report |
| SRC-05 | Gemini export archive | Not yet collected in this repository | Original export, file inventory, SHA-256, coverage report |
| SRC-06 | Hjarni/Notion/Asana source snapshots | Partial source references available from prior audit | Retrieved source/version, capture time, limitation notes |
| SRC-07 | Tool/connector permission evidence | Partial and time-bound | Per-tool capability call, scope, result, and read-back where relevant |
| SRC-08 | Phase 0–3 gate and requirement source documents | Incomplete / not approved for freeze | Source-proven requirement-to-evidence mapping and independent review |

## 6. Privacy gate

The repository was most recently observed as public. Until a fresh repository read confirms Private visibility and access has been reviewed:

- do not upload raw conversation exports;
- do not upload secrets, credentials, tokens, or private keys;
- do not upload sensitive personal data;
- use only non-sensitive specifications and evidence metadata.

A user's intention to make the repository private is not proof that visibility has changed. Re-check the repository metadata before any sensitive archive is committed.

## 7. Completion definition

The collection baseline is complete only when all in-scope source targets are either registered with provenance and integrity evidence or explicitly dispositioned with documented search scope and reason. Completion of collection does not itself pass Phase 0 gates or authorize Phase 1.
