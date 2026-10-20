# HAP Evidence Store

This directory holds non-sensitive, traceable evidence only. It is not yet a complete evidence archive.

## Directory convention

- `evidence/register/` — artifact and source registers
- `evidence/manifests/` — SHA-256 manifests and package inventories
- `evidence/execution/` — test/install/verification execution records
- `evidence/checkpoints/` — append-only checkpoint snapshots
- `evidence/reviews/` — independent review records

GitHub's file API creates directories implicitly when a file is committed beneath them; empty directories do not exist in Git.

## Evidence status

Use `PASS`, `FAIL`, `UNVERIFIED`, `NOT_RUN`, `BLOCKED`, `PENDING_REVIEW`, or `NOT_APPLICABLE` with rationale.

## SHA-256 rules

Hash the exact file bytes, not a rendered preview or copied excerpt. Record filename, byte size, SHA-256, hashing tool/version, timestamp, and source. Keep Git blob SHA in a separate field.

## Privacy and integrity

The repository was last verified as public in available audit evidence. Do not put raw conversation exports, secrets, credentials, or sensitive personal data here until private visibility and access controls have been verified. Do not fabricate execution logs, hashes, installation outcomes, or test results.

## Initial state

No claim is made that evidence for every Phase 0–3 artifact has already been collected. Register artifacts only after their sources and contents have been observed.
