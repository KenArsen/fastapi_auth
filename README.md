# Auth Service (FastAPI)

Небольшой сервис аутентификации и авторизации на FastAPI с использованием:

- SQLAlchemy 2.x (async) + Alembic
- Pydantic v2
- JWT (PyJWT) с хранением access-токена в HttpOnly cookie
- Хэширование паролей через passlib[bcrypt]
- Логи в консоль и файл

Проект предоставляет базовые эндпоинты: регистрация, логин/логаут и получение текущего пользователя.

## Содержание

- Возможности
- Технологии
- Требования
- Установка и запуск (локально)
- Переменные окружения (.env)
- База данных и миграции
- Запуск через Makefile
- Docker (замечание)
- API и примеры запросов
- Структура проекта

## Возможности

- Регистрация пользователя (email + пароль + username)
- Логин: выдача JWT access-токена и установка его в HttpOnly cookie
- Логаут: очистка cookie
- Получение текущего пользователя по access-токену из cookie

## Технологии

- Python 3.12
- FastAPI
- SQLAlchemy (async) + aiosqlite (по умолчанию SQLite) или asyncpg (Postgres)
- Alembic (миграции)
- PyJWT
- passlib[bcrypt]

## Требования

- Python 3.12+
- Poetry (для управления зависимостями)

## Установка и запуск (локально)

#### Клонируйте репозиторий и перейдите в папку проекта:

```bash
    git clone https://github.com/KenArsen/fastapi_auth.git
    cd fastapi_auth
```

#### Установите зависимости:

```bash
    pip install poetry
    poetry install
```

Создайте файл .env в корне проекта (см. раздел «Переменные окружения»).

#### Выполните миграции БД:

```bash
    alembic upgrade head
```

#### Запустите приложение:

```bash
    uvicorn src.main:app --reload
```

Интерфейсы документации будут доступны по адресам:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Переменные окружения (.env)

Пример .env (минимально необходимы JWT_SECRET_KEY, остальное имеет значения по умолчанию):

- JWT_SECRET_KEY="your-very-secret-key"

## sqlite | postgres

- DB_ENGINE=sqlite
- DB_HOST=localhost
- DB_PORT=5432
- DB_NAME=app
- DB_USER=postgres
- DB_PASS=postgres

## CORS. Можно строку со списком через запятую, либо оставить *

- CORS_ORIGINS=*

## Cookie/JWT

- COOKIE_SECURE=false
- JWT_ALGORITHM=HS256
- JWT_ACCESS_COOKIE_NAME=access_token
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

Пояснения:

- JWT_SECRET_KEY — обязателен (иначе приложение не запустится).
- Для SQLite переменные DB_HOST/PORT/NAME/USER/PASS игнорируются; используется файл sqlite.db в корне.
- Для Postgres укажите DB_ENGINE=postgres и корректные параметры подключения.

## База данных и миграции

- Конфигурация Alembic уже настроена (migrations/env.py берёт URL из настроек приложения).
- Применить все миграции: alembic upgrade head
- Откатить на одну миграцию: alembic downgrade -1
- Текущая схема включает таблицу accounts со столбцами: id, role, username, email, password, created_at, updated_at.

## Запуск через Makefile

Упростить запуск можно командой:

```bash
  make run
```

Она эквивалентна:

```bash
  uvicorn src.main:app --reload
```

## Кодстайл и линтеры (PEP8)

В проекте используется следующий набор инструментов для соответствия PEP8 и поддержания единого стиля кода:

- Black — автоформатирование кода (PEP 8 совместимо)
- Ruff — быстрый линтер (включает правила pycodestyle E/W, Pyflakes F) и сортировщик импортов (аналог isort)

Конфигурация уже добавлена в pyproject.toml:
- [tool.black] — line-length=120, target-version=py312
- [tool.ruff] — line-length=120, target-version=py312, включены наборы правил: E, W, F, I, UP, B

Как запускать:

Через Poetry:
```bash
poetry run black .
poetry run ruff check .            # проверить
poetry run ruff check --fix .      # автоматически исправить то, что можно
poetry run ruff check --select I --fix .  # только сортировка импортов
```

Через Makefile:
```bash
make format   # Black + сортировка импортов (Ruff)
make lint     # Линтинг Ruff (PEP8 и др.)
```

## Docker (замечание)

В репозитории есть Dockerfile, однако в нём указана строка COPY ./app /code/app, в то время как исходный код находится в
каталоге src/. Для корректной сборки образа рекомендуется либо:

- заменить **COPY ./app /code/app** на **COPY ./src /code/src** в Dockerfile, либо
- подготовить структуру **/app** с кодом внутри.

Пример сборки/запуска после исправления COPY:

- Сборка:

```bash
  docker build -t fastapi-auth .
```

- Запуск:

```bash
  docker run -p 8080:8080 --env-file .env fastapi-auth
```

По умолчанию CMD запускает Uvicorn на порту 8080. Документация будет доступна на http://127.0.0.1:8080/docs.

## API и примеры запросов

Базовый префикс: /api/v1

Эндпоинты аккаунтов: /api/v1/auth

1) Регистрация
   **POST /api/v1/auth/register/**

```json
{
  "email": "user@example.com",
  "password": "strong-pass",
  "username": "john"
}
```

**POST /api/v1/auth/register/**
```json
{
  "email": "user@example.com",
  "password": "strong-pass",
  "username": "john"
}
```

Ответ: 200 OK (данные пользователя без пароля)

2) Логин
   **POST /api/v1/auth/login/**
```json
{
  "email": "user@example.com",
  "password": "strong-pass"
}
```
   Ответ: 200 OK
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```
   Дополнительно сервер установит HttpOnly cookie с именем из JWT_ACCESS_COOKIE_NAME (по умолчанию access_token).

Пример curl (cookie сохраняется):

- Вход: curl -i -c cookies.txt -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strong-pass"}'

3) Текущий пользователь (me)
   GET /api/v1/auth/me/
   Требуется установленный HttpOnly cookie access_token (например, после логина):

- Пример: curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me/

4) Логаут
   POST /api/v1/auth/logout/
   Очищает cookie access_token на клиенте.

Коды ошибок:

- 400 — Пользователь уже существует при регистрации
- 401 — Неверные учётные данные / отсутствие токена / недействительный токен
- 404 — Пользователь не найден (например, если удалён)

## Структура проекта (основное)

- src/main.py — создание FastAPI-приложения
- src/core — конфигурация, БД, зависимости, исключения, логирование, базовые модели и репозитории, инициализация
  приложения
- src/accounts — модели, схемы, репозитории, сервисы, безопасность (JWT, cookie), зависимости
- src/api/v1 — маршрутизация и эндпоинты
- migrations — Alembic миграции

## Полезные заметки

- Токен — это JWT c subject=sub=email и временем жизни exp из JWT_ACCESS_TOKEN_EXPIRE_MINUTES.
- Токен хранится в HttpOnly cookie, что снижает риски XSS. Для продакшена установите COOKIE_SECURE=true и настройте
  CORS_ORIGINS под ваши домены.
- Логи пишутся в logs/app.log и в консоль.

## Лицензия

MIT (или укажите вашу лицензию).
