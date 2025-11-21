# TODO Matrix 

Приложение для управления задачами по матрице Эйзенхауэра, упакованное в Docker контейнер

---
## Как запускать
### Запуск для пользования (без bind mount)
```bash
docker run -d -p 8000:8000 skyber2/todo-app:latest
```
или
```bash
docker run -d -p 8000:8000 skyber2/todo-app:1.0
```

Важно: сайт будет находиться по ссылке: ```http://localhost:8000/```

---
## Некоторые проверки на работоспособность сайта
- Health check
```bash
curl http://localhost:8000/health
```
- Получить задачи (вернет [], если ранее задачи не добавлялись)
```bash
curl http://localhost:8000/get_tasks
```

---

## Запуск для тех, у кого есть исходный код (с bind mount)
- на винде
```bash
docker run -d -p 8000:8000 -v ${PWD}/app:/app-todo-list/app skyber2/todo-app:latest
```
- на маке/линукс
```bash
docker run -d -p 8000:8000 -v $(pwd)/app:/app-todo-list/app skyber2/todo-app:latest
```

---

## Структура проекта
```bash
корневая папка проекта/
├── app/              # ← эта папка монтируется в контейнер
│   ├── main.py
│   ├── static/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── script.js
│   └── ...
├── Dockerfile
└── requirements.txt
└── ...
```

---

## Реализовано:
- Dockerfile со всеми необходимыми зависимостями
- .dockerignore для уменьшения размера образа
- Health check для мониторинга состояния
- Bind mounts для разработки с live-reload
- Размер образа < 500MB

---

## Вывод:
Отпрактиковал основные команды докера и упаковывать небольшие приложения в контейнеры
