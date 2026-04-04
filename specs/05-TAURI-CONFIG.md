# RouterDex - Configuration Tauri

## Prérequis

- Node.js 18+
- Rust (rustup)
- Tauri CLI : `npm install -g @tauri-apps/cli`

## Initialisation projet

```bash
npm create tauri-app@latest routerdex -- --template vanilla
cd routerdex
npm install
```

## Structure finale

```
routerdex/
├── src-tauri/
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── capabilities/
│   │   └── default.json
│   ├── icons/
│   │   └── icon.png (et variantes)
│   └── src/
│       └── main.rs
├── src/
│   ├── index.html
│   ├── styles/
│   │   └── main.css
│   └── js/
│       └── app.js
├── package.json
└── README.md
```

## tauri.conf.json

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "RouterDex",
  "version": "1.0.0",
  "identifier": "com.routerdex.app",
  "build": {
    "frontendDist": "../src"
  },
  "app": {
    "withGlobalTauri": true,
    "windows": [
      {
        "title": "RouterDex - Catalogue des modèles IA",
        "width": 1200,
        "height": 800,
        "minWidth": 900,
        "minHeight": 600,
        "resizable": true,
        "decorations": false,
        "transparent": false,
        "center": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; connect-src 'self' https://openrouter.ai; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

### Notes config

- `decorations: false` → On gère notre propre barre titre
- `minWidth/minHeight` → Taille minimum de fenêtre
- `csp` → Autorise les appels à openrouter.ai

## Cargo.toml

```toml
[package]
name = "routerdex"
version = "1.0.0"
edition = "2021"

[dependencies]
tauri = { version = "2", features = [] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"

[build-dependencies]
tauri-build = { version = "2", features = [] }
```

## main.rs

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## capabilities/default.json

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "identifier": "default",
  "description": "Default capabilities",
  "windows": ["main"],
  "permissions": [
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-maximize",
    "core:window:allow-start-dragging",
    "core:window:allow-set-size"
  ]
}
```

## package.json

```json
{
  "name": "routerdex",
  "version": "1.0.0",
  "scripts": {
    "dev": "tauri dev",
    "build": "tauri build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^2"
  }
}
```

## Commandes

```bash
# Développement (hot reload)
npm run dev

# Build production
npm run build

# Le binaire sera dans:
# - Windows: src-tauri/target/release/routerdex.exe
# - macOS: src-tauri/target/release/bundle/macos/RouterDex.app
# - Linux: src-tauri/target/release/routerdex
```

## Gestion fenêtre custom (JS)

```javascript
// Dans app.js - API Tauri pour la barre titre custom

const { getCurrentWindow } = window.__TAURI__.window;

const appWindow = getCurrentWindow();

// Boutons de la barre titre
document.getElementById('btn-minimize').addEventListener('click', () => {
  appWindow.minimize();
});

document.getElementById('btn-maximize').addEventListener('click', async () => {
  const isMaximized = await appWindow.isMaximized();
  if (isMaximized) {
    appWindow.unmaximize();
  } else {
    appWindow.maximize();
  }
});

document.getElementById('btn-close').addEventListener('click', () => {
  appWindow.close();
});

// Zone draggable pour déplacer la fenêtre
document.getElementById('titlebar').addEventListener('mousedown', (e) => {
  if (e.target.closest('.titlebar-buttons')) return;
  appWindow.startDragging();
});
```

## Build multi-plateforme

### Windows
```bash
npm run build
# Produit: routerdex_1.0.0_x64-setup.exe (~5MB)
```

### macOS
```bash
npm run build
# Produit: RouterDex.app (~8MB)
```

### Linux
```bash
npm run build
# Produit: routerdex_1.0.0_amd64.deb / .AppImage (~6MB)
```
