# RouterDex V2 - Menu Implementation

## Menu Structure

```
File                View                Help
├─ Refresh          ├─ Home             ├─ About
├─ Export JSON      ├─ All Models       └─ OpenRouter Docs
├─ ─────────        ├─ Free Only
└─ Exit             ├─ ─────────
                    ├─ By Category  >   ├─ Text
                    │                   ├─ Multimodal
                    │                   ├─ Vision
                    │                   ├─ Audio
                    │                   ├─ Code
                    │                   └─ Reasoning
                    ├─ ─────────
                    └─ Compare Mode
```

---

## File Menu

### Refresh
**Status**: Already working
```javascript
function menuRefresh() {
  localStorage.removeItem(CACHE_KEY);
  fetchModels();
}
```

### Export JSON
**Status**: TODO

```javascript
function menuExportJSON() {
  const cache = localStorage.getItem(CACHE_KEY);
  if (!cache) {
    alert('No data to export. Please refresh first.');
    return;
  }
  
  const data = JSON.parse(cache);
  const blob = new Blob([JSON.stringify(data.data, null, 2)], {
    type: 'application/json'
  });
  
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `routerdex_models_${formatDateFilename(new Date())}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function formatDateFilename(date) {
  return date.toISOString().split('T')[0]; // "2026-03-08"
}
```

### Exit
**Status**: TODO (Tauri only)

```javascript
async function menuExit() {
  // In Tauri context
  if (window.__TAURI__) {
    const { getCurrentWindow } = window.__TAURI__.window;
    await getCurrentWindow().close();
  } else {
    // In browser, just close tab (may be blocked)
    window.close();
  }
}
```

---

## View Menu

### Home
**Status**: Already working
```javascript
function menuHome() {
  renderHomePage();
}
```

### All Models
**Status**: Already working
```javascript
function menuAllModels() {
  expandAllProviders();
}
```

### Free Only
**Status**: Already working
```javascript
function menuFreeOnly() {
  filterModels(m => m.isFree);
}
```

### By Category (Submenu)
**Status**: TODO

**Option A: Submenu**
```html
<div class="menu-item has-submenu">
  By Category
  <div class="submenu">
    <div class="submenu-item" onclick="filterByCategory('text')">Text</div>
    <div class="submenu-item" onclick="filterByCategory('multimodal')">Multimodal</div>
    <div class="submenu-item" onclick="filterByCategory('vision')">Vision</div>
    <div class="submenu-item" onclick="filterByCategory('audio')">Audio</div>
    <div class="submenu-item" onclick="filterByCategory('code')">Code</div>
    <div class="submenu-item" onclick="filterByCategory('reasoning')">Reasoning</div>
  </div>
</div>
```

**CSS for submenu**:
```css
.menu-item.has-submenu {
  position: relative;
}

.menu-item.has-submenu::after {
  content: '>';
  float: right;
  margin-left: 8px;
}

.submenu {
  display: none;
  position: absolute;
  left: 100%;
  top: 0;
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  box-shadow: 2px 2px 0 #404040;
  min-width: 120px;
}

.menu-item.has-submenu:hover .submenu {
  display: block;
}

.submenu-item {
  padding: 2px 20px;
  white-space: nowrap;
}

.submenu-item:hover {
  background: #000080;
  color: white;
}
```

**JavaScript**:
```javascript
function filterByCategory(category) {
  const filters = {
    'text': m => m.modality === 'text->text',
    'multimodal': m => m.inputTypes.length > 1,
    'vision': m => m.inputTypes.includes('image'),
    'audio': m => m.inputTypes.includes('audio'),
    'code': m => m.name.toLowerCase().includes('code') || 
                 m.description.toLowerCase().includes('coding'),
    'reasoning': m => m.supportedParameters.includes('reasoning')
  };
  
  const filter = filters[category];
  if (filter) {
    filterModels(filter);
    closeAllMenus();
  }
}
```

### Compare Mode
**Status**: NEW

Toggle checkbox visibility in sidebar:
```javascript
let compareModeEnabled = false;

function menuToggleCompareMode() {
  compareModeEnabled = !compareModeEnabled;
  document.body.classList.toggle('compare-mode', compareModeEnabled);
  
  // Update menu item checkmark
  const menuItem = document.querySelector('[data-menu="compare-mode"]');
  menuItem.classList.toggle('checked', compareModeEnabled);
}
```

```css
/* Checkboxes hidden by default */
.model-checkbox {
  display: none;
}

/* Show when compare mode enabled */
.compare-mode .model-checkbox {
  display: inline-block;
}

/* Menu item with checkmark */
.menu-item.checked::before {
  content: '✓';
  margin-right: 4px;
}
```

---

## Help Menu

### About
**Status**: TODO

```javascript
function menuAbout() {
  const modelCount = getAllModels().length;
  const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}');
  const lastUpdate = cache.timestamp 
    ? new Date(cache.timestamp).toLocaleString()
    : 'Never';
  
  showModal({
    title: 'About RouterDex',
    content: `
      <div style="text-align: center; padding: 20px;">
        <img src="icon.png" width="48" height="48" alt="RouterDex">
        <h2 style="margin: 10px 0;">RouterDex</h2>
        <p>Version 1.0</p>
        <hr style="margin: 15px 0;">
        <p>AI Models Catalog</p>
        <p>Powered by OpenRouter API</p>
        <p><a href="https://openrouter.ai" target="_blank">openrouter.ai</a></p>
        <hr style="margin: 15px 0;">
        <p>Models: ${modelCount}</p>
        <p>Last update: ${lastUpdate}</p>
      </div>
    `,
    buttons: ['OK']
  });
}
```

### OpenRouter Docs
**Status**: Already working
```javascript
function menuOpenRouterDocs() {
  window.open('https://openrouter.ai/docs', '_blank');
}
```

---

## Modal Component

### HTML
```html
<div class="modal-overlay" id="modal-overlay">
  <div class="modal" id="modal">
    <div class="modal-titlebar">
      <span class="modal-title" id="modal-title">Title</span>
      <button class="modal-close" onclick="closeModal()">X</button>
    </div>
    <div class="modal-content" id="modal-content">
      <!-- Content -->
    </div>
    <div class="modal-buttons" id="modal-buttons">
      <!-- Buttons -->
    </div>
  </div>
</div>
```

### CSS
```css
.modal-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent;
  z-index: 1000;
  justify-content: center;
  align-items: center;
}

.modal-overlay.visible {
  display: flex;
}

.modal {
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  box-shadow: 4px 4px 0 #404040;
  min-width: 300px;
  max-width: 500px;
}

.modal-titlebar {
  background: linear-gradient(to right, #000080, #1084D0);
  color: white;
  padding: 2px 4px;
  display: flex;
  align-items: center;
}

.modal-title {
  flex: 1;
  font-weight: bold;
}

.modal-close {
  width: 16px;
  height: 14px;
  background: #C0C0C0;
  border: 2px solid;
  border-color: #FFFFFF #808080 #808080 #FFFFFF;
  font-size: 9px;
  line-height: 10px;
  cursor: default;
}

.modal-content {
  padding: 16px;
  background: #C0C0C0;
}

.modal-buttons {
  padding: 8px;
  text-align: center;
  background: #C0C0C0;
}

.modal-buttons .btn {
  min-width: 75px;
  margin: 0 4px;
}
```

### JavaScript
```javascript
function showModal({ title, content, buttons = ['OK'], onButton }) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-content').innerHTML = content;
  
  const buttonsContainer = document.getElementById('modal-buttons');
  buttonsContainer.innerHTML = buttons.map((btn, i) => 
    `<button class="btn" onclick="handleModalButton(${i})">${btn}</button>`
  ).join('');
  
  window.modalCallback = onButton;
  document.getElementById('modal-overlay').classList.add('visible');
}

function handleModalButton(index) {
  closeModal();
  if (window.modalCallback) {
    window.modalCallback(index);
  }
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('visible');
}

// Close on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
});
```
