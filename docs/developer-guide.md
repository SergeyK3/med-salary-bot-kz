# Руководство разработчика

Это руководство поможет разработчикам понять архитектуру проекта и начать разработку.

## Быстрый старт

```mermaid
graph TD
    A[Клонирование репозитория] --> B[Установка зависимостей]
    B --> C[Настройка окружения]
    C --> D[Запуск тестов]
    D --> E[Запуск приложения]
    
    A1[git clone] --> A
    B1[pip install -r requirements.txt] --> B
    C1[Создать .env файл] --> C
    D1[pytest] --> D
    E1[python -m src.api] --> E
```

## Архитектурные слои

```mermaid
graph TB
    subgraph "Слой представления"
        A[Telegram Bot<br/>telegram_bot/main.py]
        B[HTTP API<br/>src/api.py]
    end
    
    subgraph "Слой бизнес-логики"
        C[Контроллер<br/>src/main.py]
        D[Расчёт зарплаты<br/>src/calc/totals.py]
        E[Надбавки<br/>src/calc/allowances.py]
        F[Базовый оклад<br/>src/calc/base_oklad.py]
    end
    
    subgraph "Слой данных"
        G[Загрузчики<br/>src/data_loaders.py]
        H[Конфигурация<br/>src/config.py]
        I[Утилиты<br/>src/utils/]
    end
    
    subgraph "Слой хранения"
        J[(SQLite БД<br/>data/*.sqlite)]
        K[Настройки<br/>data/settings.yml]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    C --> G
    C --> H
    G --> I
    G --> J
    H --> K
```

## Принципы архитектуры

### 1. Разделение ответственности

```mermaid
graph LR
    A[Presentation Layer] --> B[Business Logic Layer]
    B --> C[Data Access Layer]
    C --> D[Storage Layer]
    
    A1[UI/API] --> A
    B1[Calculations] --> B
    C1[Loaders/Config] --> C
    D1[SQLite/YAML] --> D
```

### 2. Модульность

Каждый модуль имеет четко определенную ответственность:

- **src/api.py** - HTTP интерфейс
- **telegram_bot/main.py** - Telegram интерфейс
- **src/main.py** - Координация бизнес-логики
- **src/calc/** - Расчётные модули
- **src/data_loaders.py** - Управление данными
- **src/config.py** - Управление конфигурацией

### 3. Тестируемость

```mermaid
graph TD
    A[Модуль] --> B[Unit Tests]
    A --> C[Integration Tests]
    A --> D[End-to-End Tests]
    
    B --> B1[tests/test_*.py]
    C --> C1[tests/test_api.py]
    D --> D1[telegram_bot/bot_tests/]
```

## Добавление новой функциональности

### Пример: Добавление нового типа надбавки

```mermaid
sequenceDiagram
    participant DEV as Разработчик
    participant DB as База данных
    participant CODE as Код
    participant TEST as Тесты
    
    DEV->>DB: 1. Добавить данные в SQLite
    DEV->>CODE: 2. Обновить src/calc/allowances.py
    DEV->>CODE: 3. Обновить src/data_loaders.py (если нужно)
    DEV->>TEST: 4. Добавить тесты
    DEV->>TEST: 5. Запустить все тесты
    DEV->>CODE: 6. Обновить документацию
```

### Шаги разработки:

1. **Анализ требований**
   - Изучить существующую логику в `src/calc/`
   - Понять структуру данных в `data/*.sqlite`

2. **Изменение данных**
   - Обновить соответствующую SQLite базу
   - Или обновить `data/settings.yml` для конфигурации

3. **Обновление кода**
   - Модифицировать функции в `src/calc/allowances.py`
   - При необходимости обновить `src/data_loaders.py`

4. **Тестирование**
   - Добавить unit тесты в `tests/`
   - Запустить `pytest` для проверки

5. **Интеграция**
   - Проверить работу через `src/api.py`
   - Проверить работу через `telegram_bot/main.py`

## Структура тестирования

```mermaid
graph TD
    A[Тесты] --> B[Unit Tests]
    A --> C[Integration Tests]
    A --> D[Bot Tests]
    
    B --> B1[test_allowances.py<br/>Тесты надбавок]
    B --> B2[test_totals.py<br/>Тесты расчётов]
    B --> B3[test_ets_coeff.py<br/>Тесты коэффициентов]
    
    C --> C1[test_api.py<br/>Тесты API]
    C --> C2[test_data_io.py<br/>Тесты данных]
    
    D --> D1[test_bot_salary_scenarios.py<br/>Тесты бота]
```

## Отладка и диагностика

### Инструменты отладки

```mermaid
graph LR
    A[Проблема] --> B{Тип проблемы}
    
    B --> C[Расчёт зарплаты]
    B --> D[Загрузка данных]
    B --> E[API]
    B --> F[Telegram Bot]
    
    C --> C1[scripts/debug_salary.py]
    D --> D1[scripts/check_sqlite.py]
    E --> E1[Логи FastAPI]
    F --> F1[Логи Telegram]
```

### Использование скриптов отладки:

```bash
# Проверка базы данных
python scripts/check_sqlite.py

# Отладка расчёта зарплаты
python scripts/debug_salary.py

# Быстрые проверки
python scripts/smoke_check.py
```

## Развертывание

```mermaid
graph TD
    A[Код в Git] --> B[CI/CD Pipeline]
    B --> C[Тесты]
    C --> D[Сборка Docker]
    D --> E[Развертывание]
    
    subgraph "GitHub Actions"
        B1[.github/workflows/tests.yml]
        B2[.github/workflows/docker.yml]
    end
    
    B --> B1
    B --> B2
```

## Лучшие практики

1. **Код**
   - Следовать принципам SOLID
   - Использовать типизацию Python
   - Документировать функции docstrings

2. **Тесты**
   - Покрывать новый код тестами
   - Использовать pytest fixtures
   - Тестировать edge cases

3. **Данные**
   - Не изменять SQLite напрямую в продакшене
   - Использовать миграции через скрипты
   - Валидировать данные перед использованием

4. **Документация**
   - Обновлять диаграммы при изменении архитектуры
   - Документировать новые API endpoints
   - Поддерживать актуальность README

Эта архитектура обеспечивает гибкость, maintainability и масштабируемость проекта для расчёта заработной платы медицинских работников Казахстана.