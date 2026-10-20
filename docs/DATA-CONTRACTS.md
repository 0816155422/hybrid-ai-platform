# HAP Data & Evidence Contracts

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Status: `DRAFT — NOT APPROVED FOR FREEZE`
- Phase: `PHASE_0_BLOCKED`

## 1. Contract principles

1. Preserve source bytes and original names when collecting source artifacts.
2. Record source provenance, version, acquisition time, byte size, and SHA-256 where the bytes are available.
3. Separate `EXPECTED` from `ACTUAL`.
4. Separate `PASS`, `FAIL`, `UNVERIFIED`, `NOT_RUN`, `BLOCKED`, and `NOT_APPLICABLE`.
5. Never mark missing evidence as passed.
6. Do not store secrets or credentials in the repository.
7. Do not treat Git blob SHA as a SHA-256 digest.

## 2. Artifact register fields

| Field | Requirement |
|---|---|
| artifact_id | Stable unique ID, e.g. `ART-0001` |
| project_id | Must equal `HAP-2026-OFFLINE-FIRST` |
| title | Human-readable artifact name |
| artifact_type | source, specification, code, test, report, manifest, decision, or other |
| origin | Repository path, canonical URL, connector ID, or user-provided source |
| original_filename | Original name, if applicable |
| version | Source version or `UNKNOWN` |
| observed_at_utc | ISO-8601 timestamp, if observed |
| byte_size | Exact byte count, if available |
| sha256 | SHA-256 of exact bytes, or `PENDING` |
| git_blob_sha | Optional Git blob identifier, kept distinct from SHA-256 |
| evidence_status | One of the statuses defined below |
| notes | Limitations, transformations, or unresolved questions |

## 3. Execution evidence contract

Each execution record should include:

- `event_id` — stable unique identifier
- `project_id`
- `phase` and `step_id`
- `actor` / tool name and version
- `started_at_utc`, `ended_at_utc` when known
- `command_or_action` with secrets redacted
- `environment` (OS/device/runtime versions where relevant)
- `expected_result`
- `actual_result`
- `exit_code` or explicit reason unavailable
- `stdout_ref`, `stderr_ref`, `report_ref`
- `input_artifact_ids`, `output_artifact_ids`
- `sha256_manifest_ref`
- `verification_status`
- `independent_verifier` and review result, if performed
- `blocker`, `root_cause`, `impact`, `unblock_method`, `completion_condition`, `next_step` when incomplete

## 4. Status vocabulary

| Status | Meaning |
|---|---|
| `PASS` | Acceptance criteria were executed and met with referenced evidence |
| `FAIL` | Execution produced a result that violates acceptance criteria |
| `UNVERIFIED` | Evidence is insufficient to establish the result |
| `NOT_RUN` | The check has not been executed |
| `BLOCKED` | The check cannot proceed due to a recorded blocker |
| `PENDING_REVIEW` | Evidence exists but independent review is incomplete |
| `NOT_APPLICABLE` | Explicit rationale demonstrates the check does not apply |

## 5. JSONL append-only ledger

One JSON object per line. Each event should include `event_id`, `previous_event_hash`, `event_hash`, and a canonical payload. Hash-chain implementation and canonicalization must be specified and tested before claiming tamper evidence. Do not retrofit an unverified hash scheme and call it secure.

## 6. Data integrity and privacy

- Never commit API keys, tokens, passwords, private keys, session cookies, or raw secrets.
- Avoid committing raw conversation exports or personal information while the repository is public.
- Before storing confidential history, verify repository visibility is private and review repository collaborators and GitHub App access.
- Keep source files, derived summaries, execution evidence, and verification reports in distinct paths.
- Any encryption-at-rest or authenticated-encryption requirement needs a concrete design and tests; a documentation statement alone is not implementation evidence.

## 7. Unresolved schema items

The canonical schema URI/version/digest and the final approved 4D data model are `UNVERIFIED`. This document is a draft contract and is not certified against an external standard.
