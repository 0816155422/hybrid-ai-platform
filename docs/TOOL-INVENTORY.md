# HAP Tool, Skill, and Connector Inventory

- Project: `HAP-2026-OFFLINE-FIRST`
- Inventory revision: `0.1.0-draft`
- Status: `INITIAL INVENTORY — NOT A CAPABILITY CERTIFICATE`
- Current phase: `PHASE_0_BLOCKED`

## Rules

This inventory distinguishes (1) a tool being listed in the current ChatGPT environment, (2) a connection being available, (3) permission to perform an action, and (4) successful execution with read-back evidence. These are separate states. A listed tool does not imply that its account is connected, licensed, authorized for every action, or tested against HAP.

Never store access tokens, API keys, credentials, private keys, cookies, or other secrets in this file or the repository.

## Tool inventory

| Tool / integration | Intended use in HAP | Availability evidence | Write boundary / restriction | Current HAP status |
|---|---|---|---|---|
| GitHub connector | Versioned source, specifications, code, manifests, test evidence, change history | Repository `0816155422/hybrid-ai-platform` was listed and files could be fetched; file creation/write-back has succeeded in prior work | User explicitly designated this repository as the main project store. Keep database writes, deployment, and unrelated remote mutations prohibited. Do not commit sensitive history while repository is public. | `AVAILABLE_FOR_REPOSITORY_WORK`; each change requires read-back |
| JobsPipe | Search live job listings and scan technology stacks for a supplied domain | Installed skill instructions are available; API requires a JobsPipe API key beginning `jp_live_` | Not a GitHub repository-management tool. No key was provided or tested here. Do not create or store a key in the repo. | `SKILL_DOCUMENTATION_READ`; API access `NOT_VERIFIED` |
| Python execution tool | Local reasoning, parsing, hashing, static checks when files are accessible in the execution environment | Tool is exposed in this ChatGPT session | A local execution result is not proof of target Android/device behavior. Capture exact command, environment, outputs, and artifact hashes. | `AVAILABLE_IN_SESSION`; target-device use `NOT_VERIFIED` |
| GitHub Actions | Repeatable repository CI for evidence register validation | Workflow definition is being added to this repository | Definition presence does not prove a workflow run passed. Read run ID, commit SHA, job result, and logs before reporting success. | `CONFIGURATION_PENDING_FIRST_RUN` |
| Dropbox / Dropbox Dash | Potential source archive or linked artifact storage | Earlier audit found no valid Dash license and no Dash content was verified | Do not treat connector names or empty search results as proof of archive completeness. | `UNVERIFIED` |
| Notion | Working notes / project references | Earlier audit identified two project pages | Existing pages are working documents, not proof of enforcement or complete source recovery. | `SOURCE_REFERENCES_ONLY` |
| Hjarni Notes | Project notes and draft contracts | Earlier audit identified project-control and evidence notes | Drafts are not authoritative standards or executed validators. | `SOURCE_REFERENCES_ONLY` |
| Asana | Task status and work tracking | Earlier audit returned 10 tasks, 2 completed and 8 incomplete at that time | Time-bound snapshot only; re-check before using as current status. | `HISTORICAL_SNAPSHOT` |
| TickTick | Potential task/checkpoint source | Earlier connector retrieval failed with a tool/API error | Failure to retrieve is not proof of absence. | `UNVERIFIED` |
| Supabase | Possible future database integration | Legacy records were reported in prior project context | Legacy data is quarantined from current HAP status; current HAP has `ZERO_DATABASE_WRITE`. Do not write. | `PROHIBITED_FOR_WRITES` |
| ChatGPT export | Original conversation archive source | Official export instructions are recorded in the external-source audit | Preserve export bytes as original; do not infer complete history from a shared link or project summary. | `NOT_YET_COLLECTED_IN_THIS_REPOSITORY` |
| Gemini export | Original Gemini conversation archive source | Official export instructions are recorded in the external-source audit | Preserve export bytes as original; distinguish export scope from derived summaries. | `NOT_YET_COLLECTED_IN_THIS_REPOSITORY` |

## Increment added 2026-10-21: fixed-command Python test orchestrator

| Component | Purpose | Current status | Boundary |
|---|---|---|---|
| `scripts/run_hap_tests.py` | Run the fixed evidence validator and Python unit-test suite with per-check timeouts, captured output, exit codes, and optional JSON report | `CI_EXECUTION_PASS_FOR_COMMIT_3861f85` | This is an orchestrator, **not** a security sandbox. It does not accept arbitrary shell commands and does not prove network/filesystem isolation. |
| `tests/test_run_hap_tests.py` | Test allowlisted step definitions, success/failure mapping, timeout handling, and `shell=False` | `PASS_IN_CI_RUN_39463527350` | Four orchestrator tests plus five evidence-validator tests passed in the combined 9-test suite. |
| GitHub Actions workflow | Invoke the orchestrator and upload the JSON report for 14 days | `PASS_FOR_RUN_39463527350` | Run `39463527350` succeeded; artifact `hap-test-report` (ID `12284026982`) was uploaded. Failure-path upload is not tested. |

## Required per-tool verification record

Before relying on any tool for a project gate, append a record under `evidence/execution/` with:

- Tool name, connector/action identifier, and version where available
- Account/connection status as actually observed (never include secrets)
- Exact requested action and declared scope
- Expected result and actual result
- Timestamp, status code/exit code, and safe output reference
- Read-back evidence for any permitted write
- Independent verifier and result, if performed
- Failure reason, impact, unblock condition, and next step

## Capability status vocabulary

- `AVAILABLE`: exposed and usable in the current session, with an observed successful call
- `CONNECTED`: authenticated connection state observed, distinct from permission for every operation
- `AUTHORIZED`: an explicit policy or user authorization covers the specific action
- `TESTED`: the specific operation executed with evidence
- `READ_BACK_VERIFIED`: a write was fetched again and compared to the intended content
- `UNVERIFIED`: evidence is insufficient
- `BLOCKED`: a documented blocker prevents use
- `NOT_APPLICABLE`: reason is recorded

Do not collapse these statuses into a single “installed” or “working” label.

## Current conclusion

The repository connector can read and write versioned text files, with prior write-back evidence. That does not establish that every plugin or skill can independently access this repository. JobsPipe is a job/technology intelligence API, not the project’s source-control system; no JobsPipe API call is claimed in this task.
