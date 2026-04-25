# URL Shortener API

Backend-сервис для сокращения ссылок с TTL, аналитикой кликов, Redis-кэшем и rate limiting.

## Возможности
- Создание короткой ссылки (`custom alias` или авто-генерация).
- Редирект на оригинальный URL.
- TTL для ссылок (истечение срока жизни).
- Счетчик кликов и endpoint статистики.
- Rate limiting по IP.
- Redis-кэш для ускорения разрешения ссылок.

## Стек
- FastAPI, SQLAlchemy 2, PostgreSQL, Alembic
- Redis
- pytest, ruff, GitHub Actions

## Локальный запуск
1. `py -m pip install -e ".[dev]"`
2. Скопировать `.env.example` в `.env`
3. `alembic upgrade head`
4. `uvicorn app.main:app --reload`

## Docker
1. `copy .env.example .env`
2. `docker compose up --build`

## API
- `POST /links`
- `GET /{code}`
- `GET /links/{code}/stats`
- `GET /health`

## CI/CD
- CI (`.github/workflows/ci.yml`): запуск lint и tests на `push`/`pull_request`.
- CD (`.github/workflows/cd.yml`): сборка Docker-образа и публикация в GitHub Container Registry (`ghcr.io`) на каждый push в `main`.

## Техотчет
- `docs/TECH_REPORT.md`
