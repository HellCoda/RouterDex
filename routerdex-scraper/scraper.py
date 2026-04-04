#!/usr/bin/env python3
"""
OpenRouter Rankings Scraper
Scrapes https://openrouter.ai/rankings and outputs leaderboard.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from urllib.parse import unquote

SCRAPER_VERSION = "1.5"
TARGET_URL = "https://openrouter.ai/rankings"
MAX_MODELS = 20


def parse_tokens(token_str: str) -> int:
    """Convert '1.59T' -> 1590000000000, '803B' -> 803000000000"""
    if not token_str:
        return 0
    # Normalize: replace comma with dot for decimal
    token_str = token_str.strip().replace(",", ".")
    multipliers = {"T": 1e12, "B": 1e9, "M": 1e6, "K": 1e3}
    for suffix, mult in multipliers.items():
        if token_str.upper().endswith(suffix):
            try:
                return int(float(token_str[:-1]) * mult)
            except ValueError:
                return 0
    try:
        return int(float(token_str))
    except ValueError:
        return 0


def scrape_with_playwright() -> str:
    """Use Playwright to render the page and return HTML."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("✗ Playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("⏳ Loading page...")
        page.goto(TARGET_URL, wait_until="networkidle", timeout=60000)
        
        # Click "Show more" to load more models
        for _ in range(2):
            try:
                show_more = page.locator("text=Show more").first
                if show_more.is_visible(timeout=2000):
                    show_more.click()
                    page.wait_for_timeout(1000)
            except:
                break
        
        page.wait_for_timeout(1000)
        html = page.content()
        browser.close()
        
    return html


def parse_html(html: str) -> tuple[list[dict], list[dict]]:
    """Parse the HTML to extract models and apps."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, "html.parser")
    models = []
    apps = []
    
    # === PARSE MODELS ===
    model_links = soup.find_all("a", href=re.compile(r"^/[a-z0-9-]+/[a-z0-9-]+", re.IGNORECASE))
    
    seen_models = set()
    
    for link in model_links:
        href = link.get("href", "")
        
        # Skip non-model links
        if href.startswith("/apps") or href.startswith("/docs"):
            continue
        if href in ["/models", "/chat", "/rankings", "/enterprise", "/pricing", "/", "/about", "/terms", "/privacy"]:
            continue
        
        # Extract model_id
        model_id = href.strip("/")
        parts = model_id.split("/")
        
        if len(parts) != 2 or not parts[1]:
            continue
        
        if model_id in seen_models:
            continue
        
        # Find the row container
        container = link
        row_text = ""
        container_html = ""
        
        for _ in range(10):
            parent = container.parent
            if parent is None:
                break
            
            parent_text = parent.get_text(" ", strip=True)
            
            if "tokens" in parent_text.lower() and len(parent_text) < 500:
                row_text = parent_text
                container_html = str(parent)
                break
            
            model_links_in_parent = parent.find_all("a", href=re.compile(r"^/[a-z0-9-]+/[a-z0-9-]+"))
            if len(model_links_in_parent) > 3:
                break
            
            container = parent
        
        if not row_text or "tokens" not in row_text.lower():
            continue
        
        seen_models.add(model_id)
        
        if len(seen_models) > MAX_MODELS:
            break
        
        name = link.get_text(strip=True)
        provider = parts[0]
        
        # Parse tokens - support both dot and comma as decimal separator
        token_match = re.search(r"(\d+(?:[,\.]\d+)?)\s*([TBMK])\s*tokens?", row_text, re.IGNORECASE)
        if token_match:
            num = token_match.group(1).replace(",", ".")
            tokens = f"{num}{token_match.group(2).upper()}"
        else:
            tokens = "0"
        
        # Parse percentage
        pct_match = re.search(r"(\d+)\s*%", row_text)
        change_pct = int(pct_match.group(1)) if pct_match else 0
        
        # Detect direction: green = up, red = down
        # Check for text-green-9 (increase) or text-red-9 (decrease)
        if "text-green-9" in container_html:
            change_direction = "up"
        elif "text-red-9" in container_html:
            change_direction = "down"
        else:
            change_direction = "none"
        
        models.append({
            "rank": len(models) + 1,
            "model_id": model_id,
            "name": name,
            "provider": provider,
            "tokens": tokens,
            "tokens_raw": parse_tokens(tokens),
            "change_pct": change_pct,
            "change_direction": change_direction
        })
    
    # === PARSE APPS ===
    app_links = soup.find_all("a", href=re.compile(r"^/apps\?url="))
    
    seen_apps = set()
    
    for link in app_links:
        href = link.get("href", "")
        url_match = re.search(r"url=([^&]+)", href)
        if not url_match:
            continue
        
        app_url = unquote(url_match.group(1))
        
        if app_url in seen_apps:
            continue
        seen_apps.add(app_url)
        
        name = link.get_text(strip=True)
        
        # Find row container - go up to grid row
        container = link
        row_text = ""
        
        for _ in range(10):
            parent = container.parent
            if parent is None:
                break
            
            parent_text = parent.get_text(" ", strip=True)
            parent_classes = parent.get("class", [])
            
            # Stop at grid row level
            if "grid" in parent_classes and "grid-cols-12" in parent_classes:
                row_text = parent_text
                break
            
            if "tokens" in parent_text.lower() and len(parent_text) < 500:
                row_text = parent_text
                break
            
            app_links_in_parent = parent.find_all("a", href=re.compile(r"^/apps\?url="))
            if len(app_links_in_parent) > 3:
                break
            
            container = parent
        
        # Parse tokens - support comma as decimal (e.g., "93,1B")
        token_match = re.search(r"(\d+(?:[,\.]\d+)?)\s*([TBMK])", row_text, re.IGNORECASE)
        if token_match:
            num = token_match.group(1).replace(",", ".")
            tokens = f"{num}{token_match.group(2).upper()}"
        else:
            tokens = "0"
        
        # Parse description from the span with class containing "truncate cursor-help"
        description = ""
        row_container = container
        desc_span = row_container.find("span", class_=lambda c: c and "truncate" in c and "cursor-help" in c)
        if desc_span:
            description = desc_span.get_text(strip=True)
        else:
            # Fallback: extract text between name and token number
            if name in row_text:
                name_idx = row_text.find(name)
                if name_idx != -1:
                    after_name = row_text[name_idx + len(name):]
                    if token_match:
                        token_num = token_match.group(1)
                        token_idx = after_name.find(token_num)
                        if token_idx > 0:
                            description = after_name[:token_idx].strip()
                            description = re.sub(r"[\d,.\s]+$", "", description).strip()
                            description = re.sub(r"^\s*\d+\.\s*", "", description)
                            description = re.sub(r"\s+", " ", description).strip()
                            if len(description) < 5 or len(description) > 150:
                                description = ""
        
        apps.append({
            "rank": len(apps) + 1,
            "name": name,
            "url": app_url,
            "description": description,
            "tokens": tokens,
            "tokens_raw": parse_tokens(tokens)
        })
    
    return models, apps


def main():
    parser = argparse.ArgumentParser(description="Scrape OpenRouter rankings")
    parser.add_argument("-o", "--output", default="leaderboard.json", help="Output file path")
    parser.add_argument("--debug", action="store_true", help="Save HTML for debugging")
    args = parser.parse_args()
    
    print(f"🔍 Scraping {TARGET_URL}...")
    
    html = scrape_with_playwright()
    
    if args.debug:
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("📄 Saved debug.html")
    
    models, apps = parse_html(html)
    
    # Build output
    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": TARGET_URL,
        "scraper_version": SCRAPER_VERSION,
        "top_models": models,
        "top_apps": apps,
        "market_share": [],
        "categories": []
    }
    
    # Write JSON
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Scraped {len(models)} models, {len(apps)} apps.")
    print(f"✓ Saved to {args.output}")
    
    if len(models) == 0:
        print("⚠ Warning: No models found. Run with --debug to inspect HTML.")


if __name__ == "__main__":
    main()
