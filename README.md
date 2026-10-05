# Engineering workflows

Public-safe reusable CI infrastructure. Agent policy is maintained separately;
repository build and test gates remain authoritative.

## Sonar scan

Call `.github/workflows/sonar.yml` at an immutable reviewed commit after your
existing tests. Supply project-key, organization, the exact-run coverage artifact
name (when available), and an explicitly selected `SONAR_TOKEN` secret. Never use
`secrets: inherit`. Caller coverage downloads to `.sonar-coverage/`; configure
repo-owned `sonar-project.properties` to reference those paths. Coverage must be
produced from the same commit as the scanner: set the coverage checkout ref to
`${{ github.event.pull_request.head.sha || github.sha }}`. Existing integration
tests can continue testing GitHub's merge candidate separately.

```yaml
sonar:
  permissions:
    contents: read
  needs: coverage
  if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository
  uses: Midtown-Technology-Group/engineering-workflows/.github/workflows/sonar.yml@REVIEWED_COMMIT_SHA
  with:
    project-key: YOUR_VERIFIED_KEY
    organization: YOUR_ORGANIZATION
    coverage-artifact: sonar-coverage
  secrets:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Python: generate coverage XML and configure `sonar.python.coverage.reportPaths`.
JavaScript/TypeScript: generate LCOV and configure `sonar.javascript.lcov.reportPaths`.
Go: generate coverprofile and configure `sonar.go.coverage.reportPaths`.
Test commands and source/test exclusions belong to each repository. Specialized
compiled-language scanners remain repo-specific; do not force them into this CLI.

Stage CI/config and prove reports before disabling automatic analysis. Enable only
one scan mode; verify the first CI scan's revision and imported coverage. Start
new-code gates without masking the existing backlog. A missing receipt or pending
provider result is unavailable evidence, never a clean scan. Fork PRs are kept
secret-free; this workflow does not use pull_request_target or execute caller shell.

The scanner waits at most five minutes for the quality gate and preserves its CE
task receipt even on failure. Agent feedback uses the completed analysis identity.
Coverage is not fabricated when a repository has no tests or supported source.
