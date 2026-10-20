# HAP Evidence-First Workflow Specification

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Workflow status: `DRAFT`
- Current phase: `PHASE_0_BLOCKED`
- Phase 1 authorization: `NOT_AUTHORIZED`

## 1. Sequential workflow

1. **Identify** — resolve artifact/source identity and project scope.
2. **Collect** — retrieve the original source where access is authorized; preserve exact bytes and provenance.
3. **Register** — append artifact metadata to the registry.
4. **Hash** — calculate SHA-256 from the exact source bytes; record tool and result.
5. **Validate** — validate file integrity, required fields, schema, version, and cross-document consistency.
6. **Test** — execute only tests permitted by the current phase and policy.
7. **Independently verify** — a verifier other than the builder checks the evidence against acceptance criteria.
8. **Gate decision** — record PASS/FAIL/UNVERIFIED/BLOCKED with evidence references and rationale.
9. **Handoff** — proceed only if the next phase is authorized and all required gates pass.

A documentation-only review cannot produce an execution PASS for an unexecuted runtime, installation, or integration test.

## 2. Failure and loop-back

On any failure or inconsistency:
- stop downstream actions;
- append an event describing the failure, observed facts, suspected root cause (labelled as suspected until confirmed), impact, and evidence;
- return to Step 1 for the affected validation chain;
- re-check prior inputs, schema, versions, hashes, connectivity, and test assumptions against the current evidence set;
- preserve earlier results rather than overwriting them;
- resume only after a new evidence-backed gate decision.

## 3. Phase boundaries

### Phase 0 — documentation and governance review
Allowed: read-only inspection, source collection, schema and architecture review, documentation, hashes of available files, static analysis where authorized, and evidence-register maintenance.

Blocked until separately authorized: database writes, production deployment, external mutations, claiming installation/activation, or moving to Phase 1.

### Phase 1+
Not authorized by this document. Entry requires completed Phase 0 acceptance criteria, independent review, and explicit human authorization.

## 4. Phase-to-phase handoff contract

Every handoff must record:
- `source_phase`
- `target_phase`
- `checkpoint_id`
- `deliverables_manifest`
- `evidence_manifest` including SHA-256 values where applicable
- `verification_result` with expected and actual values
- `gate_decision`: `PASS`, `FAIL`, `UNVERIFIED`, or `BLOCKED`
- `handoff_status`
- reviewer, timestamp, blockers, and authorization reference

## 5. Required end-of-task work log

Every task report must state:
1. Work actually completed.
2. Results and evidence, including repository paths, URLs, commit IDs, hashes, and sources.
3. Unfinished items and the reason each is unfinished, evidence of cause, impact, and unblock method.
4. Next steps and completion conditions.
5. Current project phase, gate status, and any system changes.

## 6. Four-D model

The user requested a “4D” format, but the reviewed project context does not define what the four Ds mean. Therefore the repository must not silently invent an expansion. Until the user’s intended four dimensions are identified, use the evidence-first workflow above as the provisional operational structure and record the 4D mapping as `BLOCKED — DEFINITION NOT FOUND`.
