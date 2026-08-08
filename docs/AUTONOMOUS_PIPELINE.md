# Operations Guide: Autonomous AI News Pipeline

This guide outlines how to operate, test, troubleshoot, and maintain the autonomous AI News Platform pipeline.

---

## Operations Overview

The pipeline runs fully autonomously on **GitHub Actions**.

- **Scheduled Trigger**: Runs automatically every night at **21:00 IST (15:30 UTC)**.
- **Manual Trigger**: Can be manually launched anytime via GitHub Actions `workflow_dispatch`.
- **Target Repository**: `Kabyik-Kayal/ai-news-dashboard` (`main` branch).
- **Production Site**: [news.kabyik.dev](https://news.kabyik.dev) (served via GitHub Pages).

---

## Repository Structure

```
Kabyik-Kayal/ai-news-dashboard/
├── .github/
│   └── workflows/
│       └── nightly-build.yml           # Autonomous GitHub Actions pipeline
├── docs/
│   ├── ARCHITECTURE.md                 # System architecture & data flow
│   ├── AUTONOMOUS_PIPELINE.md          # Operations guide (this document)
│   └── adr/                            # Architectural Decision Records
│       ├── 0001-github-actions-cloud-cron.md
│       ├── 0002-python-deterministic-fetcher.md
│       ├── 0003-rss-and-api-multi-source-harvesting.md
│       └── 0004-zero-dependency-html-rendering.md
├── scripts/
│   ├── rebuild_dashboard.py            # CLI entry point runner
│   ├── requirements.txt                # Python dependencies
│   └── aggregator/                     # Modular ingestion & rendering package
│       ├── __init__.py
│       ├── utils.py                    # Constants, headers, domain helpers
│       ├── fetchers.py                 # HN, GitHub, arXiv, and Reddit fetchers
│       ├── pipeline.py                 # Deduplication & taxonomy orchestrator
│       └── renderer.py                 # HTML dashboard generator
├── index.html                          # Auto-generated static HTML dashboard
├── CNAME                               # GitHub Pages custom domain configuration
├── README.md                           # Project documentation
└── .gitignore                          # Workspace ignore rules
```

---

## Local Development & Testing

You can run the ingestion pipeline locally on your machine at any time without waiting for GitHub Actions.

### 1. Prerequisites
- Python 3.10+
- Internet connection (access to Hacker News Algolia, GitHub API, arXiv)

### 2. Install Dependencies
```bash
cd "M:/Git-Hub Projects/news"
pip install -r scripts/requirements.txt
```

### 3. Run Ingestion Engine
```bash
python scripts/rebuild_dashboard.py
```

Optional environment variables:
- `GITHUB_TOKEN`: (Optional) GitHub Personal Access Token to avoid GitHub API rate limits (unauthenticated limits are 60 requests/hr; authenticated limits are 5,000/hr).
- `DRY_RUN`: Set `DRY_RUN=1` to print output summary to stdout without overwriting `index.html`.

---

## GitHub Actions Configuration

The workflow file `.github/workflows/nightly-build.yml` controls the automated build:

```yaml
name: Nightly AI News Dashboard Rebuild

on:
  schedule:
    # 15:30 UTC = 21:00 IST daily
    - cron: '30 15 * * *'
  workflow_dispatch:

jobs:
  rebuild-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r scripts/requirements.txt

      - name: Run Dashboard Generator Engine
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/rebuild_dashboard.py

      - name: Commit and Push Changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Nightly rebuild: AI releases dashboard"
          file_pattern: "index.html"
          commit_author: "github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>"
```

---

## Troubleshooting & Maintenance

### Scenario 1: GitHub API Rate Limiting
- **Symptom**: Open-source column missing or partial results.
- **Cause**: Unauthenticated API calls hit rate limit.
- **Resolution**: Ensure `GITHUB_TOKEN` is passed to the script step in `nightly-build.yml` (automatically provided by GitHub Actions).

### Scenario 2: Source API Intermittent Failure (e.g. arXiv / Reddit / RSS)
- **Symptom**: Network timeout log for arXiv or Reddit.
- **Handling**: The engine treats third-party sources as optional backstops. Failure of Reddit or arXiv will log a warning and fallback gracefully without failing the workflow build.

### Scenario 3: Diverged Git Commits
- **Symptom**: GitHub Actions fails to push commit.
- **Handling**: `stefanzweifel/git-auto-commit-action` handles rebase automatically before pushing.
