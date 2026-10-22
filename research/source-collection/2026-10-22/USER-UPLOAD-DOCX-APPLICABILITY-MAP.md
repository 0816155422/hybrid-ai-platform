# HAP Uploaded Document Applicability Map — 2026-10-22

Project: HAP-2026-OFFLINE-FIRST
State: PHASE_0_BLOCKED
Classification: preliminary source triage; not an approval, legal opinion, or final audit.
Related intake register: https://github.com/0816155422/hybrid-ai-platform/blob/research/source-collection-batch-01-2026-10-22/research/source-collection/2026-10-22/USER-UPLOAD-DOCX-INTAKE.md

## Purpose
Map the five user-uploaded DOCX files to possible HAP requirements without assuming that unrelated third-party terms are project requirements. This is a relevance screen based on the supplied document text; source authenticity, currentness, and relationship to the user's own apps/accounts are not established.

## Applicability matrix

| Intake ID | Source subject | Possible HAP use | Relevance | Evidence needed before adopting |
|---|---|---|---|---|
| HAP-UP-20261022-001 | ChatALL terms/privacy | Third-party AI connector risk review: data sent to providers, retention, subprocessors, user notice, account/security boundaries | CONDITIONAL | Confirm ChatALL is an intended HAP tool; capture official publisher URL/version/date; compare terms to actual connector behavior and permissions |
| HAP-UP-20261022-002 | Hirtius Banach app EULA | License/usage constraints only if this app or its code is a HAP dependency | UNCONFIRMED | Identify app/product and intended use; verify official source, version and applicable jurisdiction |
| HAP-UP-20261022-003 | Chromium CRX3 design document | Technical reference for signed browser-extension package integrity, signature verification and migration/security checks | POTENTIALLY RELEVANT | Confirm whether HAP includes a Chromium extension/package workflow; compare against current official Chromium source and implementation/tests |
| HAP-UP-20261022-004 | KrCiner user agreement | Third-party content-license/privacy risk only if the service or its content is used by HAP | UNCONFIRMED | Identify service and intended dependency; verify source/current version; review content license scope |
| HAP-UP-20261022-005 | Game/app privacy policy | Third-party data-processing reference only if the named app/service is used by HAP | UNCONFIRMED | Identify app/publisher and whether it is in scope; verify official source/version and actual data flows |

## Decisions from this triage
1. Do not import third-party EULAs or privacy policies as HAP requirements merely because they were uploaded.
2. Treat the CRX3 design document as a candidate technical reference, not proof that HAP has a browser extension or implements CRX3.
3. Keep each source's original file and intake hash unchanged; write interpretations in separate derived records.
4. If a source cannot be tied to an in-scope HAP component, disposition it as PENDING_SCOPE_CONFIRMATION or later NOT_APPLICABLE_WITH_REASON, not silently discard it.
5. Any privacy/security controls adopted from these sources must be mapped to a specific HAP requirement, component, owner and verification method.

## Cross-reference to Phase 0 baseline
The existing baseline calls for a tool/skill inventory and explicit capability states; data classification, provenance, access boundaries and redaction; least privilege and default read-only behavior; requirements-to-design-to-test traceability; and source applicability/evidence references.
These are baseline design targets, not evidence that the controls are implemented or tested.

## Open work
- Confirm source-to-component applicability from the authoritative HAP scope/tool inventory.
- Verify official publisher/source URL and document version for each DOCX.
- For CRX3, retrieve the current canonical Chromium source and check whether the uploaded DOCX matches it.
- Add each confirmed applicable source to the central source register with exact source/version, capture time, hash, mapped requirement IDs and test/evidence links.
- Leave phase and gate status unchanged until all required evidence is collected and independently reviewed.

No database writes, installation, deployment, phase transition, or Gate approval occurred.