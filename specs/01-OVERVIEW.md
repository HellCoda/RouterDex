# RouterDex - Spécifications Techniques

## Vue d'ensemble

**RouterDex** est une application desktop standalone (Tauri) qui catalogue les 600+ modèles IA disponibles via l'API OpenRouter. Interface style CHM Windows modernisé.

## Livrable final

- **Un seul fichier exécutable** (.exe Windows, .app Mac, binaire Linux)
- Taille estimée : 5-10 MB
- Fonctionne offline après premier chargement

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Framework desktop | Tauri 2.x |
| Backend | Rust (minimal, juste fenêtre + cache) |
| Frontend | HTML + CSS + JavaScript vanilla |
| Cache | LocalStorage (TTL 24h) |
| API | OpenRouter `/api/v1/models` |

## Fonctionnalités MVP

1. **Fetch API** : Récupérer tous les modèles OpenRouter
2. **Cache local** : Stocker avec TTL 24h, fallback offline
3. **Sidebar providers** : Arborescence Provider > Models
4. **Fiche modèle** : Template unique rempli dynamiquement
5. **Page accueil** : Leaderboard / tendances
6. **Recherche** : Filtrer par nom
7. **Barre titre custom** : Icône + titre + boutons min/max/close
8. **Menu bar** : Fichier, Affichage, Aide

## Structure des fichiers

```
routerdex/
├── src-tauri/
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   └── src/
│       └── main.rs
├── src/
│   ├── index.html
│   ├── styles/
│   │   └── main.css
│   └── js/
│       └── app.js
├── package.json
└── specs/
    ├── 01-OVERVIEW.md (ce fichier)
    ├── 02-API-DATA.md
    ├── 03-UI-DESIGN.md
    └── 04-COMPONENTS.md
```
