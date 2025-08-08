# VK PvP Arena

Многопользовательская PvP-арена для VK Mini Apps: FFA (8–12 игроков) и 1v1/2v2. Сервер: FastAPI + WebSocket. Клиент: React + VKUI + Vite. Матчмейкинг с дозаполнением ботами.

## Структура

```
vk-pvp-arena/
  client/                  # VK Mini App (React + VKUI + vk-bridge + Vite)
  backend/                 # FastAPI + Uvicorn + SQLAlchemy + Alembic
  docker/                  # Dockerfiles и nginx
  docker-compose.yml
  .env.example
  README.md
```

## .env
Скопируйте `.env.example` в `.env` и заполните значения. Ключевые переменные:
- VITE_API_BASE, VITE_WS_URL — адреса API и WebSocket
- DATABASE_URL — строка подключения к Postgres
- JWT_SECRET — секрет для JWT

## Локальная разработка

```bash
# dev фронт
cd client && npm install && npm run dev

# dev бэк
cd backend && poetry install && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# миграции
cd backend && alembic upgrade head
```

## Docker/Compose

```bash
cp .env.example .env
# отредактируйте VITE_API_BASE, VITE_WS_URL, JWT_SECRET

docker compose up -d --build

docker compose exec backend alembic upgrade head
```

Nginx слушает `:8080` и раздаёт фронт. `/api` и `/ws` проксируются на backend.

## Деплой

### Вариант A. VPS (Ubuntu 22.04+)

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER && newgrp docker

git clone <repo>
cd vk-pvp-arena
cp .env.example .env
nano .env   # выставить VITE_API_BASE, VITE_WS_URL, JWT_SECRET

docker compose up -d --build

docker compose exec backend alembic upgrade head
```

Доступ: `http://<server>:8080` — фронт; `/api` и `/ws` проксируются на backend.

### Вариант B. Frontend на GitHub Pages + Backend на VPS

```bash
# На VPS поднимите только backend + nginx (без client)
# В .env для client укажите публичные URL VPS:
VITE_API_BASE=https://your-domain/api
VITE_WS_URL=wss://your-domain/ws

# Соберите client локально
cd client
npm ci && npm run build
# Содержимое client/dist загрузите в gh-pages

# На VPS настройте CORS:
BACKEND_CORS_ORIGINS=https://<username>.github.io
```

## Протокол WebSocket

Канал: `/ws`
- Клиент → Сервер:
  - `join { mode: 'ffa'|'duo', token }`
  - `input { seq, dt, move:{x,y}, fire }`
  - `leave {}`
- Сервер → Клиент:
  - `state { t, youId, players, bullets, powerups, mapHash, timeLeft }`
  - `event { type, payload }`
  - `ack { seq }`

Сервер authoritative. Клиент делает интерполяцию и prediction.

## TODO
- Оплата (VK Pay/Stars)
- Анти-чит: rate limit, валидация урона, автокик
- Логи матчей в БД, награды по итогам