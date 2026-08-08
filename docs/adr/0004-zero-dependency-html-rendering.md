# ADR 0004: Self-Contained Zero-Dependency HTML Dashboard

- **Status**: Approved
- **Date**: 2026-08-08
- **Context**: Relying on external CSS frameworks (Tailwind CDN, Bootstrap) or web font providers introduces external latency, potential CDN downtime, and render-blocking resources for a simple news dashboard.

## Decision

The rendered dashboard (`index.html`) remains 100% self-contained:
- Inline CSS styling only.
- System sans-serif font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`).
- CSS Grid for 4-column responsive layout (4 cols on desktop, 2 on tablet, 1 on mobile).
- Strict visual tokens & Dark Mode: CSS Custom Properties (`:root` light mode / `[data-theme="dark"]` dark mode) with automatic OS preference detection (`prefers-color-scheme`) and interactive toggle persistence (`localStorage`).
- Domain header accents: Agents (`#4f46e5` / `#818cf8`), Infra (`#0891b2` / `#22d3ee`), Applied AI (`#059669` / `#34d399`), Open-source (`#d97706` / `#fbbf24`).

## Consequences

### Positive
- Sub-millisecond rendering time and lightweight file size (~8-10 KB).
- Zero external point of failure.
- Perfect mobile responsiveness and high accessibility.
