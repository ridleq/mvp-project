# Система управления бизнесом (MVP)

Это одностраничное MVP-приложение без микросервисов, с понятной архитектурой и минимальным фронтендом.

## Установка и запуск проекта

1. **Клонируйте репозиторий**:
```bash
   git clone https://github.com/ridleq/mvp-project.git;
   cd mvp-project
```
2. **Создайте файл .env в корневой директории проекта и заполните его согласно примеру**

3. **Создайте вирутальное окружение:**
```bash
   python -m venv venv
   source venv/scrtipt/activate
```
4. **Установите зависимости:**
```bash
   pip install -r requirements.txt
```
5. **Создайте и выполните миграции:**
```bash
   alembic revision --autogenerate -m "migration"
   alembic upgrade head
```
6. **Запустите сервер из корневой директории:**
```bash
   uvicorn mvp.main:app --reload
```

#### Server запущен.
#### Вы можете получить доступ по адресу: http://localhost:8000/.../.

## Стек
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- Pydantic (валидация)
- fastapi-users
- sqladmin
- Uvicorn

## Архитектура проекта 
Проект основан на архитектуре FastAPI, включая следующие основные компоненты:
- Модели:
        Модели находятся в папке models.
- Pydantic:
        Pydantic-схемы находятся в папке schemas.
- CRUD:
        Реализация CRUD технологий находится в папке crud.
- Endpoints:
        Все "ручки" находятся в папке api/endpoint. Подключены в главном файле api/routers.py
- Admin-панель:
        Все настройки и подключенные модели находятся в файле core/admin.py

- Дополнительные проверки:
        Все дополнительные проверки находятся в папке utils

---
...

[Автор приложения](https://github.com/ridleq)

