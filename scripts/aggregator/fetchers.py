"""
Data fetchers for Hacker News, GitHub Search, arXiv XML, and Reddit APIs.
"""

import sys
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import requests

from aggregator.utils import HEADERS, get_github_headers, extract_domain

def fetch_hn_stories(query, unix_cutoff, hits_per_page=12):
    """Fetch stories from Hacker News Algolia API matching query created after unix_cutoff."""
    url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story&numericFilters=created_at_i>{unix_cutoff}&hitsPerPage={hits_per_page}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            hits = []
            for item in data.get("hits", []):
                obj_id = item.get("objectID")
                title = item.get("title", "").strip()
                item_url = item.get("url") or f"https://news.ycombinator.com/item?id={obj_id}"
                points = item.get("points") or 0
                comments = item.get("num_comments") or 0
                domain = extract_domain(item_url) or "ycombinator.com"
                
                if title:
                    hits.append({
                        "id": f"hn_{obj_id}",
                        "title": title,
                        "url": item_url,
                        "points": points,
                        "comments": comments,
                        "domain": domain,
                        "type": "hn"
                    })
            return hits
    except Exception as e:
        print(f"[WARN] HN fetch error for query '{query}': {e}", file=sys.stderr)
    return []

def fetch_hn_infra_bundle(unix_cutoff):
    """Run four targeted single-keyword queries for Infra and merge/dedupe results."""
    queries = ["GPU", "inference", "Nvidia", "datacenter"]
    # "inference" and "datacenter" are ambiguous English words (statistical
    # inference, power-plant zoning fights) - require a corroborating AI
    # signal elsewhere in the title for those two. "GPU"/"Nvidia" are strong
    # enough signals on their own.
    weak_queries = {"inference", "datacenter"}
    all_hits = []
    seen_ids = set()

    # Negative filter keywords for Infra HN hits
    negative_kw = ["gaming", "geforce", "rtx 40", "rtx 50", "driver", "ps5", "xbox", "deal", "discount"]

    for q in queries:
        hits = fetch_hn_stories(q, unix_cutoff, hits_per_page=8)
        for h in hits:
            if h["id"] in seen_ids:
                continue
            title_lower = h["title"].lower()
            if any(neg in title_lower for neg in negative_kw):
                continue
            if q.lower() in weak_queries and not is_ai_relevant_text(title_lower):
                continue
            seen_ids.add(h["id"])
            all_hits.append(h)

    all_hits.sort(key=lambda x: x["points"], reverse=True)
    return all_hits[:8]

# --- GitHub trending discovery -------------------------------------------------

# Orgs whose repos are AI-relevant by definition, even when the repo name and
# description use no AI vocabulary at all (e.g. "DeepSeek Harness: Everything
# is a Plugin.").
AI_ORGS = {
    "deepseek-ai", "openai", "anthropics", "moonshotai", "qwenlm", "thudm",
    "google-deepmind", "mistralai", "meta-llama", "xai-org", "allenai",
    "huggingface", "stability-ai", "bytedance-seed", "zhipuai", "internlm",
    "vllm-project", "ggml-org", "unslothai", "sgl-project", "kvcache-ai",
    "langchain-ai", "run-llama", "crewai", "modelscope", "ai21labs",
    "cohere-ai", "nomic-ai", "baai-open", "openbmb",
}

# Whole-word tokens that mark a repo as AI-relevant. Matched against tokens of
# the repo name, description and topics, so "ai-agents" -> {"ai", "agents"}.
AI_TOKENS = {
    "ai", "llm", "llms", "slm", "vlm", "gpt", "genai", "nlp", "rag", "mcp",
    "agent", "agents", "agentic", "chatbot", "copilot", "assistant",
    "transformer", "transformers", "diffusion", "embedding", "embeddings",
    "multimodal", "inference", "finetune", "finetuning", "tokenizer",
    "prompt", "prompts", "prompting", "reasoning", "neural", "moe", "lora",
    "quantization", "quantized", "cuda", "gpu", "vllm", "sglang", "ocr",
    "tts", "asr", "claude", "chatgpt", "gemini", "llama", "qwen", "mistral",
    "deepseek", "kimi", "grok", "openai", "anthropic", "huggingface",
    "pytorch", "tensorflow", "onnx", "skill", "skills", "harness",
}

# Multi-word markers that survive tokenisation poorly.
AI_PHRASES = (
    "machine learning", "deep learning", "language model", "foundation model",
    "generative", "fine-tun", "text-to-", "-to-image", "open-weight",
    "frontier model", "world model",
)

def _tokenize(text):
    """Split text into lowercase word tokens, breaking hyphenated slugs apart."""
    return set(re.findall(r"[a-z0-9+#]+", (text or "").lower()))

def is_ai_relevant_text(text):
    """Heuristic AI-relevance check for a free-text title/description string.

    Used to drop keyword-search false positives - e.g. a single-word HN query
    like "inference" or "datacenter" also matches statistics papers and power
    -plant zoning fights that have nothing to do with AI.
    """
    haystack = (text or "").lower()
    if any(phrase in haystack for phrase in AI_PHRASES):
        return True
    return bool(_tokenize(haystack) & AI_TOKENS)

def is_ai_relevant(repo):
    """Heuristic AI-relevance check for repos found by non-keyword queries."""
    if (repo.get("owner") or "").lower() in AI_ORGS:
        return True

    haystack = " ".join([
        repo.get("full_name") or "",
        repo.get("description") or "",
        " ".join(repo.get("topics") or []),
    ])
    return is_ai_relevant_text(haystack)

def star_velocity(repo):
    """Stars gained per day since creation - our proxy for 'trending'."""
    stars = repo.get("stars", 0) or 0
    created = repo.get("created_at") or ""
    age_days = 30.0
    try:
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        age_days = (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
    except Exception:
        pass
    return stars / max(age_days, 1.0)

def fetch_github_repos(query, created_after_date, limit=8):
    """Fetch GitHub repositories created after specified date sorted by stars."""
    encoded_q = requests.utils.quote(f"{query} created:>{created_after_date}")
    url = f"https://api.github.com/search/repositories?q={encoded_q}&sort=stars&order=desc&per_page={limit}"
    try:
        res = requests.get(url, headers=get_github_headers(), timeout=10)
        if res.status_code == 200:
            items = res.json().get("items", [])
            repos = []
            for item in items:
                repos.append({
                    "id": f"gh_{item.get('id')}",
                    "title": item.get("full_name"),
                    "full_name": item.get("full_name"),
                    "url": item.get("html_url"),
                    "description": item.get("description") or "",
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language") or "",
                    "owner": (item.get("owner") or {}).get("login") or "",
                    "topics": item.get("topics") or [],
                    "created_at": item.get("created_at") or "",
                    "type": "github"
                })
            return repos
        else:
            print(f"[WARN] GitHub API status {res.status_code}: {res.text[:100]}", file=sys.stderr)
    except Exception as e:
        print(f"[WARN] GitHub fetch error: {e}", file=sys.stderr)
    return []

def fetch_github_trending(created_after_date, limit=8, breakout_min_stars=1500, min_stars=250):
    """Discover trending AI repos via complementary GitHub Search strategies.

    A single keyword query misses major releases whose name and description use
    no AI vocabulary (GitHub repo search covers name and description only - not
    topics, not README). So we union four query shapes and rank the merged set
    by star velocity rather than by absolute star count:

      1. keyword  - the classic 'LLM OR "AI agent" OR agentic' sweep
      2. topics   - topic: qualifiers cannot be OR'd, so one query per topic
      3. breakout - any repo over a star threshold, then AI-filtered locally

    Repos under `min_stars` are dropped outright - a handful of stars is not
    "trending", it is noise from a broad OR query.
    """
    strategies = [
        ('LLM OR "AI agent" OR agentic', False),
        ("topic:ai-agents", False),
        ("topic:llm", False),
        ("topic:generative-ai", False),
        (f"stars:>{breakout_min_stars}", True),
    ]

    merged = {}
    for query, needs_filter in strategies:
        for repo in fetch_github_repos(query, created_after_date, limit=15):
            key = (repo.get("full_name") or repo.get("url") or "").lower()
            if not key or key in merged:
                continue
            if (repo.get("stars") or 0) < min_stars:
                continue
            if needs_filter and not is_ai_relevant(repo):
                continue
            merged[key] = repo

    ranked = sorted(merged.values(), key=star_velocity, reverse=True)
    print(f"[INFO] GitHub trending: {len(merged)} unique repos merged, returning top {limit}")
    return ranked[:limit]

def fetch_arxiv_papers(limit=8):
    """Fetch recent papers from arXiv Atom XML feed for cs.AI, cs.LG, cs.CL."""
    url = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results={limit}"
    papers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title_elem = entry.find("atom:title", ns)
                id_elem = entry.find("atom:id", ns)
                published_elem = entry.find("atom:published", ns)
                
                if title_elem is not None and id_elem is not None:
                    raw_title = title_elem.text or ""
                    clean_title = re.sub(r"\s+", " ", raw_title).strip()
                    paper_url = id_elem.text.strip() if id_elem.text else ""
                    
                    pub_date_str = ""
                    if published_elem is not None and published_elem.text:
                        try:
                            dt = datetime.fromisoformat(published_elem.text.replace("Z", "+00:00"))
                            pub_date_str = dt.strftime("%b %d, %Y")
                        except Exception:
                            pub_date_str = published_elem.text[:10]
                            
                    papers.append({
                        "id": f"arxiv_{paper_url}",
                        "title": clean_title,
                        "url": paper_url,
                        "date": pub_date_str,
                        "type": "arxiv"
                    })
    except Exception as e:
        print(f"[WARN] arXiv fetch error (skipped silently): {e}", file=sys.stderr)
    return papers

def fetch_reddit_localllama():
    """Fetch top posts from r/LocalLLaMA."""
    url = "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=5"
    headers = {"User-Agent": "AI-News-Dashboard:v1.0 (by /u/kabyik)"}
    items = []
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            for post in data.get("data", {}).get("children", []):
                pdata = post.get("data", {})
                if not pdata.get("stickied"):
                    items.append({
                        "id": f"reddit_{pdata.get('id')}",
                        "title": pdata.get("title"),
                        "url": f"https://reddit.com{pdata.get('permalink')}",
                        "points": pdata.get("score", 0),
                        "comments": pdata.get("num_comments", 0),
                        "domain": "reddit.com/r/LocalLLaMA",
                        "type": "hn"
                    })
    except Exception as e:
        print(f"[WARN] Reddit fetch error (skipped silently): {e}", file=sys.stderr)
    return items
