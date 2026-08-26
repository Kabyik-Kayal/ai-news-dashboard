"""
Pipeline orchestrator for harvesting, deduplicating, categorizing, and quality-
gating AI news items.
"""

from datetime import datetime, timedelta, timezone

from aggregator.utils import IST
from aggregator.fetchers import (
    fetch_hn_stories,
    fetch_hn_infra_bundle,
    fetch_github_repos,
    fetch_github_trending,
    star_velocity,
    is_ai_relevant_text,
    fetch_arxiv_papers,
    fetch_reddit_localllama
)

# --- Content-based categorization -------------------------------------------
# Which HN/Reddit query originally surfaced an item is a weak signal - a
# broad "AI" search returns plenty of stories that actually read as Infra or
# Agents news, and vice versa. So every item is reclassified from its own
# title text instead of trusting the source query, and anything that reads
# as neither Agents nor Infra falls through to Applied AI (the general bucket).


# Each inner list is synonyms for ONE concept - "agent"/"agents"/"agentic"
# must count as a single hit, not three, since "agentic" contains "agent" as
# a substring and would otherwise dominate the score on its own.
AGENT_CONCEPTS = [
    ["agent", "agents", "agentic"],
    ["multi-agent"],
    ["autonomous"],
    ["orchestrat"],
    ["tool-use", "tool use", "tool-calling", "tool calling"],
    ["copilot"],
    ["coding agent"],
    ["browser agent"],
    ["workflow automation"],
    ["planner"],
    ["task automation"],
]

INFRA_CONCEPTS = [
    ["gpu", "gpus"],
    ["nvidia"],
    ["amd"],
    ["chip", "chips"],
    ["cuda"],
    ["tpu"],
    ["asic"],
    ["datacenter", "data center"],
    ["cluster"],
    ["silicon"],
    ["semiconductor"],
    ["accelerator"],
    ["supercomputer"],
    ["training run"],
    ["compute cluster"],
    ["power plant", "power grid", "megawatt"],
    ["interconnect"],
    ["fab ", "foundry"],
    ["h100", "h200", "b200"],
    ["liquid cooling"],
    ["hardware"],
]

# Minimum engagement for an HN/Reddit item to be considered "worth showing" -
# filters out near-dead posts that a broad keyword query happened to match.
MIN_POINTS = 3
MIN_COMMENTS = 2


def _concept_score(text_lower, concept_groups):
    """Count distinct concepts matched (each group of synonyms counts once)."""
    return sum(1 for group in concept_groups if any(kw in text_lower for kw in group))


def classify_topic(title):
    """Classify a title as 'agents', 'infra', or 'applied' by keyword signal."""
    t = title.lower()
    agent_score = _concept_score(t, AGENT_CONCEPTS)
    infra_score = _concept_score(t, INFRA_CONCEPTS)

    if agent_score == 0 and infra_score == 0:
        return "applied"
    # On a tie, prefer Infra: a hardware/chip story that merely name-drops
    # "agentic AI" as a marketing use-case (e.g. "New GPU ... for Agentic AI")
    # is still fundamentally infra news, not agents news.
    if agent_score > infra_score:
        return "agents"
    return "infra"


def is_worth_showing(item):
    """Quality gate: drop near-zero-engagement HN/Reddit noise."""
    if item.get("type") != "hn":
        return True
    points = item.get("points", 0) or 0
    comments = item.get("comments", 0) or 0
    return points >= MIN_POINTS or comments >= MIN_COMMENTS


def run_pipeline():
    """Execute ingestion pipeline across all sources, deduplicate, and return domain columns."""
    now_utc = datetime.now(timezone.utc)
    unix_cutoff = int((now_utc - timedelta(days=2)).timestamp())
    today_minus_30 = (now_utc - timedelta(days=30)).strftime("%Y-%m-%d")
    # Trending discovery uses a wider window; ranking is by star velocity, so
    # older-but-quieter repos sink on their own instead of being cut off hard.
    today_minus_45 = (now_utc - timedelta(days=45)).strftime("%Y-%m-%d")

    print(f"[INFO] Pipeline starting. Unix cutoff: {unix_cutoff}, GH created_after: {today_minus_30}")

    # 1. Fetch Agents
    hn_agents = fetch_hn_stories("AI+agent", unix_cutoff, hits_per_page=8)

    # 2. Fetch Applied AI
    hn_applied = fetch_hn_stories("AI", unix_cutoff, hits_per_page=12)

    # 3. Fetch Infra
    hn_infra = fetch_hn_infra_bundle(unix_cutoff)

    # 4. Fetch GitHub Open-source (multi-strategy trending discovery)
    gh_opensource = fetch_github_trending(today_minus_45, limit=10)

    # 5. Fetch GitHub Infra Backstop
    gh_infra_backstop = fetch_github_repos('inference OR CUDA OR vLLM OR GPU', today_minus_30, limit=8)
    gh_infra_backstop = [r for r in gh_infra_backstop if (r.get("stars") or 0) >= 150]
    gh_infra_backstop.sort(key=star_velocity, reverse=True)

    # 6. Fetch arXiv
    arxiv_papers = fetch_arxiv_papers(limit=8)

    # 7. Fetch Reddit
    reddit_items = fetch_reddit_localllama()

    # Deduplication across sources by canonical URL
    seen_urls = set()

    def dedupe_items(item_list):
        result = []
        for item in item_list:
            url = item.get("url", "").lower().rstrip("/")
            if url and url not in seen_urls:
                seen_urls.add(url)
                result.append(item)
        return result

    # --- Merge every HN/Reddit-sourced item into one pool, then apply
    # relevance filtering, quality gating, and content-based reclassification
    # in one pass so a story lands in the column it actually reads as.
    hn_pool = hn_agents + hn_infra + hn_applied + reddit_items
    seen_pool_ids = set()

    agents_hn, infra_hn, applied_hn = [], [], []
    for item in hn_pool:
        item_id = item.get("id")
        if item_id in seen_pool_ids:
            continue
        seen_pool_ids.add(item_id)

        if not is_ai_relevant_text(item.get("title", "")):
            continue
        if not is_worth_showing(item):
            continue

        bucket = classify_topic(item.get("title", ""))
        if bucket == "agents":
            agents_hn.append(item)
        elif bucket == "infra":
            infra_hn.append(item)
        else:
            applied_hn.append(item)

    # Rank each reclassified bucket by engagement - merging four source lists
    # loses their individual points-sorted order.
    agents_hn.sort(key=lambda x: x.get("points", 0), reverse=True)
    infra_hn.sort(key=lambda x: x.get("points", 0), reverse=True)
    applied_hn.sort(key=lambda x: x.get("points", 0), reverse=True)

    # --- AGENTS COLUMN ---
    arxiv_agents = []
    arxiv_infra = []
    for paper in arxiv_papers:
        title_lower = paper["title"].lower()
        if any(k in title_lower for k in ["agent", "tool", "reason", "multi-agent", "governance", "persona"]):
            arxiv_agents.append(paper)
        else:
            arxiv_infra.append(paper)

    agents_column = dedupe_items(agents_hn + arxiv_agents)[:7]

    # --- OPEN SOURCE COLUMN ---
    # Deduped first so the trending picks are not consumed by the infra backstop.
    opensource_column = dedupe_items(gh_opensource)[:7]

    # --- INFRA COLUMN ---
    gh_infra_items = []
    for repo in gh_infra_backstop:
        gh_infra_items.append({
            "id": repo["id"],
            "title": repo["full_name"],
            "url": repo["url"],
            "stars": repo["stars"],
            "language": repo["language"],
            "description": repo["description"],
            "type": "github"
        })

    infra_raw = infra_hn + gh_infra_items + arxiv_infra
    infra_column = dedupe_items(infra_raw)[:7]

    # --- APPLIED AI COLUMN ---
    applied_column = dedupe_items(applied_hn)[:7]

    # Snapshot IST Timestamp
    now_ist = datetime.now(IST)
    snapshot_str = now_ist.strftime("%Y-%m-%d %H:%M IST")

    return {
        "snapshot": snapshot_str,
        "agents": agents_column,
        "infra": infra_column,
        "applied": applied_column,
        "opensource": opensource_column
    }
