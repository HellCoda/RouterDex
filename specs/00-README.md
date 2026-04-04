# RouterDex - Instructions de développement

## Pour le développeur (Claude/AI)

Ce document résume les specs pour implémenter RouterDex. Lis les fichiers dans l'ordre :

1. `01-OVERVIEW.md` - Vue d'ensemble
2. `02-API-DATA.md` - Structure des données API
3. `03-UI-DESIGN.md` - Design et layout
4. `04-COMPONENTS.md` - Détail des composants
5. `05-TAURI-CONFIG.md` - Configuration Tauri

## Ordre d'implémentation recommandé

### Phase 1 : Setup Tauri
1. Créer le projet Tauri vanilla
2. Configurer `tauri.conf.json` (fenêtre sans décorations)
3. Vérifier que `npm run dev` fonctionne

### Phase 2 : Structure HTML
1. Créer le layout de base dans `index.html`
   - Barre titre custom
   - Menu bar
   - Sidebar
   - Zone contenu
   - Status bar
2. Ajouter les styles de base dans `main.css`

### Phase 3 : Logique JS
1. Module API : fetch + cache localStorage
2. Module Data : transformation des données
3. Module UI : rendu dynamique
4. Connecter les événements (click, recherche)

### Phase 4 : Pages
1. Page Accueil (leaderboard)
2. Fiche Modèle
3. Navigation sidebar

### Phase 5 : Polish
1. Gestion erreurs
2. États loading
3. Animations
4. Tests cross-platform

## Fichiers à créer

```
src/
├── index.html      # Structure HTML complète
├── styles/
│   └── main.css    # Tous les styles (un seul fichier)
└── js/
    └── app.js      # Toute la logique (un seul fichier)
```

## Points d'attention

### API OpenRouter
- Endpoint : `https://openrouter.ai/api/v1/models`
- Pas de clé API nécessaire
- Retourne `{ data: [...] }`

### Cache
- Clé : `routerdex_models`
- TTL : 24 heures
- Fallback sur ancien cache si API échoue

### Barre titre custom
- `decorations: false` dans tauri.conf.json
- Utiliser l'API Tauri pour minimize/maximize/close
- Zone draggable pour déplacer

### Performance
- 600+ modèles → utiliser DocumentFragment pour le DOM
- Recherche → debounce 300ms
- Sidebar → lazy render des sous-items

## Conventions

- Anglais pour l'interface
- Camelcase pour JS
- Kebab-case pour CSS
- Commentaires en anglais

## Résultat attendu

Une application desktop qui :
- Se lance en double-cliquant sur l'exe
- Affiche immédiatement les données (depuis cache ou API)
- Permet de naviguer dans les providers/modèles
- Affiche les fiches détaillées
- Fonctionne offline après premier chargement
