# Atlas4D - Едностраничен преглед

## Какво е Atlas4D?

Atlas4D е отворена платформа за пространствено-времеви данни (4D = 3D пространство + време), изградена върху PostgreSQL с разширения PostGIS, TimescaleDB и pgvector.

## Основни възможности

- **Пространствени заявки** - PostGIS за геолокация, геометрии, H3 хексагони
- **Времеви редове** - TimescaleDB за метрики, събития, сензорни данни
- **Векторно търсене** - pgvector за ML embeddings и семантично търсене
- **Естествени заявки (NLQ)** - питай на български или английски
- **RAG асистент** - документация с AI отговори

## Бърз старт
```bash
git clone https://github.com/crisbez/atlas4d-base
cd atlas4d-base
docker compose up -d
```

След 30 секунди отворете: http://localhost:8091

## Python SDK
```bash
pip install atlas4d
```
```python
from atlas4d import Client

client = Client(host="localhost", port=8090)
print(client.health())

# RAG заявка
answer = client.ask("Какво е Atlas4D?")
print(answer.text)
```

## Модули

Atlas4D поддържа разширяеми модули за различни индустрии:

| Модул | Описание |
|-------|----------|
| **Network Guardian** | Мониторинг на телеком мрежи |
| **Event Risk** | Оценка на риск за събития |
| **Threat Forecasting** | Прогнозиране на заплахи |
| **Wildfire Monitor** | Мониторинг на горски пожари |
| **Crop Analytics** | Анализ на земеделски култури |

## Лиценз

Apache 2.0 - свободен за комерсиална и некомерсиална употреба.

## Връзки

- GitHub: https://github.com/crisbez/atlas4d-base
- PyPI: https://pypi.org/project/atlas4d/
- Документация: https://atlas4d.tech
