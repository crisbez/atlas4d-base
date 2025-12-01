# Natural Language Queries (NLQ)

Atlas4D supports querying your spatiotemporal data using natural language in Bulgarian and English.

## Overview

NLQ translates human questions into database queries, returning formatted results with maps and visualizations.

## Supported Languages

| Language | Status | Examples |
|----------|--------|----------|
| Bulgarian | ✅ Primary | "Какво е времето в Бургас?" |
| English | ✅ Full | "Show threats near Sofia" |
| German | 🔄 Basic | "Zeige Anomalien" |
| Spanish | 🔄 Basic | "Mostrar amenazas" |

## Query Types

### Weather Queries (Fast-Path)
Instant responses (~70ms) without LLM processing.
```
"Какво е времето в Бургас?"
"What's the weather in Sofia?"
"Времето в Пловдив"
```

### Threat Queries
```
"Show threats near Burgas"
"Покажи заплахи в София"
"What are the current threat levels?"
```

### Anomaly Queries
```
"Покажи аномалии от последния час"
"Show anomalies from last 24 hours"
"What anomalies happened near the airport?"
```

### Observation Queries
```
"Show observations from last hour"
"Покажи наблюдения близо до Бургас"
"FROM OBSERVATIONS LAST 1h NEAR 42.5,27.5"
```

### Correlation Queries
```
"Покажи корелации"
"Show fused anomalies"
"What patterns were detected today?"
```

## API Endpoint
```
POST /api/nlq/universal
Content-Type: application/json
Authorization: Bearer <token>
```

### Request Body
```json
{
  "query": "Какво е времето в Бургас?",
  "session_id": "optional-uuid-for-conversation",
  "language": "bg"
}
```

### Response
```json
{
  "intent": "weather_fast",
  "response": "Времето в Бургас: 11.2°C, слънчево",
  "confidence": 0.95,
  "processing_time_ms": 70,
  "badges": ["⚡ fast-path", "🇧🇬 Български"],
  "context_used": false,
  "session_id": "08ef6053-..."
}
```

## Session Handling

NLQ supports multi-turn conversations using `session_id`:
```json
// First query
{"query": "Какво е времето в Бургас?", "session_id": "abc-123"}

// Follow-up (uses context)
{"query": "А в София?", "session_id": "abc-123"}
// → Understands you're asking about weather in Sofia
```

### Context Indicators

| Badge | Meaning |
|-------|---------|
| ⚡ fast-path | Direct response, no LLM needed |
| 🧠 LLM | Processed by language model |
| 📎 context | Used previous conversation context |

## Response Badges

| Badge | Description |
|-------|-------------|
| `weather_fast` | Weather fast-path (70ms) |
| `threats` | Threat assessment query |
| `anomalies` | Anomaly search |
| `observations` | Raw observation query |
| `stsql` | Translated to STSQL |

## Error Handling
```json
{
  "intent": "unknown",
  "response": "Не разбрах въпроса. Опитайте: 'Какво е времето в Бургас?'",
  "confidence": 0.0,
  "error": "Could not parse intent"
}
```

## Performance

| Query Type | Typical Latency |
|------------|-----------------|
| Weather (fast-path) | ~70ms |
| Cached intent | ~40ms |
| LLM processing | 500-2000ms |
| Complex STSQL | 200-500ms |

## Best Practices

1. **Be specific about location**: "в Бургас", "near Sofia"
2. **Specify time ranges**: "от последния час", "from last 24 hours"
3. **Use session_id** for follow-up questions
4. **Start simple**, then refine

## Examples

### Bulgarian Examples
```
"Какво е времето в Бургас?"
"Покажи аномалии от последните 24 часа"
"Има ли заплахи близо до летището?"
"Покажи корелации между сензорите"
"А в София?" (follow-up)
```

### English Examples
```
"What's the weather in Sofia?"
"Show threats near the port"
"Any anomalies in the last hour?"
"Show observations from vehicle sensors"
"What about yesterday?" (follow-up)
```

### STSQL Direct Queries
```
"FROM OBSERVATIONS LAST 24h NEAR 42.5,27.5 LIMIT 100"
"FROM ANOMALIES WHERE severity > 3"
"FROM THREATS LAST 1h"
```
