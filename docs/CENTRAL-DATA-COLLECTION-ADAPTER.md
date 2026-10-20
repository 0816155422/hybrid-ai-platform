# HAP Central Raw Data Collection Adapter — Design v0.1

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Document ID: `DOC-ADAPTER-001`
- Status: `DRAFT — PHASE 0 REVIEW — NOT APPROVED FOR FREEZE`
- Current phase: `PHASE_0_BLOCKED`
- Phase 1: `NOT_AUTHORIZED`
- Database write policy: `ZERO_DATABASE_WRITE`
- Remote mutation policy: `PROHIBITED`
- Human approval: `REQUIRED`
- Date: 2026-10-21

> This is a proposed design only. It does not prove that an adapter is implemented, installed, connected, secure, or operational. It does not authorize database writes, external mutations, deployments, or Phase 1.

## 1. Purpose

Define one controlled entry point for collecting raw source material and provenance from multiple source-specific adapters. The central adapter governs whether a collection attempt may proceed, normalizes its evidence envelope without silently changing source bytes, and routes results to a quarantine/staging area for independent verification.

The collector is not the verifier, approver, database writer, or phase gate owner.

## 2. Non-goals and hard boundaries

- No direct database writes, migrations, production deployment, or remote mutations.
- No arbitrary shell execution or arbitrary plugin code loaded from a source record.
- No credentials, access tokens, cookies, private keys, or raw secrets in logs or collected metadata.
- No claim that a hash proves authenticity or that a manifest alone proves source truth.
- No automatic promotion from raw collection to approved evidence or a phase PASS.
- No automatic overwrite of prior artifacts, events, manifests, or checkpoints.
- No assumption that every source is online, available, complete, or authorized.
- No silent normalization of source bytes. Any derived/transformed content is a separate artifact linked to the original.

## 3. Logical architecture

```text
Source Registry + Approved Scope
            |
            v
Source-specific Adapter (read-only, least privilege)
            |
            v
Central Collection Gate
  - project/phase/policy check
  - source identity and scope check
  - data-classification and size/type limits
  - consent/authorization and rate-limit check
            |
            v
Raw Evidence Envelope
  - original bytes or explicit external reference
  - provenance and acquisition metadata
  - SHA-256 computed over exact bytes when available
            |
            v
Independent Verifier (separate responsibility)
            |
            v
Quarantine / Staging (not the central database)
            |
            v
Human review + explicit gate decision
```

The diagram describes logical boundaries; it does not assert that these are deployed as separate processes or security domains.

## 4. Components and responsibilities

| Component | Responsibility | Must not do |
|---|---|---|
| Source Registry | Identify source, connector, owner, allowed operations, allowed paths/endpoints, version and review status | Infer permission from connector availability |
| Source Adapter | Read only the declared source scope; return raw bytes or an explicit reference plus source metadata | Approve itself, mutate source, execute arbitrary commands |
| Central Collection Gate | Enforce project policy, phase, authorization, allowlist, limits, classification and duplicate handling | Bypass a failed or unknown policy check |
| Evidence Envelope Builder | Attach provenance, exact byte count, digest and transformation links | Label unavailable metadata as observed |
| Independent Verifier | Recompute digest from exact bytes, validate schema and provenance, compare expected/actual | Reuse the collector's PASS without independent checks |
| Quarantine/Staging | Hold unverified results and failed/partial collections separately | Promote items automatically to an authoritative record |
| Gate Controller / Human Reviewer | Decide whether evidence meets approved criteria and authorize any later handoff | Treat documentation-only evidence as runtime proof |

## 5. Collection policy state machine

Each collection request must use one of these explicit states:

- `REQUESTED` — request exists; no source access implied.
- `BLOCKED_POLICY` — policy, phase, or authorization disallows the request.
- `BLOCKED_SCOPE` — source or requested path/endpoint is outside the declared scope.
- `BLOCKED_ACCESS` — source cannot be accessed with currently verified permissions.
- `COLLECTING` — an authorized read is in progress.
- `COLLECTED_UNVERIFIED` — bytes/reference were retrieved, but independent checks have not passed.
- `PARTIAL` — some requested items are missing or failed; exact coverage must be recorded.
- `VERIFIED` — only after the independent verifier's defined checks pass.
- `REJECTED` — integrity, policy, provenance, type, or safety checks failed.
- `PENDING_HUMAN_REVIEW` — evidence is available but no approval decision has been made.

A successful network response is not equivalent to `VERIFIED`; `VERIFIED` is not equivalent to a gate `PASS`; neither authorizes a database write or phase change.

## 6. Proposed request contract

Required fields:

- `request_id`: stable unique request identifier.
- `project_id`: must equal `HAP-2026-OFFLINE-FIRST`.
- `phase` and `step_id`: current authorized workflow position.
- `source_id`: registered source identity.
- `adapter_id` and `adapter_version`: exact adapter implementation/version, or `UNIMPLEMENTED` for design records.
- `requested_scope`: exact paths, object IDs, URL patterns, or bounded query.
- `requested_artifact_types`: explicit file/data types.
- `purpose`: requirement/gate or collection target this request supports.
- `authorization_ref`: reference to the applicable permission/approval evidence; if absent, block collection.
- `limits`: maximum item count, bytes per item, total bytes, depth/page count, and timeout.
- `requested_at_utc`: timestamp with timezone.

Optional fields must be omitted or explicitly marked unknown; do not synthesize them.

## 7. Raw evidence envelope

One envelope per collected item; never merge multiple unrelated originals into one record.

| Field | Meaning |
|---|---|
| `envelope_id` | Stable unique identifier |
| `request_id` | Collection request |
| `project_id` | HAP project identity |
| `source_id` | Registered source |
| `source_locator` | Canonical URL, repository/path/ref, object ID, or source-native locator |
| `source_version` | Commit, release, revision, ETag/version ID, or `UNKNOWN` |
| `captured_at_utc` | Observed collection timestamp |
| `original_filename` | Original name when supplied by source |
| `media_type` | Observed type, or `UNKNOWN` |
| `byte_size` | Exact byte count only when measured |
| `sha256` | SHA-256 of exact collected bytes, or `PENDING` with reason |
| `git_blob_sha` | Separate optional Git object ID; never substitute for SHA-256 |
| `content_location` | Local staged path or immutable external reference; never fabricate a path |
| `collection_status` | State from Section 5 |
| `transformation_status` | `NONE`, `DERIVED_COPY_CREATED`, or `UNKNOWN` |
| `derived_from` | Original envelope/artifact ID for each derived output |
| `limitations` | Coverage gaps, truncation, unavailable metadata, access restrictions |
| `collector_identity` | Tool/agent identifier and version |
| `verification_ref` | Independent verification record, if available |
| `approval_ref` | Human/gate decision, if available |

If raw bytes cannot be retrieved, record an external reference and clearly state that byte size and SHA-256 are unavailable. Never claim the external object was archived or hashed.

## 8. Required enforcement rules

1. **Default deny:** unknown source, missing authorization, unknown phase permission, or malformed scope blocks collection.
2. **Read-only source adapters:** source mutations are not exposed in the adapter interface.
3. **No implicit credential discovery:** credentials must be provided through an approved secret mechanism; never print or persist their values.
4. **Bounded collection:** enforce item, byte, depth/page, and time limits before and during retrieval.
5. **Type and content checks:** reject unexpected file types and suspicious archive expansion; do not automatically execute collected content.
6. **Integrity:** compute SHA-256 over the exact bytes received; independent verifier recomputes it from the staged bytes.
7. **Provenance:** retain canonical source locator, revision/version, capture time, collector version, and limitations.
8. **Duplicate handling:** compare stable source identity and digest; do not overwrite. Register a new observation or explicitly link it to an existing artifact.
9. **Failure behavior:** fail closed, record status and reason, preserve partial results as partial, and prevent downstream handoff.
10. **Logging:** append-only event metadata; redact secrets and sensitive payloads. Logs must not silently include raw source contents.
11. **Separation of duties:** collection code cannot mark its own output independently verified or approve a gate.
12. **No database writer:** the initial adapter exposes no database-write capability. A later writer would require a separate approved design and explicit authorization.
13. **Offline-first:** local file collection must work without network access when source material is local. Network adapters must be explicit, bounded, and separately marked online-dependent.
14. **Recovery:** interruptions produce a new event/request attempt linked to the previous attempt; they do not erase or overwrite prior history.

## 9. Adapter interface proposal

The implementation should begin with a small, typed interface. Exact code is deferred until the current package/runtime and existing extension entry point have been identified.

Conceptual operations:

- `describe_source()` — return non-secret source identity, capabilities and declared scope.
- `validate_request(request)` — check request shape and policy preconditions without fetching data.
- `collect(request)` — read only the allowed scope and return envelopes with observed metadata.
- `cancel(request_id)` — stop an in-progress read where the adapter supports cancellation.
- `health_check()` — report capability/access status without exposing secrets or mutating the source.

The interface must not include `write`, `delete`, `update_remote`, `execute_command`, or a generic arbitrary-tool invocation in this phase.



## 9A. Evidence-informed data preparation and analysis boundary

The source review and proposed data-preparation design are documented in [AI Memory and Data Preparation Research Dossier](AI-MEMORY-DATA-PREPARATION-RESEARCH.md). That dossier reviewed public W3C PROV, DCMI, IETF JSON, NASA data-management/systems-engineering guidance, NIST cloud-security and GenAI risk guidance, ISO/IEC 42001's official overview, and published AI-memory research. It is a research baseline, not an approved schema or compliance claim.

The adapter must distinguish the following artifacts and must never overwrite one with another:

1. **Raw source artifact** — exact bytes or an explicitly labelled external reference.
2. **Extraction artifact** — parsed text/rows/OCR/transcription/chunks with source locators and extractor version.
3. **Normalized record** — a typed record mapped to a versioned HAP contract, retaining unknowns and source references.
4. **Analysis artifact** — summary, comparison, hypothesis, embedding/index, or model-generated reflection, marked as derived.
5. **Approved project record** — only after independent verification and an authorized human/gate decision; the collector cannot create this status.

Every derivative must link to its immediate parent and original source through `derived_from`/source references. Parsing or normalization must not alter the stored original. A valid schema or provenance graph is evidence of structural consistency only; it does not prove a source claim is true.

### 9A.1 Supported preparation stages

`scope_and_authorize -> acquire_raw -> fingerprint -> detect_and_parse -> extract -> normalize_metadata -> validate -> analyze -> prepare_handoff -> independent_review`

- Scope/authorization comes before collection; unknown source, missing permission, or phase mismatch blocks.
- Preserve source-native formats. JSON is proposed for typed envelopes and contracts only after schema versioning; JSONL is a candidate for append-oriented records only after canonicalization and concurrency rules are specified. CSV, XML, RDF/PROV, PDF, DOCX, HTML, Markdown, code, images, and archives require format-specific handling and must not be flattened into one lossy universal representation.
- Every extraction or transformation creates a new derivative with its own identifier, format, schema/tool version, timestamp, parent references, and errors/limitations.
- AI summaries, memory reflections, vector embeddings, and retrieval indexes are derived artifacts, never original evidence or approved truth. Store the model/tool and configuration reference when observable.
- Analysis must separate source assertions, observed metadata, extracted text, normalized claims, inference/hypothesis, conflict, unknown, and human approval. These are proposed HAP epistemic statuses, not W3C/DCMI vocabulary.
- On malformed, oversized, unsupported, partial, or conflicting input, preserve the failure state and stop dependent handoff; do not silently discard or repair the source.

### 9A.2 Provenance mapping

Use W3C PROV's Entity/Activity/Agent pattern as the cross-system lineage model and DCMI terms for general descriptive metadata where useful. Minimum lineage:

`RawArtifact --used_by--> ExtractionActivity --generated--> ExtractionArtifact --used_by--> NormalizationActivity --generated--> NormalizedRecord --used_by--> AnalysisActivity --generated--> AnalysisArtifact`

Record identifiers, source version/locator, capture/processing times when observed, tool/adapter/schema versions, derivation links, validation outcomes, and limitations. Validate unique identifiers and plausible event ordering. Do not represent a PROV validation result as source authenticity or factual correctness.

### 9A.3 Cloud transfer boundary

Cloud transfer is a separate, future adapter, not an implicit part of collection. Its proposed contract must include explicit source/destination, data classification, authorization reference, allowed object scope, least privilege, transport protection, approved at-rest encryption/key custody for sensitive data, exact-byte manifest, receiver-side read-back/hash comparison, retention/disposition, partial/retry behavior, and an auditable failure status.

**Current HAP policy remains `REMOTE_MUTATION_POLICY: PROHIBITED`.** This section grants no permission to upload, synchronize, modify, or delete anything remotely. It defines only design requirements.

### 9A.4 Data-preparation acceptance criteria

The following criteria are design targets; all remain `NOT_RUN` until execution evidence exists:

| ID | Acceptance target | Initial status |
|---|---|---|
| DP-001 | Original bytes are preserved separately from extracted/normalized/analysis derivatives | `NOT_RUN` |
| DP-002 | Unknown source or missing authorization blocks before collection | `NOT_RUN` |
| DP-003 | Unsupported, malformed, or oversized data is blocked/quarantined with a reason | `NOT_RUN` |
| DP-004 | Format and schema version are explicit; invalid records fail closed | `NOT_RUN` |
| DP-005 | Every derivative links to its parent and original source | `NOT_RUN` |
| DP-006 | SHA-256 is computed over exact bytes and independently recomputed, or remains pending with a reason | `NOT_RUN` |
| DP-007 | Source assertions, observations, inferences, conflicts, unknowns, and approvals remain distinguishable | `NOT_RUN` |
| DP-008 | Updates/conflicts are retained as new versions/events rather than silently overwritten | `NOT_RUN` |
| DP-009 | Analysis abstains when evidence is insufficient or contradictory | `NOT_RUN` |
| DP-010 | Handoff manifest accounts for included, excluded, partial, and failed items | `NOT_RUN` |
| DP-011 | Cloud transfer remains blocked without explicit authorization and destination scope | `NOT_RUN` |
| DP-012 | Receiver-side copy is verified against the manifest where transfer is authorized | `NOT_RUN` |
| DP-013 | Provenance identifiers and event ordering pass consistency validation | `NOT_RUN` |
| DP-014 | An independent reviewer can trace an output claim back to source evidence | `NOT_RUN` |

## 10. Minimum test plan before implementation is considered verified

| Test ID | Scenario | Expected result | Status |
|---|---|---|---|
| COL-001 | Unknown source ID | `BLOCKED_SCOPE`; no read attempted | `NOT_RUN` |
| COL-002 | Missing authorization reference | `BLOCKED_POLICY`; no read attempted | `NOT_RUN` |
| COL-003 | Phase 1 request while Phase 1 is unauthorized | `BLOCKED_POLICY` | `NOT_RUN` |
| COL-004 | Path/endpoint outside allowlist | `BLOCKED_SCOPE` | `NOT_RUN` |
| COL-005 | Source returns bytes | Exact byte count and SHA-256 recorded; status remains unverified pending independent verification | `NOT_RUN` |
| COL-006 | Verifier recomputes a matching digest | Digest comparison passes; no gate approval implied | `NOT_RUN` |
| COL-007 | One byte changed after collection | Digest mismatch; `REJECTED` | `NOT_RUN` |
| COL-008 | Timeout or interrupted read | `PARTIAL` or blocked result with reason; prior event preserved | `NOT_RUN` |
| COL-009 | Oversized item or item-count limit exceeded | Stop or reject according to approved limit; record reason | `NOT_RUN` |
| COL-010 | Secret-like value appears in adapter error | Redacted logs; no secret persisted | `NOT_RUN` |
| COL-011 | Duplicate source locator and digest | No overwrite; explicit duplicate/link result | `NOT_RUN` |
| COL-012 | Collector attempts to self-approve | Interface/policy rejects the action | `NOT_RUN` |
| COL-013 | No network available; local source selected | Local collection works or reports a precise local blocker | `NOT_RUN` |
| COL-014 | Any adapter requests a database write | Capability unavailable; operation blocked | `NOT_RUN` |

These are planned tests, not execution results.

## 11. Threats and residual risks

- Compromised or misleading source content.
- Source locator/revision changing between listing and retrieval.
- Partial downloads, pagination gaps, truncation, rate limits, or stale connector indexes.
- Malicious archives, oversized payloads, path traversal, parser exploits, or content that attempts to influence an AI agent.
- Permission drift or a connector having broader access than the declared scope.
- Hashes being computed over a transformed/rendered representation instead of the original bytes.
- Sensitive data being captured into repository history or logs.
- Collector and verifier sharing the same flawed code or assumptions.
- CI success being mistaken for proof of local device isolation or offline operation.

Mitigations require bounded parsers, least privilege, source-version pinning where available, independent digest recomputation, adversarial tests, secret redaction, access review, and explicit residual-risk reporting. A hash detects byte changes relative to a trusted reference; it does not by itself establish source authenticity.

## 12. Proposed file layout

This is a proposed future layout, not evidence that these files exist:

- `hap/collection/contracts.py` — request/envelope/status contracts.
- `hap/collection/policy.py` — default-deny policy evaluation.
- `hap/collection/gate.py` — central gate orchestration.
- `hap/collection/adapters/base.py` — read-only adapter protocol.
- `hap/collection/adapters/local_files.py` — first local-only adapter.
- `hap/collection/envelope.py` — provenance and exact-byte digest handling.
- `hap/collection/staging.py` — quarantine/staging interface without database writes.
- `hap/verification/collection_verifier.py` — independent checks, separately invoked.
- `tests/collection/` — positive, negative, boundary and adversarial tests.
- `evidence/execution/` — append-only execution records after actual runs.

Before adding this layout, inspect the repository's existing extension/package structure and reuse its established conventions rather than creating a competing entry point.

## 13. Implementation sequence and gates

1. **C0 — Design review:** compare this proposal with existing architecture, data contracts, source registry and workflow; resolve conflicts. Status: `PENDING_REVIEW`.
2. **C1 — Contract/schema:** define typed request/envelope schema and validate it with tests. Status: `NOT_RUN`.
3. **C2 — Local-only adapter:** implement a bounded read-only local-file adapter with no network or database capability. Status: `NOT_RUN`.
4. **C3 — Independent verifier:** independently recompute digest and validate envelope; add tamper/negative tests. Status: `NOT_RUN`.
5. **C4 — CI evidence:** run tests in CI and preserve logs/report/artifact digest. CI is not proof of a security sandbox. Status: `NOT_RUN` for this adapter.
6. **C5 — Source-specific adapters:** add one source at a time only after scope, permissions, expected metadata and negative tests are defined. Status: `BLOCKED` pending earlier gates.
7. **C6 — Human review:** independent reviewer evaluates evidence and residual risks. Status: `PENDING`.
8. **C7 — Phase decision:** no Phase 1 transition unless all required gates pass and the user explicitly authorizes it.

## 14. Open questions that must not be guessed

- Canonical source registry format and current authoritative location.
- Exact approved schema/version and the intended 4D model definition.
- Whether raw bytes should be stored in the repository, an encrypted local archive, or an external object store; until decided, avoid sensitive/raw exports.
- Supported source adapters and the exact scopes/permissions available for each.
- Approved size, timeout, file-type and retention limits.
- Independent reviewer identity/process.
- Whether a later staging store is a filesystem-only artifact area or another approved storage system.

## 15. Current decision

The Central Raw Data Collection Adapter is a proposed control boundary. The initial implementation should be local-only and read-only, with no database writer and no external mutations. The design is not approved for freeze. All tests in Section 10 remain `NOT_RUN` until actual execution evidence is collected.

## 16. End-of-task record

- Work performed: drafted the adapter design and its boundaries, states, contracts, enforcement rules, test plan, risks, and implementation gates.
- Evidence used: current repository files `docs/ARCHITECTURE.md`, `docs/DATA-CONTRACTS.md`, `docs/PHASE0-3-SOURCE-COLLECTION.md`, `docs/WORKFLOW-SPEC.md`, and `docs/DATABASE-STRUCTURE.md` read from the default branch.
- Not completed: implementation, runtime tests, independent review, approval, integration, and installation.
- Reason: repository/package entry-point conventions must be inspected and the proposed contract must be reviewed before implementation; current phase prohibits database writes and Phase 1.
- Next step: inspect the existing extension/package entry point, then implement only the contract/schema and tests as the next isolated increment.
