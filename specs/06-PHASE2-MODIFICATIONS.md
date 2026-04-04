# RouterDex - Phase 2 : Modifications

## Summary

This spec describes all modifications to apply on the existing codebase (Phase 1).
Files to modify: `index.html`, `src/styles/main.css`, `src/js/app.js`.
New folders to create: `src/assets/providers/`, `src/assets/icons/`.

**Read entirely before coding. Apply all changes in a single pass.**

---

## 1. Color Palette Update

Replace the existing CSS custom properties in `:root` with these values:

```css
--bg: #FFFFFF;              /* Main background — unchanged */
--bg-sidebar: #EDEDF0;     /* Sidebar — cooler modern gray */
--bg-titlebar: #E8E8EC;    /* Titlebar */
--bg-hover: #DCDCE4;       /* Hover states */
--bg-active: #C8D0E8;      /* Active/selected state */
--border: #C8C8D0;         /* Borders — slightly stronger */
--card-bg: #F4F4F7;        /* Cards and panels background */
--card-border: #DDDDE3;    /* Card borders */
```

Keep all other variables unchanged (`--text`, `--accent`, `--font`, etc.).

Apply `--card-bg` and `--card-border` to all card-like elements (panels, info tables, stat sections).

---

## 2. Asset Folders

Create two empty directories:

```
src/assets/providers/   → SVG logos named by provider ID (e.g. openai.svg, anthropic.svg)
src/assets/icons/       → App icons (home.svg, search.svg, latest.svg, free.svg, etc.)
```

### Usage rules

- **Provider logos**: Display in sidebar (16px), home panels, model detail header, comparison cards.
- **App icons**: Replace all emoji icons (🏠, 🔍, 🆕, 💰, 🏆, 📂, 📋, ⚙️, 🏷️, 📖, 🔧, etc.) with `<img>` referencing SVG files from `src/assets/icons/`.
- **Loading**: Use `<img src="/src/assets/providers/{providerId}.svg" />` for providers and `<img src="/src/assets/icons/{name}.svg" />` for app icons.
- **Missing logo**: If the image fails to load (`onerror`), hide it entirely (`display: none`). Do NOT render a fallback initial, circle, or placeholder.
- **Icon sizing**: sidebar provider logos 16×16, home panel headers 20×20, model detail 24×24, app icons match the context (14-20px).

---

## 3. Home Page — Complete Redesign

### Remove
- The entire `stat-grid` section (4 stat cards: Models, Providers, Free, Multimodal)
- The `📂 By Category` section with its category filter buttons
- The existing 3 leaderboard sections (Latest, Free, Top Context)

### New layout

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                       RouterDex                             │  ← Hero title, centered
│           AI Models Catalogue — OpenRouter                  │  ← Subtitle, centered
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ [icon]       │  │ [icon]       │  │ [icon]       │      │
│  │ Latest       │  │ Free Models  │  │ Top Context  │      │
│  │ Models       │  │              │  │ Window       │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ model 1      │  │ model 1      │  │ 1. model 1   │      │
│  │ model 2      │  │ model 2      │  │ 2. model 2   │      │
│  │ ...scroll    │  │ ...scroll    │  │ ...scroll    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ [icon]       │  │ [icon]       │  │ [icon]       │      │
│  │ Multimodal   │  │ Text         │  │ Audio        │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ model 1      │  │ model 1      │  │ model 1      │      │
│  │ ...scroll    │  │ ...scroll    │  │ ...scroll    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ [icon]       │  │ [icon]       │                        │
│  │ Image        │  │ Video        │                        │
│  │──────────────│  │──────────────│                        │
│  │ model 1      │  │ model 1      │                        │
│  │ ...scroll    │  │ ...scroll    │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Grid specs

- CSS Grid: `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))` — responsive
- Gap: `16px`
- Each panel: `background: var(--card-bg)`, `border: 1px solid var(--card-border)`, `border-radius: 8px`
- Panel header: icon (from `src/assets/icons/`) + title, bold, padding `12px 16px`, border-bottom
- Panel body: scrollable list, `max-height: 340px`, `overflow-y: auto`
- Each row in panel: model name (clickable → opens model detail) + provider ID + relevant value (date, context size, or price)
- **20 models per panel**

### Panel definitions

| Panel | Title | Filter/Sort | Value shown |
|-------|-------|-------------|-------------|
| Latest Models | Latest Models | Sort by `createdAt` DESC | Release date |
| Free Models | Free Models | Filter `isFree === true`, sort by `contextWindow` DESC | Context size |
| Top Context Window | Top Context Window | Sort by `contextWindow` DESC | Context size (ranked 1-20) |
| Multimodal | Multimodal | Filter `category === 'multimodal'`, sort by `createdAt` DESC | Provider |
| Text | Text | Filter `category === 'text'`, sort by `createdAt` DESC | Provider |
| Audio | Audio | Filter `category === 'audio'` OR `hasAudio === true`, sort by `createdAt` DESC | Provider |
| Image | Image | Filter `category === 'image-gen'`, sort by `createdAt` DESC | Provider |
| Video | Video | Filter `hasVideo === true`, sort by `createdAt` DESC | Provider |

### Icon mapping for panels

Each panel header references an icon file:
- Latest Models → `src/assets/icons/latest.svg`
- Free Models → `src/assets/icons/free.svg`
- Top Context Window → `src/assets/icons/context.svg`
- Multimodal → `src/assets/icons/multimodal.svg`
- Text → `src/assets/icons/text.svg`
- Audio → `src/assets/icons/audio.svg`
- Image → `src/assets/icons/image.svg`
- Video → `src/assets/icons/video.svg`

---

## 4. Model Detail Page — Dashboard Layout

### Remove
The current linear single-column layout.

### New layout

```
┌─────────────────────────────────────────────────────────────┐
│  [provider-logo] ANTHROPIC                          [🔗]    │
│  Claude Sonnet 4.6                                          │
│  [Multimodal] [Vision] [Reasoning]                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────┐ ┌──────────┐ │
│  │  Context     │ │  Max Output │ │ Input    │ │ Output   │ │
│  │  1M tokens   │ │  128K       │ │ $3.00/M  │ │ $15.00/M │ │
│  └─────────────┘ └─────────────┘ └──────────┘ └──────────┘ │
│                         KPI BAR                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────┐  ┌─────────────────────────┐ │
│  │                           │  │ Details                 │ │
│  │ Description               │  │─────────────────────────│ │
│  │                           │  │ ID: anthropic/claude... │ │
│  │ Sonnet 4.6 is Anthropic's │  │ Provider: Anthropic     │ │
│  │ most capable...           │  │ Released: Feb 17, 2026  │ │
│  │                           │  │ Moderated: Yes          │ │
│  │                           │  │ Modality: text+image→..│ │
│  │                           │  │ Input: Text, Image      │ │
│  │                           │  │ Output: Text            │ │
│  ├───────────────────────────┤  ├─────────────────────────┤ │
│  │ Supported Parameters      │  │ Pricing                 │ │
│  │───────────────────────────│  │─────────────────────────│ │
│  │ temperature, top_p,       │  │ Input:  $3.00 / 1M     │ │
│  │ top_k, max_tokens, stop,  │  │ Output: $15.00 / 1M    │ │
│  │ reasoning, tools...       │  │ Cache:  $0.30 / 1M     │ │
│  └───────────────────────────┘  └─────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Structure

**A) Header — full width**
- Provider logo (`src/assets/providers/{providerId}.svg`, 24px) + provider name uppercase
- Model name (large, bold)
- Tags row (badges)
- Link to OpenRouter (icon)

**B) KPI Bar — full width, flex row**
- 4 compact metric cards on a single horizontal line
- Each: small label on top, large value below
- Cards: Context Window, Max Output, Price Input (/1M), Price Output (/1M)
- If model is free, price cards show "FREE" badge instead of $0.00
- Background: `var(--card-bg)`, subtle border, `border-radius: 6px`

**C) Two-column body — `60% / 40%`**

Left column (60%):
- **Description card**: full model description text, scrollable if long
- **Parameters card**: list of supported parameters, comma-separated

Right column (40%):
- **Details card**: ID (monospace), Provider, Release date, Moderation, Modality, Input types, Output types
- **Pricing card**: full pricing table (input, output, cache read, cache write, web search if applicable)

All cards use `var(--card-bg)`, `border: 1px solid var(--card-border)`, `border-radius: 8px`, padding `16px`.

---

## 5. Comparison Feature — New

### State additions

Add to `state`:
```js
compareList: [],       // Array of modelId strings, max 4
```

### Sidebar modifications

- Add a **checkbox** before each model name in `renderProviderModels()`.
- Checkbox toggles the model in/out of `state.compareList`.
- When `state.compareList.length >= 4`, disable (gray out) all unchecked checkboxes.
- Checked models get a subtle highlight (`background: var(--bg-active)`).
- Checkbox is small (14px), aligned left of the model name.

### Compare button

- Add a **"Compare" button** at the top of the sidebar, just below the Home nav item.
- Only visible when `state.compareList.length >= 2`.
- Shows count: `Compare (3)`.
- Clicking it opens the comparison page.
- Also add a "Clear" small link next to it to reset selection.

### Comparison page (`page-compare`)

```
┌─────────────────────────────────────────────────────────────┐
│  Compare Models (3)                          [Clear all]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ [logo]       │  │ [logo]       │  │ [logo]       │      │
│  │ Claude 4.6   │  │ GPT-5        │  │ Gemini 3 Pro │      │
│  │ Anthropic    │  │ OpenAI       │  │ Google       │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ Context      │  │ Context      │  │ Context      │      │
│  │ 1M tokens    │  │ 256K tokens  │  │ 1M tokens    │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ Max Output   │  │ Max Output   │  │ Max Output   │      │
│  │ 128K         │  │ 65K          │  │ 65K          │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ Input Price  │  │ Input Price  │  │ Input Price  │      │
│  │ $3.00/M      │  │ $5.00/M      │  │ $1.25/M      │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ Output Price │  │ Output Price │  │ Output Price │      │
│  │ $15.00/M     │  │ $15.00/M     │  │ $10.00/M     │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ Modality     │  │ Modality     │  │ Modality     │      │
│  │ text+image→  │  │ text+image→  │  │ text+image→  │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ Tags         │  │ Tags         │  │ Tags         │      │
│  │ [Multi][Vis] │  │ [Multi][Vis] │  │ [Multi][Vis] │      │
│  │──────────────│  │──────────────│  │──────────────│      │
│  │ [✕ Remove]   │  │ [✕ Remove]   │  │ [✕ Remove]   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Comparison card specs

- Grid: `repeat(auto-fit, minmax(220px, 1fr))`, gap `16px`, max 4 columns
- Each card: `var(--card-bg)`, border, `border-radius: 8px`
- Card header: provider logo (20px) + model name (bold) + provider name (small, secondary)
- Rows: label (small, secondary) + value (bold), separated by subtle border-bottom
- Fields to compare: Context Window, Max Output, Input Price, Output Price, Modality, Input Types, Output Types, Tags, Free status, Moderated
- "✕ Remove" button at bottom of each card → removes from `compareList`, unchecks sidebar, re-renders
- Clicking model name → navigates to model detail page

### Menu integration

Add in the View menu:
```html
<div class="menu-option" data-action="view-compare">Compare</div>
```

---

## 6. Export JSON

### Behavior

When clicking `File > Export JSON`:

1. Build a clean JSON object from `state.models`:

```json
{
  "export_date": "2026-03-09T14:32:00Z",
  "source": "OpenRouter API",
  "total_models": 346,
  "models": [
    {
      "id": "anthropic/claude-sonnet-4.6",
      "name": "Claude Sonnet 4.6",
      "provider": "anthropic",
      "description": "...",
      "created": 1739836800,
      "context_window": 1000000,
      "max_output_tokens": 128000,
      "pricing": {
        "input_per_million": 3.00,
        "output_per_million": 15.00,
        "cache_read_per_million": 0.30,
        "cache_write_per_million": null,
        "web_search_per_million": null
      },
      "is_free": false,
      "is_moderated": true,
      "modality": {
        "input": ["text", "image"],
        "output": ["text"]
      },
      "category": "multimodal",
      "tags": ["multimodal", "vision", "reasoning"],
      "supported_parameters": ["temperature", "top_p", "max_tokens", "reasoning", "tools"]
    }
  ]
}
```

2. Create a `Blob` with `application/json` type.
3. Trigger download as `routerdex_export_YYYY-MM-DD.json`.

### Implementation

```js
function exportJSON() {
  const data = {
    export_date: new Date().toISOString(),
    source: 'OpenRouter API',
    total_models: state.models.length,
    models: state.models.map(m => ({
      id: m.modelId,
      name: m.displayName,
      provider: m.providerId,
      description: m.description,
      created: m.createdAt,
      context_window: m.contextWindow,
      max_output_tokens: m.maxOutputTokens,
      pricing: {
        input_per_million: m.priceInputPerM,
        output_per_million: m.priceOutputPerM,
        cache_read_per_million: m.priceCacheRead ? parseFloat(m.priceCacheRead) * 1_000_000 : null,
        cache_write_per_million: m.priceCacheWrite ? parseFloat(m.priceCacheWrite) * 1_000_000 : null,
        web_search_per_million: m.priceWebSearch ? parseFloat(m.priceWebSearch) * 1_000_000 : null,
      },
      is_free: m.isFree,
      is_moderated: m.isModerated,
      modality: {
        input: m.inputTypes,
        output: m.outputTypes,
      },
      category: m.category,
      tags: buildTagList(m),
      supported_parameters: m.supportedParams,
    }))
  };

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `routerdex_export_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
```

Add a helper for tag list:
```js
function buildTagList(model) {
  const tags = [];
  if (model.isFree) tags.push('free');
  if (model.category === 'multimodal') tags.push('multimodal');
  if (model.hasVision) tags.push('vision');
  if (model.hasAudio) tags.push('audio');
  if (model.hasVideo) tags.push('video');
  if (model.isCode) tags.push('code');
  if (model.isReasoning) tags.push('reasoning');
  if (model.category === 'image-gen') tags.push('image-gen');
  if (!tags.length) tags.push('text');
  return tags;
}
```

Wire up in menu handler: `case 'export': exportJSON(); break;`

---

## 7. Replace Emojis with SVG Icons

Replace ALL emoji usage in the HTML and JS with `<img>` tags referencing `src/assets/icons/`.

### Mapping

| Current emoji | Icon file | Usage |
|---------------|-----------|-------|
| 📘 | `app-logo.svg` | Titlebar |
| 🏠 | `home.svg` | Sidebar Home nav |
| 🔍 | `search.svg` | Search input placeholder (use as icon before input, not in placeholder text) |
| 🆕 | `latest.svg` | Home panel |
| 💰 | `free.svg` | Home panel + pricing section |
| 🏆 | `context.svg` | Home panel |
| 📂 | (removed) | Category section removed |
| 📋 | `info.svg` | Model detail — Details section |
| ⚙️ | `capabilities.svg` | Model detail — KPI bar / capabilities |
| 🏷️ | `tags.svg` | Model detail — Tags |
| 📖 | `description.svg` | Model detail — Description |
| 🔧 | `parameters.svg` | Model detail — Parameters |
| 🔗 | `external-link.svg` | Model detail — OpenRouter link |
| 📝 | `text.svg` | Modality icon |
| 🖼️ | `image.svg` | Modality icon |
| 🔊 | `audio.svg` | Modality icon |
| 🎬 | `video.svg` | Modality icon |

The search input should have the search icon as an `<img>` or `::before` pseudo-element positioned inside the input field, not as placeholder text.

---

## 8. HTML Structure Changes

### New elements to add in `index.html`

**In sidebar, after `#sidebar-home`:**
```html
<div id="sidebar-compare" class="sidebar-compare hidden">
  <button id="btn-compare" class="btn-compare">Compare (<span id="compare-count">0</span>)</button>
  <button id="btn-compare-clear" class="btn-compare-clear">Clear</button>
</div>
```

**In `#content`, add new page:**
```html
<div id="page-compare" class="page hidden">
  <div class="page-header compare-header">
    <h1>Compare Models</h1>
    <button id="btn-compare-clear-all" class="btn-clear-all">Clear all</button>
  </div>
  <div id="compare-grid" class="compare-grid"></div>
</div>
```

**In View menu, add:**
```html
<div class="menu-option" data-action="view-compare">Compare</div>
```

---

## 9. Implementation Order

1. Create asset folders (`src/assets/providers/`, `src/assets/icons/`)
2. Update CSS variables (palette)
3. Replace emojis with `<img>` SVG references
4. Redesign Home page (HTML + JS + CSS)
5. Redesign Model detail page (HTML + JS + CSS)
6. Implement Comparison feature (state, sidebar checkboxes, compare page)
7. Wire Export JSON
8. Test all navigation flows (Home → Model → Compare → Home)
9. Verify responsive behavior

---

## 10. Important Notes

- **Language**: All UI stays in English.
- **Single file architecture**: Keep everything in `app.js`, `main.css`, `index.html`. Do not split into modules.
- **No new dependencies**: Pure vanilla JS, no libraries.
- **Existing features**: Keep all working features intact (search, sidebar, menu, cache, resize handle, keyboard nav, status bar).
- **Provider logos and app icons will be added manually** by the developer into the asset folders. The code should reference them but gracefully handle missing files (hide on error).
