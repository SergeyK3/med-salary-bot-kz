# Детальная структура файлов проекта

Этот документ содержит подробное описание назначения каждой папки и файла в проекте.

## Корневая структура

```mermaid
graph TD
    A[med-salary-bot-kz/] --> B[📁 src/ - Основной код приложения]
    A --> C[📁 telegram_bot/ - Telegram бот]
    A --> D[📁 data/ - Данные и конфигурация]
    A --> E[📁 docs/ - Документация]
    A --> F[📁 tests/ - Тесты]
    A --> G[📁 scripts/ - Служебные скрипты]
    A --> H[📁 .github/ - CI/CD конфигурация]
    A --> I[📄 README.md - Основная документация]
    A --> J[📄 requirements.txt - Зависимости Python]
    A --> K[📄 Dockerfile - Docker конфигурация]
    A --> L[📄 pyproject.toml - Конфигурация проекта]
```

## Папка src/ - Основной код

```mermaid
graph TD
    A[src/] --> B[📄 __init__.py - Инициализация пакета]
    A --> C[📄 api.py - FastAPI HTTP сервер]
    A --> D[📄 main.py - Основная бизнес-логика]
    A --> E[📄 config.py - Управление конфигурацией]
    A --> F[📄 data_loaders.py - Загрузка данных из SQLite]
    A --> G[📁 calc/ - Модули расчёта зарплаты]
    A --> H[📁 utils/ - Утилиты]
    
    G --> G1[📄 __init__.py]
    G --> G2[📄 totals.py - Итоговый расчёт зарплаты]
    G --> G3[📄 allowances.py - Расчёт надбавок]
    G --> G4[📄 base_oklad.py - Базовый оклад]
    
    H --> H1[📄 __init__.py]
    H --> H2[📄 data_io.py - Ввод/вывод данных]
    H --> H3[📄 data_loader.py - Загрузчик данных]
    
    style C fill:#e1f5fe
    style D fill:#e8f5e8
    style G2 fill:#fff3e0
```

## Папка telegram_bot/ - Telegram бот

```mermaid
graph TD
    A[telegram_bot/] --> B[📄 main.py - Основной код Telegram бота]
    A --> C[📄 README.md - Документация бота]
    A --> D[📄 main.py.bak - Резервная копия]
    A --> E[📁 bot_tests/ - Тесты бота]
    
    E --> E1[📄 test_bot_salary_scenarios.py - Тестовые сценарии]
    
    style B fill:#e1f5fe
```

## Папка data/ - Данные и конфигурация

```mermaid
graph TD
    A[data/] --> B[💾 ets_coefficients.sqlite - Коэффициенты ЕТС]
    A --> C[💾 zones.sqlite - Экологические зоны]
    A --> D[💾 risk_allowances.sqlite - Надбавки за вредность]
    A --> E[⚙️ settings.yml - Базовые параметры БДО, МРП]
    A --> F[📄 ets_coefficients.csv - CSV коэффициенты]
    A --> G[📄 zones.csv - CSV зоны]
    A --> H[📄 risk_allowances.csv - CSV надбавки]
    
    style B fill:#ffecb3
    style C fill:#ffecb3
    style D fill:#ffecb3
    style E fill:#e8f5e8
```

## Папка docs/ - Документация

```mermaid
graph TD
    A[docs/] --> B[📖 README.md - Обзор документации]
    A --> C[📖 architecture.md - Архитектура проекта]
    A --> D[📖 calc-model.md - Модель расчёта зарплаты]
    A --> E[📖 dialogs.md - Сценарии диалогов бота]
    A --> F[📖 TZ.md - Техническое задание]
    
    style C fill:#e3f2fd
```

## Папка tests/ - Тесты

```mermaid
graph TD
    A[tests/] --> B[📄 conftest.py - Конфигурация pytest]
    A --> C[🧪 test_allowances.py - Тесты надбавок]
    A --> D[🧪 test_allowances_more.py - Дополнительные тесты надбавок]
    A --> E[🧪 test_api.py - Тесты FastAPI]
    A --> F[🧪 test_data_io.py - Тесты ввода/вывода]
    A --> G[🧪 test_ets_coeff.py - Тесты коэффициентов ЕТС]
    A --> H[🧪 test_ets_lookup.py - Тесты поиска ЕТС]
    A --> I[🧪 test_k1_amount_zones.py - Тесты зон]
    A --> J[🧪 test_salary_calc.py - Тесты расчёта зарплаты]
    A --> K[🧪 test_salary_multi_calc.py - Тесты множественных расчётов]
    A --> L[🧪 test_totals.py - Тесты итоговых расчётов]
    
    style B fill:#f3e5f5
```

## Папка scripts/ - Служебные скрипты

```mermaid
graph TD
    A[scripts/] --> B[🔧 csv_to_sqlite.py - Конвертация CSV в SQLite]
    A --> C[🔧 csv_to_sqlite_debug.py - Отладочная конвертация]
    A --> D[🔧 zones_csv_to_sqlite.py - Конвертация зон]
    A --> E[🔧 check_sqlite.py - Проверка SQLite БД]
    A --> F[🔧 debug_salary.py - Отладка расчёта зарплаты]
    A --> G[🔧 smoke_check.py - Быстрые проверки]
    A --> H[🔧 check_*.py - Различные проверки]
    A --> I[📜 *.sh - Bash скрипты]
    
    style B fill:#e8f5e8
```

## Взаимодействие основных файлов

```mermaid
graph LR
    subgraph "Пользовательские интерфейсы"
        A[telegram_bot/main.py] 
        B[src/api.py]
    end
    
    subgraph "Бизнес логика"
        C[src/main.py]
        D[src/calc/totals.py]
    end
    
    subgraph "Данные"
        E[src/data_loaders.py]
        F[src/config.py]
    end
    
    subgraph "Хранилище"
        G[(data/*.sqlite)]
        H[data/settings.yml]
    end
    
    A --> C
    B --> C
    C --> D
    C --> E
    C --> F
    E --> G
    F --> H
    
    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

## Роли ключевых файлов

| Файл | Назначение | Тип |
|------|------------|-----|
| `src/main.py` | Основная бизнес-логика расчёта зарплаты | 🏗️ Ядро |
| `src/api.py` | HTTP API интерфейс (FastAPI) | 🌐 API |
| `telegram_bot/main.py` | Telegram бот интерфейс | 🤖 Bot |
| `src/calc/totals.py` | Итоговые расчёты зарплаты | 🧮 Calc |
| `src/calc/allowances.py` | Расчёт надбавок и доплат | 💰 Calc |
| `src/data_loaders.py` | Загрузка данных из SQLite | 📊 Data |
| `src/config.py` | Управление конфигурацией | ⚙️ Config |
| `data/settings.yml` | Базовые параметры (БДО, МРП) | 📋 Config |
| `data/*.sqlite` | База данных коэффициентов | 💾 DB |

## Потоки обработки данных

```mermaid
flowchart TD
    A[Запрос пользователя] --> B{Источник}
    B -->|Telegram| C[telegram_bot/main.py]
    B -->|HTTP API| D[src/api.py]
    
    C --> E[src/main.py calc_salary]
    D --> E
    
    E --> F[src/config.py load_settings]
    E --> G[src/data_loaders.py]
    
    F --> H[data/settings.yml]
    G --> I[data/ets_coefficients.sqlite]
    G --> J[data/zones.sqlite]
    G --> K[data/risk_allowances.sqlite]
    
    E --> L[src/calc/totals.py]
    L --> M[src/calc/allowances.py]
    L --> N[src/calc/base_oklad.py]
    
    M --> O[Результат расчёта]
    N --> O
    
    O --> P{Возврат результата}
    P -->|Telegram| Q[Сообщение в чат]
    P -->|HTTP API| R[JSON ответ]
```

Эта структура обеспечивает модульность, тестируемость и масштабируемость проекта для расчёта заработной платы медицинских работников.