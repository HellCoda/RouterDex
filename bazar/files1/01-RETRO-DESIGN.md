# RouterDex V2 - Windows 2000 Retro Design

## Design Philosophy

Full commitment to Windows 2000/ME aesthetic. No modern flat design, no emojis, no rounded corners.

---

## Color Palette

### System Colors
| Name | Hex | Usage |
|------|-----|-------|
| Desktop | #008080 | Background behind window |
| Silver | #C0C0C0 | Window frame, toolbar, statusbar |
| White | #FFFFFF | Content areas, input fields |
| Navy | #000080 | Active title bar, selection |
| Gray Dark | #808080 | Shadow edges, disabled text |
| Gray Light | #DFDFDF | Highlight edges |
| Black | #000000 | Text, borders |

### 3D Border Colors
```css
/* Raised (button, toolbar) */
--highlight: #FFFFFF;
--light: #DFDFDF;
--shadow: #808080;
--dark: #404040;

/* Sunken (input, content) */
/* Reverse highlight/shadow */
```

---

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Title bar | Tahoma, sans-serif | 11px | Bold |
| Menu | Tahoma, sans-serif | 11px | Normal |
| Body | Tahoma, sans-serif | 11px | Normal |
| Headers | Tahoma, sans-serif | 12px | Bold |
| Monospace | Courier New | 11px | Normal |

---

## Window Frame

```
┌──────────────────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ RouterDex ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ [_] [□] [X] │ <- Navy gradient
├──────────────────────────────────────────────────────────────┤
│ File   View   Help                                           │ <- Silver bar
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   CONTENT                                                    │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ Ready                                                        │ <- Sunken statusbar
└──────────────────────────────────────────────────────────────┘
```

### Title Bar CSS
```css
.titlebar {
  background: linear-gradient(to right, #000080, #1084D0);
  color: white;
  font-family: Tahoma, sans-serif;
  font-size: 11px;
  font-weight: bold;
  padding: 2px 4px;
  display: flex;
  align-items: center;
  height: 22px;
}

.titlebar-icon {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

.titlebar-buttons {
  margin-left: auto;
  display: flex;
  gap: 2px;
}

.titlebar-btn {
  width: 16px;
  height: 14px;
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  font-size: 9px;
  line-height: 10px;
  text-align: center;
}

.titlebar-btn:active {
  border-color: #808080 #FFFFFF #FFFFFF #808080;
}
```

### Window Buttons
```
[_] Minimize - small horizontal line at bottom
[□] Maximize - small square outline
[X] Close - small X
```

---

## Menu Bar

```css
.menubar {
  background: #C0C0C0;
  border-bottom: 1px solid #808080;
  padding: 2px 0;
  font-family: Tahoma, sans-serif;
  font-size: 11px;
}

.menu-item {
  padding: 2px 8px;
  cursor: default;
}

.menu-item:hover {
  background: #000080;
  color: white;
}

.dropdown {
  position: absolute;
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  box-shadow: 2px 2px 0 #404040;
}

.dropdown-item {
  padding: 2px 20px;
}

.dropdown-item:hover {
  background: #000080;
  color: white;
}

.dropdown-separator {
  border-top: 1px solid #808080;
  border-bottom: 1px solid #FFFFFF;
  margin: 2px 0;
}
```

---

## Sidebar (TreeView)

### Structure
```
┌─────────────────────┐
│ [icon] Home         │
├─────────────────────┤
│ [-] Anthropic       │ <- Expanded folder
│   ├─ Claude Opus    │
│   ├─ Claude Sonnet  │
│   └─ Claude Haiku   │
│ [+] OpenAI          │ <- Collapsed folder
│ [+] Google          │
│ [+] Meta            │
└─────────────────────┘
```

### CSS
```css
.sidebar {
  background: #FFFFFF;
  border: 2px solid;
  border-color: #808080 #FFFFFF #FFFFFF #808080;
  overflow: auto;
  font-family: Tahoma, sans-serif;
  font-size: 11px;
}

.tree-item {
  padding: 1px 2px;
  white-space: nowrap;
  cursor: default;
  display: flex;
  align-items: center;
}

.tree-item:hover {
  background: #000080;
  color: white;
}

.tree-item.selected {
  background: #000080;
  color: white;
}

.tree-icon {
  width: 16px;
  height: 16px;
  margin-right: 2px;
}

.tree-expand {
  width: 9px;
  height: 9px;
  margin-right: 2px;
  border: 1px solid #808080;
  background: white;
  font-size: 9px;
  line-height: 7px;
  text-align: center;
}

.tree-children {
  margin-left: 16px;
  border-left: 1px dotted #808080;
}
```

---

## Buttons

```css
.btn {
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  padding: 2px 12px;
  font-family: Tahoma, sans-serif;
  font-size: 11px;
  cursor: default;
}

.btn:active {
  border-color: #808080 #FFFFFF #FFFFFF #808080;
  padding: 3px 11px 1px 13px;
}

.btn:disabled {
  color: #808080;
}

.btn-default {
  border: 3px solid;
  border-color: #000000 #000000 #000000 #000000;
  outline: 1px solid #FFFFFF;
  outline-offset: -4px;
}
```

---

## Input Fields

```css
input[type="text"],
.input-field {
  background: #FFFFFF;
  border: 2px solid;
  border-color: #808080 #FFFFFF #FFFFFF #808080;
  padding: 2px 4px;
  font-family: Tahoma, sans-serif;
  font-size: 11px;
}

input:focus {
  outline: none;
}
```

---

## Scrollbars (if customizable)

```css
::-webkit-scrollbar {
  width: 16px;
  height: 16px;
}

::-webkit-scrollbar-track {
  background: #C0C0C0;
  background-image: url('data:image/png;base64,...'); /* checkered pattern */
}

::-webkit-scrollbar-thumb {
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
}

::-webkit-scrollbar-button {
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  width: 16px;
  height: 16px;
}
```

---

## Status Bar

```css
.statusbar {
  background: #C0C0C0;
  border-top: 2px solid;
  border-color: #808080 #FFFFFF;
  padding: 2px;
  font-family: Tahoma, sans-serif;
  font-size: 11px;
  display: flex;
}

.statusbar-section {
  border: 1px solid;
  border-color: #808080 #FFFFFF #FFFFFF #808080;
  padding: 0 4px;
  margin-right: 2px;
}
```

---

## Tables / Lists

```css
.list-view {
  background: #FFFFFF;
  border: 2px solid;
  border-color: #808080 #FFFFFF #FFFFFF #808080;
}

.list-header {
  background: #C0C0C0;
  border-bottom: 1px solid #808080;
  font-weight: bold;
}

.list-row {
  border-bottom: 1px solid #C0C0C0;
}

.list-row:hover {
  background: #000080;
  color: white;
}

.list-row.selected {
  background: #000080;
  color: white;
}
```

---

## Modal / Dialog

```css
.modal-overlay {
  background: transparent;
}

.modal {
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  box-shadow: 4px 4px 0 #404040;
}

.modal-titlebar {
  background: linear-gradient(to right, #000080, #1084D0);
  color: white;
  padding: 2px 4px;
  font-weight: bold;
}

.modal-content {
  padding: 12px;
}

.modal-buttons {
  text-align: center;
  padding: 8px;
}
```

---

## Icons Reference

All icons should be 16x16 PNG with transparency, pixel art style.

### File/Folder Icons
- `folder_closed.png` - Yellow folder
- `folder_open.png` - Yellow folder open
- `document.png` - White page with lines

### Action Icons
- `home.png` - House
- `search.png` - Magnifying glass
- `refresh.png` - Two curved arrows
- `export.png` - Floppy disk or arrow out

### Status Icons
- `free.png` - Green checkmark or $0
- `new.png` - Yellow star or "NEW" badge

### Provider Folders
- Can use colored folder variants per provider
- Or generic folder + provider logo overlay
