# Бърз старт с Atlas4D

## Изисквания

- Docker 24+ и Docker Compose
- 4GB RAM минимум
- Git

## Стъпка 1: Клониране и стартиране
```bash
git clone https://github.com/crisbez/atlas4d-base
cd atlas4d-base
docker compose up -d
```

Изчакайте около 30 секунди за инициализация.

## Стъпка 2: Проверка

Отворете в браузър:
- **Карта:** http://localhost:8091
- **API Health:** http://localhost:8090/health

Или с curl:
```bash
curl http://localhost:8090/health
```

## Стъпка 3: Използване на SDK

Инсталирайте Python SDK:
```bash
pip install atlas4d
```

Примерен код:
```python
from atlas4d import Client

# Свързване
client = Client(host="localhost", port=8090)

# Проверка на здравето
print(client.health())

# Списък с наблюдения
obs = client.observations.list(limit=10)
print(f"Намерени: {len(obs)} наблюдения")

# RAG заявка (документация)
answer = client.ask("Как да създам модул?")
print(answer.text)
```

## Демо данни

Платформата включва примерни данни за Бургас:
- 500+ наблюдения (GPS точки)
- Множество източници (Vehicle GPS, Sensor, Radar)
- 24 часа история

## Отстраняване на проблеми

### Docker не стартира
```bash
docker compose logs postgres
```

### Портът е зает
```bash
# Проверете кой използва порт 8091
lsof -i :8091
```

### Услугите не са здрави
```bash
docker compose ps
docker compose restart
```

## Следващи стъпки

- Прочетете [Архитектурата](../architecture/ARCHITECTURE.md)
- Вижте [API документацията](../api/API_REFERENCE.md)
- Опитайте [NLQ заявки](../api/NLQ_USAGE.md)

## Помощ

- GitHub Issues: https://github.com/crisbez/atlas4d-base/issues
- Дискусии: https://github.com/crisbez/atlas4d-base/discussions
