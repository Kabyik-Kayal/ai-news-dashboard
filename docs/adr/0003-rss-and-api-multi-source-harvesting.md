# ADR 0003: Multi-Source Query & Deduplication Strategy

- **Status**: Approved
- **Date**: 2026-08-08
- **Context**: In single-query ingestion setups, specific niche categories (such as AI Infrastructure) frequently return 0 items when Hacker News has a slow day for GPU/inference discussions. Furthermore, cross-source ingestion (HN + GitHub + arXiv + RSS) can produce duplicate records.

## Decision

We adopt a multi-query, multi-source ingestion pipeline:
1. **Hacker News Algolia API**: Execute single-keyword searches for `GPU`, `inference`, `Nvidia`, `datacenter`, `AI+agent`, and `AI`. Merge candidate lists and deduplicate by `objectID`.
2. **GitHub Search API**: Query trending repos created in the last 30 days matching `LLM OR "AI agent" OR agentic` and a secondary backstop query for `inference OR CUDA OR vLLM OR GPU`.
3. **arXiv Atom Feed**: Query recent papers from `cs.AI`, `cs.LG`, and `cs.CL`.
4. **Vendor RSS Feeds**: Direct ingestion of primary AI research blogs (OpenAI, Anthropic, Google AI).
5. **Cross-Source Canonical Deduplication**: Normalize canonical URLs to prevent the same article appearing under multiple sections.

## Consequences

### Positive
- High signal coverage even during quiet news cycles.
- Eliminates 0-hit sections in the Infra bundle.
- Guarantees clean, non-duplicated output.
