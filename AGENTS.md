# Shared workflow guidance

Keep this repository public-safe: no private skill content, vault identifiers,
customer information or credentials. Pin third-party actions and caller workflow
refs to immutable commits. Keep permissions read-only and fork PRs secret-free.
Validate workflow YAML and security invariants with `python -m unittest discover
-s tests`; validate runtime changes with a real caller run before claiming proof.

## Secret gate before publication

Before publishing the current PR branch, commit the complete candidate and run
`python3 scripts/secret_gate.py` (native Windows: `python`). Require exit 0;
missing tooling/authentication, scan errors and skipped scans block publication.
Then run the existing repository gates. Repeat after changing outgoing commits.
Push exactly the scanned HEAD. This PR scan covers the current branch against its
fetched intended base; other refs, multi-ref pushes and rewritten history require
`--pre-push` with Git's complete ref-update stream. Stop if any pushed ref is
uncovered. See [secret scanning](SECRET-SCANNING.md) for base selection, new branches,
pre-push input and prerequisites. Preserve GitGuardian App, CI and Gitleaks checks.
