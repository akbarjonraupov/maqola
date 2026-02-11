# maqola.tj

Учебная платформа для авторизации пользователей и публикации материалов, вдохновлённая интерфейсом журналов OpenEdu.

## Возможности

- Регистрация и вход пользователей
- Сессии через JWT в `HttpOnly` cookie
- Создание публикаций
- Просмотр ленты публикаций
- Личный кабинет автора
- Современный фронтенд на HTML/CSS/JavaScript с анимациями и интерактивными эффектами

## Стек

- Backend: FastAPI
- База данных: SQLite + SQLAlchemy
- Фронтенд: HTML + CSS + JavaScript
- Шаблоны: Jinja2

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте `http://127.0.0.1:8000`.
