# HAP Architecture Baseline

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Status: `PHASE_0_BLOCKED`
- Approval: `NOT_APPROVED_FOR_FREEZE`
- Last updated: 2026-10-20
- This document is a Phase 0 specification baseline, not evidence of an installed or running system.

## 1. Purpose

Define the evidence-first architecture for Hybrid AI Platform — Offline-first (HAP), keeping project artifacts, source code, verification evidence, and decisions traceable in this Git repository.

## 2. System boundaries

The repository is the versioned project record for source-controlled documents, code, tests, manifests, and non-sensitive evidence. It is not itself proof that any external database, mobile device, extension, API, or service is connected or operational.

External systems must be described by explicit adapters and scopes. Until independently verified, each integration is `UNVERIFIED`. Secrets, access tokens, private keys, raw credentials, and sensitive personal data must never be committed.

## 3. Phase and mutation controls

- Current phase: `PHASE_0_DOCUMENTATION_AND_GOVERNANCE_REVIEW`
- Phase 1: `NOT_AUTHORIZED`
- Database writes: `ZERO_DATABASE_WRITE`
- Remote mutations: `PROHIBITED`
- Human approval: `REQUIRED`

This repository documentation action does not authorize database writes, deployments, installations, remote service mutations, or phase progression.

## 4. Logical layers

1. **Control plane** — project identity, phase state, policy, gate decisions, approval records.
2. **Artifact plane** — source code, architecture, data contracts, workflow definitions, schemas, specifications.
3. **Evidence plane** — immutable execution records, test outputs, SHA-256 manifests, source/version metadata, independent verification.
4. **Recovery plane** — append-only event ledger, checkpoints, recovery instructions, integrity checks.
5. **Adapter plane** — narrowly scoped connectors for GitHub, local/mobile storage, databases, and AI providers; each integration has an explicit permission boundary.
6. **Verification plane** — independent checks of artifact identity, schema consistency, tests, and gate acceptance criteria.

These are logical responsibilities, not claims that separate services or runtimes have already been deployed.

## 5. Data and evidence flow

`source -> register -> hash -> validate -> review -> gate decision -> authorized handoff`

Every transition records expected result, actual result, evidence references, verification status, and responsible actor. If any validation fails, block the handoff and restart the relevant validation sequence from Step 1 against the current evidence set.

## 6. Source-of-truth rules

- Git history is the versioned source of truth for artifacts committed to this repository.
- External sources remain external; register their canonical URLs/IDs and observed metadata rather than claiming they were copied.
- Preserve original files separately from summaries, normalized copies, and derived artifacts.
- Do not overwrite checkpoints or execution history; append a new event and link it to the previous event/checkpoint.
- Record SHA-256 for file bytes where available. Git blob SHA is not a substitute for SHA-256.

## 7. Offline-first requirements

The future architecture should support local-first operation, explicit sync boundaries, conflict detection, integrity verification, and controlled recovery. Specific database technology, encryption implementation, mobile behavior, and sync guarantees remain proposals until backed by approved specifications and executable tests.

## 8. Open architecture blockers

- Exact approved 4D model is not defined in the evidence reviewed; do not invent what the four Ds stand for.
- Canonical data schema URI/version/digest is unresolved.
- Gate definitions and acceptance criteria require a reviewed, authoritative register.
- Runtime, installation, device, and integration evidence must be collected from actual execution before operational claims.
- Independent review and user approval remain required before specification freeze or Phase 1.
