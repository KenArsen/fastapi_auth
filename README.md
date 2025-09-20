# Auth Service (FastAPI)

Небольшой сервис аутентификации на FastAPI с хранением пользователей в БД и авторизацией через JWT-токен в HttpOnly cookie.

- Эндпоинты: регистрация, логин, логаут, текущий пользователь.
- Хранение паролей в хэшированном виде.
- JWT (HS256) хранится в защищённой cookie (HttpOnly, опционально Secure).
- Поддержка CORS.
- База данных: SQLite (по умолчанию) или PostgreSQL (asyncpg).
- Миграции базы данных на Alembic.
- Управление зависимостями через Poetry.

## Стек
- Python 3.12
- FastAPI, Pydantic v2
- SQLAlchemy (async) + Alembic
- Uvicorn
- Poetry
- Docker (опционально)

## Старт проекта

### 1) Клонирование и зависимости
```bash
git clone https://github.com/KenArsen/fastapi_auth.git
cd fastapi_auth

# Установите Poetry, если не установлен
pip install poetry

# Установка зависимостей
poetry install
```

### 2) Настройка окружения
Создайте файл .env в корне проекта на основе примера:
```bash
cp .env_example .env
```
Обязательно укажите секретный ключ JWT_SECRET_KEY — без него приложение не стартует.

Доступные переменные (.env):
- DB_ENGINE=postgres | sqlite (по умолчанию sqlite)
- DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS — для PostgreSQL
- CORS_ORIGINS — список через запятую, например: http://localhost:3000,http://127.0.0.1:8000
- COOKIE_SECURE=true|false — помечать ли cookie как Secure
- JWT_ALGORITHM — по умолчанию HS256
- JWT_SECRET_KEY — обязательный секрет
- JWT_ACCESS_COOKIE_NAME — имя cookie с токеном (по умолчанию access_token)
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES — срок жизни Access Token в минутах (по умолчанию 30)

### 3) База данных и миграции
По умолчанию используется SQLite-файл sqlite.db в корне проекта — можно сразу запускать.

Для PostgreSQL укажите DB_ENGINE=postgres и параметры подключения,
затем выполните миграции:
```bash
poetry run alembic upgrade head
```
Файлы миграций находятся в папке migrations/ (alembic.ini — в корне).

### 4) Запуск
- Быстрый запуск через Makefile:
```bash
make run
```
- Либо напрямую через uvicorn:
```bash
poetry run uvicorn src.main:app --reload
```
После старта документация доступна по адресу:
- Swagger: http://localhost:8000/docs
- ReDoc:   http://localhost:8000/redoc

Префикс API: /api/v1

## Эндпоинты аутентификации
Базовый путь: /api/v1/auth

1) Регистрация
- POST /api/v1/auth/register/
- Request body (application/json):
```json
{
  "email": "user@example.com",
  "password": "your_password",
  "username": "optional_name"
}
```
- Response 200 (application/json):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "optional_name"
}
```

2) Логин
- POST /api/v1/auth/login/
- Request body:
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```
- Response 200:
```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```
Одновременно в ответе устанавливается HttpOnly cookie с access_token
(имя cookie задаётся переменной JWT_ACCESS_COOKIE_NAME).

3) Логаут
- POST /api/v1/auth/logout/
- Очищает cookie с токеном. Ответ:
```json
{ "detail": "Successfully logged out" }
```

4) Текущий пользователь
- GET /api/v1/auth/me/
- Требуется валидная cookie с access_token.
- Response 200:
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "optional_name"
}
```

### Примеры curl
- Регистрация:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret","username":"user"}'
```

- Логин (с сохранением cookie):
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"user@example.com","password":"secret"}'
```

- Текущий пользователь (используя cookie из логина):
```bash
curl http://localhost:8000/api/v1/auth/me/ -b cookies.txt
```

- Логаут:
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout/ -b cookies.txt -c cookies.txt
```

## Конфигурация и важные детали
- CORS: список доменов настраивается через CORS_ORIGINS. Значение-строка
  автоматически разбивается по запятой.
- JWT_SECRET_KEY обязателен. Без него Settings валидатор поднимет ошибку при старте.
- COOKIE_SECURE: на проде выставляйте true, чтобы cookie передавались только по HTTPS.
- Имя cookie и время жизни настраиваются через переменные окружения.

## Docker
Пример сборки и запуска:
```bash
docker build -t fastapi-auth .
docker run -p 8080:8080 --env-file .env fastapi-auth
```
Сервис стартует на 0.0.0.0:8080, команда запуска внутри контейнера:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080
```
Примечание: убедитесь, что в образ попадает исходный код (папка `src`).
Текущий Dockerfile может требовать корректировки COPY для вашей среды.

## Структура проекта (важное)
- src/main.py — создание FastAPI приложения
- src/core/* — конфиг, логгер, инициализация CORS/роутов, БД
- src/accounts/* — модели, схемы, репозитории и сервисы аккаунтов, API v1
- migrations/*, alembic.ini — миграции базы данных
- Makefile — утилитарные команды

## Лицензия
MIT (или укажите вашу лицензию, если иная).
