# RouterDex

> Le Pokédex des modèles IA — Catalogue interactif de 642+ modèles via OpenRouter API

---

## 📋 Résumé

**RouterDex** est une application standalone au style rétro (inspirée des fichiers d'aide CHM Windows 2000/XP) qui catalogue l'ensemble des modèles IA disponibles via l'API OpenRouter. L'application se met à jour automatiquement depuis l'API et offre une interface nostalgique mais fonctionnelle pour explorer, comparer et référencer les modèles.

---

## 🎯 Contexte et Motivation

### Le problème
- **642+ modèles IA** disponibles via OpenRouter, difficile de s'y retrouver
- Informations dispersées : prix, context window, capabilities, providers...
- Pas d'outil offline/standalone pour consulter ce catalogue
- Les comparateurs existants sont des sites web classiques, sans âme

### La solution
- Un catalogue **auto-alimenté** par l'API OpenRouter
- Une interface **rétro-geek** (style CHM/Help Windows) qui se démarque
- Fonctionne **offline** après le premier chargement
- **Portable** : un seul fichier HTML ou une app légère

### Pourquoi le style CHM ?
- Nostalgie de la culture geek années 2000
- Interface efficace : sidebar + contenu, pas de bullshit
- Se différencie des dashboards modernes génériques
- Fun à utiliser et à montrer

---

## 🏆 Objectifs

### Objectif principal
Créer un catalogue **dynamique** et **auto-mis à jour** des modèles IA OpenRouter, avec une interface rétro distinctive.

### Objectifs secondaires
1. **Zéro maintenance manuelle** : tout vient de l'API
2. **Portable** : un fichier HTML autonome ou app légère
3. **Rapide** : chargement instantané, recherche fluide
4. **Utile** : vraie valeur ajoutée pour les devs/utilisateurs IA
5. **Partageable** : peut servir de contenu pour article/LinkedIn

---

## 🏗️ Architecture Technique

### Principe de fonctionnement

```
┌─────────────────────────────────────────────────────────────────┐
│                        ROUTERDEX APP                            │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │   UI Layer  │◄──►│  Data Layer │◄──►│  OpenRouter API     │ │
│  │  (HTML/CSS) │    │    (JS)     │    │  /api/v1/models     │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│         │                  │                                    │
│         ▼                  ▼                                    │
│  ┌─────────────┐    ┌─────────────┐                            │
│  │   Render    │    │ LocalStorage│                            │
│  │  Components │    │   (Cache)   │                            │
│  └─────────────┘    └─────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### Flux de données

```
1. APP LAUNCH
   │
   ├─► Vérifier cache local (localStorage)
   │   │
   │   ├─► Cache valide (< 24h) ──► Utiliser données cachées
   │   │
   │   └─► Cache expiré/absent ──► Fetch API OpenRouter
   │                                      │
   │                                      ▼
   │                              Transformer données
   │                                      │
   │                                      ▼
   │                              Sauvegarder en cache
   │                                      │
   └──────────────────────────────────────┘
                    │
                    ▼
            2. RENDER UI
                    │
                    ├─► Générer arborescence providers
                    ├─► Indexer modèles pour recherche
                    └─► Afficher page d'accueil
```

---

## 📡 Données de l'API OpenRouter

### Endpoint principal
```
GET https://openrouter.ai/api/v1/models
```

### Structure de réponse (par modèle)
```json
{
  "id": "anthropic/claude-sonnet-4.5",
  "name": "Claude Sonnet 4.5",
  "description": "...",
  "context_length": 200000,
  "pricing": {
    "prompt": "0.000003",
    "completion": "0.000015"
  },
  "top_provider": {
    "name": "Anthropic",
    "is_moderated": true
  },
  "architecture": {
    "input_modalities": ["text", "image"],
    "output_modalities": ["text"],
    "tokenizer": "claude"
  },
  "supported_parameters": ["temperature", "top_p", "..."],
  "created": 1234567890
}
```

### Données à extraire et normaliser

| Champ API | Champ RouterDex | Description |
|-----------|-----------------|-------------|
| `id` | `modelId` | Identifiant unique (ex: `anthropic/claude-sonnet-4.5`) |
| `name` | `displayName` | Nom affiché |
| `description` | `description` | Description du modèle |
| `context_length` | `contextWindow` | Taille du contexte en tokens |
| `pricing.prompt` | `priceInput` | Prix par token (input) |
| `pricing.completion` | `priceOutput` | Prix par token (output) |
| `top_provider.name` | `providerName` | Nom du provider |
| `architecture.input_modalities` | `inputTypes` | Types d'entrée supportés |
| `architecture.output_modalities` | `outputTypes` | Types de sortie supportés |
| `created` | `createdAt` | Date de création (timestamp) |

### Données dérivées (calculées côté client)

| Champ | Calcul | Description |
|-------|--------|-------------|
| `providerId` | Extrait de `id` (avant le `/`) | Identifiant du provider |
| `priceInputPerMillion` | `priceInput * 1_000_000` | Prix pour 1M tokens input |
| `priceOutputPerMillion` | `priceOutput * 1_000_000` | Prix pour 1M tokens output |
| `isFree` | `priceInput === 0 && priceOutput === 0` | Modèle gratuit ? |
| `hasVision` | `inputTypes.includes('image')` | Supporte les images ? |
| `categories` | Dérivé de `name` + `description` | Tags catégories |

---

## ✨ Fonctionnalités

### MVP (Version 1.0)

| Fonctionnalité | Priorité | Description |
|----------------|----------|-------------|
| **Fetch API** | 🔴 Critique | Récupérer tous les modèles depuis OpenRouter |
| **Cache local** | 🔴 Critique | Stocker en localStorage avec TTL 24h |
| **Arborescence providers** | 🔴 Critique | Sidebar avec liste des providers et leurs modèles |
| **Fiche modèle** | 🔴 Critique | Affichage détaillé d'un modèle sélectionné |
| **Page d'accueil** | 🟡 Important | Stats globales + catégories |
| **Recherche basique** | 🟡 Important | Filtrer par nom de modèle |
| **Style CHM** | 🟡 Important | Look Windows 2000/XP authentique |
| **Responsive minimal** | 🟢 Bonus | Utilisable sur tablette |

### Version 2.0 (Future)

| Fonctionnalité | Description |
|----------------|-------------|
| **Comparateur** | Comparer 2-3 modèles côte à côte |
| **Filtres avancés** | Par prix, context, capabilities |
| **Favoris** | Marquer des modèles en favoris |
| **Mode sombre** | Thème Windows 98 gris foncé |
| **Export** | Exporter sélection en JSON/CSV |
| **PWA** | Installation comme app native |
| **App Electron/Tauri** | Vrai exécutable standalone |

### Version 3.0 (Idées)

| Fonctionnalité | Description |
|----------------|-------------|
| **Historique prix** | Graphique d'évolution des prix |
| **Alertes** | Notification nouveaux modèles |
| **Notes perso** | Ajouter ses notes sur chaque modèle |
| **Intégration API key** | Tester directement un modèle |

---

## 🛠️ Stack Technique

### Option A : HTML/CSS/JS Vanilla (Recommandé pour MVP)
```
Avantages :
  ✅ Un seul fichier, ultra-portable
  ✅ Aucune dépendance
  ✅ Fonctionne partout
  ✅ Facile à partager

Inconvénients :
  ❌ Code peut devenir verbeux
  ❌ Pas de composants réutilisables natifs
```

### Option B : React + Vite (Pour version avancée)
```
Avantages :
  ✅ Code modulaire et maintenable
  ✅ Hot reload pour le dev
  ✅ Écosystème riche

Inconvénients :
  ❌ Build nécessaire
  ❌ Plus lourd
```

### Décision MVP
**→ HTML/CSS/JS Vanilla** avec architecture modulaire :
- Séparation claire : data / ui / utils
- Code commenté et structuré
- Un fichier final compilable si besoin

---

## 📁 Structure des fichiers

```
routerdex/
│
├── PROJECT.md              # Ce document
├── README.md               # Documentation utilisateur
├── CHANGELOG.md            # Historique des versions
│
├── src/
│   ├── index.html          # Point d'entrée + structure HTML
│   ├── styles/
│   │   ├── main.css        # Styles principaux
│   │   ├── chm-theme.css   # Thème Windows CHM
│   │   └── components.css  # Styles des composants
│   │
│   ├── js/
│   │   ├── app.js          # Point d'entrée JS, orchestration
│   │   ├── api.js          # Fetch OpenRouter + cache
│   │   ├── data.js         # Transformation et normalisation
│   │   ├── ui.js           # Rendu de l'interface
│   │   ├── search.js       # Logique de recherche/filtres
│   │   └── utils.js        # Fonctions utilitaires
│   │
│   └── assets/
│       └── icons/          # Icônes providers (SVG/PNG)
│
├── dist/                   # Build final
│   └── routerdex.html      # Fichier unique standalone
│
└── scripts/
    └── build.js            # Script pour bundler en un fichier
```

---

## 🗺️ Roadmap

### Phase 1 : Fondations (Semaine 1)
- [ ] Setup projet + structure fichiers
- [ ] Module API : fetch + cache localStorage
- [ ] Module Data : normalisation des données
- [ ] Tests avec données réelles OpenRouter

### Phase 2 : Interface (Semaine 2)
- [ ] Structure HTML de base (window frame, panels)
- [ ] CSS thème CHM complet
- [ ] Génération dynamique de l'arborescence
- [ ] Affichage fiche modèle

### Phase 3 : Fonctionnalités (Semaine 3)
- [ ] Page d'accueil avec stats
- [ ] Recherche basique
- [ ] Catégories cliquables
- [ ] Polish et bugfix

### Phase 4 : Release (Semaine 4)
- [ ] Build fichier unique
- [ ] Tests cross-browser
- [ ] Documentation README
- [ ] Article de blog / post LinkedIn

---

## 📐 Conventions de code

### Nommage
- **Variables/fonctions** : camelCase (`fetchModels`, `modelData`)
- **Constantes** : UPPER_SNAKE_CASE (`API_URL`, `CACHE_TTL`)
- **Classes CSS** : kebab-case (`tree-node`, `model-card`)
- **Fichiers** : kebab-case (`chm-theme.css`)

### Commentaires
```javascript
// === SECTION NAME === //

/**
 * Description de la fonction
 * @param {Type} param - Description
 * @returns {Type} Description
 */
function example(param) {
  // Commentaire inline si nécessaire
}
```

### Structure des fonctions
```javascript
// 1. Imports / Dependencies (si modules)
// 2. Constants
// 3. State / Variables
// 4. Init / Setup functions
// 5. Core logic functions
// 6. UI functions
// 7. Event handlers
// 8. Utility functions
// 9. Bootstrap / Entry point
```

---

## 🔗 Ressources

### API OpenRouter
- Documentation : https://openrouter.ai/docs
- Endpoint models : https://openrouter.ai/api/v1/models
- Liste des modèles : https://openrouter.ai/models

### Inspiration design CHM
- Windows 2000 UI Guidelines
- Screenshots vieux fichiers .chm
- WinClassic theme references

### Outils
- LocalStorage API : https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
- Fetch API : https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

## 📝 Notes

### Limitations connues
- L'API OpenRouter est publique mais peut avoir des rate limits
- Certains providers peuvent ne pas avoir de logo officiel
- Les prix changent fréquemment, le cache de 24h est un compromis

### Questions ouvertes
- [ ] Faut-il une clé API pour fetch les modèles ? (À vérifier)
- [ ] Quel fallback si l'API est down ? (Données statiques ?)
- [ ] Hébergement du fichier final ? (GitHub Pages, site perso)

---

*Document créé le 08/03/2026 — RouterDex v0.1*
