# Лабораторная работа 3

Многоконтейнерное приложение TODO Matrix с использованием матрицы Эйзенхауэра, состоящее из трёх сервисов: базы данных PostgreSQL, бэкенда на FastAPI и панели администратора PgAdmin.

---

Docker Hub: ```skyber2/ipr-lab-3:latest```

---

## Структура проекта

```bash
lab3/
├── app/                    # Основное приложение (FastAPI + фронт)
├── docker-compose.yml      # Docker Compose конфигурация
├── Dockerfile             # Докерфайл
├── .env.example           # Пример файла с переменными окружения
├── requirements.txt       # Зависимости проекта
└── README.md              # Документация
```

## Как запускать
1. Скопировать файлы docker-compose.yml и .env.example
2. Выполнить команду
```bash 
cp .env.example .env
```
3. Отредактируйте .env
4. Запустить приложение командой ```bash docker compose --profile development up -d```

---
После запуска система будет доступна:

- Само приложение: http://localhost:8000
- Документация API (Swagger): http://localhost:8000/docs
- PgAdmin (управление БД): http://localhost:5050

---

## Что реализовано:
- 3 сервиса в Docker Compose: PostgreSQL, FastAPI приложение, PgAdmin.
- Multi-stage Dockerfile: итоговый образ < 200 МБ.
- Изоляция: сервисы работают в отдельной сети.
- Health checks для основных сервисов.
- Volumes для сохранения данных БД.
- Профили (development - запускаются все сервисы, production - все, кроме pgAdmin)

---
## Некоторые проверки на работоспособность сайта
Health check
```bash
curl http://localhost:8000/health
```

## Вывод:
Отпрактиковал навыки упаковки многокомпонентного приложения (БД, бэкенд, админка) в контейнеры с управлением через Docker Compose
