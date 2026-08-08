# ADR 0002: Autonomous Python Ingestion & Execution Engine

- **Status**: Approved
- **Date**: 2026-08-08
- **Context**: Relying on generic LLM prompts to perform HTTP fetching, string parsing, and HTML synthesis led to non-deterministic execution, risk of invented headlines, formatting drift, and dependency on LLM tokens/quota.

## Decision

We implement a dedicated, lightweight Python 3 execution engine (`scripts/rebuild_dashboard.py`) responsible for data ingestion, deduplication, taxonomy mapping, ranking, and HTML template generation.

## Consequences

### Positive
- **Strict Data Integrity**: Only real data returned by public APIs is rendered; eliminating hallucinations or invented headlines.
- **Fast Execution**: Completes in under 5 seconds (compared to 60+ seconds for LLM agent loops).
- **Zero API Cost**: Does not consume LLM token quotas.
- **Strict Visual Standards**: Renders exact HTML/CSS structure every night without layout drift.

### Negative
- Require maintaining a standalone Python script (~250-350 lines).
