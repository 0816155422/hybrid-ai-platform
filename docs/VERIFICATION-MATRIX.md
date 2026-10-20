# HAP Verification Matrix

- Project ID: `HAP-2026-OFFLINE-FIRST`
- Review status: `INITIAL BASELINE — ALL CHECKS UNVERIFIED UNLESS EVIDENCE IS LINKED`
- Phase 0: `BLOCKED`
- Phase 1: `NOT_AUTHORIZED`

| Check ID | Area | Acceptance target | Current status | Evidence required / blocker |
|---|---|---|---|---|
| VM-01 | Repository identity | Correct owner/repository/default branch confirmed | `PASS` for identity only | Repository README and commit read-back; does not prove privacy |
| VM-02 | Repository privacy | Private visibility confirmed before sensitive archive storage | `PASS` for visibility only | GitHub connector repository listing returned `visibility: private` on 2026-10-21; collaborator/app access and prior public exposure are not assessed |
| VM-03 | Artifact inventory | All in-scope artifacts listed with source and version | `UNVERIFIED` | Enumerate repository files and connected source references; preserve user clarification that the linked repo contains the intended initial-period conversation only |
| VM-04 | Original file preservation | Original bytes retained separately from derived summaries | `UNVERIFIED` | Source files, exact byte counts, and SHA-256 |
| VM-05 | Hash manifest | SHA-256 reproducible for each collected file | `NOT_RUN` | Actual bytes and recorded hashing tool/output |
| VM-06 | Data contract | Required fields and schema version fixed | `BLOCKED` | Canonical schema URI/version/digest unresolved; draft contract is not approved |
| VM-07 | Workflow | Sequential stages, loop-back, handoff, and end log documented | `PASS` for documentation presence only | This document and WORKFLOW-SPEC; no runtime enforcement claim |
| VM-08 | Installation | Intended extension/package installs on a named environment | `NOT_RUN` | Exact artifact, device/runtime, procedure, logs, and independent confirmation |
| VM-09 | Tests | Required tests execute with captured output | `NOT_RUN` | Test suite, environment, command, exit code, output, and artifact hashes |
| VM-10 | Integration | Each external adapter is proven within declared permissions | `UNVERIFIED` | Per-connector scope, authorized test, observed result, and read-back |
| VM-11 | Independent verification | Verifier checks evidence independently of builder | `BLOCKED` | Named verifier procedure and evidence-backed review record |
| VM-12 | 4D model | User-intended four dimensions are explicitly defined and mapped | `BLOCKED` | Four-D definition not found in the reviewed context; do not infer |
| VM-13 | Phase 0 gate | Every required Phase 0 criterion passes | `BLOCKED` | Required source evidence, schema, independent review, and gate record |
| VM-14 | Phase 1 authorization | Explicit user authorization after Phase 0 passes | `NOT_AUTHORIZED` | Phase 0 is still blocked |

## Gate decision rule

No overall PASS is permitted while any required check is FAIL, BLOCKED, NOT_RUN, or UNVERIFIED. Documentation presence can only pass a documentation-presence check; it cannot establish runtime behavior.


| VM-15 | Evidence register validator | Validator rejects malformed IDs/statuses/hashes and accepts the current pending-hash register | `PASS` for tested commit only | GitHub Actions run `39463527350`, commit `3861f85a68d151803248f65368f98e3612e3873c`; log: `VALIDATION_OK structure_only=true` |
| VM-16 | Validator unit tests | All validator unit tests execute and pass in a recorded environment | `PASS` for tested commit only | GitHub Actions run `39463527350`, Python `3.12.15`; 9 unit tests ran and reported `OK` |
| VM-17 | CI automation | GitHub Actions run is observed successful for a specific commit | `PASS` for run `39463527350` | Job `118768776314` completed with conclusion `success` for commit `3861f85a68d151803248f65368f98e3612e3873c`; this does not pass the overall Phase 0 gate |
| VM-18 | Artifact register alignment | Every row has 13 columns, required project ID, permitted status, and distinct Git blob SHA / SHA-256 fields | `UNVERIFIED` | The register was corrected and read back; execute the validator and independently inspect parsed CSV rows |
| VM-19 | Repository privacy | Private visibility and collaborator/app access reviewed before sensitive source archive collection | `PARTIAL` | Private visibility was observed via GitHub connector; collaborator/app access and whether sensitive data was previously exposed remain unreviewed |

| VM-20 | Test orchestrator implementation | Fixed allowlisted checks, bounded timeout, captured stdout/stderr, exit status, and optional JSON report | `PASS` for tested behavior | CI executed the orchestrator successfully; unit tests cover fixed command list, success/failure mapping, timeout handling, and `shell=False` |
| VM-21 | Test orchestrator unit tests | Orchestrator unit tests execute and pass | `PASS` for tested commit only | GitHub Actions run `39463527350`; all 9 combined unit tests passed |
| VM-22 | CI execution report | Report artifact is uploaded even when checks fail | `PASS` for successful-run upload only | Artifact `hap-test-report`, ID `12284026982`, uploaded (1,128 bytes); failure-path upload is not yet tested |
