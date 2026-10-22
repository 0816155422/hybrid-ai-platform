# HAP External Evidence Snapshot — Batch 001

- Project: `HAP-2026-OFFLINE-FIRST`
- Record ID: `EXT-EVIDENCE-BATCH-001`
- Snapshot revision: `1.0.0-draft`
- Captured/normalized on: `2026-10-22` (date only; exact time not recorded)
- Status: `UNVERIFIED` — research notes normalized from reviewed source pages/search extracts; this is not a byte-for-byte archive of the source websites.
- Phase: `PHASE_0_BLOCKED`
- Phase 1: `PHASE_1_NOT_AUTHORIZED`
- Database writes: `ZERO_DATABASE_WRITE`

## Preservation and copyright policy

This file stores self-contained, cleaned notes, source identity, key claims, HAP relevance, limitations, and short excerpts where useful. It does **not** reproduce entire third-party pages. Full-page copies should only be retained when the source license/terms permit it. Source websites can change; this record preserves the observations below, not a guarantee that a source will remain available or unchanged.

For each source, the URL is provenance—not the stored evidence itself. This batch's exact-byte SHA-256 values are `NOT_COMPUTED`; no source bytes were archived or hashed in this batch. Git blob SHA and SHA-256 must not be conflated. If a source is recaptured, add a new revision/record and compare it to this record rather than silently overwriting it.

## Source records

### EXT-001 — Android Developers: Build an offline-first app

- Canonical URL: https://developer.android.com/topic/architecture/data-layer/offline-first
- Publisher: Android Developers / Google
- Source version/revision: `UNKNOWN` (page revision metadata not captured)
- Observed: `2026-10-22`
- Source type: official developer documentation
- Capture level: reviewed page/search extract; no raw HTML/PDF bytes preserved
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED` (source content reviewed; not an independently archived exact-byte snapshot)

**Cleaned content**
- An offline-first application should keep its core functionality usable without network access; at minimum, reads should work offline.
- A local data source should be the source of truth for higher layers of the application.
- When remote data is involved, reconnection requires a synchronization strategy and conflict handling.
- Backoff is appropriate for retrying transient failures; authorization failures should not be blindly retried without valid credentials.

**Short source excerpt:** “At a minimum, an offline-first app must be able to perform reads without network access.”

**HAP application (design inference, not source requirement):**
- Treat local persisted state as the primary read path for offline operation.
- Specify sync direction, conflict policy, retry classification, and recovery behavior before implementation.
- Do not treat offline-first as merely a cache in front of a mandatory network dependency.

**Limitations:** This page is Android-focused. Its architectural principles can inform HAP, but platform-specific implementation details must not be assumed to apply to every adapter/runtime.

### EXT-002 — GitHub Docs: GitHub CLI quickstart

- Canonical URL: https://docs.github.com/en/github-cli/github-cli/quickstart
- Publisher: GitHub
- Source version/revision: `UNKNOWN` (page revision metadata not captured)
- Observed: `2026-10-22`
- Source type: official product documentation
- Capture level: reviewed search extract; no raw bytes preserved
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED`

**Cleaned content**
- GitHub CLI supports authenticated command-line workflows, including an interactive login flow.
- Authentication and authorization are separate from whether a particular command has sufficient scopes/permissions.
- The availability of a CLI workflow does not prove that the current machine is logged in, that a token has the needed scope, or that a requested operation succeeded.

**Related official authentication page:** https://docs.github.com/en/github-cli/github-cli/authenticating-with-github-cli

**HAP application (design inference):**
- Prefer a provider's supported CLI/native workflow when it meets the task and is authorized.
- Record the actual identity/scope check and command result as execution evidence; never infer success from tool presence.
- Do not write token values into repository files, logs, snapshots, or manifests.

**Limitations:** This note does not claim that GitHub CLI is installed or authenticated on any HAP device. No local CLI command was executed as part of this research record.

### EXT-003 — Model Context Protocol (MCP): Server overview, draft specification

- Canonical URL: https://modelcontextprotocol.io/specification/draft/server/index
- Publisher: Model Context Protocol
- Source version/revision: draft specification; exact revision identifier not captured
- Observed: `2026-10-22`
- Source type: protocol specification (draft)
- Capture level: reviewed page/search extract; no raw bytes preserved
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED`

**Cleaned content**
- The specification distinguishes prompts, resources, and tools by role: prompts are user-controlled templates, resources are application-controlled context, and tools are executable functions that can retrieve information or perform actions.
- The reviewed URL is explicitly under the draft specification path. Draft semantics may change and must not be represented as a stable, frozen contract.

**Short source excerpt:** “Tools: Executable functions that allow models to perform actions or retrieve information.”

**HAP application (design inference):**
- Keep tool execution, contextual resources, and reusable prompts/skills as distinct module types.
- If HAP adopts MCP, pin a concrete specification revision and SDK version in its compatibility record; define an adapter boundary rather than making the draft protocol the sole internal architecture.

**Limitations:** Draft page only. This is not proof that an HAP MCP client/server exists, is integrated, or passes conformance tests.

### EXT-004 — NIST SP 800-171 Rev. 3

- Canonical URL: https://csrc.nist.gov/pubs/sp/800/171/r3/final
- Publisher: U.S. National Institute of Standards and Technology (NIST)
- Publication: May 2024 (as stated on the official publication landing page)
- Source version: SP 800-171 Revision 3
- Observed: `2026-10-22`
- Source type: official cybersecurity publication landing page
- Capture level: landing-page metadata reviewed; full control text not captured in this batch
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED`

**Cleaned content**
- SP 800-171 Rev. 3 addresses protection of Controlled Unclassified Information (CUI) in applicable nonfederal systems and organizations.
- It is a defined security publication with a specific scope; it should not be presented as a blanket certification or automatically applicable legal requirement for every HAP deployment.

**HAP application (design inference):**
- Use the publication as a candidate source for control mapping only after confirming HAP's data classification, deployment context, and applicable obligations.
- Capture the exact control text and identifiers before mapping any control to HAP requirements.

**Limitations:** The full publication/control text was not captured here. No claim is made that HAP complies with NIST SP 800-171 Rev. 3.

### EXT-005 — OpenTelemetry: Context propagation

- Canonical URL: https://opentelemetry.io/docs/concepts/context-propagation/
- Related specification URL: https://opentelemetry.io/docs/specs/otel/context/
- Publisher: OpenTelemetry
- Source version/revision: `UNKNOWN` (page/spec revision not captured)
- Observed: `2026-10-22`
- Source type: official observability documentation/specification
- Capture level: reviewed page/search extract; no raw bytes preserved
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED`

**Cleaned content**
- Context propagation allows trace/span context to travel across process and network boundaries, supporting correlation across distributed operations.
- Incoming context from external boundaries can be forged or untrusted.
- Propagated baggage can disclose internal or personal information; secrets such as credentials and API keys should not be put into baggage.

**HAP application (design inference):**
- Use stable correlation IDs across Gate → Workflow → Skill → Tool/Adapter calls where observability is enabled.
- Treat externally supplied correlation/context fields as untrusted input.
- Apply an allowlist to propagated metadata and exclude credentials, tokens, and unnecessary personal data.

**Limitations:** Documentation reviewed, not a HAP tracing implementation or security test.

### EXT-006 — OpenAI Help Center: Connected apps in ChatGPT

- Canonical URL: https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt
- Publisher: OpenAI
- Source version/revision: `UNKNOWN`; page appeared recently updated in the search result at capture time, but exact revision timestamp was not preserved
- Observed: `2026-10-22`
- Source type: official product/help documentation
- Capture level: reviewed search extract; no raw bytes preserved
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED`; time-sensitive

**Cleaned content**
- Connected-app availability and behavior may depend on factors such as app, plan, region, workspace configuration, role, model, and interface.
- A connector shown in ChatGPT is not evidence that an external API is available independently, that every action is permitted, or that the provider's quotas and restrictions do not apply.
- Product behavior and plan limits can change; re-check this source before making an operational decision.

**HAP application (design inference):**
- Maintain separate capability states for “listed in this ChatGPT environment,” “connected,” “authorized for this operation,” “within quota,” and “execution verified.”
- Do not assume ChatGPT connector access can be reused by an external HAP process.

**Limitations:** This is volatile product documentation. Revalidate before relying on it for plan or connector behavior.

### EXT-007 — OpenAI API Pricing

- Canonical URL: https://platform.openai.com/pricing
- Publisher: OpenAI
- Source version/revision: live pricing page; no immutable revision identifier captured
- Observed: `2026-10-22`
- Source type: official pricing page
- Capture level: pricing page referenced; no complete price table or raw bytes preserved
- Exact source SHA-256: `NOT_COMPUTED`
- Status: `UNVERIFIED`; highly time-sensitive

**Cleaned content**
- API prices and billable units are published by product/model or service and may change.
- A price observation is meaningful only when paired with the capture date, product/model, unit, currency, and applicable billing conditions.
- Do not generalize a price for one API feature to every ChatGPT feature, connected app, or external provider.

**HAP application (design inference):**
- Store pricing as dated observations with product/model, unit, currency, source URL, and review date.
- Do not hard-code this page's current prices as durable architecture constants.

**Limitations:** This batch intentionally does not freeze numerical prices because no complete, exact table was captured. Check the official page at decision time.

## Cross-source conclusions for HAP (inferences, not direct source mandates)

1. **Offline-first:** local reads, a defined sync model, conflict policy, and retry classification should be explicit design contracts.
2. **Modularity:** keep prompt/template, context/resource, executable tool, workflow, skill, and adapter concepts distinct where the HAP requirements need them; do not assume a draft external protocol is the internal source of truth.
3. **Permission-aware execution:** tool discovery, authentication, authorization, quota availability, successful execution, and read-back verification are separate states.
4. **Traceability:** correlate cross-module operations without propagating credentials or unnecessary sensitive data.
5. **Security standards:** map standards to HAP only after confirming scope and preserving the exact control references used.
6. **Volatile information:** pricing, plan limits, connector availability, and draft protocol pages require dated recapture and revision comparison.

## Recapture and revision protocol

For each future source recapture:
1. Record canonical URL, publisher, page/release revision, capture time in UTC, and retrieval method.
2. Preserve exact bytes only when lawful and permitted; otherwise preserve permitted excerpts and a cleaned derivative.
3. Compute SHA-256 over the exact saved bytes using a documented tool/version; store the digest separately from any Git blob SHA.
4. Keep the prior snapshot unchanged. Add a new record/revision and write a diff/changed-claims report.
5. Reassess all HAP decisions that depended on changed claims.
6. Never mark the source or a HAP gate `PASS` solely because a note exists.

## Change log

- `1.0.0-draft` — Initial cleaned external-evidence batch committed to the designated HAP repository. No source websites were modified. No code, database, deployment, or external service configuration was changed by this record.
