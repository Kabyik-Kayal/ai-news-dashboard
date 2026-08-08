# ADR 0001: Cloud Migration from Desktop LLM Task to GitHub Actions Cron

- **Status**: Approved
- **Date**: 2026-08-08
- **Context**: Formerly, the AI News Dashboard relied on a scheduled Claude Code task running on a local desktop machine at 21:00 IST. If the desktop was powered off, sleeping, or disconnected from the internet, the nightly rebuild failed to fire. Additionally, executing an interactive LLM session for daily deterministic data gathering added unnecessary fragility.

## Decision

We migrate the automated nightly rebuild pipeline from a desktop-scheduled agent to a cloud-native **GitHub Actions Workflow** triggered via `cron` (`30 15 * * *` UTC = 21:00 IST) and `workflow_dispatch`.

## Consequences

### Positive
- **100% Availability**: The pipeline runs reliably in the cloud regardless of local desktop power state.
- **Zero Cost**: Utilizes GitHub Actions free tier for public repositories.
- **Automated Deployments**: Commits directly to `main` via `github-actions[bot]`, triggering GitHub Pages deployment within ~30 seconds.
- **Auditable Execution Logs**: Full build history and execution logs accessible in the repository's Actions tab.

### Negative
- Cloud network timeouts or GitHub API outages can affect scheduled runs (handled via graceful retry/failback).
