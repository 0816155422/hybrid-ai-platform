# HAP Decision Log

This log is append-only. Add new entries; do not silently rewrite earlier decisions.

## DEC-2026-10-20-001 — Main repository designation

- Date: 2026-10-20
- Decision: Use `0816155422/hybrid-ai-platform` as the main versioned project repository for HAP files, specifications, code, installation/test evidence, verification records, and project history within the scope that can legitimately be stored there.
- Source: Explicit user instruction in ChatGPT conversation.
- Status: `RECORDED`
- Qualification: Repository is the primary Git record, not proof that external services or devices are operational. Sensitive history must not be committed while visibility is public.

## DEC-2026-10-20-002 — Phase controls remain in force

- Date: 2026-10-20
- Decision: Preserve `PHASE_0_BLOCKED`, `PHASE_1_NOT_AUTHORIZED`, `ZERO_DATABASE_WRITE`, `REMOTE_MUTATION_POLICY: PROHIBITED`, and `HUMAN_APPROVAL_REQUIRED: TRUE`.
- Source: Existing project governance requirements.
- Status: `ACTIVE`
- Qualification: User-authorized Git documentation writes do not imply permission for database writes, deployment, installation, or other remote mutations.

## DEC-2026-10-20-003 — 4D definition unresolved

- Date: 2026-10-20
- Decision: Do not invent the four dimensions represented by “4D.” Use the sequential evidence-first workflow as a provisional process and keep 4D mapping blocked until the intended definition is recovered or explicitly supplied.
- Source: Review of available project context; no explicit four-D expansion found.
- Status: `BLOCKED — DEFINITION REQUIRED`

## DEC-2026-10-20-004 — Evidence and status integrity

- Date: 2026-10-20
- Decision: Separate reported historical results from tests freshly executed and independently verified. Do not call an installation, deployment, database integration, or runtime check successful without direct evidence.
- Source: HAP evidence-first and independent-verification requirements.
- Status: `ACTIVE`

## Entry template

### DEC-YYYY-MM-DD-NNN — Short title

- Date:
- Decision:
- Source/evidence:
- Status:
- Consequences:
- Review/approval:


## DEC-2026-10-20-005 — Repository operational baseline scaffold

- Date: 2026-10-20
- Decision: Extend the main repository with a tool inventory, proposed database boundary document, Phase 0–3 source collection plan, dependency-free evidence metadata validator, unit tests, GitHub Actions workflow, execution-evidence instructions, and checkpoint snapshot.
- Source/evidence: Explicit user request to make this repository the primary project store; created file commit IDs are recorded in the task execution response and can be inspected in Git history.
- Status: `IMPLEMENTED — READ-BACK VERIFICATION PENDING`
- Consequences: This adds repository structure and a proposed CI validation path only. It does not establish that the workflow has run, that tests pass, that source collection is complete, that the database schema is approved, or that Phase 1 is authorized.
- Review/approval: Independent review pending.
