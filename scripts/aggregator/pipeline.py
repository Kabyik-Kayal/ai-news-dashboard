"""
Pipeline orchestrator for harvesting, deduplicating, and categorizing AI news items.
"""

from datetime import datetime, timedelta, timezone

from aggregator.utils import IST
from aggregator.fetchers import (
    fetch_hn_stories,
    fetch_hn_infra_bundle,
    fetch_github_repos,
    fetch_arxiv_papers,
    fetch_reddit_localllama
)

def run_pipeline():
    """Execute ingestion pipeline across all sources, deduplicate, and return domain columns."""
    now_utc = datetime.now(timezone.utc)
    unix_cutoff = int((now_utc - timedelta(days=2)).timestamp())
    today_minus_30 = (now_utc - timedelta(days=30)).strftime("%Y-%m-%d")
    
    print(f"[INFO] Pipeline starting. Unix cutoff: {unix_cutoff}, GH created_after: {today_minus_30}")

    # 1. Fetch Agents
    hn_agents = fetch_hn_stories("AI+agent", unix_cutoff, hits_per_page=8)
    
    # 2. Fetch Applied AI
    hn_applied = fetch_hn_stories("AI", unix_cutoff, hits_per_page=12)

    # 3. Fetch Infra
    hn_infra = fetch_hn_infra_bundle(unix_cutoff)

    # 4. Fetch GitHub Open-source
    gh_opensource = fetch_github_repos('LLM OR "AI agent" OR agentic', today_minus_30, limit=8)
    
    # 5. Fetch GitHub Infra Backstop
    gh_infra_backstop = fetch_github_repos('inference OR CUDA OR vLLM OR GPU', today_minus_30, limit=8)

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

    # --- AGENTS COLUMN ---
    arxiv_agents = []
    arxiv_infra = []
    for paper in arxiv_papers:
        title_lower = paper["title"].lower()
        if any(k in title_lower for k in ["agent", "tool", "reason", "multi-agent", "governance", "persona"]):
            arxiv_agents.append(paper)
        else:
            arxiv_infra.append(paper)

    agents_column = dedupe_items(hn_agents + arxiv_agents)[:7]

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
        
    infra_raw = hn_infra + gh_infra_items + arxiv_infra
    infra_column = dedupe_items(infra_raw)[:7]

    # --- APPLIED AI COLUMN ---
    applied_column = dedupe_items(hn_applied + reddit_items)[:7]

    # --- OPEN SOURCE COLUMN ---
    opensource_column = dedupe_items(gh_opensource)[:7]

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
