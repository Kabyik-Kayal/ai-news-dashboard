#!/usr/bin/env python3
"""
CLI Runner for Rebuilding the AI News Dashboard.
Orchestrates pipeline execution via the modular aggregator package.
"""

import os
import sys
import time

# Ensure scripts directory is in sys.path for clean imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aggregator.pipeline import run_pipeline
from aggregator.renderer import generate_dashboard_html

def main():
    start_time = time.time()
    
    # 1. Execute ingestion & deduplication pipeline
    data = run_pipeline()
    
    # 2. Render self-contained HTML dashboard
    html_output = generate_dashboard_html(data)
    
    # 3. Determine target file path (root index.html)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    target_path = os.path.join(project_root, "index.html")
    
    # 4. Save output or print dry run preview
    if os.getenv("DRY_RUN"):
        print("[INFO] DRY_RUN enabled. Generated HTML preview:")
        print(html_output[:500] + "\n...\n" + html_output[-300:])
    else:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"[SUCCESS] Rebuilt index.html in {time.time() - start_time:.2f}s -> {target_path}")

if __name__ == "__main__":
    main()
