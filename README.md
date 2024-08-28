**MA**

Для запуска:
```
pip install -r requirements.txt
uvicorn app.main:app --host localhost --port 8000 --reload --workers 4
alembic upgrade head
```
