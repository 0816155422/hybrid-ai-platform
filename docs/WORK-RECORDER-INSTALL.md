# HAP Work Recorder — First Installable Component

- Package: `hap-work-recorder`
- Version: `0.1.0`
- Project: `HAP-2026-OFFLINE-FIRST`
- Status: prototype / Phase 0 review; not approved for freeze
- Runtime: Python 3.10+; standard-library runtime only
- Storage: local JSON Lines (`.jsonl`) file; no database, network, cloud, or telemetry calls

## What this first component does

1. Requires a recorded preflight decision of `PASS` before a work-start event is accepted.
2. Appends explicit work events to a JSONL ledger; it never intentionally rewrites prior records.
3. Adds a SHA-256 hash chain so later edits, reordering, and deletion within the checked chain are detectable when they break the chain.
4. Requires a reason when a task closes as `PARTIAL`, `BLOCKED`, `FAILED`, or `UNVERIFIED`.
5. Provides a verifier command and unit tests.

**Limitations:** a hash chain is not tamper-proof storage; someone able to rewrite the entire ledger can recompute it. Back up the ledger and store signed/externally anchored digests later if required. It validates events that an operator or integration explicitly sends to it; it cannot observe ChatGPT's private reasoning or actions that were never emitted by an instrumented tool. A passing hash check proves only internal chain consistency, not that an event is true, complete, or independently reviewed.

## Install on Android using Termux

This requires Termux with Python and Git available. It is a command-line package, not an APK and not a one-tap ChatGPT UI extension.

```sh
pkg update
pkg install python git
git clone https://github.com/0816155422/hybrid-ai-platform.git
cd hybrid-ai-platform
python -m pip install .
hap-worklog --help
```

If you already cloned the private repository, use its existing folder and skip `git clone`. Git access must already be authenticated; do not paste access tokens into command arguments or logs.

## Basic use

Run these commands from the repository root. The default ledger is `evidence/work-log/events.jsonl`.

```sh
# 1. Start only after checking the task's policy, scope and baseline.
hap-worklog start --task "Implement lifecycle recorder" --scope "Local repo files and tests only" --preflight PASS --acceptance "Unit tests pass" --baseline "main commit SHA recorded separately"

# 2. Record observable events as they occur.
hap-worklog event --type "github_readback" --summary "Read back committed file" --source github_readback --evidence-ref "GitHub URL" --result PASS
hap-worklog event --type "unit_tests" --summary "Five unit tests executed" --source test_runner --evidence-ref "test report path" --result PASS

# 3. Close with evidence and blockers.
hap-worklog end --status PARTIAL --summary "Recorder prototype committed" --reason "Live ChatGPT tool-event integration is not yet implemented" --evidence-ref "commit SHA" --next-step "Add event hooks for supported tool actions"

# 4. Verify the ledger.
hap-worklog verify
```

Use `--log /path/to/events.jsonl` before the subcommand to select a different ledger.

## Real-time event visibility design

The ledger can be checked during work by invoking `hap-worklog verify` and reading the appended JSONL records. To let ChatGPT check events during a task, each supported action must emit a structured event to this recorder and the integration must expose the latest records to the assistant. This initial version has a manual CLI event interface only; automatic ChatGPT tool instrumentation and a live dashboard are not implemented. It deliberately does not claim to see hidden model reasoning.

## Safety and project gates

- No database writes.
- No remote mutation by this package.
- No deployment or activation of Phase 1.
- No automatic GitHub commit/push by the recorder.
- This is not a security sandbox and does not isolate the Python process.
- Do not record secrets, access tokens, or sensitive personal data in event summaries.
- Independent review remains `NOT_PERFORMED` unless evidence of a separate review is recorded.
