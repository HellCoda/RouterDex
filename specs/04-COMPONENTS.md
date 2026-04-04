# RouterDex - Composants

## Page Accueil (Leaderboard)

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│                        ROUTERDEX                            │
│              Catalogue des modèles IA OpenRouter            │
├─────────────────────────────────────────────────────────────┤
│  📊 STATISTIQUES                                            │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  │   642   │ │   45    │ │   128   │ │   89    │            │
│  │ Modèles │ │Providers│ │ Gratuits│ │Multimod.│            │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘            │
├─────────────────────────────────────────────────────────────┤
│  🆕 DERNIERS MODÈLES                                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ ByteDance Seed 2.0 Mini    │ bytedance │ 24 Feb 2026│    │
│  │ Gemini 3.1 Flash Image     │ google    │ 26 Feb 2026│    │
│  │ Qwen 3.5 35B               │ qwen      │ 24 Feb 2026│    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  💰 MODÈLES GRATUITS POPULAIRES                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Free Models Router         │ openrouter │ 200K ctx  │    │
│  │ Step 3.5 Flash             │ stepfun    │ 256K ctx  │    │
│  │ Trinity Large Preview      │ arcee-ai   │ 131K ctx  │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  🏆 TOP CONTEXT WINDOW                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 1. Grok 4.1 Fast           │ x-ai      │ 2M tokens  │    │
│  │ 2. Gemini 3 Pro            │ google    │ 1M tokens  │    │
│  │ 3. Claude Opus 4.6         │ anthropic │ 1M tokens  │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  📂 PAR CATÉGORIE                                           │
│  [Text] [Multimodal] [Image Gen] [Audio] [Code] [Reasoning] │
└─────────────────────────────────────────────────────────────┘
```

### Données affichées

**Statistiques** :
- Total modèles
- Total providers
- Modèles gratuits
- Modèles multimodaux

**Leaderboards** :
- 5 derniers modèles (tri par `created` desc)
- 5 modèles gratuits (filtre `isFree`)
- 5 plus grands context (tri par `context_length` desc)

**Catégories** (boutons cliquables) :
- Filtre la sidebar par catégorie

---

## Fiche Modèle

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ANTHROPIC                                          [🔗]    │
│  ═══════════════════════════════════════════════════════    │
│  Claude Sonnet 4.6                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📋 INFORMATIONS                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ ID           │ anthropic/claude-sonnet-4.6         │    │
│  │ Provider     │ Anthropic                           │    │
│  │ Date sortie  │ 17 Février 2026                     │    │
│  │ Modération   │ ✅ Oui                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  💰 TARIFICATION                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Input        │ $3.00 / 1M tokens                   │    │
│  │ Output       │ $15.00 / 1M tokens                  │    │
│  │ Cache read   │ $0.30 / 1M tokens                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ⚙️ CAPACITÉS                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Context      │ 1,000,000 tokens                    │    │
│  │ Max output   │ 128,000 tokens                      │    │
│  │ Modalité     │ text+image → text                   │    │
│  │ Input        │ 📝 Text  🖼️ Image                   │    │
│  │ Output       │ 📝 Text                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  🏷️ TAGS                                                    │
│  [Multimodal] [Vision] [Reasoning] [Tool Use]               │
│                                                             │
│  📖 DESCRIPTION                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Sonnet 4.6 is Anthropic's most capable Sonnet-     │    │
│  │ class model yet, with frontier performance across  │    │
│  │ coding, agents, and professional work...           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  🔧 PARAMÈTRES SUPPORTÉS                                    │
│  temperature, top_p, top_k, max_tokens, stop,               │
│  reasoning, tool_choice, tools, structured_outputs...       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Sections

1. **Header**
   - Provider (petit, uppercase)
   - Nom du modèle (grand, bold)
   - Lien externe OpenRouter

2. **Informations**
   - ID complet
   - Provider
   - Date de sortie (formatée)
   - Modération (oui/non avec icône)

3. **Tarification**
   - Prix input ($/1M tokens)
   - Prix output ($/1M tokens)
   - Autres prix si présents (cache, web_search, etc.)
   - Badge "GRATUIT" si applicable

4. **Capacités**
   - Context window (formaté avec séparateurs)
   - Max output tokens
   - Modalité (format lisible)
   - Types input (icônes)
   - Types output (icônes)

5. **Tags**
   - Badges colorés selon catégorie
   - Cliquables pour filtrer

6. **Description**
   - Texte complet (scrollable si long)
   - Anglais (pas de traduction)

7. **Paramètres**
   - Liste des paramètres supportés
   - Format compact

---

## Composants réutilisables

### Badge

```html
<span class="badge badge-{type}">{text}</span>
```

Types : `free`, `multimodal`, `vision`, `audio`, `code`, `reasoning`

### Stat Card

```html
<div class="stat-card">
  <div class="stat-value">642</div>
  <div class="stat-label">Modèles</div>
</div>
```

### Table Row (Leaderboard)

```html
<div class="leaderboard-row">
  <span class="model-name">Claude Opus 4.6</span>
  <span class="provider">anthropic</span>
  <span class="value">1M tokens</span>
</div>
```

### Provider Item (Sidebar)

```html
<div class="provider-item" data-expanded="false">
  <div class="provider-header">
    <span class="expand-icon">▸</span>
    <span class="provider-name">Anthropic</span>
    <span class="model-count">(12)</span>
  </div>
  <div class="provider-models">
    <div class="model-item" data-id="anthropic/claude-opus-4.6">
      Claude Opus 4.6
    </div>
    <!-- ... -->
  </div>
</div>
```

### Info Row (Fiche)

```html
<div class="info-row">
  <span class="info-label">Context</span>
  <span class="info-value">1,000,000 tokens</span>
</div>
```

---

## États

### Loading

```html
<div class="loading">
  <div class="spinner"></div>
  <span>Chargement des modèles...</span>
</div>
```

### Error

```html
<div class="error">
  <span class="error-icon">⚠️</span>
  <span>Impossible de charger les données</span>
  <button class="retry-btn">Réessayer</button>
</div>
```

### Empty (recherche sans résultats)

```html
<div class="empty">
  <span>Aucun modèle trouvé pour "{query}"</span>
</div>
```

---

## Icônes modalités

| Type | Icône |
|------|-------|
| text | 📝 |
| image | 🖼️ |
| audio | 🔊 |
| video | 🎬 |
| file | 📁 |
| code | 💻 |
