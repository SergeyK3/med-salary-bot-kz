# Развёртывание (Docker Compose + Caddy)

Этот сценарий поднимет 3 сервиса:
- api (FastAPI, порт 8000 внутри сети)
- bot (Telegram long polling)
- caddy (reverse proxy c авто-HTTPS для домена)

Требования:
- Ubuntu 22.04+ / 24.04
- Установлен Docker и Docker Compose (плагин)
- Домен kimserg.store указывает A-записью на IP сервера

## 1. Установка Docker

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
. /etc/os-release
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $VERSION_CODENAME stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

(Опционально) добавить пользователя в группу docker и выйти/войти:
```bash
sudo usermod -aG docker $USER
```

## 2. Клонирование проекта

```bash
git clone https://github.com/SergeyK3/med-salary-bot-kz.git
cd med-salary-bot-kz/deploy
```

## 3. Подготовка .env

Создайте файл `deploy/.env` со значениями:
```
TELEGRAM_TOKEN=123456:ABC...  # токен вашего бота
TZ=Asia/Almaty
```

## 4. Проверка DNS

Убедитесь, что домен `kimserg.store` указывает на IP сервера (A-запись). Можно проверить:
```bash
dig +short kimserg.store A
```

## 5. Старт сервисов

```bash
# находясь в каталоге deploy/
docker compose build
docker compose up -d
```

Проверка статуса:
```bash
docker compose ps
```

## 6. Тестирование

- API: https://kimserg.store/docs (Caddy выдаст сертификат Let’s Encrypt автоматически)
- Бот: напишите /start вашему боту в Telegram

Логи:
```bash
docker compose logs -f api
# или
docker compose logs -f bot
# или
docker compose logs -f caddy
```

## 7. Обновление версии

```bash
cd med-salary-bot-kz
git pull
cd deploy
docker compose build
docker compose up -d
```

## 8. Резервное копирование

- Каталог `data/` (в корне репозитория) содержит SQLite и настройки (`settings.yml`). Он монтируется read-only в контейнеры.
- Файл `deploy/.env` с токеном бота и TZ — храните отдельно и не коммитьте в репозиторий.

## Примечания

- Если домен будет другим — замените его в `deploy/Caddyfile` и перезапустите:
```bash
docker compose up -d --force-recreate --no-deps caddy
```
- Если HTTPS не нужен (на время тестов), можно временно не запускать caddy и пробросить порт API наружу, но это не рекомендуется для продакшн.