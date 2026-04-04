# RouterDex V2 - Home Page Redesign

## Layout Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            ROUTERDEX                                    │
│                     AI Models Catalog - OpenRouter                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐│
│  │ [*] LATEST MODELS   │ │ [$] FREE MODELS     │ │ [C] LARGEST CONTEXT ││
│  ├─────────────────────┤ ├─────────────────────┤ ├─────────────────────┤│
│  │ > Model Name    Date│ │ > Model Name    Ctx │ │ > Model Name    Ctx ││
│  │ > Model Name    Date│ │ > Model Name    Ctx │ │ > Model Name    Ctx ││
│  │ > Model Name    Date│ │ > Model Name    Ctx │ │ > Model Name    Ctx ││
│  │ > ...               │ │ > ...               │ │ > ...               ││
│  │   (scroll 20)       │ │   (scroll 20)       │ │   (scroll 20)       ││
│  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘│
│                                                                         │
│  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐│
│  │ [$] CHEAPEST MODELS │ │ [#] BY CATEGORY     │ │ [P] BY PROVIDER     ││
│  ├─────────────────────┤ ├─────────────────────┤ ├─────────────────────┤│
│  │ > Model Name  Price │ │ [Text]  [Multimodal]│ │ [Anthropic]  (12)   ││
│  │ > Model Name  Price │ │ [Vision] [Audio]    │ │ [OpenAI]     (45)   ││
│  │ > Model Name  Price │ │ [Code]  [Reasoning] │ │ [Google]     (28)   ││
│  │ > ...               │ │ [Image Gen]         │ │ [Meta]       (8)    ││
│  │   (scroll 20)       │ │                     │ │ > ...               ││
│  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Section Details

### 1. Latest Models

**Header**: `[*] LATEST MODELS`

**Data Source**: All models sorted by `created` DESC

**Columns**:
| Column | Width | Content |
|--------|-------|---------|
| Icon | 16px | Provider logo (16x16) |
| Name | flex | Model display name (truncate) |
| Date | 80px | Release date (DD MMM YYYY) |

**Items**: 20 (scrollable)

**Click Action**: Navigate to model page

---

### 2. Free Models

**Header**: `[$] FREE MODELS`

**Data Source**: Filter where `pricing.prompt === "0" && pricing.completion === "0"`

**Columns**:
| Column | Width | Content |
|--------|-------|---------|
| Icon | 16px | Provider logo |
| Name | flex | Model name |
| Context | 70px | Context window (formatted: "200K", "1M") |

**Items**: 20 (scrollable)

---

### 3. Largest Context

**Header**: `[C] LARGEST CONTEXT`

**Data Source**: All models sorted by `context_length` DESC

**Columns**:
| Column | Width | Content |
|--------|-------|---------|
| Rank | 20px | 1. 2. 3. etc |
| Icon | 16px | Provider logo |
| Name | flex | Model name |
| Context | 70px | Context window formatted |

**Items**: 20 (scrollable)

---

### 4. Cheapest Models

**Header**: `[$] CHEAPEST MODELS`

**Data Source**: Non-free models sorted by `pricing.prompt` ASC

**Columns**:
| Column | Width | Content |
|--------|-------|---------|
| Rank | 20px | 1. 2. 3. etc |
| Icon | 16px | Provider logo |
| Name | flex | Model name |
| Price | 80px | Input price $/1M tokens |

**Items**: 20 (scrollable)

---

### 5. By Category

**Header**: `[#] BY CATEGORY`

**Content**: Clickable buttons/tags

**Categories** (derived from modality):
| Category | Filter Logic | Icon |
|----------|--------------|------|
| Text | `modality === "text->text"` | [TXT] |
| Multimodal | `input_modalities.length > 1` | [MM] |
| Vision | `input_modalities.includes("image")` | [IMG] |
| Audio | `input_modalities.includes("audio")` | [AUD] |
| Video | `input_modalities.includes("video")` | [VID] |
| Code | `name` or `description` contains "code" | [</>] |
| Reasoning | `supported_parameters.includes("reasoning")` | [R] |
| Image Gen | `output_modalities.includes("image")` | [GEN] |

**Click Action**: Filter sidebar to show only matching models

---

### 6. By Provider

**Header**: `[P] BY PROVIDER`

**Data Source**: Group models by provider, count each

**Columns**:
| Column | Width | Content |
|--------|-------|---------|
| Icon | 16px | Provider logo |
| Name | flex | Provider name |
| Count | 40px | Number of models |

**Items**: All providers (scrollable)

**Click Action**: Expand provider in sidebar + scroll to it

---

## Grid CSS

```css
.home-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  padding: 8px;
}

/* Tablet */
@media (max-width: 1100px) {
  .home-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile */
@media (max-width: 700px) {
  .home-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## Section Card CSS

```css
.home-card {
  background: #FFFFFF;
  border: 2px solid;
  border-color: #808080 #FFFFFF #FFFFFF #808080;
  display: flex;
  flex-direction: column;
  max-height: 300px;
}

.home-card-header {
  background: #C0C0C0;
  border-bottom: 1px solid #808080;
  padding: 4px 8px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 4px;
}

.home-card-header-icon {
  width: 16px;
  height: 16px;
}

.home-card-content {
  flex: 1;
  overflow-y: auto;
  padding: 2px;
}

.home-card-row {
  display: flex;
  align-items: center;
  padding: 2px 4px;
  gap: 4px;
  cursor: default;
}

.home-card-row:hover {
  background: #000080;
  color: white;
}

.home-card-row-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.home-card-row-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.home-card-row-value {
  flex-shrink: 0;
  text-align: right;
  color: #808080;
}

.home-card-row:hover .home-card-row-value {
  color: #C0C0C0;
}
```

---

## Category Buttons CSS

```css
.category-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 8px;
}

.category-btn {
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  padding: 4px 8px;
  font-size: 11px;
  cursor: default;
}

.category-btn:hover {
  background: #DFDFDF;
}

.category-btn:active,
.category-btn.active {
  border-color: #808080 #FFFFFF #FFFFFF #808080;
  background: #A0A0A0;
}
```

---

## Helper Functions

### Format Context Window
```javascript
function formatContext(tokens) {
  if (tokens >= 1000000) {
    return (tokens / 1000000).toFixed(1).replace('.0', '') + 'M';
  }
  if (tokens >= 1000) {
    return (tokens / 1000).toFixed(0) + 'K';
  }
  return tokens.toString();
}
// 1000000 -> "1M"
// 262144 -> "262K"
// 200000 -> "200K"
```

### Format Price
```javascript
function formatPrice(pricePerToken) {
  const perMillion = parseFloat(pricePerToken) * 1000000;
  if (perMillion === 0) return 'Free';
  if (perMillion < 0.01) return '<$0.01';
  if (perMillion < 1) return '$' + perMillion.toFixed(2);
  return '$' + perMillion.toFixed(2);
}
// "0.000003" -> "$3.00"
// "0.0000001" -> "$0.10"
// "0" -> "Free"
```

### Format Date
```javascript
function formatDate(timestamp) {
  const date = new Date(timestamp * 1000);
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return date.getDate() + ' ' + months[date.getMonth()] + ' ' + date.getFullYear();
}
// 1771342990 -> "17 Feb 2026"
```
