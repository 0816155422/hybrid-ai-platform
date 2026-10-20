# Execution Evidence

Store non-sensitive, reproducible execution reports here. Keep one file per execution or review event and link it from the artifact register or checkpoint.

## Minimum record

- Event ID and project ID
- Phase, step, and check IDs
- Start/end timestamp in UTC, when available
- Tool/action, version, and environment
- Exact command or action with secrets removed
- Expected result and observed result
- Exit code/status and relevant output/log references
- Input and output artifact IDs, with SHA-256 when bytes are available
- Independent review status and reviewer evidence
- If incomplete: blocker, reason, root cause (confirmed or suspected), impact, unblock method, completion condition, and next step

## Evidence discipline

A test is `PASS` only when it was actually executed and met its acceptance criteria. A workflow definition is not a workflow result. A test suite that times out is not a passing test. Historical claims must be labelled as historical until independently reproduced.

Do not store secrets, tokens, passwords, private user data, or raw conversation exports while repository privacy is unverified.
