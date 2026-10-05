# Shared workflow guidance

Keep this repository public-safe: no private skill content, vault identifiers,
customer information or credentials. Pin third-party actions and caller workflow
refs to immutable commits. Keep permissions read-only and fork PRs secret-free.
Validate workflow YAML and security invariants with `python -m unittest discover
-s tests`; validate runtime changes with a real caller run before claiming proof.
