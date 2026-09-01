# Архитектура проекта med-salary-bot-kz

Этот документ описывает архитектуру папок и файлов проекта с использованием диаграмм.

## Обзор архитектуры

Проект представляет собой систему для расчёта заработной платы медицинских работников Казахстана, состоящую из:
- HTTP API (FastAPI)
- Telegram Bot
- Модулей расчёта зарплаты
- Базы данных SQLite
- Документации и тестов

## Структура папок проекта

```mermaid
graph TD
    A[med-salary-bot-kz] --> B[src/]
    A --> C[telegram_bot/]
    A --> D[data/]
    A --> E[docs/]
    A --> F[tests/]
    A --> G[scripts/]
    A --> H[.github/]
    
    B --> B1[api.py - FastAPI сервер]
    B --> B2[main.py - основная логика]
    B --> B3[config.py - конфигурация]
    B --> B4[data_loaders.py - загрузка данных]
    B --> B5[calc/ - модули расчёта]
    B --> B6[utils/ - утилиты]
    
    B5 --> B51[totals.py - итоговые расчёты]
    B5 --> B52[allowances.py - надбавки]
    B5 --> B53[base_oklad.py - базовый оклад]
    
    B6 --> B61[data_io.py - ввод/вывод данных]
    B6 --> B62[data_loader.py - загрузчик данных]
    
    C --> C1[main.py - Telegram бот]
    C --> C2[README.md - документация бота]
    C --> C3[bot_tests/ - тесты бота]
    
    D --> D1[ets_coefficients.sqlite - коэффициенты ЕТС]
    D --> D2[zones.sqlite - экологические зоны]
    D --> D3[risk_allowances.sqlite - вредные условия]
    D --> D4[settings.yml - настройки]
    D --> D5[*.csv - CSV данные]
    
    E --> E1[README.md - обзор документации]
    E --> E2[calc-model.md - модель расчёта]
    E --> E3[dialogs.md - диалоги бота]
    E --> E4[TZ.md - техзадание]
    
    F --> F1[test_*.py - тесты модулей]
    F --> F2[conftest.py - конфигурация тестов]
    
    G --> G1[*.py - скрипты обслуживания]
    G --> G2[*.sh - bash скрипты]
    
    H --> H1[workflows/ - CI/CD]
```

## Архитектура компонентов

```mermaid
graph LR
    A[Пользователь] --> B[Telegram Bot]
    A --> C[HTTP API]
    
    B --> D[src/main.py]
    C --> D
    
    D --> E[calc/totals.py]
    D --> F[data_loaders.py]
    
    E --> G[calc/allowances.py]
    E --> H[calc/base_oklad.py]
    
    F --> I[(SQLite БД)]
    F --> J[settings.yml]
    
    I --> I1[ets_coefficients.sqlite]
    I --> I2[zones.sqlite] 
    I --> I3[risk_allowances.sqlite]
    
    K[config.py] --> J
    K --> D
    
    L[tests/] --> D
    L --> E
    L --> G
    L --> H
```

## Поток данных

```mermaid
sequenceDiagram
    participant U as Пользователь
    participant TB as Telegram Bot
    participant API as FastAPI
    participant CALC as calc/totals.py
    participant DL as data_loaders.py
    participant DB as SQLite БД
    participant CFG as settings.yml
    
    U->>TB: Ввод данных через диалог
    TB->>API: POST /calc
    API->>CALC: calc_salary(params)
    
    CALC->>DL: Загрузка коэффициентов ЕТС
    DL->>DB: Запрос ets_coefficients.sqlite
    DB-->>DL: Данные коэффициентов
    DL-->>CALC: Коэффициенты ЕТС
    
    CALC->>DL: Загрузка зон и рисков
    DL->>DB: Запрос zones.sqlite, risk_allowances.sqlite
    DB-->>DL: Данные зон и рисков
    DL-->>CALC: Зоны и риски
    
    CALC->>CFG: Загрузка базовых параметров
    CFG-->>CALC: БДО, МРП, коэффициенты
    
    CALC->>CALC: Расчёт зарплаты
    CALC-->>API: Результат расчёта
    API-->>TB: JSON ответ
    TB-->>U: Результат расчёта
```

## Жизненный цикл данных

```mermaid
graph TD
    A[CSV файлы] --> B[scripts/csv_to_sqlite.py]
    B --> C[(SQLite БД)]
    
    D[settings.yml] --> E[config.py]
    E --> F[src/main.py]
    
    C --> G[data_loaders.py]
    G --> F
    
    F --> H[calc/totals.py]
    H --> I[Результат расчёта]
    
    J[tests/] --> K[Валидация]
    K --> F
    K --> H
    
    L[scripts/] --> M[Обслуживание БД]
    M --> C
```

## Модульная архитектура

```mermaid
graph TD
    subgraph "Внешний интерфейс"
        A[telegram_bot/main.py]
        B[src/api.py]
    end
    
    subgraph "Бизнес-логика"
        C[src/main.py]
        D[src/calc/totals.py]
        E[src/calc/allowances.py]
        F[src/calc/base_oklad.py]
    end
    
    subgraph "Данные и конфигурация"
        G[src/data_loaders.py]
        H[src/config.py]
        I[src/utils/]
    end
    
    subgraph "Хранилище данных"
        J[(data/ets_coefficients.sqlite)]
        K[(data/zones.sqlite)]
        L[(data/risk_allowances.sqlite)]
        M[data/settings.yml]
    end
    
    subgraph "Поддержка разработки"
        N[tests/]
        O[scripts/]
        P[docs/]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    C --> G
    C --> H
    G --> J
    G --> K
    G --> L
    H --> M
    N --> C
    N --> D
    O --> J
    O --> K
    O --> L
```

## Зависимости файлов

```mermaid
graph LR
    subgraph "Основные модули"
        A[src/main.py] --> B[src/calc/totals.py]
        A --> C[src/data_loaders.py]
        A --> D[src/config.py]
        
        B --> E[src/calc/allowances.py]
        B --> F[src/calc/base_oklad.py]
        
        C --> G[src/utils/data_io.py]
        C --> H[src/utils/data_loader.py]
    end
    
    subgraph "API и Bot"
        I[src/api.py] --> A
        J[telegram_bot/main.py] --> A
    end
    
    subgraph "Данные"
        C --> K[(data/*.sqlite)]
        D --> L[data/settings.yml]
    end
    
    subgraph "Тесты"
        M[tests/test_*.py] --> A
        M --> B
        M --> E
        M --> F
    end
```

## Развертывание и запуск

```mermaid
graph TD
    A[Разработчик] --> B[git clone]
    B --> C[pip install -r requirements.txt]
    
    C --> D{Режим запуска}
    
    D --> E[HTTP API]
    D --> F[Telegram Bot]
    D --> G[Тесты]
    
    E --> H[python -m src.api]
    F --> I[python telegram_bot/main.py]
    G --> J[pytest]
    
    H --> K[FastAPI сервер :8000]
    I --> L[Telegram Bot активен]
    J --> M[Отчёт о тестах]
    
    N[Docker] --> O[Dockerfile]
    O --> P[Контейнер приложения]
```

Эта документация предоставляет полное представление об архитектуре проекта, включая структуру папок, взаимодействие компонентов, поток данных и зависимости между модулями.