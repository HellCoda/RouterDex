# RouterDex V2 - Changelog

## Changes from V1

This document lists all changes to implement in version 2.

---

## BUGS TO FIX

### Critical: Only 346 models displayed
- **Issue**: App shows only 346 models instead of 600+
- **Cause**: Likely a filter, slice, or JSON parsing issue
- **Fix**: Ensure ALL models from `data` array are processed
- **Check**: 
  - No `.slice()` or `.filter()` limiting results
  - JSON parsing handles full response
  - No pagination issue with API fetch

---

## STYLE CHANGES

### Full Retro Windows 2000 Theme
- **No emojis** - Replace all emojis with pixel icons or text
- **Beveled borders** - 3D raised/sunken effects
- **System fonts** - MS Sans Serif, Tahoma style
- **16-color palette feel** - Limited, muted colors
- **Pixel icons** - 16x16 icons for folders, files, categories

### Color Palette Update

| Element | Old | New |
|---------|-----|-----|
| Window background | #FFFFFF | #C0C0C0 (silver) |
| Content area | #FFFFFF | #FFFFFF (keep white) |
| Borders | #D0D0D0 | 3D beveled (highlight/shadow) |
| Title bar | #F0F0F0 | #000080 (navy blue) + white text |
| Selection | #CCE0FF | #000080 background, white text |
| Buttons | flat | 3D raised, sunken on click |

### CSS Effects to Add
```css
/* Beveled border - raised */
.raised {
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
}

/* Beveled border - sunken */
.sunken {
  border: 2px solid;
  border-color: #808080 #FFFFFF #FFFFFF #808080;
}

/* Title bar gradient */
.titlebar {
  background: linear-gradient(to right, #000080, #1084D0);
  color: white;
  font-weight: bold;
}
```

---

## LANGUAGE

- **Full English UI**
- All labels, buttons, menus in English
- Keep model descriptions as-is (from API, already English)

---

## HOME PAGE REDESIGN

### Remove
- Stats cards (X models, X providers, X free, X multimodal)

### Add/Keep (6 sections, 20 items each with scroll)

| Section | Sort/Filter | Icon |
|---------|-------------|------|
| Latest Models | `created` DESC | [NEW] |
| Free Models | `pricing.prompt === "0"` | [FREE] |
| Largest Context | `context_length` DESC | [CTX] |
| Cheapest Models | `pricing.prompt` ASC (non-free) | [$] |
| By Category | Buttons: Text, Multimodal, Vision, Audio, Code | [CAT] |
| By Provider | Quick links to providers | [PRV] |

### Layout
- **Grid 3x2** on desktop
- **Responsive**: 2 columns on tablet, 1 on mobile
- Each section: header + scrollable list (max-height with overflow)

---

## NEW FEATURE: Model Comparator

### How it works
1. User checks up to 4 models in sidebar (checkbox next to each model)
2. "Compare" button appears in toolbar/menu when 2+ selected
3. Click opens comparison view in content area
4. Side-by-side table with all model attributes

### Comparison Table Columns
| Attribute | Model 1 | Model 2 | Model 3 | Model 4 |
|-----------|---------|---------|---------|---------|
| Provider | | | | |
| Context | | | | |
| Input Price | | | | |
| Output Price | | | | |
| Modalities | | | | |
| Created | | | | |

### UI Elements
- Checkbox in sidebar: `[ ] Model Name`
- Counter badge: "2 selected"
- Compare button: enabled when 2-4 selected
- Clear selection button

---

## PROVIDER LOGOS

### Implementation
- Store logos as base64 in JS object
- Fallback: First letter in colored circle
- Size: 16x16 in sidebar, 32x32 in model page

### Logo Sources
- Use Clearbit Logo API: `https://logo.clearbit.com/{domain}`
- Or bundle SVG/PNG for main providers

### Known Providers to Include
- Anthropic, OpenAI, Google, Meta, Mistral, Cohere
- DeepSeek, xAI, Qwen, ByteDance, Amazon
- NVIDIA, Microsoft, Alibaba, etc.

---

## SIDEBAR IMPROVEMENTS

### Resizable
- Add drag handle on right edge
- Min width: 150px
- Max width: 400px
- Store preference in localStorage

### CSS
```css
.sidebar {
  width: 250px;
  min-width: 150px;
  max-width: 400px;
  resize: horizontal;
  overflow: auto;
}

/* Or custom drag handle */
.sidebar-resizer {
  width: 5px;
  cursor: ew-resize;
  background: #C0C0C0;
}
```

---

## MENU ITEMS TO IMPLEMENT

### File Menu
| Item | Status | Action |
|------|--------|--------|
| Refresh | OK | Re-fetch API |
| Export JSON | TODO | Download models as JSON file |
| Exit | TODO | Close window (Tauri API) |

### View Menu
| Item | Status | Action |
|------|--------|--------|
| Home | OK | Show home page |
| All Models | OK | Expand all providers |
| Free Only | OK | Filter free models |
| By Category | TODO | Show category filter submenu/modal |
| Compare Mode | NEW | Toggle checkbox visibility in sidebar |

### Help Menu
| Item | Status | Action |
|------|--------|--------|
| About | TODO | Show about modal |
| OpenRouter Docs | OK | Open external link |

### About Modal Content
```
RouterDex v1.0

AI Models Catalog powered by OpenRouter API
https://openrouter.ai

Models: {count}
Last update: {date}

[OK]
```

---

## ICONS TO CREATE (Pixel Art 16x16)

Replace emojis with pixel icons:

| Use | Old | New |
|-----|-----|-----|
| Folder closed | (none) | folder_closed.png |
| Folder open | (none) | folder_open.png |
| Model/Document | (none) | document.png |
| Home | 🏠 | home.png |
| Search | 🔍 | search.png |
| Free | 💰 | free.png |
| Context | (none) | context.png |
| Category | 📂 | category.png |
| Provider | (none) | provider.png |
| New | 🆕 | new.png |
| Checkbox empty | [ ] | checkbox_empty.png |
| Checkbox checked | [x] | checkbox_checked.png |
| Compare | (none) | compare.png |

---

## SUMMARY CHECKLIST

- [ ] Fix: Display ALL models (not just 346)
- [ ] Style: Full Windows 2000 retro (no emojis)
- [ ] Language: English only
- [ ] Home: 6 sections, 20 items each, grid layout
- [ ] Feature: Comparator (max 4 models)
- [ ] Feature: Provider logos
- [ ] Feature: Resizable sidebar
- [ ] Menu: Export JSON
- [ ] Menu: By Category filter
- [ ] Menu: About modal
- [ ] Icons: Pixel art replacements
