Клонировать репозиторий, зайти в папку репозитория:
```
git@github.com:LevKorobeinikov/test_task1.git
```

Активировать виртуальное окружение, установить UV,
выполнить установку зависимостей:
```
python3.13 -m venv .venv
source .venv/bin/activate       # Для MacOS/Linux
source .venv\Scripts\activate   # Для Windows
pip install uv
pip install --upgrade pip
uv sync
```
Создать файл .env, заполнить по примеру файла .env.example

Примените миграции и запустите проект  
```
uv run alembic upgrade head       
uv run uvicorn app.main:app --reload
```
Для новых миграций
```
 uv run alembic revision --autogenerate -m "..."
```
## Доступ к документации
# [Swagger](http://127.0.0.0:8000/docs)
