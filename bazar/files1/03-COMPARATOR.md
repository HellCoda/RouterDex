# RouterDex V2 - Model Comparator

## Overview

Allow users to select 2-4 models and compare them side-by-side in a table view.

---

## User Flow

```
1. User browses sidebar
2. User checks checkbox next to model name (up to 4)
3. Badge shows "X selected" in toolbar
4. User clicks "Compare" button
5. Comparison table opens in content area
6. User can uncheck models or click "Clear" to reset
```

---

## UI Components

### Sidebar Checkbox

```
┌─────────────────────────┐
│ [-] Anthropic           │
│   [x] Claude Opus 4.6   │  <- Checkbox before name
│   [ ] Claude Sonnet 4.6 │
│   [x] Claude Haiku      │
│ [+] OpenAI              │
└─────────────────────────┘
```

**CSS**:
```css
.model-checkbox {
  width: 13px;
  height: 13px;
  margin-right: 4px;
  appearance: none;
  background: #FFFFFF;
  border: 1px solid #808080;
  cursor: default;
}

.model-checkbox:checked {
  background: #FFFFFF url('checkbox_check.png') center no-repeat;
}

.model-checkbox:checked::after {
  content: '✓';
  font-size: 10px;
  color: #000000;
}
```

### Toolbar Section

```
┌───────────────────────────────────────────────────────────┐
│ [Compare (3)]  [Clear Selection]                          │
└───────────────────────────────────────────────────────────┘
```

**Logic**:
- "Compare" button: Disabled if < 2 selected, enabled if 2-4
- Badge shows count: "Compare (3)"
- "Clear Selection": Only visible if > 0 selected

**CSS**:
```css
.compare-toolbar {
  background: #C0C0C0;
  padding: 4px 8px;
  border-bottom: 1px solid #808080;
  display: flex;
  gap: 8px;
}

.compare-btn {
  /* Standard button style */
}

.compare-btn:disabled {
  color: #808080;
}

.compare-count {
  background: #000080;
  color: white;
  padding: 0 4px;
  font-size: 10px;
  margin-left: 4px;
}
```

---

## Comparison Table

### Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MODEL COMPARISON                                │
├─────────────┬─────────────────┬─────────────────┬─────────────────┬─────┤
│ Attribute   │ Claude Opus 4.6 │ GPT-5.2         │ Gemini 3 Pro    │     │
│             │ [Anthropic]     │ [OpenAI]        │ [Google]        │     │
├─────────────┼─────────────────┼─────────────────┼─────────────────┼─────┤
│ Context     │ 1,000,000       │ 400,000         │ 1,048,576       │ [W] │
│ Input Price │ $5.00/1M        │ $1.75/1M        │ $2.00/1M        │ [W] │
│ Output Price│ $25.00/1M       │ $14.00/1M       │ $12.00/1M       │ [W] │
│ Input Types │ text, image     │ text, image     │ text, img, aud  │     │
│ Output Types│ text            │ text            │ text            │     │
│ Moderated   │ Yes             │ Yes             │ No              │     │
│ Released    │ 05 Feb 2026     │ 11 Dec 2025     │ 17 Nov 2025     │     │
│ Reasoning   │ Yes             │ Yes             │ Yes             │     │
│ Tools       │ Yes             │ Yes             │ Yes             │     │
└─────────────┴─────────────────┴─────────────────┴─────────────────┴─────┘

[W] = Winner indicator (best value highlighted)
```

### Attributes to Compare

| Attribute | Field | Best = |
|-----------|-------|--------|
| Provider | derived from id | - |
| Context Window | context_length | Highest |
| Input Price | pricing.prompt | Lowest |
| Output Price | pricing.completion | Lowest |
| Input Types | architecture.input_modalities | Most |
| Output Types | architecture.output_modalities | Most |
| Max Output | top_provider.max_completion_tokens | Highest |
| Moderated | top_provider.is_moderated | - |
| Released | created | - |
| Reasoning | supported_parameters includes "reasoning" | - |
| Tools | supported_parameters includes "tools" | - |
| Structured Output | supported_parameters includes "structured_outputs" | - |

### Winner Highlighting

For numeric comparisons, highlight the "best" value:
- Context, Max Output: **Highest** = green background
- Prices: **Lowest** = green background (but not $0 free)

```css
.compare-cell-winner {
  background: #90EE90; /* Light green */
  font-weight: bold;
}

.compare-cell-free {
  background: #90EE90;
  font-weight: bold;
}
```

---

## Table CSS

```css
.compare-table {
  width: 100%;
  border-collapse: collapse;
  background: #FFFFFF;
  font-size: 11px;
}

.compare-table th,
.compare-table td {
  border: 1px solid #808080;
  padding: 4px 8px;
  text-align: left;
  vertical-align: top;
}

.compare-table th {
  background: #C0C0C0;
  font-weight: bold;
}

.compare-table th.model-header {
  text-align: center;
  min-width: 150px;
}

.compare-table .attr-label {
  background: #DFDFDF;
  font-weight: bold;
  width: 120px;
}

.compare-table .provider-name {
  font-size: 10px;
  color: #808080;
}

.compare-table tr:hover td {
  background: #E8E8E8;
}

.compare-table tr:hover td.compare-cell-winner {
  background: #7CCD7C;
}
```

---

## JavaScript Logic

### State Management
```javascript
// Selected models (max 4)
let selectedModels = new Set();

function toggleModelSelection(modelId) {
  if (selectedModels.has(modelId)) {
    selectedModels.delete(modelId);
  } else if (selectedModels.size < 4) {
    selectedModels.add(modelId);
  }
  updateCompareUI();
}

function updateCompareUI() {
  const count = selectedModels.size;
  
  // Update button state
  const compareBtn = document.getElementById('compare-btn');
  compareBtn.disabled = count < 2;
  compareBtn.textContent = `Compare (${count})`;
  
  // Update clear button visibility
  const clearBtn = document.getElementById('clear-btn');
  clearBtn.style.display = count > 0 ? 'inline-block' : 'none';
  
  // Update checkboxes visual state
  document.querySelectorAll('.model-checkbox').forEach(cb => {
    const modelId = cb.dataset.modelId;
    cb.checked = selectedModels.has(modelId);
    
    // Disable unchecked checkboxes if 4 selected
    if (count >= 4 && !selectedModels.has(modelId)) {
      cb.disabled = true;
    } else {
      cb.disabled = false;
    }
  });
}

function clearSelection() {
  selectedModels.clear();
  updateCompareUI();
}

function showComparison() {
  if (selectedModels.size < 2) return;
  
  const models = Array.from(selectedModels).map(id => getModelById(id));
  renderComparisonTable(models);
}
```

### Render Comparison
```javascript
function renderComparisonTable(models) {
  const attributes = [
    { label: 'Context Window', key: 'context_length', format: formatContext, best: 'max' },
    { label: 'Input Price', key: 'priceInputPerMillion', format: formatPricePer1M, best: 'min' },
    { label: 'Output Price', key: 'priceOutputPerMillion', format: formatPricePer1M, best: 'min' },
    { label: 'Input Types', key: 'inputTypes', format: v => v.join(', '), best: 'length' },
    { label: 'Output Types', key: 'outputTypes', format: v => v.join(', ') },
    { label: 'Max Output', key: 'maxOutput', format: formatContext, best: 'max' },
    { label: 'Moderated', key: 'isModerated', format: v => v ? 'Yes' : 'No' },
    { label: 'Released', key: 'createdAt', format: formatDate },
    { label: 'Reasoning', key: 'hasReasoning', format: v => v ? 'Yes' : 'No' },
    { label: 'Tool Use', key: 'hasTools', format: v => v ? 'Yes' : 'No' },
  ];
  
  let html = '<table class="compare-table">';
  
  // Header row with model names
  html += '<tr><th class="attr-label">Attribute</th>';
  models.forEach(m => {
    html += `<th class="model-header">
      <img src="${getProviderLogo(m.providerId)}" width="16" height="16">
      ${m.displayName}<br>
      <span class="provider-name">${m.providerId}</span>
    </th>`;
  });
  html += '</tr>';
  
  // Attribute rows
  attributes.forEach(attr => {
    html += `<tr><td class="attr-label">${attr.label}</td>`;
    
    // Find best value if applicable
    let bestValue = null;
    if (attr.best) {
      const values = models.map(m => m[attr.key]).filter(v => v != null);
      if (attr.best === 'max') bestValue = Math.max(...values);
      if (attr.best === 'min') bestValue = Math.min(...values.filter(v => v > 0));
      if (attr.best === 'length') bestValue = Math.max(...values.map(v => v?.length || 0));
    }
    
    models.forEach(m => {
      const value = m[attr.key];
      const formatted = attr.format ? attr.format(value) : value;
      
      let cellClass = '';
      if (attr.best && value === bestValue) {
        cellClass = 'compare-cell-winner';
      }
      
      html += `<td class="${cellClass}">${formatted}</td>`;
    });
    
    html += '</tr>';
  });
  
  html += '</table>';
  
  document.getElementById('content').innerHTML = `
    <div class="compare-container">
      <h2>Model Comparison</h2>
      ${html}
      <div class="compare-actions">
        <button class="btn" onclick="clearSelection(); showHome();">Done</button>
      </div>
    </div>
  `;
}
```

---

## Responsive Behavior

On smaller screens, table can:
1. Horizontal scroll
2. Or switch to card view (one model per card, stacked)

```css
.compare-container {
  overflow-x: auto;
  padding: 8px;
}

@media (max-width: 700px) {
  .compare-table {
    font-size: 10px;
  }
  
  .compare-table th,
  .compare-table td {
    padding: 2px 4px;
  }
}
```
