# Словарь (Dictionary)

Простой сервис «Словарь»: поиск перевода слов, добавление новых слов и просмотр всех записей.

## Стек

- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2 (async), psycopg3
- **Frontend:** HTML + vanilla JS (без сборки), nginx
- **БД:** PostgreSQL 16
- **Оркестрация:** Docker Compose

## Структура

```
.
├── backend/            # FastAPI-приложение
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/           # статика + nginx-прокси
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
├── openapi.yaml        # OpenAPI 3.0 спецификация
├── docker-compose.yml
└── .env.example
```

## Запуск

1. Создайте `.env` по образцу `.env.example`:
   ```
   POSTGRES_USER=dictionary
   POSTGRES_PASSWORD=dictionary
   POSTGRES_DB=dictionary
   ```
2. Запустите:
   ```bash
   docker compose up --build
   ```

Сервисы:

| Сервис | Адрес |
|---|---|
| Frontend | http://localhost:8080 |
| Backend / Swagger | http://localhost:8000/docs |
| PostgreSQL | localhost:5433 |

Порядок запуска: `postgres` (healthcheck) → `backend` (healthcheck) → `frontend`.

## API

| Метод | Путь | Описание |
|---|---|---|
| GET | `/api/v1/entries/search?word=...` | Регистронезависимый поиск (404 если нет) |
| POST | `/api/v1/entries` | Создать запись (409 если слово уже есть) |
| GET | `/api/v1/entries` | Список всех слов |

Полная спецификация — в [`openapi.yaml`](./openapi.yaml).

## Локальный запуск без Docker

```bash
export DB_HOST=localhost DB_PORT=5433 DB_NAME=dictionary DB_USER=dictionary DB_PASSWORD=dictionary
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```
