# OpenRouter Rankings Scraper — Spec for Opus

## Objective

Build a Python script (`scraper.py`) that scrapes the OpenRouter rankings page (`https://openrouter.ai/rankings`) and outputs a clean, structured JSON file (`leaderboard.json`).

This JSON will be pushed manually to a GitHub repo and consumed by the RouterDex desktop app to display a "Leaderboard" panel.

---

## Target URL

```
https://openrouter.ai/rankings
```

The page is server-side rendered (SSR) but some data may be loaded via JavaScript (Next.js app). If `requests` + `BeautifulSoup` doesn't capture all the data, use `playwright` or `selenium` as fallback to render the page fully before scraping.

---

## Data to Extract

### 1. Top Models (section "LLM Leaderboard" / "Top Models")

For each model in the ranking list:

| Field | Example | Source |
|-------|---------|--------|
| `rank` | `1` | Position in the list |
| `model_id` | `minimax/minimax-m2.5-20260211` | From the `<a href="/minimax/minimax-m2.5-20260211">` link |
| `name` | `Minimax M2.5` | Display name text |
| `provider` | `minimax` | First part of model_id before `/` |
| `tokens` | `1.59T` | Token usage string (keep as-is: "1.59T", "803B", etc.) |
| `tokens_raw` | `1590000000000` | Parsed to raw number for sorting (T=1e12, B=1e9, M=1e6) |
| `change_pct` | `24` | The percentage value shown (weekly change). `0` if none. Negative if decrease. |

**Goal**: Extract ALL models shown on the page (not just top 10 — click "Show more" if needed or find the full dataset).

### 2. Top Apps (section "Top Apps")

For each app:

| Field | Example | Source |
|-------|---------|--------|
| `rank` | `1` | Position |
| `name` | `OpenClaw` | App name |
| `url` | `https://openclaw.ai/` | App URL |
| `description` | `The AI that actually does things` | Tagline |
| `tokens` | `360B` | Token usage |
| `tokens_raw` | `360000000000` | Parsed number |

### 3. Market Share by Provider (section "Market Share")

If accessible, extract provider market share data:

| Field | Example |
|-------|---------|
| `provider` | `google` |
| `share_pct` | `28.5` |

### 4. Category Rankings (section "Categories")

If accessible, extract category data showing which models dominate per use-case.

---

## Output Format

Generate a single file `leaderboard.json`:

```json
{
  "updated": "2026-03-10T14:30:00Z",
  "source": "https://openrouter.ai/rankings",
  "scraper_version": "1.0",
  "top_models": [
    {
      "rank": 1,
      "model_id": "minimax/minimax-m2.5-20260211",
      "name": "Minimax M2.5",
      "provider": "minimax",
      "tokens": "1.59T",
      "tokens_raw": 1590000000000,
      "change_pct": 24
    },
    {
      "rank": 2,
      "model_id": "google/gemini-3-flash-preview-20251217",
      "name": "Gemini 3 Flash Preview",
      "provider": "google",
      "tokens": "1.08T",
      "tokens_raw": 1080000000000,
      "change_pct": 18
    }
  ],
  "top_apps": [
    {
      "rank": 1,
      "name": "OpenClaw",
      "url": "https://openclaw.ai/",
      "description": "The AI that actually does things",
      "tokens": "360B",
      "tokens_raw": 360000000000
    }
  ],
  "market_share": [
    {
      "provider": "google",
      "share_pct": 28.5
    }
  ],
  "categories": []
}
```

If a section can't be scraped (JS-rendered charts), leave it as an empty array `[]` and add a comment in the code explaining why.

---

## Technical Requirements

### Dependencies

```
requests
beautifulsoup4
playwright  (fallback if requests doesn't get the full data)
```

### Script behavior

1. First, try with `requests` + `BeautifulSoup` (fast, no browser needed)
2. If the HTML doesn't contain the ranking data (JS-rendered), fall back to `playwright` (headless Chromium) to render the page and extract from the rendered DOM
3. Parse all data, build the JSON structure
4. Write `leaderboard.json` to the current directory
5. Print a summary: `✓ Scraped X models, Y apps, Z providers. Saved to leaderboard.json`

### Token parsing helper

```python
def parse_tokens(token_str: str) -> int:
    """Convert '1.59T' -> 1590000000000, '803B' -> 803000000000, '5.4M' -> 5400000"""
    token_str = token_str.strip()
    multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3}
    for suffix, mult in multipliers.items():
        if token_str.endswith(suffix):
            return int(float(token_str[:-1]) * mult)
    return int(token_str)
```

### Error handling

- If the page is unreachable, print error and exit with code 1
- If data is partially extracted, still output what was found + warn about missing sections
- Never crash silently

### CLI usage

```bash
python scraper.py                    # default output: ./leaderboard.json
python scraper.py -o /path/to/out    # custom output path
python scraper.py --headless         # force playwright mode
```

---

## Important Notes

- The page is a Next.js app. The initial HTML may contain the data in a `<script>` tag as `__NEXT_DATA__` JSON — **check this first** as it's the easiest and most reliable extraction method. If the rankings data is embedded there, no need for BeautifulSoup HTML parsing at all.
- The "Show more" button at the bottom of the models list likely loads more data — handle this.
- Keep the script simple, single file, no over-engineering.
- The JSON must be valid and pretty-printed (2-space indent).
- The script will be run manually once a week on Windows.

---

## Workflow

1. Camille runs `python scraper.py` once a week
2. Checks the output `leaderboard.json`
3. Pushes it to `github.com/<user>/routerdex-data/main/leaderboard.json`
4. The RouterDex app fetches it from `https://raw.githubusercontent.com/<user>/routerdex-data/main/leaderboard.json`
