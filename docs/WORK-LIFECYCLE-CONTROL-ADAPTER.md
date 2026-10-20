# HAP Work Lifecycle Control Adapter — Preflight and Postflight

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Document ID: `DOC-WORK-LIFECYCLE-001`
- Version: `0.1.0-draft`
- Status: `DRAFT — PHASE 0 REVIEW — NOT APPROVED FOR FREEZE`
- Current phase: `PHASE_0_BLOCKED`
- Phase 1: `NOT_AUTHORIZED`
- Database write policy: `ZERO_DATABASE_WRITE`
- Remote mutation policy: `PROHIBITED`
- Human approval: `REQUIRED`
- Date: 2026-10-21

> This specification defines the required control process. It does not prove that an automated adapter has been implemented or that any control is enforced at runtime.

## 1. Purpose

Establish a mandatory **before-work and after-work control layer** that wraps every HAP task. No implementation task—including the Central Raw Data Collection Adapter—should start substantive work until the preflight check has established the task's identity, scope, permissions, phase, source baseline, and acceptance criteria. Every task must finish with a postflight reconciliation and an append-only work record.

This lifecycle adapter is the outer control plane. Task-specific adapters operate inside its authorization boundary.

## 2. Operating principle

```text
REQUEST / TASK
   |
   v
PRE-FLIGHT CONTROL
  identify -> read current state -> check scope/policy
  -> establish baseline -> define expected results
   |
   +-- BLOCKED --> record reason and stop before substantive work
   |
   v
AUTHORIZED TASK EXECUTION (bounded to approved scope)
   |
   v
POST-FLIGHT CONTROL
  stop -> collect outputs -> verify changes -> run allowed tests
  -> compare expected vs actual -> record blockers and evidence
   |
   +-- FAIL / INCOMPLETE --> preserve results; block dependent work
   |
   v
APPEND-ONLY WORK LOG + CHECKPOINT / NEXT-STEP DECISION
```

A task may end as `COMPLETE`, `PARTIAL`, `BLOCKED`, `FAILED`, or `UNVERIFIED`. A task must not be labelled complete solely because the assistant has stopped responding.

## 3. Preflight adapter: mandatory steps

### PF-01 — Identify task and project

Record:
- task/request ID and concise objective;
- project ID and current phase;
- current branch/commit or equivalent baseline where applicable;
- expected deliverables and explicit exclusions.

If project identity or target repository is ambiguous, do not write or mutate anything.

### PF-02 — Read authoritative current state

Read the relevant current repository files, latest checkpoint, work log, policies, and prior evidence before deciding what to do. Identify prior attempts and unresolved blockers. Do not rely solely on summaries when current source files are available.

### PF-03 — Check phase, policy, permission, and capability

Evaluate separately:
- whether the tool/action is available;
- whether the connection is observed;
- whether the specific action is authorized;
- whether the requested scope is within policy;
- whether the action is permitted in the current phase.

Unknown permission, missing approval, phase mismatch, or prohibited mutation means `BLOCKED`. Do not infer authorization from a tool being listed or connected.

### PF-04 — Scope and impact boundary

Declare paths, sources, records, endpoints, expected writes, external side effects, data classifications, and maximum limits. Explicitly state which effects are prohibited. For HAP Phase 0, database writes and remote mutations remain prohibited.

### PF-05 — Establish baseline and protect history

Record the current commit/path/blob identifiers or source revision needed for comparison. Confirm that history/checkpoints are append-only. For an existing file update, fetch its current version and use a version-aware update; if the baseline changes unexpectedly, stop and reconcile rather than overwrite.

### PF-06 — Define acceptance and failure criteria

Before execution, state:
- expected result;
- tests/checks to run;
- evidence that will prove each result;
- stop conditions;
- rollback/recovery method where applicable;
- independent review needs;
- definition of done.

A plan or a test definition is not execution evidence.

### PF-07 — Preflight decision

Write a preflight record with `PASS`, `BLOCKED`, or `UNVERIFIED`.
- `PASS`: all required preconditions are supported by observed evidence.
- `BLOCKED`: a policy or scope rule prevents the task.
- `UNVERIFIED`: necessary facts cannot be established.

Only `PASS` permits the bounded task to start. This does not authorize actions outside the recorded scope.

## 4. Postflight adapter: mandatory steps

### PO-01 — Stop and enumerate actual changes

List files created/modified/deleted, commits, tool calls with side effects, generated artifacts, external calls, and anything that may have changed. Distinguish intended changes from observed actual changes. Do not claim no side effects unless checked to the extent possible.

### PO-02 — Read back and compare

For repository changes, fetch the committed file(s) and verify the path, content, commit SHA, and blob SHA. For a permitted external action, use a safe read-back if supported. If read-back is unavailable, record that limitation. Never infer successful persistence from a tool invocation alone.

### PO-03 — Verify artifacts and integrity

Where relevant, validate schema, file format, exact byte size, SHA-256 of exact bytes, and manifest consistency. Keep Git blob SHA separate from SHA-256. If a hash was not computed, record `PENDING` and why.

### PO-04 — Execute authorized checks

Run only tests permitted by the current phase and preflight scope. Record command/action, environment, version, start/end time where available, exit code, expected and actual result, and output/report references. CI success must not be described as proof of local-device behavior, offline isolation, or security sandboxing.

### PO-05 — Reconcile expected vs actual

For each deliverable, record one of:
- `PASS` — criteria were executed and met with evidence;
- `FAIL` — observed result violates criteria;
- `PARTIAL` — some work succeeded, with specific gaps;
- `BLOCKED` — a recorded dependency or policy prevented completion;
- `UNVERIFIED` — evidence is insufficient;
- `NOT_RUN` — check was not executed;
- `NOT_APPLICABLE` — reason is explicit.

Do not promote `PARTIAL`, `BLOCKED`, `UNVERIFIED`, or `NOT_RUN` to PASS by narrative.

### PO-06 — Record blockers and recovery

Every incomplete item must state:
- observed fact/evidence;
- root cause, or `SUSPECTED` if not confirmed;
- impact;
- what remains unfinished;
- exact condition needed to unblock;
- next action and responsible role.

Preserve earlier logs and checkpoints. Add a new record; never silently rewrite history.

### PO-07 — Independent review and closure decision

Where required by the gate, a verifier independent of the builder reviews the artifact/evidence. Record reviewer identity/role, scope, findings, and decision. A successful postflight does not authorize the next phase or a prohibited write.

### PO-08 — User-facing work report

Every task response must provide, in concise form:
1. actual work completed;
2. links to files/evidence, commit identifiers, and hashes when available;
3. tests run and exact results;
4. unfinished items and why they remain unfinished;
5. blockers, impact, and unblock method;
6. next step and completion condition;
7. current phase/policy status and whether any external/system state changed.

## 5. Required record contract

Each task lifecycle record should include:

- `lifecycle_id`, `task_id`, `project_id`;
- `preflight_status`, `postflight_status`;
- `started_at_utc`, `ended_at_utc` when observed;
- `actor`, `tool/action`, version where available;
- `baseline_ref`, `scope`, `authorization_ref`;
- `expected_deliverables`, `actual_deliverables`;
- `changed_paths`, `commit_refs`, `artifact_refs`;
- `checks` with expected/actual/status/exit code/evidence reference;
- `blockers`, `root_cause`, `impact`, `unblock_method`;
- `side_effects` and `readback_status`;
- `independent_review_ref` where required;
- `previous_lifecycle_record` or checkpoint reference;
- `next_step`, `completion_condition`.

Unknown values must be explicit; do not fabricate timestamps, IDs, digests, or test results.

## 6. Minimum acceptance tests

All tests start as `NOT_RUN` until actually executed.

| ID | Scenario | Expected result | Initial status |
|---|---|---|---|
| LIFE-001 | Missing task objective or project identity | Block writes; ask for or resolve the missing essential detail | `NOT_RUN` |
| LIFE-002 | Phase 1 or database write requested while prohibited | Preflight blocks the action and records policy reason | `NOT_RUN` |
| LIFE-003 | Tool listed but action permission not verified | `UNVERIFIED` or `BLOCKED`; no assumed permission | `NOT_RUN` |
| LIFE-004 | Existing file changes after baseline read | Stop and re-fetch/reconcile; do not blindly overwrite | `NOT_RUN` |
| LIFE-005 | Repository file create/update returns a commit | Fetch file back and compare intended content and identifiers | `NOT_RUN` |
| LIFE-006 | Task ends with an incomplete deliverable | Postflight reports reason, impact, and unblock condition | `NOT_RUN` |
| LIFE-007 | Test was planned but not run | Status remains `NOT_RUN`, not PASS | `NOT_RUN` |
| LIFE-008 | Hash unavailable or computed over a preview | Mark unavailable/invalid; do not claim exact-byte integrity | `NOT_RUN` |
| LIFE-009 | Unexpected external side effect is observed | Stop dependent actions; record and escalate/recover under policy | `NOT_RUN` |
| LIFE-010 | Task report omits unfinished-item rationale | Postflight contract validation fails | `NOT_RUN` |
| LIFE-011 | Builder attempts to approve their own evidence where independent review is required | Gate remains pending/blocking | `NOT_RUN` |
| LIFE-012 | User asks for phase progression without required evidence/approval | Keep phase unchanged; record missing gate evidence | `NOT_RUN` |

## 7. Integration contract with task-specific adapters

- The Work Lifecycle Control Adapter runs first and last around every task.
- The Central Raw Data Collection Adapter must provide its request, scope, authorization reference, outputs, and test results to this lifecycle adapter.
- No task-specific adapter may bypass preflight or suppress postflight findings.
- The lifecycle adapter records status but does not replace the independent verifier or human approval gate.
- A blocked preflight prevents substantive work and all related mutations. A failed postflight blocks dependent work until the failure is reviewed and dispositioned.
- The initial implementation should itself be local/testable and avoid network access except for the explicitly authorized repository operations used to version project artifacts.

## 8. Implementation plan

1. Review this lifecycle specification against `docs/WORKFLOW-SPEC.md`, `docs/ARCHITECTURE.md`, and `docs/DATA-CONTRACTS.md`. Status: `PENDING_REVIEW`.
2. Define a versioned JSON Schema for the lifecycle record and test valid/invalid records. Status: `NOT_RUN`.
3. Implement a small deterministic preflight/postflight validator that checks records and required fields; do not claim it enforces operating-system security. Status: `NOT_RUN`.
4. Add positive, negative, missing-evidence, unexpected-change, and postflight-completeness tests. Status: `NOT_RUN`.
5. Integrate with the existing test orchestrator/CI only after inspecting existing package structure and avoiding duplicate entry points. Status: `NOT_RUN`.
6. Preserve execution evidence and an append-only checkpoint after actual test runs. Status: `NOT_RUN`.
7. Obtain independent review and explicit user approval before freeze or Phase 1. Status: `PENDING`.

## 9. Current decision and work log

- Decision: treat preflight/postflight control as the outermost workflow layer and implement/review it before the raw-data collection adapter.
- Completed in this task: drafted this specification, including mandatory checks, status vocabulary, record contract, test plan, integration boundaries, and implementation gates.
- Not completed: validator/schema implementation, runtime tests, CI integration, independent review, approval, and enforcement.
- Why incomplete: this increment is specification-only; the existing extension/package entry point must be inspected before code is added.
- Impact: lifecycle controls are not yet automatically enforced. Current controls remain procedural/specification-level.
- Unblock method: inspect the repository structure, then implement the schema and validator as the next isolated increment.
- Next step: link this specification from the workflow and architecture baselines, then implement the record schema and tests.
