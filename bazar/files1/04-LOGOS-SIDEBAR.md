# RouterDex V2 - Provider Logos & Resizable Sidebar

## Provider Logos

### Implementation Strategy

Option 1: **Bundled base64** (recommended for offline)
- Store logos as base64 strings in JS
- ~2KB per logo, ~50 providers = ~100KB total
- Works offline

Option 2: **External fetch**
- Use Clearbit or similar API
- Requires internet
- Fallback to letter avatar

### Logo Object

```javascript
const PROVIDER_LOGOS = {
  'anthropic': 'data:image/png;base64,iVBORw0KGgo...',
  'openai': 'data:image/png;base64,iVBORw0KGgo...',
  'google': 'data:image/png;base64,iVBORw0KGgo...',
  'meta-llama': 'data:image/png;base64,iVBORw0KGgo...',
  'mistralai': 'data:image/png;base64,iVBORw0KGgo...',
  'cohere': 'data:image/png;base64,iVBORw0KGgo...',
  'deepseek': 'data:image/png;base64,iVBORw0KGgo...',
  'x-ai': 'data:image/png;base64,iVBORw0KGgo...',
  'qwen': 'data:image/png;base64,iVBORw0KGgo...',
  'amazon': 'data:image/png;base64,iVBORw0KGgo...',
  'nvidia': 'data:image/png;base64,iVBORw0KGgo...',
  'microsoft': 'data:image/png;base64,iVBORw0KGgo...',
  // ... more providers
};

function getProviderLogo(providerId) {
  if (PROVIDER_LOGOS[providerId]) {
    return PROVIDER_LOGOS[providerId];
  }
  // Fallback: generate letter avatar
  return generateLetterAvatar(providerId);
}
```

### Letter Avatar Fallback

```javascript
function generateLetterAvatar(providerId) {
  const letter = providerId.charAt(0).toUpperCase();
  const colors = {
    'a': '#E53935', 'b': '#D81B60', 'c': '#8E24AA', 'd': '#5E35B1',
    'e': '#3949AB', 'f': '#1E88E5', 'g': '#039BE5', 'h': '#00ACC1',
    'i': '#00897B', 'j': '#43A047', 'k': '#7CB342', 'l': '#C0CA33',
    'm': '#FDD835', 'n': '#FFB300', 'o': '#FB8C00', 'p': '#F4511E',
    'q': '#6D4C41', 'r': '#757575', 's': '#546E7A', 't': '#E53935',
    'u': '#D81B60', 'v': '#8E24AA', 'w': '#5E35B1', 'x': '#3949AB',
    'y': '#1E88E5', 'z': '#039BE5'
  };
  
  const color = colors[letter.toLowerCase()] || '#808080';
  
  // Generate SVG data URL
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">
      <rect width="16" height="16" fill="${color}"/>
      <text x="8" y="12" text-anchor="middle" fill="white" 
            font-family="Tahoma" font-size="11" font-weight="bold">${letter}</text>
    </svg>
  `;
  
  return 'data:image/svg+xml;base64,' + btoa(svg);
}
```

### Known Providers List

Logos to source/create for main providers:

| Provider ID | Company | Domain for Clearbit |
|-------------|---------|---------------------|
| anthropic | Anthropic | anthropic.com |
| openai | OpenAI | openai.com |
| google | Google | google.com |
| meta-llama | Meta | meta.com |
| mistralai | Mistral AI | mistral.ai |
| cohere | Cohere | cohere.com |
| deepseek | DeepSeek | deepseek.com |
| x-ai | xAI | x.ai |
| qwen | Alibaba Qwen | alibaba.com |
| amazon | Amazon | amazon.com |
| nvidia | NVIDIA | nvidia.com |
| microsoft | Microsoft | microsoft.com |
| ai21 | AI21 Labs | ai21.com |
| together | Together AI | together.ai |
| perplexity | Perplexity | perplexity.ai |
| groq | Groq | groq.com |
| fireworks | Fireworks AI | fireworks.ai |
| bytedance-seed | ByteDance | bytedance.com |
| allenai | Allen AI | allenai.org |
| minimax | MiniMax | minimax.io |
| z-ai | Z.ai | z.ai |

### Logo Usage

**Sidebar** (16x16):
```html
<img src="${getProviderLogo(providerId)}" width="16" height="16" class="provider-logo-sm">
```

**Model Page Header** (32x32):
```html
<img src="${getProviderLogo(providerId)}" width="32" height="32" class="provider-logo-lg">
```

**CSS**:
```css
.provider-logo-sm,
.provider-logo-lg {
  vertical-align: middle;
  image-rendering: pixelated; /* Keep crisp on scale */
}

.provider-logo-sm {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

.provider-logo-lg {
  width: 32px;
  height: 32px;
  margin-right: 8px;
}
```

---

## Resizable Sidebar

### Method 1: CSS resize (simple but limited)

```css
.sidebar {
  width: 250px;
  min-width: 150px;
  max-width: 400px;
  resize: horizontal;
  overflow: auto;
}
```

**Limitation**: Only works if overflow is set, handle not very visible.

### Method 2: Custom drag handle (recommended)

**HTML Structure**:
```html
<div class="main-layout">
  <div class="sidebar" id="sidebar">
    <!-- Sidebar content -->
  </div>
  <div class="sidebar-resizer" id="sidebar-resizer"></div>
  <div class="content" id="content">
    <!-- Content area -->
  </div>
</div>
```

**CSS**:
```css
.main-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  min-width: 150px;
  max-width: 400px;
  overflow: auto;
  flex-shrink: 0;
}

.sidebar-resizer {
  width: 4px;
  cursor: ew-resize;
  background: #C0C0C0;
  border-left: 1px solid #808080;
  border-right: 1px solid #FFFFFF;
}

.sidebar-resizer:hover {
  background: #A0A0A0;
}

.sidebar-resizer.dragging {
  background: #808080;
}

.content {
  flex: 1;
  overflow: auto;
}
```

**JavaScript**:
```javascript
function initSidebarResize() {
  const sidebar = document.getElementById('sidebar');
  const resizer = document.getElementById('sidebar-resizer');
  
  let isResizing = false;
  let startX, startWidth;
  
  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    startX = e.clientX;
    startWidth = sidebar.offsetWidth;
    resizer.classList.add('dragging');
    document.body.style.cursor = 'ew-resize';
    document.body.style.userSelect = 'none';
  });
  
  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    
    const diff = e.clientX - startX;
    let newWidth = startWidth + diff;
    
    // Enforce min/max
    newWidth = Math.max(150, Math.min(400, newWidth));
    
    sidebar.style.width = newWidth + 'px';
  });
  
  document.addEventListener('mouseup', () => {
    if (isResizing) {
      isResizing = false;
      resizer.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      
      // Save preference
      localStorage.setItem('routerdex_sidebar_width', sidebar.offsetWidth);
    }
  });
  
  // Restore saved width
  const savedWidth = localStorage.getItem('routerdex_sidebar_width');
  if (savedWidth) {
    sidebar.style.width = savedWidth + 'px';
  }
}

// Call on init
document.addEventListener('DOMContentLoaded', initSidebarResize);
```

### Visual Feedback

```css
/* Show resize cursor on entire sidebar edge */
.sidebar-resizer::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  width: 4px;
  height: 20px;
  margin-top: -10px;
  background: repeating-linear-gradient(
    to bottom,
    #808080 0px,
    #808080 2px,
    #C0C0C0 2px,
    #C0C0C0 4px
  );
}
```

---

## Double-click to Reset

```javascript
resizer.addEventListener('dblclick', () => {
  sidebar.style.width = '250px'; // Default width
  localStorage.removeItem('routerdex_sidebar_width');
});
```
