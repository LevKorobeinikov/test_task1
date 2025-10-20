Клонировать репозиторий, зайти в папку репозитория:
```
git clone git@github.com:AquaLedStroy-development/backend.git
cd backend
```

Активировать виртуальное окружение, установить UV,
выполнить установку зависимостей:
```
python3.13 -m venv .venv
source .venv/bin/activate       # Для MacOS/Linux
source .venv\Scripts\activate   # Для Windows
pip install uv
uv sync
```

Создать файл .env, заполнить по примеру файла .env.example