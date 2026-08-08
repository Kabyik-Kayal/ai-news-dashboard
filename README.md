# AI News Dashboard

An automated, cloud-native daily news aggregator and dashboard covering developments in **Agents**, **Infra**, **Applied AI**, and **Open-source**.

Live Dashboard: [news.kabyik.dev](https://news.kabyik.dev)

---

## 🚀 Fully Autonomous Architecture

The dashboard is built, updated, and deployed automatically every night at **21:00 IST (15:30 UTC)** via a **GitHub Actions Cron Workflow** running a deterministic Python ingestion engine.

- **Zero Desktop Dependency**: Operates 100% in the cloud without requiring a local machine or interactive LLM sessions.
- **Multi-Source Ingestion**: Ingests data from Hacker News (Algolia API), GitHub Trending (Search API), arXiv Atom XML, and RSS feeds.
- **Zero-Dependency Web Output**: Renders a self-contained, light-mode HTML dashboard (`index.html`) with inline CSS.
- **Instant GitHub Pages Deployment**: Automatically commits updated snapshots to `main`, triggering GitHub Pages deployment within ~30 seconds.

---

## 📚 Documentation & Architecture Decision Records (ADRs)

- [Architecture Overview](docs/ARCHITECTURE.md) — High-level architecture, domain taxonomy, data pipeline mechanics, and visual standards.
- [Operations Guide](docs/AUTONOMOUS_PIPELINE.md) — Local testing, environment setup, troubleshooting, and GitHub Actions workflow configuration.
- [ADR 0001: Cloud Migration from Desktop LLM to GitHub Actions](docs/adr/0001-github-actions-cloud-cron.md)
- [ADR 0002: Autonomous Python Ingestion & Execution Engine](docs/adr/0002-python-deterministic-fetcher.md)
- [ADR 0003: Multi-Source Query & Deduplication Strategy](docs/adr/0003-rss-and-api-multi-source-harvesting.md)
- [ADR 0004: Self-Contained Zero-Dependency HTML Dashboard](docs/adr/0004-zero-dependency-html-rendering.md)

---

## 🛠️ Local Development & Testing

To test the ingestion pipeline locally:

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run rebuild script
python scripts/rebuild_dashboard.py
```
