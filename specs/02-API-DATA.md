# RouterDex - Données API

## Endpoint

```
GET https://openrouter.ai/api/v1/models
```

- Pas de clé API requise
- Retourne ~600+ modèles
- Format JSON

## Structure réponse

```json
{
  "data": [
    {
      "id": "anthropic/claude-sonnet-4.6",
      "name": "Anthropic: Claude Sonnet 4.6",
      "description": "Sonnet 4.6 is Anthropic's most capable...",
      "created": 1771342990,
      "context_length": 1000000,
      "pricing": {
        "prompt": "0.000003",
        "completion": "0.000015",
        "input_cache_read": "0.0000003"
      },
      "architecture": {
        "modality": "text+image->text",
        "input_modalities": ["text", "image"],
        "output_modalities": ["text"],
        "tokenizer": "Claude"
      },
      "top_provider": {
        "context_length": 1000000,
        "max_completion_tokens": 128000,
        "is_moderated": true
      },
      "supported_parameters": ["temperature", "top_p", "..."]
    }
  ]
}
```

## Mapping des champs

| Champ API | Champ App | Type | Description |
|-----------|-----------|------|-------------|
| `id` | `modelId` | string | ID unique (format: `provider/model-name`) |
| `name` | `displayName` | string | Nom affiché |
| `description` | `description` | string | Description EN |
| `created` | `createdAt` | number | Timestamp Unix |
| `context_length` | `contextWindow` | number | Tokens max |
| `pricing.prompt` | `priceInput` | string | Prix/token input |
| `pricing.completion` | `priceOutput` | string | Prix/token output |
| `architecture.modality` | `modality` | string | Ex: `text+image->text` |
| `architecture.input_modalities` | `inputTypes` | array | `["text", "image", ...]` |
| `architecture.output_modalities` | `outputTypes` | array | `["text", "image", ...]` |
| `top_provider.is_moderated` | `isModerated` | boolean | Modération active |

## Données dérivées (calculées côté client)

| Champ | Calcul | Description |
|-------|--------|-------------|
| `providerId` | `id.split('/')[0]` | Ex: `anthropic` |
| `modelSlug` | `id.split('/')[1]` | Ex: `claude-sonnet-4.6` |
| `priceInputPerMillion` | `parseFloat(priceInput) * 1_000_000` | $/1M tokens input |
| `priceOutputPerMillion` | `parseFloat(priceOutput) * 1_000_000` | $/1M tokens output |
| `isFree` | `priceInput === "0" && priceOutput === "0"` | Modèle gratuit |
| `hasVision` | `inputTypes.includes("image")` | Support images |
| `hasAudio` | `inputTypes.includes("audio")` | Support audio |
| `hasVideo` | `inputTypes.includes("video")` | Support vidéo |
| `category` | Déduit de `modality` | `text`, `multimodal`, `image-gen`, `audio` |
| `createdDate` | `new Date(created * 1000)` | Date lisible |

## Catégories (déduites)

| Catégorie | Condition |
|-----------|-----------|
| `text` | `modality === "text->text"` |
| `multimodal` | `inputTypes` contient `image` ou `video` ou `audio` |
| `image-gen` | `outputTypes` contient `image` |
| `audio` | `outputTypes` contient `audio` |
| `code` | `name` ou `description` contient "code" ou "codex" |
| `reasoning` | `supported_parameters` contient "reasoning" |

## Cache localStorage

```javascript
const CACHE_KEY = 'routerdex_models';
const CACHE_TTL = 24 * 60 * 60 * 1000; // 24h

const cache = {
  data: [...],           // Modèles
  timestamp: Date.now(), // Date fetch
  version: "1.0"         // Version schema
};

localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
```

## Logique de chargement

```
1. Vérifier localStorage
   ├── Cache existe ET < 24h → Utiliser cache
   └── Sinon → Fetch API
       ├── Succès → Sauvegarder cache + Afficher
       └── Échec → Utiliser ancien cache si existe
                   Sinon → Message erreur
```
