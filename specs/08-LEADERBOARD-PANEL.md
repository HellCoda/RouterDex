# Leaderboard Panel — Spec

## Objectif

Remplacer le placeholder "Leaderboard" actuel dans la page d'accueil par un vrai panneau affichant les 20 modèles ET 20 apps les plus utilisés sur OpenRouter, avec un toggle pour switcher entre les deux vues.

---

## Source de données

Fichier JSON fetchable depuis GitHub Raw :
```
https://raw.githubusercontent.com/<user>/routerdex-data/main/leaderboard.json
```

Le fichier JSON est également stocké localement dans `src/data/leaderboard.json` pour le développement.

### Structure du JSON

```json
{
  "updated": "2026-03-10T12:00:06Z",
  "source": "https://openrouter.ai/rankings",
  "scraper_version": "1.1",
  "top_models": [
    {
      "rank": 1,
      "model_id": "minimax/minimax-m2.5-20260211",
      "name": "Minimax M2.5",
      "provider": "minimax",
      "tokens": "1.94T",
      "tokens_raw": 1940000000000,
      "change_pct": 24
    }
  ],
  "top_apps": [
    {
      "rank": 1,
      "name": "OpenClaw",
      "url": "https://openclaw.ai/",
      "description": "The AI that actually does things",
      "tokens": "422B",
      "tokens_raw": 422000000000
    }
  ]
}
```

---

## Emplacement

Le panneau Leaderboard existe déjà dans `HOME_PANELS` (app.js ligne ~180) avec `placeholder: true`. Il faut :
1. Supprimer le placeholder
2. Implémenter le rendu réel avec toggle Models/Apps

Le panneau occupe `grid-area: leaderboard` (2 colonnes de large, 2 lignes de haut).

---

## UI/UX

### Layout du panneau

```
┌─────────────────────────────────────────────────────────────┐
│  🏆 Leaderboard                              Updated: 2h ago│
├─────────────────────────────────────────────────────────────┤
│  [ Models ]  [ Apps ]                      ← Toggle buttons │
├─────────────────────────────────────────────────────────────┤
│  1.  🥇 Minimax M2.5        minimax    1.94T    ▲ 24%       │
│  2.  🥈 Gemini 3 Flash      google     1.02T    ▲ 18%       │
│  3.  🥉 Deepseek V3.2       deepseek   867B     —           │
│  4.     Claude Opus 4.6     anthropic  770B     ▲ 10%       │
│  ...                                                         │
│  20.    ...                                                  │
└─────────────────────────────────────────────────────────────┘
```

### Toggle Models / Apps

- Deux boutons côte à côte dans le header ou juste en dessous
- Style actif : `background: var(--accent); color: #fff;`
- Style inactif : `background: transparent; border: 1px solid var(--border); color: var(--text);`
- Transition douce au switch (fade 150ms)
- Par défaut : "Models" sélectionné

### Affichage Models (20 lignes)

Chaque ligne affiche :

| Élément | Style |
|---------|-------|
| **Rank** | `1.` `2.` etc. — Les 3 premiers avec médailles 🥇🥈🥉 (optionnel) ou juste en gras |
| **Name** | Nom du modèle, `font-weight: 500`, couleur `var(--text)` |
| **Provider** | Badge petit comme `.panel-row-provider` existant |
| **Tokens** | Texte monospace bleu `var(--accent)` — ex: "1.94T" |
| **Change %** | `▲ 24%` vert si positif, `▼ 5%` rouge si négatif, `—` si 0 |

**Clic sur une ligne** → `selectModel(model_id)` pour ouvrir la page détail du modèle (réutiliser la logique existante).

### Affichage Apps (20 lignes)

Chaque ligne affiche :

| Élément | Style |
|---------|-------|
| **Rank** | `1.` `2.` etc. |
| **Name** | Nom de l'app, `font-weight: 500` |
| **Description** | Texte secondaire tronqué, `color: var(--text-secondary)`, `font-size: 11px` |
| **Tokens** | Monospace bleu |

**Clic sur une ligne** → `window.open(url, '_blank')` pour ouvrir le site de l'app.

### Header du panneau

Modifier le header pour inclure :
- Icône + titre "Leaderboard"
- Texte "Updated: X ago" aligné à droite (calculé depuis `data.updated`)

---

## Implémentation

### 1. Nouveau fichier : `src/data/leaderboard.json`

Créer le dossier `src/data/` et y placer le fichier JSON pour le dev local.

### 2. Modifications dans `app.js`

#### a) Ajouter le fetch du leaderboard

```javascript
const LEADERBOARD_URL = 'https://raw.githubusercontent.com/<user>/routerdex-data/main/leaderboard.json';

let leaderboardData = null;

async function fetchLeaderboard() {
  try {
    const res = await fetch(LEADERBOARD_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    leaderboardData = await res.json();
  } catch (err) {
    console.warn('Leaderboard fetch failed:', err);
    leaderboardData = null;
  }
}
```

Appeler `fetchLeaderboard()` dans `loadData()` en parallèle du fetch des modèles.

#### b) Modifier le panneau Leaderboard dans `HOME_PANELS`

Supprimer `placeholder: true` et ajouter une logique de rendu custom.

#### c) Fonction de rendu

```javascript
function renderLeaderboardPanel(container) {
  if (!leaderboardData) {
    container.innerHTML = '<div class="panel-placeholder">Unable to load leaderboard</div>';
    return;
  }

  const { top_models, top_apps, updated } = leaderboardData;
  
  // Calculer "Updated X ago"
  const updatedAgo = formatTimeAgo(new Date(updated));

  container.innerHTML = `
    <div class="leaderboard-header">
      <div class="leaderboard-toggle">
        <button class="leaderboard-tab active" data-tab="models">Models</button>
        <button class="leaderboard-tab" data-tab="apps">Apps</button>
      </div>
      <span class="leaderboard-updated">Updated: ${updatedAgo}</span>
    </div>
    <div class="leaderboard-content" id="leaderboard-models"></div>
    <div class="leaderboard-content hidden" id="leaderboard-apps"></div>
  `;

  // Render models
  renderLeaderboardModels(container.querySelector('#leaderboard-models'), top_models);
  
  // Render apps
  renderLeaderboardApps(container.querySelector('#leaderboard-apps'), top_apps);

  // Toggle logic
  container.querySelectorAll('.leaderboard-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      container.querySelectorAll('.leaderboard-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const target = tab.dataset.tab;
      container.querySelector('#leaderboard-models').classList.toggle('hidden', target !== 'models');
      container.querySelector('#leaderboard-apps').classList.toggle('hidden', target !== 'apps');
    });
  });
}

function renderLeaderboardModels(container, models) {
  container.innerHTML = models.map(m => `
    <div class="panel-row leaderboard-row" data-model-id="${m.model_id}">
      <span class="panel-row-rank">${m.rank}.</span>
      <span class="panel-row-name">${m.name}</span>
      <span class="panel-row-provider">
        <img src="/src/assets/providers/${m.provider}.svg" width="12" height="12" alt="" onerror="this.style.display='none'" />
        ${m.provider}
      </span>
      <span class="panel-row-value">${m.tokens}</span>
      <span class="leaderboard-change ${m.change_pct > 0 ? 'up' : m.change_pct < 0 ? 'down' : ''}">${formatChange(m.change_pct)}</span>
    </div>
  `).join('');

  container.querySelectorAll('.leaderboard-row').forEach(row => {
    row.addEventListener('click', () => selectModel(row.dataset.modelId));
  });
}

function renderLeaderboardApps(container, apps) {
  container.innerHTML = apps.map(a => `
    <div class="panel-row leaderboard-row" data-url="${a.url}">
      <span class="panel-row-rank">${a.rank}.</span>
      <span class="panel-row-name">${a.name}</span>
      <span class="leaderboard-desc">${a.description}</span>
      <span class="panel-row-value">${a.tokens}</span>
    </div>
  `).join('');

  container.querySelectorAll('.leaderboard-row').forEach(row => {
    row.addEventListener('click', () => window.open(row.dataset.url, '_blank'));
  });
}

function formatChange(pct) {
  if (pct > 0) return `▲ ${pct}%`;
  if (pct < 0) return `▼ ${Math.abs(pct)}%`;
  return '—';
}

function formatTimeAgo(date) {
  const now = new Date();
  const diff = now - date;
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(hours / 24);
  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  return 'just now';
}
```

### 3. Styles à ajouter dans `main.css`

```css
/* ============================================================
   LEADERBOARD PANEL
   ============================================================ */

.leaderboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  border-bottom: 1px solid var(--card-border);
  background: var(--card-bg);
}

.leaderboard-toggle {
  display: flex;
  gap: 4px;
}

.leaderboard-tab {
  padding: 4px 12px;
  border: 1px solid var(--border);
  border-radius: 3px;
  background: transparent;
  color: var(--text);
  font-family: var(--font);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 150ms ease;
}

.leaderboard-tab:hover {
  background: var(--bg-hover);
}

.leaderboard-tab.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.leaderboard-updated {
  font-size: 10px;
  color: var(--text-secondary);
}

.leaderboard-content {
  max-height: calc(100% - 50px);
  overflow-y: auto;
}

.leaderboard-row {
  cursor: pointer;
}

.leaderboard-change {
  font-size: 11px;
  font-family: var(--font-mono);
  min-width: 50px;
  text-align: right;
  color: var(--text-secondary);
}

.leaderboard-change.up {
  color: #28a745;
}

.leaderboard-change.down {
  color: #dc3545;
}

.leaderboard-desc {
  flex: 1;
  font-size: 11px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-right: 8px;
}
```

---

## Résumé des fichiers à modifier/créer

| Fichier | Action |
|---------|--------|
| `src/data/leaderboard.json` | Créer (copier le JSON du scraper) |
| `src/js/app.js` | Ajouter fetch + fonctions de rendu |
| `src/styles/main.css` | Ajouter styles leaderboard |

---

## Notes importantes

- Respecter le style existant : couleurs `var(--accent)`, `var(--text)`, `var(--border)`, etc.
- Utiliser les classes existantes `.panel-row`, `.panel-row-rank`, `.panel-row-name`, `.panel-row-value` quand possible
- Le panneau doit être scrollable si le contenu dépasse
- Animation fade 150ms sur le switch Models/Apps
- Clic sur un modèle → ouvre la page détail (fonction `selectModel()` existante)
- Clic sur une app → ouvre l'URL dans un nouvel onglet
