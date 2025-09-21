# med-salary-bot-kz

[![tests](https://github.com/SergeyK3/med-salary-bot-kz/actions/workflows/tests.yml/badge.svg)](https://github.com/SergeyK3/med-salary-bot-kz/actions/workflows/tests.yml)

## О проекте
Бот и HTTP API для расчёта типовой заработной платы медицинских работников Казахстана.

### Ключевые изменения
- **Тесты**: поддержка async-тестов через `pytest-asyncio`.

## HTTP API (FastAPI)
Сервис можно запускать как HTTP-API для интеграции с ботом, фронтендом или curl.

### Установка и запуск
```bash
pip install -r requirements.txt
python -m src.api
```

## Структура данных
- `data/ets_coefficients.sqlite` — коэффициенты ЕТС
- `data/zones.sqlite` — экологические зоны
- `data/risk_allowances.sqlite` — вредные условия
- `data/settings.yml` — базовые параметры (БДО, МРП, коэффициенты)

## Документация
- [docs/calc-model.md](docs/calc-model.md) — формулы и примеры расчёта
- [docs/dialogs.md](docs/dialogs.md) — сценарии диалогов бота
- [docs/TZ.md](docs/TZ.md) — техническое задание

## Лицензия
MIT
