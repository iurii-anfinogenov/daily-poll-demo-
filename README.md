# Daily Poll Demo 🗳️

Учебное **stateless-приложение-опрос** на FastAPI,  
которое использует **PostgreSQL** для хранения вопросов/голосов  
и **Redis** для кэша и live-счётчиков.  
Репозиторий нужен, чтобы демонстрировать разные приёмы DevOps-деплоя  
(Ansible, Kaniko, Terraform, Kubernetes и т. д.) над неизменным кодом.

---

## 📦 Технологии

| Слой            | Стек (версия по умолчанию) |
|-----------------|---------------------------|
| Язык / API      | Python 3.12 · FastAPI 0.115 |
| База данных     | PostgreSQL 16 |
| Кэш / Pub-Sub   | Redis 8 |
| Web-сервер      | Uvicorn (ASGI) |
| Контейнеризация | Docker + docker-compose |

---

## 🚀 Быстрый старт

```bash
# 1 — клонируем репозиторий
git clone https://github.com/<ваш-ник>/daily-poll-demo.git
cd daily-poll-demo

# 2 — создаём файл окружения
cp .env.example .env      # при необходимости отредактируйте

# 3 — строим и запускаем весь стек
docker compose up --build
```

Откройте <http://localhost:8000/docs> — встроенный Swagger-UI.

---

## 🔗 Основные эндпоинты

| Метод | URL        | Назначение                     |
|-------|------------|--------------------------------|
| GET   | `/`        | Информация о контейнере        |
| GET   | `/poll`    | Активный вопрос дня            |
| POST  | `/vote`    | Отдать голос (`choice_id`)     |
| GET   | `/results` | Текущие результаты голосования |

---

## ⚙️ Переменные окружения (`.env`)

| Переменная     | Значение по умолчанию                          | Назначение                         |
|----------------|------------------------------------------------|------------------------------------|
| `DATABASE_URL` | `postgresql+psycopg2://user:pass@db:5432/poll` | строка подключения к PostgreSQL    |
| `REDIS_HOST`   | `redis`                                        | хост Redis-сервиса                 |
| `REDIS_PORT`   | `6379`                                         | порт Redis                         |
| `CACHE_TTL`    | `86400` (24 ч)                                 | время жизни кэша вопроса (сек)     |

---

## 🏗️ Как использовать на курсе DevOps

| Приём                    | Что пробовать                                                         |
|--------------------------|-----------------------------------------------------------------------|
| **docker-compose → Helm**| перенести `api`, `db`, `redis` в Helm-чарт                            |
| **Kaniko**               | собрать образ внутри кластера, прокинув `GIT_SHA`                     |
| **Terraform**            | описать ресурсы `kubernetes_deployment` и `service`                   |
| **Ansible**              | роль, ставящая Docker и запускающая контейнер с `.env`                 |
| **HPA / авто-скейл**     | добавить `HorizontalPodAutoscaler` по CPU / RPS                       |
| **Blue-Green / Canary**  | выкатывать новый тег образа, проверять `/` и `/results`               |

---

## 📚 Планы на развитие

- [ ] миграции Alembic  
- [ ] прометеевские метрики `/metrics`  
- [ ] CI-workflow (lint → build → test → push)  

---

## 🤝 Contributing

PR и issue приветствуются!  
Перед мёрджем запускайте локальные тесты:

```bash
docker compose run --rm api pytest
```

---

## 🪪 License

MIT © 2025 Iurii Anfinogenov
