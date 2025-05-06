# Daily Poll Demo 🗳️

Учебное **stateless-приложение-опрос** на FastAPI + Jinja2,
с простым веб-интерфейсом для голосования и администрирования.
Приложение использует:

* **PostgreSQL** для хранения вопросов, вариантов и голосов
* **Redis** для кэша текущего опроса и live-счётчиков

Репозиторий предназначен для демонстрации различных приёмов DevOps-деплоя (Ansible, Kaniko, Terraform, Kubernetes и т. д.) над неизменным кодом.

---

## 📦 Технологии

| Слой             | Стек (версия)               |
| ---------------- | --------------------------- |
| Язык / API       | Python 3.12 · FastAPI 0.115 |
| Web-шаблонизация | Jinja2                      |
| База данных      | PostgreSQL 16               |
| Кэш / Pub-Sub    | Redis 8                     |
| Web-сервер       | Uvicorn (ASGI)              |
| Контейнеризация  | Docker + docker-compose     |

---

## 🚀 Быстрый старт

```bash
# 1. Клонируем репозиторий
git clone https://github.com/<ваш-ник>/daily-poll-demo.git
cd daily-poll-demo

# 2. Создаём файл окружения (.env)
cat > .env <<EOF
DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/poll
REDIS_HOST=redis
REDIS_PORT=6379
CACHE_TTL=86400
EOF

# 3. Поднимаем стек
docker compose up --build
```

*Swagger и веб-интерфейс:*
[http://localhost:8000](http://localhost:8000) — UI опроса
[http://localhost:8000/admin](http://localhost:8000/admin) — администрирование
[http://localhost:8000/docs](http://localhost:8000/docs) — Swagger-UI

---

## 🔗 Основные эндпоинты

| Метод | URL        | Описание                                |
| ----- | ---------- | --------------------------------------- |
| GET   | `/`        | Отображает текущий опрос и результаты\| |
| POST  | `/vote`    | Голосовать (поле `choice_id` формы)     |
| GET   | `/results` | API-данные результатов (JSON)           |
| GET   | `/admin`   | Форма создания нового опроса            |
| POST  | `/admin`   | Создать опрос (поля `text`, `options`)  |

---

## 🛠 Структура проекта

```
app/
├─ main.py              # логика FastAPI + Jinja2
├─ templates/           # Jinja2-шаблоны
│   ├─ base.html
│   ├─ poll.html
│   └─ admin.html
└─ static/
    └─ style.css        # простой CSS
Dockerfile
docker-compose.yml
README.md
.env.example
```

---

## 📚 Задачи DevOps

После того, как приложение готово и проверено, студенты могут:

1. **Docker Compose → Helm**
   Перенести сервисы (`api`, `db`, `redis`) в Helm-чарт.

2. **Kaniko**
   Локальная тренировка сборки контейнера без Docker-daemon.

   ```bash
   # запустить Kaniko Executor в контейнере
   docker run --rm -v $(pwd):/workspace \
     gcr.io/kaniko-project/executor:latest \
     --dockerfile=/workspace/Dockerfile \
     --context=/workspace \
     --destination=ghcr.io/<ваш-ник>/daily-poll-demo:kaniko
   ```

3. **Terraform + Kubernetes**
   Описать Deployment/Service, настроить `image: ghcr.io/...:kaniko`.

4. **Ansible**
   Роль для установки Docker, загрузки образа и запуска контейнера `daily-poll-demo`.

5. **Авто-скейлинг (HPA)**
   Добавить `HorizontalPodAutoscaler` по CPU/RPS.

6. **Blue-Green / Canary**
   Показать стратегию выкатывания новых образов по тегам.

---

## 📈 Масштабирование с Docker Compose

```bash
docker compose up --build --scale api=3
```

При динамическом запуске нескольких инстансов порт 8000 на хосте будет балансироваться между контейнерами.

---

## 🤝 Contributing

PR и issue приветствуются!
Перед мёрджем запускайте:

```bash
docker compose run --rm api pytest
```

---

## 🪪 License

MIT © 2025 Your Name
