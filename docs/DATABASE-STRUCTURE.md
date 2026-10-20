# HAP Database Structure and Data Boundaries

- Project: `HAP-2026-OFFLINE-FIRST`
- Status: `PROPOSED — NOT APPROVED FOR FREEZE`
- Current phase: `PHASE_0_BLOCKED`
- Database writes: `ZERO_DATABASE_WRITE`

## 1. Boundary statement

This file documents a proposed logical model for Phase 0 review. It is not a live database schema, migration, deployment, RLS policy, or proof that any table exists. Do not apply migrations or write to Supabase, CouchDB, RxDB, or any other database in the current phase.

The GitHub repository is the primary versioned project record for specifications, source code, evidence metadata, test outputs, and change history. The repository is not a substitute for preserving exact source archives when those become available.

## 2. Proposed logical entities

| Entity | Purpose | Required identity | Core fields (proposed) | Write rule |
|---|---|---|---|---|
| Project | Current HAP project identity and policy snapshot | `project_id` | name, current_phase, specification_status, policy_revision, created_at | Versioned file changes only; database writes prohibited |
| Artifact | Source, document, code, package, or report metadata | `artifact_id` | project_id, origin, version, captured_at, byte_size, sha256, status | Append/register only after observing source |
| Requirement | Stable requirement and its evidence mapping | `requirement_id` | project_id, statement, source_ref, acceptance_criteria, status | Do not invent missing requirements |
| Gate | Phase/step acceptance decision | `gate_id` | criteria_refs, evidence_refs, decision, reviewer, decided_at | Never PASS without required evidence |
| ExecutionEvent | One attempt, test, error, recovery, or review event | `event_id` | project_id, phase, step_id, actor, inputs, outputs, expected, actual, status, blocker | Append-only history |
| Checkpoint | Recoverable state pointer, not a replacement for history | `checkpoint_id` | event_head, current_phase, step_id, manifest_ref, checksum, status | Append new checkpoints; never silently overwrite |
| ToolScope | Observed tool/account permissions and boundary | `scope_id` | tool_id, action, observed_permission, source_ref, verified_at, status | Record evidence; no inference from tool presence |
| Review | Independent evidence review | `review_id` | reviewer_role, reviewed_refs, findings, decision, timestamp | Reviewer should be independent of builder |
| Decision | Durable project decision and rationale | `decision_id` | source, decision, status, consequences, supersedes | Append-only; supersession must be explicit |

## 3. Key and relationship rules

- Every entity must carry `project_id` where it is project-scoped.
- Proposed identity keys should be stable and unique; the project identity must be part of logical scoping.
- Artifact, execution, checkpoint, review, and decision records must retain source/evidence references.
- A checkpoint summarizes the current recovery position; it does not replace event history.
- Cross-system identifiers must be stored with their system name and must not be mistaken for local primary keys.
- No schema can be frozen until canonical data contract, 4D definition, key rules, migration/recovery behavior, and acceptance tests are reviewed.

## 4. Integrity and security requirements (not yet implemented)

1. Validate every record against a versioned schema.
2. Use authenticated encryption for sensitive stored content where required by the approved design; document key custody and recovery.
3. Separate metadata from source bytes; keep immutable originals and derived summaries distinct.
4. Use SHA-256 over exact bytes and retain tool/version and capture time.
5. A hash chain requires canonical serialization, domain separation, append ordering, and adversarial tests before it can be described as tamper-evident.
6. Access control and row-level security must be verified through negative and positive authorization tests; a policy file alone is not proof.
7. Restore tests and backup integrity checks are required before claiming recoverability.
8. No raw secrets in logs or source control.

## 5. Current legacy-data boundary

Prior project context reported legacy Supabase records (one project, five tasks, two checkpoints, two execution events, and one tool scope) as unrelated to the current HAP. Treat them as quarantined historical material, not current progress, permissions, checkpoints, or gate decisions. No current HAP write or migration is authorized.

## 6. Acceptance conditions before implementation

- [ ] Approved data contract and canonical schema/version/digest identified
- [ ] The user's intended “4D” dimensions explicitly defined
- [ ] Logical and physical schema reviewed independently
- [ ] Key, uniqueness, append-only, and rollback semantics tested
- [ ] Threat model, access policy, and secret-handling design approved
- [ ] Migration and recovery plan reviewed
- [ ] Test data clearly separated from real project records
- [ ] Explicit authorization for any database mutation
- [ ] Gate decision and authorization recorded in repository

Until all applicable conditions are evidenced, status remains `PROPOSED` and database writes remain prohibited.
