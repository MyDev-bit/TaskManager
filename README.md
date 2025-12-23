# Task Manager API

**Task Manager API** — современное, безопасное и масштабируемое REST API на **FastAPI** для управления задачами, пользователями и базой данных.  
Поддерживает **OAuth2-авторизацию**, **CRUD-операции**, **rate limiting**, **dev-инструменты**, **Docker + Nginx** и **автоматическую документацию (Swagger UI)**.

---

## Содержание

- [Технологии](#технологии)
- [Структура проекта](#структура-проекта)
- [Запуск](#запуск)
  - [Локально](#локально)
  - [Через Docker](#через-docker)
- [API Эндпоинты](#api-эндпоинты)
  - [Root Router](#root-router)
  - [Tasks Router](#tasks-router)
  - [Test Router](#test-router)
  - [User Actions](#user-actions)
- [Docker & Nginx](#docker--nginx)
  - [`docker-compose.yml`](#docker-composeyml)
  - [`Dockerfile`](#dockerfile)
  - [`nginx.conf`](#nginxconf)
- [Конфигурация](#конфигурация)
- [Контрибьютинг](#контрибьютинг)
- [Лицензия](#лицензия)

---

## Технологии

| Технология       | Назначение                     |
|------------------|--------------------------------|
| **FastAPI**      | Веб-фреймворк                  |
| **Python 3.11**  | Язык разработки                |
| **Pydantic**     | Валидация данных               |
| **OAuth2**       | Авторизация                    |
| **Docker**       | Контейнеризация                |
| **Nginx**        | Reverse proxy + rate limiting  |
| **SQLite**       | База данных (dev)              |

---

## Структура проекта

```text
PythonProject2/
├── venv/                  # Виртуальное окружение (не в git)
├── src/
│   ├── core/              # Ядро приложения
│   ├── database/          # Подключение к БД
│   ├── dinamic_schemas/   # Динамические схемы
│   ├── models/            # Pydantic модели
│   ├── routers/           # Роутеры API
│   ├── schemas/           # Схемы ответов/запросов
│   ├── services/          # Бизнес-логика
│   ├── __init__.py
│   └── jwt.env            # JWT секреты (не коммитить!)
├── main.py                # Точка входа
├── main.db                # SQLite база (dev)
├── .dockerignore
├── .gitignore
├── docker-compose.yml     # Docker Compose
├── Dockerfile              # Сборка бэкенда
├── nginx.conf             # Конфиг Nginx
└── requirements.txt       # Зависимости
```

---

## Запуск

### Локально

```bash
git clone https://github.com/username/task-manager-api.git
cd task-manager-api

pip install -r requirements.txt

uvicorn main:app --reload --port 8080
```

> **API:** `http://localhost:8080`  
> **Документация:** `http://localhost:8080/docs`

---

### Через Docker

```bash
docker-compose up --build
```

> **API:** `http://localhost:40/api`  
> **Документация:** `http://localhost:40/docs`

---

## API Эндпоинты

### Root Router (`/`)

| Метод | Путь               | Описание                     | Статус |
|-------|--------------------|------------------------------|--------|
| `GET` | `/`                | Проверка работоспособности   | `200`  |
| `POST`| `/create_db`       | Создать БД                   | `201`  |
| `HEAD`| `/check_db`        | Проверить подключение к БД   | `200`  |

---

### Tasks Router (`/api/tasks`)

| Метод   | Путь                            | Описание                     | Статус |
|---------|---------------------------------|------------------------------|--------|
| `POST`  | `/add_task`                     | Добавить задачу              | `201`  |
| `PATCH` | `/patch_task_status/{status}`   | Изменить статус              | `200`  |
| `PUT`   | `/put_task/{task_id}`           | Обновить задачу              | `200`  |
| `GET`   | `/all_tasks`                    | Все задачи                   | `200`  |
| `DELETE`| `/delete_task`                  | Удалить задачу               | `200`  |

> Данные передаются через `Form()` + `Annotated`.

---

### Test Router (`/tests/dev`)

> **Только для разработки!**

| Метод   | Путь                                | Описание                     | Статус |
|---------|-------------------------------------|------------------------------|--------|
| `POST`  | `/root_token/set_token`             | Установить root cookie       | `201`  |
| `DELETE`| `/root_token/delete_token`          | Удалить root cookie          | `200`  |

---

### User Actions (`/api`)

| Метод   | Путь              | Описание                     |
|---------|-------------------|------------------------------|
| `POST`  | `/register`       | Регистрация                  |
| `POST`  | `/login`          | Вход (OAuth2)                |
| `POST`  | `/logout`         | Выход                        |
| `DELETE`| `/delete_account` | Удаление аккаунта            |

---

## Docker & Nginx

### `docker-compose.yml`

```yaml
version: '3.8'
services:
  nginx:
    image: nginx:latest
    ports:
      - "40:40"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    command: [nginx-debug, '-g', 'daemon off;']

  backend:
    build:
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    depends_on:
      - nginx
```

---

### `Dockerfile`

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY src ./src
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

---

### `nginx.conf` — **Rate Limiting: 10 запросов/сек на IP**

```nginx
worker_processes auto;
events {
    worker_connections 1024;
}

http {
    client_body_temp_path /tmp/client_temp;
    proxy_temp_path /tmp/proxy_temp_path;
    fastcgi_temp_path /tmp/fastcgi_temp;
    uwsgi_temp_path /tmp/uwsgi_temp;
    scgi_temp_path /tmp/scgi_temp;

    limit_req_zone $binary_remote_addr zone=perip:10m rate=10r/s;

    upstream api {
        least_conn;
        server backend:8080;
    }

    server {
        listen 40;

        location /api {
            limit_req zone=perip burst=20 nodelay;
            proxy_pass http://api;
        }

        location /docs {
            proxy_pass http://api/docs;
        }

        location /openapi.json {
            proxy_pass http://api/openapi.json;
        }
    }
}
```

---

## Конфигурация

| Файл             | Назначение                     |
|------------------|--------------------------------|
| `jwt.env`        | Секреты JWT (не коммитить!)    |
| `main.db`        | SQLite база (dev)              |
| `requirements.txt` | Все зависимости              |

---

## Контрибьютинг

1. Сделайте **форк** репозитория
2. Создайте ветку:  
   ```bash
   git checkout -b feature/новая-функция
   ```
3. Зафиксируйте изменения:  
   ```bash
   git commit -m "feat: добавлена новая функция"
   ```
4. Отправьте в ветку:  
   ```bash
   git push origin feature/новая-функция
   ```
5. Создайте **Pull Request**

> Используйте:  
> - `black` — форматирование  
> - `isort` — сортировка импортов  
> - `pytest` — тесты  
> - `Pydantic` — типизация

---

