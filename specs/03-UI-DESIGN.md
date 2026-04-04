# RouterDex - Design UI

## Concept visuel

**Style CHM Windows modernisé** : Structure classique (sidebar + contenu) mais avec palette moderne et épurée.

## Layout principal

```
┌─────────────────────────────────────────────────────────────────┐
│ [icon] RouterDex                              [─] [□] [×]       │  ← Barre titre
├─────────────────────────────────────────────────────────────────┤
│ Fichier   Affichage   Aide                                      │  ← Menu bar
├─────────────────┬───────────────────────────────────────────────┤
│                 │                                               │
│   SIDEBAR       │              CONTENU                          │
│                 │                                               │
│  ▸ Anthropic    │   [Page Accueil / Fiche Modèle]               │
│    └ Claude...  │                                               │
│  ▸ OpenAI       │                                               │
│    └ GPT-5...   │                                               │
│  ▸ Google       │                                               │
│    └ Gemini...  │                                               │
│                 │                                               │
│  [Recherche]    │                                               │
│                 │                                               │
├─────────────────┴───────────────────────────────────────────────┤
│ 642 modèles | Dernière mise à jour: 08/03/2026 14:32            │  ← Status bar
└─────────────────────────────────────────────────────────────────┘
```

## Palette de couleurs

| Élément | Couleur | Hex |
|---------|---------|-----|
| Fond fenêtre | Blanc | `#FFFFFF` |
| Fond sidebar | Gris très clair | `#F5F5F5` |
| Bordures | Gris moyen | `#D0D0D0` |
| Texte principal | Noir | `#1A1A1A` |
| Texte secondaire | Gris | `#666666` |
| Accent / liens | Bleu | `#0066CC` |
| Hover | Bleu clair | `#E8F0FE` |
| Sélection active | Bleu | `#CCE0FF` |
| Barre titre | Blanc/gris clair | `#F0F0F0` |
| Boutons fenêtre | Gris | `#888888` |

## Typographie

| Élément | Police | Taille | Poids |
|---------|--------|--------|-------|
| Titres | Segoe UI / system | 18px | 600 |
| Sous-titres | Segoe UI | 14px | 600 |
| Corps | Segoe UI | 13px | 400 |
| Code/monospace | Consolas / monospace | 12px | 400 |
| Sidebar items | Segoe UI | 13px | 400 |
| Status bar | Segoe UI | 11px | 400 |

## Composants

### Barre titre (32px hauteur)

```
┌─────────────────────────────────────────────────────────────┐
│ [📘] RouterDex - Catalogue des modèles IA    [─] [□] [×]    │
└─────────────────────────────────────────────────────────────┘
```

- Icône 16x16 à gauche
- Titre centré ou à gauche
- Boutons 32x32 à droite (minimize, maximize, close)
- Draggable pour déplacer fenêtre

### Menu bar (24px hauteur)

```
┌─────────────────────────────────────────────────────────────┐
│ Fichier   Affichage   Aide                                  │
└─────────────────────────────────────────────────────────────┘
```

Menus :
- **Fichier** : Actualiser, Exporter JSON, Quitter
- **Affichage** : Accueil, Tous les modèles, Gratuits, Par catégorie
- **Aide** : À propos, Documentation OpenRouter

### Sidebar (250px largeur)

```
┌─────────────────────┐
│ 🔍 Rechercher...    │  ← Input recherche
├─────────────────────┤
│ 🏠 Accueil          │  ← Lien accueil
├─────────────────────┤
│ PROVIDERS           │  ← Section header
│ ▸ Anthropic (12)    │  ← Provider expandable
│   ├ Claude Opus 4.6 │  ← Model item
│   ├ Claude Sonnet.. │
│   └ Claude Haiku..  │
│ ▸ OpenAI (45)       │
│ ▸ Google (28)       │
│ ▸ Meta (8)          │
│ ▸ Mistral (15)      │
│ ...                 │
└─────────────────────┘
```

- Scroll vertical si nécessaire
- Providers triés alphabétiquement
- Compteur de modèles par provider
- Click provider → expand/collapse
- Click model → affiche fiche

### Zone contenu

Variable selon la page :
- Page Accueil (Leaderboard)
- Fiche Modèle

### Status bar (20px hauteur)

```
┌─────────────────────────────────────────────────────────────┐
│ 642 modèles | Mis à jour: 08/03/2026 14:32 | ● En ligne     │
└─────────────────────────────────────────────────────────────┘
```

## Responsive

- **Largeur min** : 900px
- **Hauteur min** : 600px
- Sidebar collapsible sous 1000px (icône hamburger)

## Animations

Subtiles et rapides :
- Hover sur items : 150ms ease
- Expand/collapse providers : 200ms ease-out
- Transition de pages : 150ms fade

## Accessibilité

- Navigation clavier (Tab, Enter, Arrows)
- Focus visible
- Contraste suffisant (WCAG AA)
