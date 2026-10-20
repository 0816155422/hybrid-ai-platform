# HAP Research Dossier — AI Memory, Data Preparation, Provenance, Transfer, and NASA Practice

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Document ID: `DOC-RESEARCH-DATA-001`
- Version: `0.1.0`
- Status: `RESEARCH BASELINE — PRIMARY SOURCES REVIEWED; HAP ADAPTATION PROPOSED; INDEPENDENT REVIEW PENDING`
- Current phase: `PHASE_0_BLOCKED`
- Phase 1: `NOT_AUTHORIZED`
- Database write policy: `ZERO_DATABASE_WRITE`
- Remote mutation policy: `PROHIBITED`
- Research date: 2026-10-21

> This dossier records public standards, official institutional guidance, and published research. It is not a claim that HAP is compliant with these standards, that all source files have been archived locally, or that the proposed adapter is implemented. Public source pages were reviewed; full source bytes, exact-byte SHA-256 manifests, and independent review have not yet been completed for every source.

## 1. Research question and method

The target is a data-preparation and analysis adapter for HAP that can ingest heterogeneous source material, preserve the original, extract structure without losing provenance, normalize it into a documented intermediate contract, and prepare it for later analysis and controlled handoff. The adapter must not turn an AI-generated summary into an original source, silently merge conflicting claims, or promote collected material into approved project truth.

Source priority used here:
1. Official standards bodies and institutional sources (W3C, IETF/RFC Editor, NIST, NASA, ISO).
2. Peer-reviewed or published research papers on AI memory.
3. Secondary commentary only for context, not as the normative basis.

This is a source review, not a systematic literature review: search coverage and source retrieval are bounded, and the research is not exhaustive.

## 2. Primary-source register

| ID | Source and type | Relevant finding | HAP use | Status / limitation |
|---|---|---|---|---|
| SRC-R01 | W3C, [PROV-DM](https://www.w3.org/TR/prov-dm/) — Recommendation | Provenance can be modeled through entities, activities, agents, time, derivation, responsibility, and collections/bundles. It is designed for interoperable provenance exchange across heterogeneous systems. | Map original artifacts, extraction/normalization activities, responsible tools/agents, and derived outputs. | Official specification page reviewed; local archival bytes/hash not yet registered. |
| SRC-R02 | W3C, [PROV-O](https://www.w3.org/TR/prov-o/) — Recommendation | Provides an OWL ontology representation of PROV-DM for expressing and exchanging provenance; can be specialized for domain-specific details. | Optional semantic export/mapping; do not require RDF for the initial lightweight envelope. | Official specification page reviewed. |
| SRC-R03 | W3C, [PROV Constraints](https://www.w3.org/TR/prov-constraints/) — Recommendation | Provenance validity includes identifier uniqueness, event-order consistency, typing, and impossibility constraints; consistency validation is distinct from source truth. | Validate provenance graph consistency and event ordering; never treat valid provenance as proof that a source claim is true. | Official specification page reviewed. |
| SRC-R04 | DCMI, [Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) — Recommendation | General metadata vocabulary includes creator, identifier, date, format, provenance, source, rights, type, and related terms; can be combined with other vocabularies and used outside RDF. | Common cross-format descriptive metadata, while HAP adds required integrity, policy, and verification fields. | Official specification page reviewed. |
| SRC-R05 | IETF, [RFC 8259 JSON](https://www.rfc-editor.org/rfc/rfc8259.html) — Internet Standard | JSON is a portable, language-independent structured data interchange format. | Use UTF-8 JSON for individual typed records/contracts; specify schema/version and reject ambiguous malformed input. | Official RFC page reviewed. |
| SRC-R06 | NASA PO.DAAC, [Data Management Plan guidance](https://podaac.jpl.nasa.gov/NASA_ROSES_DataManagementPlan) — institutional guidance | Data plans cover data sources, formats, packaging, metadata, conventions, and lifecycle sharing; plans can evolve as data are collected and processed. | Require a per-collection data inventory and format/metadata plan; update it when observed sources differ from expectation. | Official NASA-affiliated guidance page reviewed; details vary by program. |
| SRC-R07 | NASA SMD, [Data Management and Sharing guidance](https://github.com/nasa/smd-open-science-guidelines/blob/main/Research_Guidance/Data_Management_Sharing.md) — institutional policy guidance | Data-management plans describe data types, approximate amounts, machine-readable/file formats, applicable standards/metadata, preservation and sharing; legal/export-control exceptions can apply. | Record format, scale, standards, preservation/access restrictions, and sharing decision before transfer. | Official NASA SMD guidance repository reviewed; apply only where relevant, not as a universal NASA rule. |
| SRC-R08 | NASA, [Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/) — handbook | NASA describes lifecycle systems engineering, technical management, and requirements/verification processes; it is a guide used with applicable NASA requirements. | Trace source requirement → derived requirement → design decision → verification evidence. | Official handbook page reviewed; HAP is not NASA and is not claiming NASA compliance. |
| SRC-R09 | NASA, [NPR 7150.2C Software Engineering Requirements](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7150_002C_&page_name=all) — agency requirements | Software configuration management identifies controlled items and versions, tracks/evaluates changes, and preserves product integrity over the lifecycle. | Pin source revisions and adapter/schema versions; record changes and their rationale. | Official NASA directive page reviewed; applicability to HAP is by design analogy, not legal mandate. |
| SRC-R10 | NIST, [SP 800-144: Public Cloud Security and Privacy](https://csrc.nist.gov/pubs/sp/800/144/final) — guidance | Moving data/services outside an organization changes security and privacy responsibilities; outsourcing does not remove the organization's accountability. | Treat cloud transfer as an explicit trust boundary with scope, classification, authorization, encryption, retention, and read-back checks. | Official NIST publication page reviewed; published 2011, still useful baseline but not a complete current cloud control set. |
| SRC-R11 | NIST, [AI RMF Generative AI Profile (AI 600-1)](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — guidance | Applies AI RMF risk-management thinking to generative AI across lifecycle and context-specific risk priorities. | Include source reliability, privacy, provenance, human review, uncertainty, and risk/impact fields in analysis preparation. | Official NIST publication page reviewed; voluntary framework, not a HAP certification. |
| SRC-R12 | ISO, [ISO/IEC 42001:2023 overview](https://www.iso.org/standard/42001) — management-system standard | Defines requirements and guidance for an AI management system covering responsible development, provision, and use of AI systems. | Use as a governance cross-reference for roles, policy, risk assessment, documented processes, and continual improvement. | Official overview reviewed; full standard text was not retrieved, so no clause-level conformity claim. |
| SRC-R13 | Packer et al., [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) — research preprint | Proposes virtual context management inspired by hierarchical memory, moving information between limited fast context and larger external memory; evaluates document analysis and multi-session chat. | Separate working context from durable external memory; retrieval and memory movement should be explicit and inspectable. | Paper abstract/metadata reviewed; implementation claims are paper-specific, not universal best practice. |
| SRC-R14 | Park et al., [Generative Agents](https://arxiv.org/abs/2304.03442) / ACM DOI [10.1145/3586183.3606763](https://doi.org/10.1145/3586183.3606763) — research paper | Uses a natural-language memory stream, synthesizes higher-level reflections, and retrieves memories dynamically for planning. | Separate raw event/observation records from derived summaries/reflections and retrieval indexes. | Published research; simulation architecture, not a general-purpose enterprise memory standard. |
| SRC-R15 | Wu et al., [LongMemEval](https://arxiv.org/abs/2410.10813) — research benchmark | Evaluates information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention; reports long-term memory failure modes and evaluates retrieval/indexing choices. | Memory adapter acceptance criteria must cover temporal updates, conflicting/updated facts, multi-source reasoning, and abstention when evidence is insufficient. | Published benchmark paper; its benchmark scores do not certify HAP. |

## 3. Findings: what the evidence supports

### 3.1 AI memory should be layered, not a single undifferentiated summary

The research supports experimenting with a hierarchy of limited active context and external memory (MemGPT), event-like memory with derived reflections and retrieval (Generative Agents), and evaluation of temporal updates, multi-session reasoning, and abstention (LongMemEval). These are research designs, not a consensus standard that every AI must use one exact architecture.

**HAP design implication:** keep at least these separate:
- **Original source** — bytes or exact source reference, never overwritten by a summary.
- **Extracted observations** — parsed text/records and source locations, each linked to the original.
- **Normalized facts/claims** — typed values with time, confidence/epistemic status, and supporting source references.
- **Derived analysis** — summaries, comparisons, hypotheses, embeddings/indexes, or model-generated reflections; always marked derived.
- **Retrieval view** — a temporary selection assembled for a specific task, with the query and selected evidence IDs recorded when appropriate.
- **Decision/approved project state** — only created through the project's human/gate process, not by memory retrieval alone.

Do not collapse "remembered", "retrieved", "inferred", and "approved" into one status.

### 3.2 Provenance is a graph of evidence, not merely a source URL

W3C PROV provides an interoperable model: entities (files, claims, outputs), activities (capture, parse, transform, analyze, transfer), and agents (human, tool, service), plus generation/use/derivation/association relations. DCMI provides general descriptive metadata. HAP should combine these ideas rather than forcing every data field into a single vocabulary.

Minimum lineage:
`original artifact -> extraction activity -> extracted record -> normalization activity -> normalized record -> analysis activity -> derived output`

Every transformation must preserve a `derived_from` link. Record the exact tool/version, schema version, timestamp, and limitations. Validate identifier uniqueness and sensible event order. A valid provenance graph still does not prove the underlying claim is true.

### 3.3 NASA practice emphasizes plans, controlled baselines, and traceability

NASA public guidance demonstrates lifecycle-oriented data management plans, explicit data/file formats and metadata, preservation/sharing decisions, and configuration management for controlled software items. This is the useful transferable pattern; HAP must not imply it follows NASA internal procedures or is certified to NASA requirements.

**HAP design implication:** for each source collection, declare expected source, format, scope, size/count limits, applicable metadata, preservation/retention, access restrictions, and downstream use. Keep requirements-to-design-to-evidence traceability and version the contract/adapter itself.

### 3.4 Cloud transfer is a trust-boundary crossing, not a file-copy detail

NIST SP 800-144 emphasizes security/privacy considerations when data and services are outsourced to public cloud. Therefore, a cloud transfer adapter needs an explicit authorization and classification check, least-privilege scope, transport protection, encryption/key-custody policy for stored sensitive material, integrity verification after transfer, retention/deletion policy, and an audit trail. The cloud provider's existence or a successful upload response is not sufficient evidence of secure or complete transfer.

**HAP Phase 0 implication:** define the transfer contract only. No cloud upload, secret handling, or remote mutation is authorized by this research.

### 3.5 Use multiple representations without confusing them

- **Original bytes:** preserved unchanged where collection is authorized and safe.
- **JSON:** suitable for typed request/envelope/record exchange; requires explicit schema/version and validation.
- **JSONL:** useful as an append-oriented event/evidence ledger (one JSON object per line), but atomic append, concurrency, canonicalization, and integrity must be specified by the implementation.
- **CSV:** useful for tabular inventories and registers; retain original file and document delimiter/encoding/header expectations.
- **XML / RDF / PROV-O:** useful when the source or interchange profile requires structured XML or semantic provenance; not mandatory for all artifacts.
- **PDF / DOCX / HTML / Markdown / source code / binary files:** preserve original; text extraction is a separate derivative and must retain page/line/offset references where available.
- **Images/scans/audio/video/archives:** use modality-specific extraction with tool/version and extraction limitations; do not silently treat OCR/transcription as original source.
- **Embeddings/vector indexes:** derived retrieval artifacts, not authoritative source records; version them and link them to the source chunks/model configuration where available.

Do not convert all source material into a single universal format at ingestion time. The common envelope normalizes metadata; content-specific adapters preserve the source-native payload and create separately versioned derivatives.

## 4. Proposed HAP data-preparation pipeline

1. **Scope and authorize** — resolve source identity, exact scope, permissions, classification, purpose, and limits. Unknown/missing authorization blocks collection.
2. **Acquire raw** — collect exact bytes if permitted, or record an external reference with explicit limitations. Never claim bytes were archived if only a URL/connector result was observed.
3. **Fingerprint** — record exact byte count and SHA-256 only when exact bytes are available. Keep Git blob IDs, ETags, object version IDs, and SHA-256 as distinct identifiers.
4. **Detect and parse** — identify media type from observed evidence; parse with bounded, format-specific handlers. Do not execute source content. Reject or quarantine malformed, oversized, or suspicious inputs.
5. **Extract** — create a derived artifact with page/line/record/chunk locators and extraction tool/version. Preserve original and extraction errors.
6. **Normalize metadata** — map available fields to a versioned HAP envelope plus DCMI/PROV mappings. Unknown values remain unknown; no invented timestamps, sizes, hashes, owners, or versions.
7. **Validate** — validate structure/schema, provenance relations, IDs, temporal ordering, cross-reference integrity, source scope, duplicates, and required fields.
8. **Analyze** — perform comparisons/summaries only over identified evidence; separate observations, source claims, inferences, conflicts, and unanswered questions.
9. **Prepare handoff** — emit a package manifest with source list, versions, hashes, schema version, derived-from links, coverage/gaps, and validation status.
10. **Independent review and gate** — verifier checks raw-to-derived linkage and integrity; human/gate controller decides whether evidence is accepted. No automatic promotion or phase transition.

Any error stops dependent steps, preserves prior artifacts/events, records the exact failed stage and recovery path, and restarts the affected validation chain from scope/source identity.

## 5. Proposed canonical record families (not a frozen schema)

| Record family | Purpose | Required distinguishing fields |
|---|---|---|
| `SourceDescriptor` | Registered source and its permissions | source_id, source_type, canonical_locator, owner/authority if observed, allowed_scope, auth_ref, access_mode, version_observation |
| `CollectionRequest` | Bounded request | request_id, project_id, phase, source_id, scope, purpose/requirement refs, limits, authorization_ref, requested_at |
| `RawArtifact` | Original object or explicit external reference | artifact_id, source_locator, source_version, capture time, media type, byte size/hash if available, raw/external-reference state, limitations |
| `ExtractionArtifact` | Parsed text, OCR, transcription, chunking, or structured rows | derivative_id, derived_from, extractor/tool/version, locator mapping, output format/schema, extraction status, errors |
| `NormalizedRecord` | Typed metadata/claim/observation | record_id, schema_version, record_type, subject, predicate/field, value, valid_time, observed_time, source_refs, epistemic_status |
| `AnalysisArtifact` | Summary, comparison, hypothesis, or model-generated interpretation | analysis_id, input_record_ids, method/model/tool version, prompt/config ref where available, generated_at, uncertainty, conflicts, limitations |
| `TransferManifest` | Controlled package/transfer | transfer_id, source/destination identity, authorization, artifact manifest, hashes, encryption/key reference (never key material), transfer status, receiver read-back result |
| `VerificationRecord` | Independent validation | verifier identity/role, criteria/version, inputs, checks, expected/actual, status, evidence refs, timestamp |
| `GateDecision` | Human/authorized gate result | gate_id, decision, rationale, reviewer, evidence refs, decided_at, supersedes |

### Epistemic status (proposed)

Use explicit values such as `SOURCE_ASSERTION`, `OBSERVED_METADATA`, `EXTRACTED_TEXT`, `NORMALIZED_CLAIM`, `INFERENCE`, `HYPOTHESIS`, `CONFLICTED`, `UNKNOWN`, and `HUMAN_APPROVED`. These are proposed HAP vocabulary, not W3C/DCMI terms. A source assertion must not be silently upgraded to observed fact or human approval.

## 6. Cloud-transfer adapter contract (design only)

A future cloud transfer adapter must have a narrow, typed interface such as `prepare_transfer`, `validate_transfer`, `send_authorized_package`, and `verify_receiver_copy`. It must not expose generic arbitrary cloud commands. Required checks include:
- explicit source/destination and data-classification authorization;
- approved transfer direction and object scope;
- least privilege and credential handling through an approved secret mechanism;
- TLS/transport protection and a separately approved at-rest encryption/key-management design for sensitive data;
- manifest of exact bytes and hashes, source versions, schema version, and package count/size;
- resumable/partial status without overwriting prior evidence;
- receiver-side read-back/hash comparison where supported;
- retention, access review, and disposition rules;
- explicit failure state and no retry that silently duplicates or overwrites;
- no transfer when policy/phase/authorization is unknown.

The HAP current policy prohibits remote mutations. This section is a future design contract only; it authorizes no transfer.

## 7. Data preparation acceptance criteria

All statuses begin `NOT_RUN` until executed with evidence.

| ID | Acceptance target | Initial status |
|---|---|---|
| DP-001 | Raw source bytes remain unchanged when captured; derivative is separate | `NOT_RUN` |
| DP-002 | Missing authorization or unknown source blocks before reading | `NOT_RUN` |
| DP-003 | Unsupported/malformed/oversized input is blocked or quarantined with reason | `NOT_RUN` |
| DP-004 | Schema version and format are explicit; invalid records fail validation | `NOT_RUN` |
| DP-005 | Every extracted/normalized/analysis artifact links to its immediate parent and original source | `NOT_RUN` |
| DP-006 | Exact-byte SHA-256 can be independently recomputed; unavailable hashes remain pending | `NOT_RUN` |
| DP-007 | Source assertions, observations, inferences, hypotheses, conflicts, and approvals remain distinguishable | `NOT_RUN` |
| DP-008 | Temporal updates/conflicts are retained rather than silently overwritten | `NOT_RUN` |
| DP-009 | Analysis can abstain when evidence is missing or contradictory | `NOT_RUN` |
| DP-010 | Export manifest accounts for included, excluded, partial, and failed items | `NOT_RUN` |
| DP-011 | Cloud transfer remains blocked without explicit authorization and approved destination scope | `NOT_RUN` |
| DP-012 | Receiver-side read-back is compared to manifest where transfer is authorized | `NOT_RUN` |
| DP-013 | Provenance identifiers and event ordering pass consistency validation | `NOT_RUN` |
| DP-014 | Independent reviewer can reproduce the mapping from output claim to source evidence | `NOT_RUN` |

## 8. Gaps and decisions still required

- The approved HAP “4D” dimensions are not defined in reviewed evidence; do not infer them.
- Canonical JSON Schema URI/version/digest and versioning policy remain unapproved.
- Source registry and canonical authority for source permissions remain unresolved.
- Exact raw-archive destination, retention, encryption/key custody, and backup/restore approach remain unapproved.
- The initial local-only adapter implementation and independent verifier have not been executed.
- The user’s available connectors and source scopes must be verified individually; this dossier does not imply broad access.
- Full ISO/IEC 42001 text was not retrieved; only the official overview was reviewed.
- The sources above are reviewed pages/papers, not yet a complete exact-byte local source archive with SHA-256 manifest.

## 9. Current decision

Use W3C PROV-DM/PROV-O as the provenance model reference, DCMI as general descriptive metadata vocabulary, JSON with a versioned schema for typed records, JSONL for append-oriented event records only when canonicalization/concurrency rules are defined, NASA guidance as a lifecycle/data-management and traceability reference, NIST cloud guidance as the trust-boundary reference, NIST AI RMF GenAI profile and ISO/IEC 42001 overview as governance references, and the three AI-memory research papers as design/evaluation evidence rather than normative standards.

This is a **proposed HAP design baseline**, not an approved schema, implemented adapter, compliance certificate, or phase gate pass.

## 10. Work record

- Actual work: reviewed official public source pages and published AI-memory papers; synthesized findings into a proposed HAP data-preparation and analysis pipeline, record families, cloud-transfer contract, and acceptance criteria.
- Evidence: URLs and source IDs SRC-R01 through SRC-R15 above.
- Not completed: exact-byte source archive/hash manifest, full systematic literature review, implementation, execution tests, independent review, schema approval, and Phase 0 gate.
- Why incomplete: current work retrieved public source pages/abstracts; full original files and exact-byte digests have not all been archived, and the HAP schema and 4D definition remain unresolved.
- Next step: integrate this research into the Central Raw Data Collection Adapter, then define a versioned schema and implement the bounded local-only collection/extraction path after review.
